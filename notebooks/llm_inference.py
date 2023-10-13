# Load model directly
import re
import os
import time
import torch
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForCausalLM
from one_shot_example import one_shot
from common import (
    compute_recommendation_metrics,
    compute_recommendation_metrics_row,
    load_cmd_line,
)


if __name__ == "__main__":
    args = load_cmd_line()
    # cache_dir = Path(args.get("cache_dir", "/scratch/16206782/hg_cache"))
    news_path = (
        Path(args.get("mind_root", "/home/people/16206782/ExplainableNRS/dataset/MIND"))
        / "small/news.csv"
    )
    news_df = pd.read_csv(news_path)
    sample_num = args.get("sample_num", 1000)
    sampled_df = pd.read_csv(f"sampled_{sample_num}.csv")
    model_name = args.get("model_name", "Llama-2-13b-hf")
    mode = args.get("mode", "rank")
    zero_shot = args.get("zero_shot", False)
    suffix = f"{sample_num}_{model_name}_{mode}"
    suffix += "_zero_shot" if zero_shot else "_one_shot"
    token = "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"
    root = Path("generated_data/")
    os.makedirs(root, exist_ok=True)
    start = time.time()
    tokenizer = AutoTokenizer.from_pretrained(
        f"meta-llama/{model_name}",
        # cache_dir=f"/scratch/16206782/hg_cache/{model_name}",
        token=token,
        force_download=False,
    )
    print(f"Loading tokenizer takes {time.time() - start} seconds")
    model = AutoModelForCausalLM.from_pretrained(
        f"meta-llama/{model_name}",
        # cache_dir=f"/scratch/16206782/hg_cache/{model_name}",
        token=token,
        force_download=False,
        device_map="auto",
        torch_dtype=torch.float16 if args.get("fp16", False) else "auto",
    )
    print(f"Loading Device: {model.device}")
    failed_imp = []
    for index in tqdm(sampled_df.index, total=len(sampled_df)):
        hist, cand, label = sampled_df.loc[index, ["history", "candidate", "label"]]
        try:
            if mode == "explanation":
                full_prompt = f"""You are a news recommender. Now rank the following input and output up to 10 news index in the format like C1,C4,C2,C3.\n#Input:\nUser's History News:\n{hist}\nCandidate News:\n{cand}\nPlease think step by step and explain the recommended results.\n#Output:"""
            else:
                if zero_shot:
                    full_prompt = f"""You are a news recommender. Based on the user's news history, think step by step and recommend up to 10 news articles. First, provide the indices (start with 'C') of the top 10 candidate articles.\n#Input:\nUser's History News:\n{hist}\nCandidate News:\n{cand}\n#Output:"""
                else:
                    full_prompt = f"""You are a news recommender. Given an example like:\n{one_shot}\nBased on the user's news history, think step by step and recommend up to 10 news articles. First, provide the indices (start with 'C') of the top 10 candidate articles.\n#Input:\nUser's History News:\n{hist}\nCandidate News:\n{cand}\n#Output:"""
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
            )[0][len(full_prompt) :]
            if mode == "rank":
                output = ",".join(re.findall(r"C\d+", output))
                sampled_df.loc[index, model_name] = output
                ndcg5_at_k, ndcg10_at_k, mrr = compute_recommendation_metrics_row(
                    sampled_df.loc[index], "label", model_name
                )
                sampled_df.loc[index, "nDCG@5"] = ndcg5_at_k
                sampled_df.loc[index, "nDCG@10"] = ndcg10_at_k
                sampled_df.loc[index, "MRR"] = mrr
            else:
                sampled_df.loc[index, model_name] = output
            sampled_df.to_csv(
                f"generated_data/sampled_{suffix}.csv",
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
    sampled_df = sampled_df[~sampled_df["impression_id"].isin(failed_imp)]
    sampled_df.to_csv(
        f"generated_data/sampled_{suffix}.csv", index=False
    )  # save the successful ones
    if mode == "rank":
        performance_dict = {
            "Metric": ["nDCG@5", "nDCG@10", "MRR"],
            model_name: list(
                compute_recommendation_metrics(sampled_df, "label", model_name)
            ),
        }
        performance_df = pd.DataFrame(performance_dict)
        performance_df.to_csv(
            f"result/sampled_{suffix}_performance.csv",
            index=False,
        )
