import pandas as pd
import os
import re
import openai
from tqdm import tqdm
from common import (
    chat,
    load_api_key,
    load_cmd_line,
    compute_recommendation_metrics_row,
    compute_recommendation_metrics,
)
from one_shot_example import one_shot


if __name__ == "__main__":
    openai.api_key = load_api_key()
    args = load_cmd_line()
    model_name = args.get("model_name", "gpt-3.5-turbo")
    sample_num = args.get("sample_num", 1000)
    params = {
        "max_tokens": args.get("max_tokens", args.get("max_tokens", 30)),
    }
    mode = args.get("mode", "rank")
    zero_shot = args.get("zero_shot", False)
    suffix = f"{sample_num}_{model_name}_{mode}"
    suffix += "_zero_shot" if zero_shot else "_one_shot"
    sampled_df = pd.read_csv(f"sampled_{sample_num}.csv")
    os.makedirs("generated_data", exist_ok=True)
    os.makedirs("result", exist_ok=True)
    for index in tqdm(sampled_df.index, total=len(sampled_df)):
        hist, cand, label = sampled_df.loc[index, ["history", "candidate", "label"]]
        if mode == "explanation":
            full_prompt = f"""You are a news recommender. Now rank the following input and output up to 10 news index in the format like C1,C4,C2,C3.\n#Input:\nUser's History News:\n{hist}\nCandidate News:\n{cand}\nPlease think step by step and explain the recommended results.\n#Output:"""
        else:
            if zero_shot:
                full_prompt = f"""You are a news recommender. Based on the user's news history, think step by step and recommend up to 10 news articles. First, provide the indices (start with 'C') of the top 10 candidate articles.\n#Input:\nUser's History News:\n{hist}\nCandidate News:\n{cand}\n#Output:"""
            else:
                full_prompt = f"""You are a news recommender. Given an example like:\n{one_shot}\nBased on the user's news history, think step by step and recommend up to 10 news articles. First, provide the indices (start with 'C') of the top 10 candidate articles.\n#Input:\nUser's History News:\n{hist}\nCandidate News:\n{cand}\n#Output:"""
        try:
            output = chat(
                [{"role": "user", "content": full_prompt}],
                model=model_name,
                max_try=5,
                **params,
            )
        except:
            output = None
        if mode == "explanation":
            sampled_df.loc[index, model_name] = output
        else:
            sampled_df.loc[index, "prediction"] = output
            sampled_df.loc[index, model_name] = ",".join(re.findall(r"C\d+", output))
            ndcg5_at_k, ndcg10_at_k, mrr = compute_recommendation_metrics_row(
                sampled_df.loc[index], "label", model_name
            )
            sampled_df.loc[index, "nDCG@5"] = ndcg5_at_k
            sampled_df.loc[index, "nDCG@10"] = ndcg10_at_k
            sampled_df.loc[index, "MRR"] = mrr
            sampled_df.to_csv(f"generated_data/sampled_{suffix}.csv", index=False)
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
