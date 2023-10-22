import pandas as pd


def evaluate_performance(performance):
    performance_df = pd.DataFrame.from_records(performance, columns=["ID", "MRR", "nDCG@5", "nDCG@10"])
    avg_values = performance_df[["MRR", "nDCG@5", "nDCG@10"]].mean().round(3).tolist()
    tmp_list = performance.copy() + [["avg_value"] + avg_values]
    performance_df = pd.DataFrame.from_records(tmp_list, columns=["ID", "MRR", "nDCG@5", "nDCG@10"])
    return performance_df
