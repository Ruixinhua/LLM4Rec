import json
import os
import re
import time
import google.generativeai as palm
import pandas as pd

from tqdm import tqdm
from one_shot_example import one_shot
from utils import evaluate_performance
from common import load_api_key, load_cmd_line, evaluate_one


if __name__ == "__main__":
    palm.configure(api_key=load_api_key("google_key.json"))
    args = load_cmd_line()
    sample_num = args.get("sample_num", 1000)
    temp_name = args.get("prompt_temp", "naive_zero_shot")
    prompt_temp = json.load(open("prompt_temp.json", "r"))[temp_name]
    sampled_df = pd.read_csv(f"sampled_{sample_num}.csv")
    metric_cols = ["nDCG@5", "nDCG@10", "MRR"]
    max_num = min(args.get("max_num", 10), len(sampled_df))  # only request 10 samples by default
    suffix = f"{max_num}_palm_{temp_name}"
    os.makedirs("generated_data", exist_ok=True)
    os.makedirs("result", exist_ok=True)
    performance = []
    for index in tqdm(sampled_df.sample(max_num).index, total=max_num):
        hist, cand, label = sampled_df.loc[index, ["history", "candidate", "label"]]
        if "one_shot" in temp_name:
            full_prompt = prompt_temp.format(one_shot=one_shot, hist=hist, cand=cand)
        else:
            full_prompt = prompt_temp.format(hist=hist, cand=cand)
        print(full_prompt)
        response = palm.chat(messages=[full_prompt])
        output = response.last
        if output is None:
            print(response)
        else:
            print(output)
        sampled_df.loc[index, "prediction"] = ",".join(re.findall(r"C\d+", output))
        sampled_df.loc[index, "palm"] = output
        result = list(evaluate_one(label.split(","), sampled_df.loc[index, "prediction"].split(",")))
        # ndcg5_at_k, ndcg10_at_k, mrr
        sampled_df.loc[index, metric_cols] = result
        performance.append([sampled_df.loc[index, "impression_id"]] + result)
        performance_df = evaluate_performance(performance, metric_cols=metric_cols)
        sampled_df.to_csv(f"generated_data/sampled_{suffix}.csv", index=False)
        performance_df.to_csv(
            f"result/sampled_{suffix}.csv",
            index=False,
        )
        time.sleep(20)
