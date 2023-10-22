import json
import re
import os
import time
import torch
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForCausalLM
from one_shot_example import one_shot
from common import load_cmd_line, load_api_key, evaluate_one
from utils import evaluate_performance


if __name__ == "__main__":
    args = load_cmd_line()
    cache_dir = Path(args.get("cache_dir", None))
    sample_num = args.get("sample_num", 1000)
    sampled_df = pd.read_csv(f"sampled_{sample_num}.csv")
    temp_name = args.get("prompt_temp", "naive_zero_shot")
    prompt_temp = json.load(open("prompt_temp.json", "r"))[temp_name]
    model_name = args.get("model_name", "Llama-2-13b-hf")
    suffix = f"{sample_num}_{model_name}_{temp_name}"
    token = load_api_key("hf_token.json")
    root = Path("generated_data/")
    os.makedirs(root, exist_ok=True)
    start = time.time()
    tokenizer = AutoTokenizer.from_pretrained(
        f"meta-llama/{model_name}",
        cache_dir=cache_dir,
        token=token,
        force_download=False,
    )
    print(f"Loading tokenizer takes {time.time() - start} seconds")
    model = AutoModelForCausalLM.from_pretrained(
        f"meta-llama/{model_name}",
        cache_dir=cache_dir,
        token=token,
        force_download=False,
        device_map="auto",
        torch_dtype=torch.float16 if args.get("fp16", False) else "auto",
    )
    print(f"Loading Device: {model.device}")
    failed_imp = []
    performance = []
    for index in tqdm(sampled_df.index, total=len(sampled_df)):
        hist, cand, label = sampled_df.loc[index, ["history", "candidate", "label"]]
        if "one_shot" in temp_name:
            full_prompt = prompt_temp.format(one_shot=one_shot, hist=hist, cand=cand)
        else:
            full_prompt = prompt_temp.format(hist=hist, cand=cand)
        try:
            inputs = tokenizer(full_prompt, return_tensors="pt")
            start = time.time()
            torch.cuda.empty_cache()
            generate_ids = model.generate(
                inputs.input_ids,
                max_length=1800,
                max_new_tokens=args.get("max_new_tokens", 40),
            )
            output = tokenizer.batch_decode(
                generate_ids,
                skip_special_tokens=True,
                clean_up_tokenization_spaces=False,
            )[0][len(full_prompt):]
            sampled_df.loc[index, "prediction"] = ",".join(re.findall(r"C\d+", output))
            sampled_df.loc[index, model_name] = output
            result = list(evaluate_one(label.split(","), output.split(",")))
            # ndcg5_at_k, ndcg10_at_k, mrr
            sampled_df.loc[index, ["ndcg5", "ndcg10", "mrr"]] = result
            sampled_df.to_csv(
                f"generated_data/sampled_{suffix}.csv",
                index=False,
            )
            performance.append([sampled_df.loc[index, "impression_id"]] + result)
            performance_df = evaluate_performance(performance)
            sampled_df[~sampled_df["impression_id"].isin(failed_imp)].to_csv(
                f"generated_data/sampled_{suffix}.csv", index=False
            )
            performance_df.to_csv(
                f"result/sampled_{suffix}.csv",
                index=False,
            )
        except:
            sampled_df.loc[index, model_name] = ""
            failed_imp.append(sampled_df.loc[index, "impression_id"])
            sampled_df[sampled_df["impression_id"].isin(failed_imp)].to_csv(
                f"generated_data/sampled_{suffix}_failed.csv",
                index=False,
            )
            continue
