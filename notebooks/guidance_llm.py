import os
import pandas as pd
from common import load_cmd_line, load_api_key
from utils import seed_everything
from prompt_tuning import run_recommender
import sys
sys.path.append("../")
import prompt_template as module_templates


if __name__ == "__main__":
    args = load_cmd_line()
    os.environ['OPENAI_API_KEY'] = load_api_key()
    seed_everything(args.get("seed", 42))
    template_name = args.get("template_name", "final")
    num = args.get("num", 100)
    data_root_dir = args.get("data_root_dir", "test_group/variant5")
    variant_name = args.get("variant_name", "sample400by_ratio")
    sampled_df = pd.read_csv(f"{data_root_dir}/{variant_name}.csv")
    samples = sampled_df.sample(num)
    model_name = args.get("model_name", "gpt-3.5-turbo")
    temperature = args.get("temperature", 0)
    llm_seed = args.get("llm_seed", 42)
    suffix = f"template-{template_name}_seed-{llm_seed}_{variant_name}{args.get('suffix', '')}"
    generated_data_root = f"generated_data/{model_name}/{data_root_dir}_{num}"
    os.makedirs(generated_data_root, exist_ok=True)
    score_root = f"result/{data_root_dir}_{num}"
    generated_output_path = f"{generated_data_root}/{suffix}.csv"
    os.makedirs(score_root, exist_ok=True)
    score_path = f"{score_root}/{model_name}/{suffix}.csv"
    user_template = getattr(module_templates, f"template_{template_name}")
    max_tokens = args.get("max_tokens", 2048)
    caching = args.get("caching", True)
    params = {
        "samples": samples, "recommender": model_name, "temperature": temperature, "llm_seed": llm_seed,
        "generated_output_path": generated_output_path, "score_path": score_path, "max_tokens": max_tokens,
        "caching": caching, "use_guidance": args.get("use_guidance", True)
    }
    df = run_recommender(user_template, **params)
    df["template_name"] = template_name
    df["data_group"] = variant_name
    df["llm_seed"] = llm_seed
    df.to_csv(score_path, index=False)
