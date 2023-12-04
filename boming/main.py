import os
import pandas as pd
import numpy as np
import pandas as pd
from tqdm import tqdm
from common import *
from prompt import *
from request_api import *
import sys

score_path = f"result/metrics_news.csv"
metric_list = ["nDCG@5", "nDCG@10", "MRR"]

def run(func):
    for i in range(1, 5):
        folder_path = f"../notebooks/test_group/variant{i}"

        results = []
        for filename in os.listdir(folder_path):
            if filename.endswith(".csv"):
                file_path = os.path.join(folder_path, filename)
                origin_df = pd.read_csv(file_path)
                print("Path: ", file_path)
                print("Shape: ", origin_df.shape)
                
                result_path = f"result/{filename[:-4]}_result.csv"

                for j in range(origin_df.shape[0]):
                    history = origin_df.loc[j, 'history']
                    candidate = origin_df.loc[i, 'history']

                    prompt_input = func(history, candidate)

                    response = request_from_gpt(prompt_input)
                    print(response)
                    
                    # save2file(results, result_path)
                    # result_df = cal_avg_scores(results, model_name, metric_list, choice)

            # if os.path.exists(score_path):
            #     result_df.to_csv(score_path, mode='a', index=False, header=False)
            # else:
            #     result_df.to_csv(score_path, index=False)
                                


if __name__ == '__main__':
    if len(sys.argv) > 1:
        choice = sys.argv[1]
    else:
        choice = "0"
    func = function_dispatcher.get(choice)

    run(func)