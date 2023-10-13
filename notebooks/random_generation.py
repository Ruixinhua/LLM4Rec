import random
import os
import pandas as pd
from tqdm import tqdm
from common import (
    load_cmd_line,
    compute_recommendation_metrics_row,
    compute_recommendation_metrics,
)


def generate_random_predictions(candidate_col):
    """Generate random recommendations based on the candidate column with correct format."""
    return candidate_col.apply(
        lambda x: ",".join(
            [
                f"C{item + 1}"
                for item in random.sample(range(len(x.split("\n"))), len(x.split("\n")))
            ]
        )
    )


if __name__ == "__main__":
    args = load_cmd_line()
    sample_num = args.get("sample_num", 1000)
    params = {
        "max_tokens": args.get("max_tokens", 30),
    }
    sampled_df = pd.read_csv(f"sampled_{sample_num}.csv")
    os.makedirs("generated_data", exist_ok=True)
    os.makedirs("result", exist_ok=True)
    model_name = "random"
    sampled_df[model_name] = generate_random_predictions(sampled_df["candidate"])
    for index in tqdm(sampled_df.index, total=len(sampled_df)):
        hist, cand, label = sampled_df.loc[index, ["history", "candidate", "label"]]
        ndcg5_at_k, ndcg10_at_k, mrr = compute_recommendation_metrics_row(
            sampled_df.loc[index], "label", model_name
        )
        sampled_df.loc[index, "nDCG@5"] = ndcg5_at_k
        sampled_df.loc[index, "nDCG@10"] = ndcg10_at_k
        sampled_df.loc[index, "MRR"] = mrr
        sampled_df.to_csv(
            f"generated_data/sampled_{sample_num}_{model_name}.csv", index=False
        )
    performance_dict = {
        "Metric": ["nDCG@5", "nDCG@10", "MRR"],
        model_name: list(
            compute_recommendation_metrics(sampled_df, "label", model_name)
        ),
    }
    performance_df = pd.DataFrame(performance_dict)
    performance_df.to_csv(
        f"result/sampled_{sample_num}_{model_name}_performance.csv", index=False
    )
