# SATQuest: A Verifier for Logical Reasoning Evaluation and Reinforcement Fine-Tuning of LLMs

<div align="center">

<img src="./docs/media/satquest.png" width="450">

<br>

[![PyPI](https://img.shields.io/pypi/v/satquest?logo=pypi)](https://pypi.org/project/satquest/)
[![License](https://img.shields.io/pypi/l/satquest)](https://github.com/sdpkjc/satquest)
[![arXiv](https://img.shields.io/badge/arXiv-2509.00930-b31b1b.svg)](https://arxiv.org/abs/2509.00930)
[![GitHub Repo](https://img.shields.io/badge/GitHub-sdpkjc/SATQuest-181717?logo=github)](https://github.com/sdpkjc/SATQuest)
[![HF Datasets](https://img.shields.io/badge/HF-datasets-orange?logo=huggingface)](https://huggingface.co/collections/sdpkjc/satquest-6820687d856b96f869921e53)

[![pytest](https://github.com/sdpkjc/SATQuest/actions/workflows/pytest.yml/badge.svg)](https://github.com/sdpkjc/SATQuest/actions/workflows/pytest.yml)
[![pre-commit](https://github.com/sdpkjc/SATQuest/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/sdpkjc/SATQuest/actions/workflows/pre-commit.yml)
[![docs](https://img.shields.io/github/deployments/sdpkjc/SATQuest/Production?label=docs&logo=vercel)](https://SATQuest.sdpkjc.com/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Type Checked: Pyright](https://img.shields.io/badge/Type%20Checked-Pyright-blue)](https://github.com/microsoft/pyright)
[![python versions](https://img.shields.io/pypi/pyversions/satquest)](https://pypi.org/project/satquest)

</div>


## 🧰 What's Inside

- CNF-based problems spanning three orthogonal dimensions: instance scale, problem type, and question format.
- A PySAT-backed verifier that scores binary answers and exposes solver metadata for reproducible diagnostics.
- Ready-to-use datasets on Hugging Face, evaluation scripts, and RFT scripts.


## ⚡ Quickstart

```python
# Install dependencies
# pip install datasets satquest

from datasets import load_dataset

from satquest import CNF, create_problem, create_question

item = load_dataset("sdpkjc/SATQuest", split="test")[0]
cnf = CNF(dimacs=item["sat_dimacs"])
# cnf.shuffle()

problem = create_problem("SATSP", cnf)  # or 'SATDP', 'MaxSAT', 'MCS', 'MUS'
question = create_question("math")  # or 'dimacs', 'story', 'dualstory'

prompt = problem.accept(question)
"""
Given a CNF formula with 3 variables and 12 clauses in mathematical notation:

(x_1 \lor x_2 \lor x_3) \land (x_3 \lor \neg x_1 \lor x_2) \land (x_1 \lor x_3 \lor \neg x_2) \land (x_1 \lor \neg x_2) \land (x_3 \lor x_1 \lor \neg x_2) \land (x_3 \lor \neg x_1 \lor x_2) \land (\neg x_3 \lor \neg x_1) \land (\neg x_1 \lor x_2 \lor x_3) \land (\neg x_2 \lor \neg x_3) \land (\neg x_2 \lor x_3 \lor x_1) \land (x_1 \lor \neg x_3) \land (\neg x_3 \lor \neg x_2 \lor \neg x_1)

Find a satisfying assignment for the formula.
Output a binary string of length 3 ('1' for true, '0' for false).
"""

answer = problem.solution  # reference answer
# 110

reward = int(problem.check(answer))  # 1 if answer is correct, 0 otherwise, 0.5 if answer is partial
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

The evaluation results will be logged to Weights & Biases.

## 🏄 Reinforcement Fine-Tuning (RFT)

```bash
# Run RFT training
CUDA_VISIBLE_DEVICES=0,1,2,3 nohup uv run --group rft trl vllm-serve --model "Qwen/Qwen2.5-7B-Instruct" --tensor_parallel_size 4 --max_model_len 16384  --gpu_memory_utilization 0.9 --enable_prefix_caching True &

CUDA_VISIBLE_DEVICES=4,5,6,7 uv run --group rft accelerate launch --num-processes 4 --config-file zero3.yaml rft.py \
    --model-id "Qwen/Qwen2.5-7B-Instruct" \
    --p-list SATSP --q-list math \
    --server-ip "0.0.0.0" \
    --exp-name "test"
```


## 📝 Citing SATQuest

```bibtex
@misc{zhao2025satquestverifierlogicalreasoning,
    title={SATQuest: A Verifier for Logical Reasoning Evaluation and Reinforcement Fine-Tuning of LLMs}, 
    author={Yanxiao Zhao and Yaqian Li and Zihao Bo and Rinyoichi Takezoe and Haojia Hui and Mo Guang and Lei Ren and Xiaolin Qin and Kaiwen Long},
    year={2025},
    eprint={2509.00930},
    archivePrefix={arXiv},
    primaryClass={cs.AI},
    url={https://arxiv.org/abs/2509.00930}, 
}
```
