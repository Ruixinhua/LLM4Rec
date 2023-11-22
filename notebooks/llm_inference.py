import json
import re
import os
import time
import torch
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForCausalLM
from common import load_cmd_line, load_api_key
from utils import evaluate_output, save2csv, cal_avg_scores, seed_everything
from llama_templates import template4


if __name__ == "__main__":
    args = load_cmd_line()
    cache_dir = args.get("cache_dir", None)
    sample_num = args.get("sample_num", 1000)
    sampled_df = pd.read_csv(f"sampled_{sample_num}.csv")
    seed_everything(args.get("seed", 42))
    template_list = {4: template4}
    template_no = args.get("template_no", 4)
    temp_name = args.get("prompt_temp", "naive_zero_shot")
    prompt_temp = json.load(open("prompt_temp.json", "r"))[temp_name]
    model_name = args.get("model_name", "Llama-2-13b-hf")
    suffix = f"template-{template_no}_{model_name}"
    token = load_api_key("hf_token.json")
    root = Path("generated_data/")
    os.makedirs(root, exist_ok=True)
    tokenizer = AutoTokenizer.from_pretrained(
        f"meta-llama/{model_name}",
        cache_dir=cache_dir,
        token=token,
        force_download=False,
    )
    model = AutoModelForCausalLM.from_pretrained(
        f"meta-llama/{model_name}",
        cache_dir=cache_dir,
        token=token,
        force_download=False,
        device_map="auto",
        torch_dtype=torch.float16 if args.get("fp16", False) else "auto",
    )
    print(f"Loading Device: {model.device}")
    os.makedirs("generated_data", exist_ok=True)
    os.makedirs("result", exist_ok=True)
    # metric_cols = ["AUC", "MRR", "nDCG@5", "nDCG@10"]
    # "ndcg5", "ndcg10", "mrr"
    metric_cols = ["nDCG@5", "nDCG@10", "MRR"]
    data_cols = ["impression_id", "history", "candidate", "label"]
    failed_ins = []
    results = []
    for index in tqdm(sampled_df.index, total=len(sampled_df)):
        line = {col: sampled_df.loc[index, col] for col in data_cols}
        full_prompt = template_list[template_no].format(history=line["history"], candidate=line["candidate"])
        inputs = tokenizer(full_prompt, return_tensors="pt")
        torch.cuda.empty_cache()
        input_ids = inputs.input_ids.to(model.device)
        try:
            generate_ids = model.generate(
                input_ids,
                max_length=4000,
                max_new_tokens=args.get("max_new_tokens", 40),
            )
            line["output"] = tokenizer.batch_decode(
                generate_ids,
                skip_special_tokens=True,
                clean_up_tokenization_spaces=False,
            )[0][len(full_prompt):]
            line.update(evaluate_output(line["output"], line["label"], line["candidate"], metric_cols))
            results.append(line)
            save2csv(results, f"generated_data/{suffix}.csv")
            cal_avg_scores(results, f"result/{suffix}.csv", model_name, metric_cols)
        except Exception as e:
            print(e)
            failed_ins.append(line)
            save2csv(failed_ins, f"generated_data/{suffix}-failed.csv")
            continue
