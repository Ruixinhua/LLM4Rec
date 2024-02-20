import re
import json
import pandas as pd
from string import Template
from pathlib import Path
from common import load_cmd_line, to_format_excel
from rec_utils import request_llama

check_correctness = """# User's History
${history}
# Summarized Topics
${topics}
# Output Format
```json
{
    "correctness": {
        "xxx": 1,
        "xxx": 0,
        "xxx": 1,
        ...
        "xxx": 1
    }
}
```
For each topic, 1 means the topic is related to the user's historical records, 0 means the topic is irrelevant. 
"""

correct_instr = """You are a helpful assistant designed to output JSON. You are given a list of news headlines from a user's historical news consumption and a list of topics summarized from these headlines. You are aim to determine the correctness of these topics according to the given historical headlines."""


if __name__ == "__main__":
    args = load_cmd_line()
    root_dir = args.get("root_dir", "explanation")
    explanation_file = args.get("explanation_file")
    if explanation_file is None:
        raise ValueError("Please specify the explanation file.")
    saved_filename = args.get("saved_filename", "sample10_no_example.xlsx")
    saved_path = Path(f"{root_dir}/{saved_filename}")
    if saved_path.exists():
        df = pd.read_excel(saved_path)
    else:
        df = pd.read_excel(f"{root_dir}/{explanation_file}")
    column_widths = {
        "A:B": 15, "C:XFD": 80  # XFD is the last column in Excel
    }
    if "user_interest" not in df.columns:
        df["user_interest"] = df.json_string.apply(
            lambda x: json.loads("{" + re.findall(r"\{(.*?)\}", x, re.DOTALL)[0].rstrip(',\n') + "}")
        )
    saved_cols = ["impression_id", "label", "history", "candidate", "output", "user_interest", "correctness"]
    for index in df.index:
        line = df.loc[index]
        history, topics = line["history"], line["user_interest"]["user_interests"]
        extraction_prompt = Template(check_correctness).safe_substitute({"history": history, "topics": topics})
        params = {"temperature": 0, "system_instruction": correct_instr}
        df.loc[index, "correctness"] = request_llama(extraction_prompt, **params)
        saved_path = f"{root_dir}/{saved_filename}"
        to_format_excel(df[saved_cols], saved_path, column_widths=column_widths)
        print(index, df.loc[index, "correctness"])
