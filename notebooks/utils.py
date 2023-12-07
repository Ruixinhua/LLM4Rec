import re
import os
import numpy as np
import pandas as pd
import random
from common import evaluate_one


def evaluate_performance(performance, metric_cols=None):
    if metric_cols is None:
        metric_cols = ["MRR", "nDCG@5", "nDCG@10"]
    performance_df = pd.DataFrame.from_records(performance, columns=["ID"] + metric_cols)
    avg_values = performance_df[["MRR", "nDCG@5", "nDCG@10"]].mean().round(3).tolist()
    tmp_list = performance.copy() + [["avg_value"] + avg_values]
    performance_df = pd.DataFrame.from_records(tmp_list, columns=["ID"] + metric_cols)
    return performance_df


def seed_everything(seed=42):
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    np.random.seed(seed)


def shuffle_candidates(candidates: str):
    candidates = candidates.split("\n")
    random.shuffle(candidates)
    return "\n".join(candidates)


def save2csv(results_list, saved_path):
    df = pd.DataFrame.from_records(results_list)
    df.to_csv(saved_path, index=False)


def unique_in_order(iterable):
    unique_list = []
    for item in iterable:
        if item not in unique_list:
            unique_list.append(item)
    return unique_list


def extract_output(output, candidates):
    pattern = r"<START>(.+?)<END>"
    extracted_text = re.search(pattern, output)
    # Check if the pattern was found and extract the group
    ranks = extracted_text.group(1) if extracted_text else output
    ranks = unique_in_order(re.findall(r"C\d+", ranks))
    if len(ranks) == 0:
        return extract_raw_output(output, candidates)
    return ranks


def extract_raw_output(out, cans):
    ranks = []
    filter_index = 0
    for match in re.finditer(re.escape("The recommended news headlines by rank are:"), out):
        filter_index = match.start()
    out = out[filter_index:]
    for i, c in enumerate(cans.split('\n')):
        c = re.sub(r"C\d+: ", '', c)
        start = len(out)
        for match in re.finditer(re.escape(c), out):
            start = match.start()
        ranks.append(start)
    index_sorted = sorted(range(len(ranks)), key=lambda k: ranks[k])
    return [f"C{i+1}" for i in index_sorted][:10]


def evaluate_output(output: str, label: str, candidates, metrics=None):
    """Evaluate the raw output of the model and return a dictionary of scores."""
    if metrics is None:
        metrics = ["nDCG@5", "nDCG@10", "MRR"]
    output = extract_output(output, candidates)
    label = label.split(",")
    score = {k: v for k, v in zip(metrics, evaluate_one(label, output))}
    return score


def search_label_index(label: str, candidates: str):
    """Search the index of the label in the candidates."""
    match = re.search(r"C\d+", label)
    if match:
        label_index = [int(re.findall(r'\d+', i)[0]) - 1 for i in label.split(",")]
        label_list = [1 if i in label_index else 0 for i in range(len(candidates.split("\n")))]
    else:
        label_list = [1 if candidate in label else 0 for candidate in candidates.split("\n")]
    return label_list


def convert2list(ranks: str, label: str, candidates: str):
    length = len(candidates.split("\n"))
    label_list = search_label_index(label, candidates)
    output_list = [0] * length
    for i, c in enumerate(ranks.split(',')):
        index = int(re.findall(r'\d+', c)[0])-1
        if index >= length:
            continue
        output_list[index] = round(1 / (i + 1), 3)
    return np.array(output_list), np.array(label_list)


def evaluate_list(output: list, label: list, metrics=None):
    return {func.__name__: round(func(label, output), 5) for func in metrics}


def cal_avg_scores(results_list, saved_path, model="gpt-3.5-turbo", metrics=None):
    """Calculate the average scores of the results."""
    if metrics is None:
        metrics = ["nDCG@5", "nDCG@10", "MRR"]
    df = pd.DataFrame.from_records(results_list)
    df[metrics] = df[metrics] * 100
    avg_scores = df[metrics].mean().round(2).to_dict()
    avg_scores["model"] = model
    avg_scores["sample_num"] = len(results_list)
    df = pd.DataFrame.from_records([avg_scores])
    df.to_csv(saved_path, index=False)
