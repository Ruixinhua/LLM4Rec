# %%
import openai
import numpy as np
import pandas as pd
from tqdm import tqdm
from common import *
from prompt import *
import urllib.request
import json

url = "http://bendstar.com:8000/v1/chat/completions"
req_header = {
    'Content-Type': 'application/json',
}



openai.api_key = "EMPTY"
openai.api_base = "http://bendstar.com:8000/v1"
models = openai.Model.list()
model_name = models["data"][0]["id"]

# %%
sampled_df = pd.read_csv("sampled_100.csv")
samples = sampled_df.sample(100)
data_cols = ["impression_id", "history", "candidate", "label"]


result_path = f"result/sampled_100_result.csv"
score_path = f"result/metrics_key.csv"
metric_list = ["nDCG@5", "nDCG@10", "MRR"]
results = []

# %%
for index in tqdm(samples.index, total=len(samples)):
    line = {col: samples.loc[index, col] for col in data_cols}
    user_content = build_prompt(history=line["history"], candidate=line["candidate"])


    chat_completion = json.dumps({
        "model": "meta-llama/Llama-2-70b-chat-hf",
        "messages": [{"role": "system", "content": build_instruction()}, {"role": "user", "content": user_content}],
        "temperature": 0,
    })

    req = urllib.request.Request(url, data=chat_completion.encode(), method='POST', headers=req_header)

    with urllib.request.urlopen(req) as response:
        body = json.loads(response.read())
        headers = response.getheaders()
        status = response.getcode()
        print(body['choices'][0]['message']['content'])


    line["output"] = body['choices'][0]['message']['content']
    line.update(evaluate_output(line['output'], line["label"], metric_list))
    results.append(line)
    save2file(results, result_path)
    cal_avg_scores(results, score_path, model_name, metric_list)


# %%
