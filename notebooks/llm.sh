#PJM -L rscgrp=share
#PJM -L elapse=00:28:00 (change time here)
#PJM -g gc86
#PJM -L gpu=2 (change gpu number here)
#PJM -j
#module load cuda/11.1
#module load pytorch/1.8.1
source /home/d72000/llm4rec/bin/activate
cache_root="/work/gd72/share/cache"
export XDG_CACHE_HOME=$cache_root
export HF_DATASETS_CACHE=$cache_root
export TRANSFORMERS_CACHE=$cache_root  # setup pretrained model weights cache
mind_root="/work/gd72/share/data/MIND"
python llm_inference.py --mind_root=$mind_root

