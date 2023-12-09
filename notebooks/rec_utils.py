import os
import json
import guidance
import urllib.request

import metric_utils as module_metric
import pandas as pd
import numpy as np
from string import Template
from tqdm import tqdm
import sys
sys.path.append("../")
from common import load_api_key
from templates import gpt_template
from utils import convert2list, save2csv, cal_avg_scores, extract_output, evaluate_list

url = "http://bendstar.com:8000/v1/chat/completions"
req_header = {
    'Content-Type': 'application/json',
}


def is_descending(lst):
    for i in range(len(lst) - 1):
        if lst[i] < lst[i + 1]:
            return False
    return True


def build_instruction():
    return "You serve as a personalized news recommendation system."


def request_llama(data, temp):
    user_content = temp.replace("{{history}}", data["history"]).replace("{{candidate}}", data["candidate"])
    chat_completion = json.dumps({
        "model": "meta-llama/Llama-2-70b-chat-hf",
        "messages": [{"role": "system", "content": build_instruction()}, {"role": "user", "content": user_content}],
        "temperature": 0,
    })
    req = urllib.request.Request(url, data=chat_completion.encode(), method='POST', headers=req_header)

    with urllib.request.urlopen(req) as response:
        body = json.loads(response.read())
        print(body['choices'][0]['message']['content'])
        return body['choices'][0]['message']['content']


def run_recommender(prompt_template, **kwargs):
    data_group = kwargs.get("data_group", "sample100by_ratio")
    samples = kwargs.get("samples", pd.read_csv(f"valid/{data_group}.csv"))
    metric_list = ["group_auc", "mean_mrr", "ndcg_5", "ndcg_10"]
    data_cols = ["impression_id", "history", "candidate", "label"]
    metric_funcs = [getattr(module_metric, met) for met in metric_list]
    recommender_model = kwargs.get("recommender", "gpt-3.5-turbo")
    temperature = kwargs.get("temperature", 0)
    max_tokens = kwargs.get("max_tokens", 2048)
    model = guidance.llms.OpenAI(recommender_model, api_key=load_api_key(), chat_mode=True)
    template = Template(gpt_template).safe_substitute(
        {"temperature": temperature, "prompt_temp": prompt_template, "max_tokens": max_tokens}
    )
    epoch = kwargs.get("epoch", None)
    generated_output_path = f"generated_data/prompt_tuning/{recommender_model}/"
    if epoch is not None:
        generated_output_path += f"epoch_{epoch}.csv"
    else:
        generated_output_path += f"default.csv"
    generated_output_path = kwargs.get("generated_output_path", generated_output_path)
    score_path = f"result/prompt_tuning/{recommender_model}/epoch_{epoch}.csv"
    score_path = kwargs.get("score_path", score_path)
    os.makedirs(os.path.dirname(generated_output_path), exist_ok=True)
    os.makedirs(os.path.dirname(score_path), exist_ok=True)
    results = []
    in_order_ratio = 0
    for index in tqdm(samples.index, total=len(samples)):
        line = {col: samples.loc[index, col] for col in data_cols}
        full_prompt = Template(template).safe_substitute(history=line["history"], candidate=line["candidate"])
        line["full_prompt"] = full_prompt
        line["output"] = guidance(full_prompt, llm=model, silent=True)()["rank"]
        line["rank"] = ','.join(extract_output(line["output"], line["candidate"]))
        output_list, label_list = convert2list(line["rank"], line["label"], line["candidate"])
        in_order_ratio += 1 if is_descending(output_list[np.nonzero(output_list)[0]]) else 0
        line.update(evaluate_list(output_list, label_list, metric_funcs))
        results.append(line)
        save2csv(results, generated_output_path)
        cal_avg_scores(results, score_path, recommender_model, metric_list)
    in_order_ratio = in_order_ratio / len(samples)
    df = pd.read_csv(score_path)
    df["in_order_ratio"] = round(in_order_ratio, 3)
    df["max_tokens"] = max_tokens
    df["temperature"] = temperature
    df["data_group"] = data_group
    if epoch is not None:
        df["epoch"] = epoch
    df.to_csv(score_path, index=False)
    return df
