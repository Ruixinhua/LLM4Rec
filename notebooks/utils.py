import pandas as pd


def evaluate_performance(performance, metric_cols=None):
    if metric_cols is None:
        metric_cols = ["MRR", "nDCG@5", "nDCG@10"]
    performance_df = pd.DataFrame.from_records(performance, columns=["ID"] + metric_cols)
    avg_values = performance_df[["MRR", "nDCG@5", "nDCG@10"]].mean().round(3).tolist()
    tmp_list = performance.copy() + [["avg_value"] + avg_values]
    performance_df = pd.DataFrame.from_records(tmp_list, columns=["ID"] + metric_cols)
    return performance_df
