import pandas as pd
import numpy as np
import re
import os

def save2file(results_list, saved_path):
    df = pd.DataFrame.from_records(results_list)
    df.to_csv(saved_path, index=False)
    # df.to_csv(saved_path, mode='a', index=False, header=False)

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

def evaluate_one(labels, predictions):
    """
    Compute nDCG@k and MRR for a single row in recommendation tasks.

    Parameters:
    - labels: list of true labels, like ['C1', 'C3', 'C5']
    - predictions: list of predicted labels in order, like ['C2', 'C5', 'C1', 'C3', 'C4']

    Returns:
    - ndcg5_at_k: nDCG@5 for the row
    - ndcg10_at_k: nDCG@10 for the row
    - mrr: MRR for the row
    """
    # Compute relevance scores for nDCG@k
    relevance = [1 if item in labels else 0 for item in predictions]

    def dcg_at_k(r, k):
        """Compute DCG@k for a single sample.
        Args:
        r: list of relevance scores in the order they were ranked
        k: number of results to consider
        Returns:
        DCG@k
        """
        r = np.asfarray(r)[:k]
        return np.sum(r / np.log2(np.arange(2, r.size + 2)))

    def ndcg_at_k(r, k):
        """Compute nDCG@k for a single sample.
        Args:
        r: list of relevance scores in the order they were ranked
        k: number of results to consider
        Returns:
        nDCG@k
        """
        dcg_max = dcg_at_k(sorted(r, reverse=True), k)
        if not dcg_max:
            return 0.0
        return dcg_at_k(r, k) / dcg_max

    # Calculate nDCG@k values
    ndcg5_at_k = ndcg_at_k(relevance, 5)
    ndcg10_at_k = ndcg_at_k(relevance, 10)

    # Helper function to compute MRR for a single row
    def compute_mrr(labels, predictions):
        for index, item in enumerate(predictions, 1):
            if item in labels:
                return 1.0 / index
        return 0

    # Calculate MRR
    mrr = compute_mrr(labels, predictions)
    return ndcg5_at_k, ndcg10_at_k, mrr

def cal_avg_scores(results_list, model="gpt-3.5-turbo", metrics=None, template=None, tag=None):
    """Calculate the average scores of the results."""
    if metrics is None:
        metrics = ["nDCG@5", "nDCG@10", "MRR"]
    df = pd.DataFrame.from_records(results_list)
    avg_scores = df[metrics].mean().to_dict()
    avg_scores["model"] = model
    avg_scores["sample_num"] = len(results_list)
    avg_scores["template_name"] = template
    avg_scores["tag"] = tag
    df = pd.DataFrame.from_records([avg_scores])

    return df
