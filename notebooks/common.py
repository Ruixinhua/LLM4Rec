import copy
import sys
import openai
import time
import numpy as np
import json

from logging import getLogger
from enum import Enum


def convert_config_dict(config_dict):
    r"""This function convert the str parameters to their original type."""
    check_set = (str, int, float, list, tuple, dict, bool, Enum)
    for key in config_dict:
        param = config_dict[key]
        if not isinstance(param, str):
            continue
        try:
            value = eval(
                param
            )  # convert str to int, float, list, tuple, dict, bool. use ',' to split integer values
            if value is not None and not isinstance(value, check_set):
                value = param
        except (NameError, SyntaxError, TypeError, ValueError):
            if isinstance(param, str):
                if param.lower() == "true":
                    value = True
                elif param.lower() == "false":
                    value = False
                else:
                    if "," in param:  # split by ',' if it is a string
                        value = []
                        for v in param.split(","):
                            if len(v) == 0:
                                continue
                            try:
                                v = eval(v)
                            except (NameError, SyntaxError, TypeError, ValueError):
                                v = v
                            value.append(v)
                    else:
                        value = param
            else:
                value = param
        config_dict[key] = value
    return config_dict


def load_cmd_line():
    """
    Load command line arguments
    :return: dict
    """
    cmd_config_dict = {}
    unrecognized_args = []
    if "ipykernel_launcher" not in sys.argv[0]:
        for arg in sys.argv[1:]:
            if not arg.startswith("--") or len(arg[2:].split("=")) != 2:
                unrecognized_args.append(arg)
                continue
            cmd_arg_name, cmd_arg_value = arg[2:].split("=")
            if (
                cmd_arg_name in cmd_config_dict
                and cmd_arg_value != cmd_config_dict[cmd_arg_name]
            ):
                raise SyntaxError(
                    "There are duplicate commend arg '%s' with different value." % arg
                )
            else:
                cmd_config_dict[cmd_arg_name] = cmd_arg_value
    if len(unrecognized_args) > 0:
        logger = getLogger()
        logger.warning(
            f"Unrecognized command line arguments(correct is '--key=value'): {' '.join(unrecognized_args)}"
        )
    cmd_config_dict = convert_config_dict(cmd_config_dict)
    cmd_config_dict["cmd_args"] = copy.deepcopy(cmd_config_dict)
    return cmd_config_dict


def chat(messages, model="gpt-3.5-turbo", max_try=5, **model_params):
    """Set up the Openai API key using openai.api_key = api_key"""
    try:
        chat_completion = openai.ChatCompletion.create(
            model=model, messages=messages, **model_params
        )
        content = chat_completion.choices[0].message["content"]
        return content
    except:
        if max_try > 0:
            time.sleep(1)
            return chat(messages, model, max_try - 1)
        else:
            raise Exception("Max try exceeded")


def get_history_candidate_prompt(news_df, behavior):
    history_news = news_df[news_df["news_id"].isin(behavior["history"].split())]
    cand_news_index = [i.split("-")[0] for i in behavior["impressions"].split()]
    cand_label = [i.split("-")[1] for i in behavior["impressions"].split()]
    # get candidate news from news_df and save them to a list with the same order as cand_news_index
    candidate_news = [
        news_df[news_df["news_id"] == i].iloc[0]["title"] for i in cand_news_index
    ]
    history_prompt = "\n".join(
        [f"H{i + 1}: {news}" for i, news in enumerate(history_news["title"].values)]
    )
    candidate_prompt = "\n".join(
        [f"C{i + 1}: {news}" for i, news in enumerate(candidate_news)]
    )
    return (
        history_prompt,
        candidate_prompt,
        ",".join([f"C{i + 1}" for i, l in enumerate(cand_label) if int(l)]),
    )


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


def compute_mrr(gt_list, pred_list):
    """Compute MRR (Mean Reciprocal Rank).
    Args:
    gt_list: list of ground truth labels
    pred_list: list of predicted labels
    Returns:
    MRR
    """
    mrr = 0.0
    for gt, preds in zip(gt_list, pred_list):
        for i, p in enumerate(preds):
            if p in gt:
                mrr += 1.0 / (i + 1)
                break
    return mrr / len(gt_list)


def compute_recommendation_metrics(input_data, label_col, prediction_col):
    """
    Compute mean nDCG@k and MRR for recommendation tasks.

    Parameters:
    - input_data: dataframe containing the data
    - label_col: column name containing the true labels
    - prediction_col: column name containing the predicted recommendations

    Returns:
    - mean_ndcg5_at_k: mean nDCG@5
    - mean_ndcg10_at_k: mean nDCG@10
    - mean_mrr: mean MRR
    """
    # Process input columns
    input_data = input_data.copy()
    input_data[label_col] = input_data[label_col].str.split(",")
    input_data[prediction_col] = input_data[prediction_col].str.split(",")

    # Compute relevance scores for nDCG@k
    input_data["relevance"] = input_data.apply(
        lambda row: [
            1 if item in row[label_col] else 0 for item in row[prediction_col]
        ],
        axis=1,
    )

    # Calculate nDCG@k values
    ndcg5_values = input_data["relevance"].apply(lambda x: ndcg_at_k(x, 5))
    ndcg10_values = input_data["relevance"].apply(lambda x: ndcg_at_k(x, 10))
    mean_ndcg5_at_k = np.mean(ndcg5_values)
    mean_ndcg10_at_k = np.mean(ndcg10_values)

    # Calculate MRR
    mean_mrr = compute_mrr(
        input_data[label_col].tolist(), input_data[prediction_col].tolist()
    )

    return mean_ndcg5_at_k, mean_ndcg10_at_k, mean_mrr


def compute_recommendation_metrics_row(row, label_col, prediction_col):
    """
    Compute nDCG@k and MRR for a single row in recommendation tasks.

    Parameters:
    - row: a single row from a dataframe containing the data
    - label_col: column name containing the true labels
    - prediction_col: column name containing the predicted recommendations

    Returns:
    - ndcg5_at_k: nDCG@5 for the row
    - ndcg10_at_k: nDCG@10 for the row
    - mrr: MRR for the row
    """
    # Process input columns
    labels = row[label_col].split(",")
    predictions = row[prediction_col].split(",")

    # Compute relevance scores for nDCG@k
    relevance = [1 if item in labels else 0 for item in predictions]

    # Calculate nDCG@k values
    ndcg5_at_k = ndcg_at_k(relevance, 5)
    ndcg10_at_k = ndcg_at_k(relevance, 10)

    # Calculate MRR
    mrr = compute_mrr_for_row(labels, predictions)

    return ndcg5_at_k, ndcg10_at_k, mrr


# Helper function to compute MRR for a single row
def compute_mrr_for_row(labels, predictions):
    for index, item in enumerate(predictions, 1):
        if item in labels:
            return 1.0 / index
    return 0


def load_api_key(json_path="openai_key.json"):
    return json.load(open(json_path))["api_key"]
