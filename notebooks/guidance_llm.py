import os
import templates
import pandas as pd
from common import load_cmd_line, load_api_key
from utils import seed_everything
from prompt_tuning import run_recommender
import sys
sys.path.append("../")


if __name__ == "__main__":
    args = load_cmd_line()
    os.environ['OPENAI_API_KEY'] = load_api_key()
    seed_everything(args.get("seed", 42))
    template_no = args.get("template_no", 4)
    num = args.get("num", 100)
    data_root_dir = args.get("data_root_dir", "test_group/variant5")
    variant_name = args.get("variant_name", "cold_user-match_topic-fix_candidate")
    sampled_df = pd.read_csv(f"{data_root_dir}/{variant_name}.csv")
    samples = sampled_df.sample(num)
    model_name = args.get("model_name", "gpt-3.5-turbo")
    temperature = args.get("temperature", 0)
    suffix = f"template-{template_no}_{model_name}_temperature-{temperature}_{variant_name}"
    generated_data_root = f"generated_data/{data_root_dir}_{num}"
    os.makedirs(generated_data_root, exist_ok=True)
    score_root = f"result/{data_root_dir}_{num}"
    generated_output_path = f"{generated_data_root}/{suffix}.csv"
    os.makedirs(score_root, exist_ok=True)
    score_path = f"{score_root}/{suffix}.csv"
    user_template = getattr(templates, f"template{template_no}")
    params = {
        "samples": samples, "recommender": model_name, "temperature": temperature,
        "generated_output_path": generated_output_path, "score_path": score_path
    }
    df = run_recommender(user_template, **params)
    df["template_no"] = template_no
    df["data_group"] = variant_name
    df.to_csv(score_path, index=False)
