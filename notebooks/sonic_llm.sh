#!/bin/bash -l
#SBATCH --job-name=LLM4Rec-llama
# speficity number of nodes
#SBATCH -N 1
# specify the gpu queue

#SBATCH --partition=csgpu
# Request 2 gpus
#SBATCH --gres=gpu:2
# specify number of tasks/cores per node required
#SBATCH --ntasks-per-node=35


# specify the walltime e.g 20 mins
#SBATCH -t 168:00:00

# set to email at start,end and failed jobs
#SBATCH --mail-type=ALL
#SBATCH --mail-user=dairui.liu@ucdconnect.ie
# run from current directory
cd $SLURM_SUBMIT_DIR
export PYTHONPATH=PYTHONPATH:./:../:../modules
cache_root="/scratch/16206782/hg_cache"
export XDG_CACHE_HOME=$cache_root
export HF_DATASETS_CACHE=$cache_root
export TRANSFORMERS_CACHE=$cache_root  # setup pretrained model weights cache
nvidia-smi
conda activate explainable_nrs
model_name="Llama-2-7b-hf"

python guidance_llm.py --model_name=$model_name
#python llm_inference.py --model_name=$model_name --max_new_tokens=$max_new_tokens --prompt_temp=$prompt_temp
#python llm_inference.py --model_name="Llama-2-7b-hf" --max_new_tokens=$max_new_tokens --prompt_temp=$prompt_temp
#python llm_inference.py --model_name="Llama-2-13b-hf" --max_new_tokens=$max_new_tokens --prompt_temp=$prompt_temp
#python llm_inference.py --model_name="Llama-2-7b-chat-hf" --max_new_tokens=$max_new_tokens --prompt_temp=$prompt_temp
#python llm_inference.py --model_name="Llama-2-13b-chat-hf" --max_new_tokens=$max_new_tokens --prompt_temp=$prompt_temp