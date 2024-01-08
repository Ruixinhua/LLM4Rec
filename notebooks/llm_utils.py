import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from common import load_api_key


def load_model_tokenizer(model_name, **kwargs):
    cache_dir = kwargs.get("cache_dir", None)
    token = load_api_key(kwargs.get("hg_token_path", "hf_token.json"))
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        cache_dir=cache_dir,
        token=token,
        force_download=False,
    )
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        cache_dir=cache_dir,
        token=token,
        force_download=False,
        device_map="auto",
        torch_dtype=torch.float16 if kwargs.get("fp16", False) else "auto",
    )
    return model, tokenizer


def inference_llm_hf(model, tokenizer, full_prompt, **kwargs):
    torch.cuda.empty_cache()
    inputs = tokenizer(full_prompt, return_tensors="pt")
    input_ids = inputs.input_ids.to(model.device)
    while True:
        try:
            generate_ids = model.generate(
                input_ids,
                max_length=kwargs.get("max_length", 2048),
                max_new_tokens=kwargs.get("max_new_tokens", 1024),
                do_sample=kwargs.get("do_sample", False),
            )
            output = tokenizer.batch_decode(
                generate_ids,
                skip_special_tokens=True,
                clean_up_tokenization_spaces=False,
            )[0][len(full_prompt):]
            return output
        except Exception as e:
            print(e)
            torch.cuda.empty_cache()
