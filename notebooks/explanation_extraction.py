import pandas as pd
from string import Template
from pathlib import Path
from tqdm import tqdm
from common import load_cmd_line, to_format_excel, check_empty
from rec_utils import request_llama

extraction_temp = """You should only extract topics from the content below and do not generate or create topics that do not exist under "# Input".
# Input
```
${output}
```
The topics of the user's interests usually appear in the context like "The user's interests ... focus on ..." or "The user is interested in ...". Ignore the topics that are mentioned for candidate news "C#" in the context, like "C# is about ..., which might interest the user".
Your response should be in the following format:
```json
{
    "user_interests": ["xxx", "xxx", "xxx"],

}
```
You should output all topics that the user is interested in under keyword "user_interests". 
Please response with the above json format as the output only.
"""

sys_inst = """You are a helpful assistant designed to output JSON. You are aim to extract the user's interests from the given input content under "#Input"."""


if __name__ == "__main__":
    args = load_cmd_line()
    root_dir = args.get("root_dir", "explanation")
    explanation_file = args.get("explanation_file")
    saved_filename = args.get("saved_filename", "sample10_no_example.xlsx")
    saved_path = Path(f"{root_dir}/{saved_filename}")
    saved_cols = ["impression_id", "label", "history", "candidate", "output", "json_string"]
    column_widths = {
        "A:B": 15, "C:XFD": 80  # XFD is the last column in Excel
    }
    if saved_path.exists():
        df = pd.read_excel(saved_path)
    else:
        df = pd.read_csv(f"{root_dir}/{explanation_file}")
    for index in df.index:
        line = df.loc[index]
        if "json_string" in line and not check_empty(line["json_string"]):
            continue
        output = line["output"]
        extraction_prompt = Template(extraction_temp).safe_substitute({"output": output})
        params = {
            "temperature": 0, "system_instruction": sys_inst,
        }
        df.loc[index, "json_string"] = request_llama(extraction_prompt, **params)
        saved_path = f"{root_dir}/{saved_filename}"
        to_format_excel(df[saved_cols], saved_path, column_widths=column_widths)
        print(index, df.loc[index, "json_string"])
