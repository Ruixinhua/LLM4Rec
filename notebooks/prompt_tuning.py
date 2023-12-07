import os
import random
import re
import json
import openai_v137
import pandas as pd
from common import load_api_key, load_cmd_line
import metric_utils as module_metric
import numpy as np
from string import Template
from tqdm import tqdm
import sys
from utils import convert2list, save2csv, cal_avg_scores, extract_output, evaluate_list, seed_everything
from instructions import meta_instruction, sample_temp, prompt_temp, observation_instruction
import instructions as module_instruction
from gptcache.adapter import openai
from gptcache import cache
from gptcache.manager import get_data_manager
sys.path.append("../")


def build_sample(history, candidate, answer, click, **kwargs):
    full_prompt = Template(kwargs["prompt_temp"]).safe_substitute(history=history, candidate=candidate)
    return Template(sample_temp).safe_substitute(full_prompt=full_prompt, answer=answer, click=click)


def build_prompt4opt(**kwargs):
    prompt4opt = Template(prompt_temp).safe_substitute(prompt_temp=kwargs["prompt_temp"])
    prompt4opt += build_sample(**kwargs)
    prompt4opt += observation_instruction
    return prompt4opt


def response_text(openai_resp):
    return openai_resp['choices'][0]['message']['content']


def is_descending(lst):
    for i in range(len(lst) - 1):
        if lst[i] < lst[i + 1]:
            return False
    return True


def request_gpt28(content, model, **kwargs):
    while True:
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{
                    'role': 'user',
                    'content': "You serve as a personalized news recommendation system.\n" + content,
                }],
                max_tokens=kwargs.get("max_tokens", 2048),
                temperature=kwargs.get("temperature", 0)
            )
            return response_text(response)
        except Exception as e:
            print(e)
            import time
            time.sleep(30)
            continue


def run_recommender(prompt_template, **kwargs):
    set_openai_key()
    data_group = kwargs.get("data_group", "sample100by_ratio")
    samples = kwargs.get("samples", pd.read_csv(f"valid/{data_group}.csv"))
    metric_list = ["group_auc", "mean_mrr", "ndcg_5", "ndcg_10"]
    data_cols = ["impression_id", "history", "candidate", "label"]
    metric_funcs = [getattr(module_metric, met) for met in metric_list]
    recommender_model = kwargs.get("recommender", "gpt-3.5-turbo")
    cache.init(data_manager=get_data_manager(data_path=f"{recommender_model}.txt"))
    optimizer_model = kwargs.get("optimizer", "gpt-3.5-turbo")
    temperature = kwargs.get("temperature", 0)
    max_tokens = kwargs.get("max_tokens", 2048)
    epoch = kwargs.get("epoch", 0)
    generated_output_path = f"generated_data/prompt_tuning/{recommender_model}-{optimizer_model}/epoch_{epoch}.csv"
    generated_output_path = kwargs.get("generated_output_path", generated_output_path)
    score_path = f"result/prompt_tuning/{recommender_model}-{optimizer_model}/epoch_{epoch}.csv"
    score_path = kwargs.get("score_path", score_path)
    os.makedirs(os.path.dirname(generated_output_path), exist_ok=True)
    os.makedirs(os.path.dirname(score_path), exist_ok=True)
    results = []
    in_order_ratio = 0
    for index in tqdm(samples.index, total=len(samples)):
        line = {col: samples.loc[index, col] for col in data_cols}
        full_prompt = Template(prompt_template).safe_substitute(history=line["history"], candidate=line["candidate"])
        line["full_prompt"] = full_prompt
        line["output"] = request_gpt28(full_prompt, recommender_model, **kwargs)
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
    df["epoch"] = epoch
    df.to_csv(score_path, index=False)
    return df


def set_openai_key():
    import openai
    openai.api_key = load_api_key()
    openai.organization = 'org-3Btx7SoUaviVtc7JNH6nKeub'


def cal_avg_performance(result):
    return round(result[["group_auc", "mean_mrr", "ndcg_5", "ndcg_10"]].mean(axis=1)[0], 2)


def update_monitor_scores(monitor_records, monitor_path, monitor_columns):
    monitor_scores = pd.DataFrame.from_records(monitor_records, columns=monitor_columns)
    if os.path.exists(monitor_path):
        monitor_scores = pd.concat([monitor_scores, pd.read_csv(monitor_path, index_col=False)])
    monitor_scores.drop_duplicates(subset=["epoch", "prompt_template", "group_auc"], inplace=True)
    monitor_scores.to_csv(monitor_path, index=False)
    return monitor_scores


