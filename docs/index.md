# **SATQuest**: A Verifier for Logical Reasoning Evaluation and Reinforcement Fine-Tuning of LLMs

![satquest](./media/satquest.png)

## 🚀 Quickstart

```python
# Install dependencies
# pip install datasets satquest

from datasets import load_dataset
from satquest import CNF, create_problem, create_question

item = load_dataset('sdpkjc/SATQuest', split='test')[0]
cnf = CNF(dimacs=item['sat_dimacs'])
# cnf.shuffle()

problem = create_problem('SATSP', cnf) # or 'SATDP', 'MaxSAT', 'MCS', 'MUS'
question = create_question('math')  # or 'dimacs', 'story', 'dualstory'
prompt = problem.accept(question)
'''
Given a CNF formula with 3 variables and 12 clauses in mathematical notation:

(x_1 \lor x_2 \lor x_3) \land (x_3 \lor \neg x_1 \lor x_2) \land (x_1 \lor x_3 \lor \neg x_2) \land (x_1 \lor \neg x_2) \land (x_3 \lor x_1 \lor \neg x_2) \land (x_3 \lor \neg x_1 \lor x_2) \land (\neg x_3 \lor \neg x_1) \land (\neg x_1 \lor x_2 \lor x_3) \land (\neg x_2 \lor \neg x_3) \land (\neg x_2 \lor x_3 \lor x_1) \land (x_1 \lor \neg x_3) \land (\neg x_3 \lor \neg x_2 \lor \neg x_1)

Find a satisfying assignment for the formula.
Output a binary string of length 3 ('1' for true, '0' for false).
'''
answer = problem.solution  # reference answer
# 110
reward = int(problem.check(answer))  # 1 if answer is correct, 0 otherwise
# 1
```

## 🏭 Dataset Generation

[![Dataset on HF](https://huggingface.co/datasets/huggingface/badges/resolve/main/dataset-on-hf-sm.svg)]([https://huggingface.co/sdpkjc/](https://huggingface.co/collections/sdpkjc/satquest-6820687d856b96f869921e53))

```bash
# Run dataset generation
uv run --group gen gen_cnf_dataset.py --hf-entity {YOUR_HF_ENTITY} --seed 9527

uv run --group gen gen_cnf_rft_dataset.py --hf-entity {YOUR_HF_ENTITY} --seed 9527
```

## 📊 Evaluation

```bash
# Run evaluation
uv run --group eval eval_model.py \
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

The evaluation results will be logged to Weights & Biases.

## 🏄 Reinforcement Fine-Tuning (RFT)

```bash
# Run RFT training
CUDA_VISIBLE_DEVICES=0,1,2,3 nohup uv run --group rft trl vllm-serve --model "Qwen/Qwen2.5-7B-Instruct" --tensor_parallel_size 4 --max_model_len 16384  --gpu_memory_utilization 0.9 --enable_prefix_caching True &
CUDA_VISIBLE_DEVICES=4,5,6,7 uv run --group rft accelerate launch --num-processes 4 --config-file zero3.yaml rft.py --model-id "Qwen/Qwen2.5-7B-Instruct" --p-list SATSP --q-list math --exp-name "test" --server-ip "0.0.0.0"
```

### RFT Parameters

- `model-id`: Base model to fine-tune (default: "Qwen/Qwen2.5-7B-Instruct")
- `p-list`: Problem types for training (e.g., "SATSP", "MaxSAT", "MCS", "MUS", "SATDP_SAT", "SATDP_UNSAT")
- `q-list`: Question formats for training (e.g., "math", "story")
- `exp-name`: Name of your experiment
- `server-ip`: IP address for VLLM server


## 🔖 Citing SATQuest

```bibtex
@misc{satquest2025,
  author = {Yanxiao Zhao, Yaqian Li, Zihao Bo, Rinyoichi Takezoe, Haojia Hui, Mo Guang, Lei Ren, Xiaolin Qin, Kaiwen Long},
  title = {SATQuest: A Verifier for Logical Reasoning Evaluation and Reinforcement Fine-Tuning of LLMs},
  year = {2025},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/sdpkjc/SATQuest}},
}
```
