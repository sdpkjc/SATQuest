# SATQuest 🚀

<div align="center">

<img src="./media/satquest.png" width="450">

<br>

[![License](https://img.shields.io/pypi/l/satquest)](https://github.com/sdpkjc/satquest)
[![arXiv](https://img.shields.io/badge/arXiv-2509.00930-b31b1b.svg)](https://arxiv.org/abs/2509.00930)
[![GitHub Repo](https://img.shields.io/badge/GitHub-sdpkjc/SATQuest-181717?logo=github)](https://github.com/sdpkjc/SATQuest)
[![HF Datasets](https://img.shields.io/badge/HF-datasets-orange?logo=huggingface)](https://huggingface.co/collections/sdpkjc/satquest-6820687d856b96f869921e53)
[![PyPI](https://img.shields.io/pypi/v/satquest?logo=pypi)](https://pypi.org/project/satquest/)

[![docs](https://img.shields.io/github/deployments/sdpkjc/SATQuest/Production?label=docs&logo=vercel)](https://SATQuest.sdpkjc.com/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![python versions](https://img.shields.io/pypi/pyversions/satquest)](https://pypi.org/project/satquest)

</div>

SATQuest packages CNF-derived logical reasoning tasks, a verifier, and reinforcement fine-tuning (RFT) rewards so you can probe and improve LLM reasoning with controllable difficulty.

## 🧰 What's Inside

- CNF problems spanning three orthogonal dimensions: instance scale, problem type, and question format.
- A PySAT-backed verifier that scores binary answers and exposes solver metadata for reproducible diagnostics.
- Ready-to-use datasets on Hugging Face, evaluation scripts, and GRPO-style RFT recipes.

## ⚡ Quickstart

```python
from datasets import load_dataset
from satquest import CNF, create_problem, create_question

item = load_dataset("sdpkjc/SATQuest", split="test")[0]
cnf = CNF(dimacs=item["sat_dimacs"])

problem = create_problem("SATSP", cnf)
question = create_question("math")
prompt = problem.accept(question)
print(prompt)
print(problem.check(problem.solution))
```

## 🗺️ Explore the Workflow

- [Datasets](datasets.md): CNF schema, regeneration flags, and Hugging Face links.
- [Evaluate](evaluate.md): batch LLM scoring with Weave -> W&B logging.
- [Finetuning](finetuning.md): GRPO setup using the verifier-driven reward functions.
- [Examples](examples.md): prompts and API snippets for every problem/question pairing.

## 📈 Highlights from the Paper

- Reasoning-tuned models lead the leaderboard: `o3-mini` (0.56), `DeepSeek-R1` (0.42), `QwQ-32B` (0.40), and `DeepSeek-R1-Distill-Qwen-32B` (0.39) outperform vanilla LLMs such as `GPT-4.1` (0.38) and `DeepSeek-V3-0324` (0.36), while `Qwen2.5-7B-Instruct` stays below 0.10 accuracy.
- Accuracy drops as solver effort grows; hallucinated "reasoning shortcuts" appear on hard MCS/MUS instances, underscoring the need for verifier feedback.
- Question presentation matters: math prompts are easiest, whereas story/dualstory formats expose sizable regressions for open-weight models. RFT experiments show verifier rewards extend reasoning traces and transfer to harder instances, but cross-format generalisation remains challenging.

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