def build_optimizer(**kwargs):
    recommender = kwargs.get("recommender", "gpt-3.5-turbo-1106")
    optimizer = kwargs.get("optimizer", "gpt-3.5-turbo-1106")
    client = openai_v137.OpenAI(
        api_key=load_api_key()
    )
    assistant = client.beta.assistants.create(
        name="Prompt Optimizer",
        instructions=meta_instruction,
        # tools=[{"type": "code_interpreter"}],
        model=optimizer
    )
    middle_name = f"{recommender}--{optimizer}--{kwargs.get('tag', 'naive-format')}"
    initial_prompt = getattr(module_instruction, kwargs.get("initial_prompt", "initial_prompt"))
    generated_output_path = f"generated_data/prompt_tuning/{middle_name}/epoch_0.csv"
    score_path = f"result/prompt_tuning/{middle_name}/epoch_0.csv"
    initial_result = run_recommender(initial_prompt, recommender=recommender, optimizer=optimizer, epoch=0,
                                     generated_output_path=generated_output_path, score_path=score_path)
    avg_performance = cal_avg_performance(initial_result)
    record = [assistant.id, 0, initial_prompt] + initial_result[[
        "group_auc", "mean_mrr", "ndcg_5", "ndcg_10"]].loc[0].tolist() + [avg_performance]
    monitor_columns = ["id", "epoch", "prompt_template", "group_auc", "mean_mrr", "ndcg_5", "ndcg_10", "avg_performance"]
    monitor_records = [record]
    monitor_path = f"result/prompt_tuning/{middle_name}/monitor_scores.csv"
    monitor_scores = update_monitor_scores(monitor_records, monitor_path, monitor_columns)
    best_scores = {"epoch": 0, "best_performance": avg_performance, "best_prompt_temp": initial_prompt}
    data_cols = ["impression_id", "history", "candidate", "label", "output"]
    thread = client.beta.threads.create()
    thread_id = thread.id
    for epoch in range(0, kwargs.get("epochs", 5)):
        generated_output_path = f"generated_data/prompt_tuning/{middle_name}/epoch_{epoch}.csv"
        samples = kwargs.get("samples", pd.read_csv(generated_output_path))
        line = {col: samples.loc[random.randint(0, len(samples)), col] for col in data_cols}
        line["full_prompt"] = Template(prompt_temp).safe_substitute(history=line["history"],
                                                                    candidate=line["candidate"])
        prompt4opt = build_prompt4opt(prompt_temp=initial_prompt, history=line["history"],
                                      candidate=line["candidate"], answer=line["output"], click=line["label"])

        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=prompt4opt
        )
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant.id,
        )
        while 1:
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )
            messages = client.beta.threads.messages.list(thread_id=thread_id)
            if run.status == "completed" and messages is not None:
                break
        current_prompt_temp = messages.data[0].content[0].text.value
        match = re.search(r"# Prompt Template Begin\n(.*)# Prompt Template End", current_prompt_temp, re.DOTALL)
        if match is not None:
            current_prompt_temp = match.group(1)
        else:
            print(current_prompt_temp)
            continue
        if "${history}" not in current_prompt_temp or "${candidate}" not in current_prompt_temp:
            print(current_prompt_temp)
            continue
        else:
            current_result = run_recommender(current_prompt_temp, recommender=recommender, optimizer=optimizer,
                                             epoch=epoch+1, generated_output_path=generated_output_path,
                                             score_path=score_path)
            avg_performance = cal_avg_performance(current_result)
            record = [assistant.id, epoch+1, current_prompt_temp] + current_result[[
                "group_auc", "mean_mrr", "ndcg_5", "ndcg_10"]].loc[0].tolist() + [avg_performance]
            monitor_records.append(record)
            monitor_scores = update_monitor_scores(monitor_records, monitor_path, monitor_columns)
            if avg_performance > best_scores["best_performance"]:
                best_scores["epoch"] = epoch + 1
                best_scores["best_performance"] = avg_performance
                best_scores["best_prompt_temp"] = current_prompt_temp
    with open(f"result/prompt_tuning/{middle_name}/best_scores.json", "w") as f:
        json.dump(best_scores, f)
    return monitor_scores, best_scores


if __name__ == "__main__":
    seed_everything(42)
    args = load_cmd_line()
    # initial_result = run_recommender(initial_prompt, epoch=0, **args["cmd_args"])
    build_optimizer(epochs=5, **args["cmd_args"])

