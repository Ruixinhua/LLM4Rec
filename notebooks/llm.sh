#PJM -L rscgrp=share
#PJM -L elapse=06:00:00
#PJM -g gd72
#PJM -L gpu=1
#PJM -j
module load cuda/12.0
source /work/gd72/d72000/LLM4Rec/llm4rec/bin/activate
cache_root="/work/gd72/share/cache"
export XDG_CACHE_HOME=$cache_root
export HF_DATASETS_CACHE=$cache_root
export TRANSFORMERS_CACHE=/work/gd72/share/cache  # setup pretrained model weights cache
export 'PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:32'
model_name="Llama-2-7b-hf"
prompt_temp="naive_zero_shot"
python llm_inference.py --model_name=$model_name --max_new_tokens=128 --prompt_temp=$prompt_temp
