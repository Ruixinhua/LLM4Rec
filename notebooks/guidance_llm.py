import re
import os
import numpy as np
import random
import pandas as pd
import guidance
from tqdm import tqdm
from string import Template
from common import load_api_key, evaluate_one, load_cmd_line
from templates import template1, template2, template3, template4, gpt_template, llama_template


def seed_everything(seed=42):
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    np.random.seed(seed)


def shuffle_candidates(candidates: str):
    candidates = candidates.split("\n")
    random.shuffle(candidates)
    return "\n".join(candidates)


def save2file(results_list, saved_path):
    df = pd.DataFrame.from_records(results_list)
    df.to_csv(saved_path, index=False)


def unique_in_order(iterable):
    unique_list = []
    for item in iterable:
        if item not in unique_list:
            unique_list.append(item)
    return unique_list


def evaluate_output(output: str, label: str, metrics=None):
    """Evaluate the raw output of the model and return a dictionary of scores."""
    if metrics is None:
        metrics = ["nDCG@5", "nDCG@10", "MRR"]
    output = unique_in_order(re.findall(r"C\d+", output))
    print(output)
    label = label.split(",")
    score = {k: v for k, v in zip(metrics, evaluate_one(label, output))}
    score["rank"] = ",".join(output)
    return score


def cal_avg_scores(results_list, saved_path, model="gpt-3.5-turbo", metrics=None):
    """Calculate the average scores of the results."""
    if metrics is None:
        metrics = ["nDCG@5", "nDCG@10", "MRR"]
    df = pd.DataFrame.from_records(results_list)
    avg_scores = df[metrics].mean().to_dict()
    avg_scores["model"] = model
    avg_scores["sample_num"] = len(results_list)
    df = pd.DataFrame.from_records([avg_scores])
    df.to_csv(saved_path, index=False)


if __name__ == "__main__":
    # we use LLaMA here, but any GPT-style model will do
    args = load_cmd_line()
    seed_everything(args.get("seed", 42))
    template_list = {1: template1, 2: template2, 3: template3, 4: template4}
    template_no = args.get("template_no", 4)
    num = args.get("num", 1000)
    sampled_df = pd.read_csv("sampled_1000.csv")
    # sampled_df["candidate"] = sampled_df["candidate"].apply(shuffle_candidates)
    samples = sampled_df.sample(num)
    model_name = args.get("model_name", "gpt-3.5-turbo")
    temperature = args.get("temperature", 0)
    suffix = f"template-{template_no}_{model_name}_temperature-{temperature}"
    result_path = f"generated_data/{suffix}.csv"
    data_cols = ["impression_id", "history", "candidate", "label"]
    user_template = template_list[template_no]
    if "gpt" in model_name.lower():
        model = guidance.llms.OpenAI(model_name, api_key=load_api_key())
        template = Template(gpt_template).safe_substitute({"temperature": temperature, "input": user_template})
    else:
        model = guidance.llms.Transformers(f"meta-llama/{model_name}")
        template = Template(llama_template).safe_substitute({"input": user_template})
    score_path = f"result/{suffix}.csv"
    metric_list = ["nDCG@5", "nDCG@10", "MRR"]
    results = []
    for index in tqdm(samples.index, total=len(samples)):
        line = {col: samples.loc[index, col] for col in data_cols}
        experts = guidance(template, llm=model, silent=True)
        out = experts(history=line["history"], candidate=line["candidate"])
        line["output"] = out["rank"]
        line.update(evaluate_output(out["rank"], line["label"], metric_list))
        results.append(line)
        save2file(results, result_path)
        cal_avg_scores(results, score_path, model_name, metric_list)
