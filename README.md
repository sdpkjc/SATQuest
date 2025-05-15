# SATQuest: A Verifier for Logical Reasoning Evaluation and Reinforcement Fine-Tuning of LLMs

## 🚀 Quickstart

```python
# !pip install datasets satquest
from datasets import load_dataset
from satquest import CNF, create_problem, create_question
cnf = CNF(dimacs=load_dataset('sdpkjc/SATQuest', split='test')[0]['sat_dimacs'])
# cnf.shuffle()
P, Q = create_problem('SATSP', cnf), create_question('math')
prompt = P.accept(Q)
answer = P.solution # LLM(prompt)
reward = int(P.check(answer))
```
