# SATQuest

![satquest](./media/satquest.png)

SATQuest packages CNF-derived logical reasoning tasks, a verifier, and reinforcement fine-tuning (RFT) rewards so you can probe and improve LLM reasoning with controllable difficulty.

## What's Inside

- CNF problems spanning three orthogonal dimensions: instance scale, problem type, and question format (as highlighted in the paper).
- A PySAT-backed verifier that scores binary answers and exposes solver metadata for reproducible diagnostics.
- Ready-to-use datasets on Hugging Face, evaluation scripts, and GRPO-style RFT recipes.

## Quickstart

```bash
uv sync
```

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

## Explore the Workflow

- [Datasets](datasets.md): CNF schema, regeneration flags, and Hugging Face links.
- [Evaluate](evaluate.md): batch LLM scoring with Weave -> W&B logging.
- [Finetuning](finetuning.md): GRPO setup using the verifier-driven reward functions.
- [Examples](examples.md): prompts and API snippets for every problem/question pairing.

## Highlights from the Paper

- Reasoning-tuned models lead the leaderboard: `o3-mini` (0.56), `DeepSeek-R1` (0.42), `QwQ-32B` (0.40), and `DeepSeek-R1-Distill-Qwen-32B` (0.39) outperform vanilla LLMs such as `GPT-4.1` (0.38) and `DeepSeek-V3-0324` (0.36), while `Qwen2.5-7B-Instruct` stays below 0.10 accuracy.
- Accuracy drops as solver effort grows; hallucinated "reasoning shortcuts" appear on hard MCS/MUS instances, underscoring the need for verifier feedback.
- Question presentation matters: math prompts are easiest, whereas story/dualstory formats expose sizable regressions for open-weight models. RFT experiments show verifier rewards extend reasoning traces and transfer to harder instances, but cross-format generalisation remains challenging.

## Citing SATQuest

```bibtex
@misc{satquest2025,
  author = {Yanxiao Zhao and Yaqian Li and Zihao Bo and Rinyoichi Takezoe and Haojia Hui and Mo Guang and Lei Ren and Xiaolin Qin and Kaiwen Long},
  title = {SATQuest: A Verifier for Logical Reasoning Evaluation and Reinforcement Fine-Tuning of LLMs},
  year = {2025},
  howpublished = {\url{https://github.com/sdpkjc/SATQuest}}
}
```
