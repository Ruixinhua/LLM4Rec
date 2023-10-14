source llama/venv/bin/activate

# 句子补全
# torchrun --nproc_per_node 1 example_text_completion.py --ckpt_dir llama-2-7b --tokenizer_path tokenizer.model --max_seq_len 128 --max_batch_size 4


# 对话生成
torchrun --nproc_per_node 1 chat_completion.py     --ckpt_dir llama/llama-2-7b-chat    --tokenizer_path llama/tokenizer.model   --max_seq_len 512 --max_batch_size 6