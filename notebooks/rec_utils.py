import os
import time
import json
import guidance
import openai

import metric_utils as module_metric
import pandas as pd
import numpy as np
import urllib.request
from string import Template
from tqdm import tqdm
import sys
sys.path.append("../")
from common import load_api_key
from templates import gpt_template
import templates
from utils import convert2list, save2csv, cal_avg_scores, extract_output, evaluate_list
from llm_utils import load_model_tokenizer, inference_llm_hf


def is_descending(lst):
    for i in range(len(lst) - 1):
        if lst[i] < lst[i + 1]:
            return False
    return True


def build_instruction():
    return "You serve as a personalized news recommendation system."


def request_llama(user_content, **kwargs):
    url = "http://bendstar.com:8000/v1/chat/completions"
    req_header = {
        'Content-Type': 'application/json',
    }
    system_instruction = kwargs.get("system_instruction", build_instruction())
    chat_completion = json.dumps({
        "model": "meta-llama/Llama-2-70b-chat-hf",
        "messages": [
            {"role": "system", "content": kwargs.get("system_instruction", system_instruction)},
            {"role": "user", "content": user_content}
        ],
        # "do_sample": kwargs.get("do_sample", False),
        "temperature": kwargs.get("temperature", 0.1),
    })
    req = urllib.request.Request(url, data=chat_completion.encode(), method='POST', headers=req_header)

    with urllib.request.urlopen(req) as response:
        body = json.loads(response.read())
        return body['choices'][0]['message']['content']


def request_gpt(messages, model="gpt-3.5-turbo", **model_params):
    """Set up the Openai API key using openai.api_key = api_key"""
    try:
        chat_completion = openai.ChatCompletion.create(
            model=model, messages=messages, **model_params
        )
        content = chat_completion.choices[0].message["content"]
        if content is None:
            time.sleep(20)
            content = request_gpt(messages, model, **model_params)
        return content
    except:
        time.sleep(20)
        return request_gpt(messages, model, **model_params)


def run_llm(model_name, llm_params, prompt_str, **kwargs):
    """
    :param model_name: a string indicating the model name
    :param llm_params: a dict with keys: temperature, max_tokens, seed
    :param prompt_str: a string indicating the prompt string with filled placeholders
    :param kwargs: a dict with keys: use_guidance, caching, system_instruction, candidate, use_hf
    """
    sys_instruct = kwargs.get("system_instruction", "sys_instruction")
    sys_instruct = getattr(templates, sys_instruct) if hasattr(templates, sys_instruct) else sys_instruct
    candidate = kwargs.get("candidate", None)
    if kwargs.get("use_hf", False):
        model, tokenizer = llm_params["model"], llm_params["tokenizer"]
        params = {
            "max_length": llm_params["max_length"], "max_new_tokens": llm_params["max_tokens"],
            "do_sample": llm_params["do_sample"]
        }
        # if "mixtral" in model_name.lower():
        #     full_prompt = ""
        full_prompt = prompt_str
        output = inference_llm_hf(model, tokenizer, full_prompt, **params)
        ranks = extract_output(output, candidate, match_pattern=False)
    else:
        if "llama" in model_name.lower():
            # from guidance import gen
            output = request_llama(prompt_str, system_instruction=sys_instruct, **llm_params)
            # full_prompt = Template(llama_template).safe_substitute(
            #     {"prompt_temp": prompt_str, "system_instruction": sys_instruct, "max_tokens": llm_params['max_tokens']}
            # )
            # output = guidance(full_prompt, silent=True)()["output"]
            full_prompt = prompt_str
            ranks = extract_output(output, candidate, match_pattern=False)
        else:  # default for openai models family
            caching = kwargs.get("caching", True)
            full_prompt = Template(gpt_template).safe_substitute(
                {"temperature": llm_params['temperature'], "prompt_temp": prompt_str, "seed": llm_params['seed'],
                 "system_instruction": sys_instruct, "max_tokens": llm_params['max_tokens']}
            )
            if kwargs.get("use_guidance", True):
                model = guidance.llms.OpenAI(model_name, api_key=load_api_key(), chat_mode=True, caching=caching)
                output = guidance(full_prompt, llm=model, silent=True)()["output"]
            else:
                full_prompt = [{"role": "system", "content": sys_instruct}, {"role": "user", "content": prompt_str}]
                output = request_gpt(full_prompt, model=model_name, **llm_params)
            ranks = extract_output(output, candidate, match_pattern=True)
    return output, ranks, full_prompt


