import os
import pandas as pd
import numpy as np
import pandas as pd
from tqdm import tqdm
from common import function_dispatcher
from prompt import *
from request_api import *
import sys


import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(os.path.join(parent_dir, 'notebooks'))
from utils import convert2list, save2csv, cal_avg_scores, seed_everything, extract_output, evaluate_list, extract_raw_output
import metric_utils as module_metric



metric_list = ["group_auc", "mean_mrr", "ndcg_5", "ndcg_10"]
metric_funcs = [getattr(module_metric, met) for met in metric_list]
data_cols = ["impression_id","history","candidate","label","history_news_id","history_title","history_category","history_subvert","history_abstract","candidate_news_id","candidate_title","candidate_category","candidate_subvert","candidate_abstract"]


def run(func, tag):
    # for i in range(1, 5):
    for i in [5]:
        folder_path = f"../notebooks/test_group/variant{i}"

        for filename in os.listdir(folder_path):
            results = []
            if filename.endswith(".csv"):
                file_path = os.path.join(folder_path, filename)
                origin_df = pd.read_csv(file_path)
                print("Path: ", file_path)
                print("Shape: ", origin_df.shape)
                
                result_path = f"result/{filename[:-4]}_{tag}_result.csv"
                score_path = f"result/{filename[:-4]}_{tag}_metric.csv"
                for index in range(origin_df.shape[0]):
                    line = {col: origin_df.loc[index, col] for col in data_cols}

                    prompt_input = func(line['history'], line["candidate"])

                    line["output"]  = request_from_llama2(prompt_input)
                    print(line["output"])
                    
                    line["rank"] = ','.join(extract_raw_output(line["output"], line["candidate"]))
                    
                    output_list, label_list = convert2list(line["rank"], line["label"], line["candidate"])

                    line.update(evaluate_list(output_list, label_list, metric_funcs))

                    results.append(line)
                    save2csv(results, result_path)
                    cal_avg_scores(results, score_path, 'llama2-70b-chat', metric_list)

if __name__ == '__main__':
    # if len(sys.argv) > 1:
    #     choice = sys.argv[1]
    # else:
    #     choice = "0"
    seed_everything()

    func = function_dispatcher.get('dairui4')
    run(func, tag='dairui4')

    func = function_dispatcher.get('dairui15')
    run(func, tag='dairui15')

    func = function_dispatcher.get('dairui16')
    run(func, tag='dairui16')