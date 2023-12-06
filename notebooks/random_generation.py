import random
import os
import metric_utils as module_metric
import pandas as pd
from tqdm import tqdm
from common import load_cmd_line
from utils import convert2list, evaluate_list, save2csv, cal_avg_scores, seed_everything


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
    seed_everything(args.get("seed", 42))
    params = {
        "max_tokens": args.get("max_tokens", 30),
    }
    data_root_dir = args.get("data_root_dir", "test_group/variant3")
    variant_name = args.get("variant_name", "cold_user-match_topic-fix_candidate")
    sampled_df = pd.read_csv(f"{data_root_dir}/{variant_name}.csv")
    num = args.get("num", 100)
    sampled_df = sampled_df.sample(num)
    os.makedirs("generated_data", exist_ok=True)
    os.makedirs("result", exist_ok=True)
    model_name = "random"
    sampled_df[model_name] = generate_random_predictions(sampled_df["candidate"])
    data_cols = ["impression_id", "history", "candidate", "label", model_name]
    metric_list = ["group_auc", "mean_mrr", "ndcg_5", "ndcg_10"]
    suffix = f"random_{variant_name}"
    generated_data_root = f"generated_data/{data_root_dir}"
    os.makedirs(generated_data_root, exist_ok=True)
    score_root = f"result/{data_root_dir}"
    generated_output_path = f"{generated_data_root}/{suffix}.csv"
    os.makedirs(score_root, exist_ok=True)
    score_path = f"{score_root}/{suffix}.csv"
    metric_funcs = [getattr(module_metric, met) for met in ["group_auc", "mean_mrr", "ndcg_5", "ndcg_10"]]
    results = []
    for index in tqdm(sampled_df.index, total=len(sampled_df)):
        line = {col: sampled_df.loc[index, col] for col in data_cols}
        output_list, label_list = convert2list(line[model_name], line["label"], line["candidate"])
        line.update(evaluate_list(output_list, label_list, metric_funcs))
        line.update(evaluate_list(output_list, label_list, metric_funcs))
        results.append(line)
        save2csv(results, generated_output_path)
        cal_avg_scores(results, score_path, model_name, metric_list)
    df = pd.read_csv(score_path)
    df["data_group"] = variant_name
    df["seed"] = args.get("seed", 42)
    df.to_csv(score_path, index=False)