def run_recommender(prompt_template, **kwargs):
    """
    :param prompt_template: template of prompt with placeholders: history and candidate
    """
    data_group = kwargs.get("data_group", "sample100by_ratio")
    samples = kwargs.get("samples", pd.read_csv(f"valid/{data_group}.csv"))
    metric_list = ["group_auc", "mean_mrr", "ndcg_5", "ndcg_10"]
    data_cols = ["impression_id", "history", "candidate", "label"]
    metric_funcs = [getattr(module_metric, met) for met in metric_list]
    recommender_model = kwargs.get("recommender", "gpt-3.5-turbo")
    temperature = kwargs.get("temperature", 0)
    max_tokens = kwargs.get("max_tokens", 2048)
    max_output_tokens = kwargs.get("max_output_tokens", 8192)
    llm_seed = kwargs.get("llm_seed", 42)
    caching = kwargs.get("caching", True)
    openai.api_key = load_api_key()
    sys_instruct = kwargs.get("system_instruction", "sys_instruction")
    sys_instruct = getattr(templates, sys_instruct) if hasattr(templates, sys_instruct) else sys_instruct
    llm_params = {
        "temperature": temperature, "max_tokens": max_tokens, "seed": llm_seed
    }
    use_hf = kwargs.get("use_hf", False)
    use_guidance = kwargs.get("use_guidance", True)
    if use_hf:
        model, tokenizer = load_model_tokenizer(recommender_model)
        llm_params.update({
            "model": model, "tokenizer": tokenizer, "max_length": kwargs.get("max_length", 4096),
            "do_sample": kwargs.get("do_sample", False)
        })
    if "llama" in recommender_model.lower() and use_guidance:
        # from guidance import models
        # llm_params.update({"model": models.Transformers(recommender_model)})
        guidance.llm = guidance.llms.Transformers(recommender_model)
    epoch = kwargs.get("epoch", None)
    generated_output_path = f"generated_data/prompt_tuning/{recommender_model}/"
    if epoch is not None:
        generated_output_path += f"epoch_{epoch}_{llm_seed}.csv"
    else:
        generated_output_path += f"default.csv"
    generated_output_path = kwargs.get("generated_output_path", generated_output_path)
    score_path = f"result/prompt_tuning/{recommender_model}/epoch_{epoch}_{llm_seed}.csv"
    score_path = kwargs.get("score_path", score_path)
    os.makedirs(os.path.dirname(generated_output_path), exist_ok=True)
    os.makedirs(os.path.dirname(score_path), exist_ok=True)
    results = []
    in_order_ratio = 0
    for index in tqdm(samples.index, total=len(samples)):
        line = {col: samples.loc[index, col] for col in data_cols}
        prompt_str = Template(prompt_template).safe_substitute(history=line["history"], candidate=line["candidate"])
        run_kwargs = {
            "use_guidance": use_guidance, "caching": caching, "system_instruction": sys_instruct,
            "candidate": line["candidate"], "use_hf": use_hf
        }
        output, ranks, full_prompt = run_llm(recommender_model, llm_params, prompt_str, **run_kwargs)
        current_max_tokens = max_tokens
        while ranks is False and current_max_tokens < max_output_tokens:
            current_max_tokens = current_max_tokens * 2
            llm_params["max_tokens"] = current_max_tokens
            output, ranks, full_prompt = run_llm(recommender_model, llm_params, prompt_str, **run_kwargs)
        if ranks is False:
            continue
        line["rank"] = ','.join(ranks)
        line["full_prompt"] = full_prompt
        line["output"] = output
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
