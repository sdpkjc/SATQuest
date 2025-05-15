# SATQuest: A Verifier for Logical Reasoning Evaluation and Reinforcement Fine-Tuning of LLMs

## 🚀 Quickstart

```python
# Install dependencies
# pip install datasets satquest

from datasets import load_dataset
from satquest import CNF, create_problem, create_question
cnf = CNF(dimacs=load_dataset('sdpkjc/SATQuest', split='test')[0]['sat_dimacs'])
# cnf.shuffle()
P, Q = create_problem('SATSP', cnf), create_question('math')
prompt = P.accept(Q)
answer = P.solution # LLM(prompt)
reward = int(P.check(answer))
```

## Dataset Generation

```bash
# Install dependencies
pip install datasets numpy tyro

# Run dataset generation
python gen_cnf_dataset.py --hf-entity {YOUR_HF_ENTITY} --seed 9527

python gen_cnf_rft_dataset.py --hf-entity {YOUR_HF_ENTITY} --seed 9527
```

## Evaluation

```bash
# Install dependencies
pip install datasets weave wandb tyro openai

# Run evaluation
python eval_model.py \
    --exp-name {YOUR_EXP_NAME} \
    --wandb-project "SATQuest-Eval" \
    --hf-dataset-name "sdpkjc/SATQuest" \
    --p-type-list SATSP \
    --q-type-list math \
    --llm-model "gpt-4o" \
    --max-tokens 16384 \
    --temperature 0.6 \
    --num-example 10 \
    --stream True \
    --cnf-shuffle False \
    --n-repeat 1
```

### Evaluation Parameters

- `exp-name`: Name of your experiment
- `wandb-project`: Weights & Biases project name
- `hf-dataset-name`: HuggingFace dataset name
- `p-type-list`: Problem types to evaluate (e.g., "SATSP", "MaxSAT", "MCS", "MUS", "SATDP_SAT", "SATDP_UNSAT")
- `q-type-list`: Question types to evaluate (e.g., "math", "dimacs", "story", "dualstory")
- `llm-model`: LLM model to use for evaluation
- `max-tokens`: Maximum tokens for LLM response
- `temperature`: Temperature for LLM generation
- `num-example`: Number of examples to evaluate
- `stream`: Whether to stream LLM responses
- `cnf-shuffle`: Whether to shuffle CNF formulas
- `n-repeat`: Number of times to repeat evaluation

The evaluation results will be logged to Weights & Biases, including:
- Correctness of answers
- Format correctness
- Detailed evaluation metrics

## Reinforcement Fine-Tuning (RFT)

```bash
# Install dependencies
pip install git+https://github.com/huggingface/trl.git@aaf396  # for reproducibility
pip install datasets vllm tyro

# Run RFT training
CUDA_VISIBLE_DEVICES=0,1,2,3 nohup trl vllm-serve --model "Qwen/Qwen2.5-7B-Instruct" --tensor_parallel_size 4 --max_model_len 16384  --gpu_memory_utilization 0.9 --enable_prefix_caching True &
CUDA_VISIBLE_DEVICES=4,5,6,7 accelerate launch --num-processes 4 --config-file zero3.yaml rft.py --model-id "Qwen/Qwen2.5-7B-Instruct" --p-list SATSP --q-list math --exp-name "test" --server-ip "0.0.0.0"
```

### RFT Parameters

- `model-id`: Base model to fine-tune (default: "Qwen/Qwen2.5-7B-Instruct")
- `p-list`: Problem types for training (e.g., "SATSP", "MaxSAT", "MCS", "MUS", "SATDP_SAT", "SATDP_UNSAT")
- `q-list`: Question types for training (e.g., "math", "story")
- `exp-name`: Name of your experiment
- `server-ip`: IP address for VLLM server

### Training Details

The RFT process uses GRPO (Generative Reinforcement Policy Optimization) with the following features:

- **Reward Functions**:
  - Score reward: Evaluates answer correctness
  - Tag count reward: Ensures proper formatting with `<think>` and `<answer>` tags
  - Format reward: Checks overall response structure

- **Training Configuration**:
  - Uses VLLM for efficient inference
  - Gradient checkpointing enabled
  - BF16 mixed precision training
  - Cosine learning rate scheduler
  - Maximum prompt length: 2048 tokens
  - Maximum completion length: 8192 tokens

The model is trained on the "sdpkjc/SATQuest-RFT-3k" dataset, which contains examples for various problem and question types.
