import pandas as pd
import guidance
import metric_utils as module_metric
from tqdm import tqdm
from string import Template
from common import load_api_key, load_cmd_line
from utils import convert2list, save2file, cal_avg_scores, seed_everything, extract_output, evaluate_list, extract_raw_output
import templates
from templates import gpt_template, llama_template


def is_descending(lst):
    # 遍历列表中的每个元素（除了最后一个）
    for i in range(len(lst) - 1):
        # 如果当前元素小于下一个元素，则列表不是降序的
        if lst[i] < lst[i + 1]:
            return False
    # 如果没有找到任何违反降序的元素，则返回 True
    return True


if __name__ == "__main__":
    # we use LLaMA here, but any GPT-style model will do
    args = load_cmd_line()
    seed_everything(args.get("seed", 42))
    # template_list = {1: template1, 2: template2, 3: template3, 4: template4, 5: template5}
    template_no = args.get("template_no", 4)
    num = args.get("num", 1000)
    data_used = args.get("data_used", "order")
    sampled_df = pd.read_csv(f"sampled_1000_{data_used}.csv")
    # sampled_df["candidate"] = sampled_df["candidate"].apply(shuffle_candidates)
    samples = sampled_df.sample(num)
    model_name = args.get("model_name", "gpt-3.5-turbo")
    temperature = args.get("temperature", 0)
    suffix = f"template-{template_no}_{model_name}_{data_used}_temperature-{temperature}"
    result_path = f"generated_data/{suffix}.csv"
    score_path = f"result/{suffix}.csv"
    data_cols = ["impression_id", "history", "candidate", "label"]
    user_template = getattr(templates, f"template{template_no}")
    if "gpt" in model_name.lower():
        model = guidance.llms.OpenAI(model_name, api_key=load_api_key())
        template = Template(gpt_template).safe_substitute({"temperature": temperature, "input": user_template})
    else:
        model = guidance.llms.Transformers(f"meta-llama/{model_name}", device_map="auto")
        template = Template(llama_template).safe_substitute({"input": user_template})
    metric_list = ["group_auc", "mean_mrr", "ndcg_5", "ndcg_10"]
    # metric_list = ["nDCG@5", "nDCG@10", "MRR"]
    metric_funcs = [getattr(module_metric, met) for met in metric_list]
    results = []
    in_order_ratio = 0
    for index in tqdm(samples.index, total=len(samples)):
        line = {col: samples.loc[index, col] for col in data_cols}
        experts = guidance(template, llm=model, silent=True)
        out = experts(history=line["history"], candidate=line["candidate"])
        line["output"] = out["rank"]
        if data_used == "order":
            line["rank"] = ','.join(extract_output(out["rank"], line["candidate"]))
        else:
            line["rank"] = ','.join(extract_raw_output(out["rank"], line["candidate"]))
        output_list, label_list = convert2list(line["rank"], line["label"], line["candidate"])
        in_order_ratio += 1 if is_descending(output_list) else 0
        line.update(evaluate_list(output_list, label_list, metric_funcs))
        results.append(line)
        save2file(results, result_path)
        cal_avg_scores(results, score_path, model_name, metric_list)
    print(f"the ratio of in-order output is {in_order_ratio / num}")