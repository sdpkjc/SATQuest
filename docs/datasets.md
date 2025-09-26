# Datasets

SATQuest bundles paired SAT/UNSAT CNF instances that can be consumed directly via Hugging Face Datasets or regenerated locally with the provided scripts. Each record contains solver metadata for every supported problem family, making it straightforward to benchmark models across SAT decision, optimisation, and explanation tasks.

## Hosted Collections

- `sdpkjc/SATQuest`: evaluation-ready split of 140 paired CNFs. The public `test` split powers examples in the quickstart and evaluation scripts.
- `sdpkjc/SATQuest-RFT-3k`: 3k training items designed for reinforcement fine-tuning. Instances cover a broader clause-to-variable ratio to encourage curriculum-style training.
- `sdpkjc/SATQuest-RFT-1k`: a lighter-weight variant suitable for prototyping reward functions or running ablations.

Download items with the standard `datasets` API:

```python
from datasets import load_dataset

cnf_eval = load_dataset("sdpkjc/SATQuest", split="test")
cnf_rft = load_dataset("sdpkjc/SATQuest-RFT-3k", split="train")
```

## Record Structure

Every row combines both satisfiable and unsatisfiable versions of the same CNF:

- `id`: stable integer identifier.
- `sat_dimacs` / `unsat_dimacs`: DIMACS-encoded strings for satisfiable and unsatisfiable variants.
- `num_variable`, `num_clause`: counts derived from the unsatisfiable formula (the satisfiable one matches except for literal flips).
- `num_literal`: total literal occurrences across clauses.
- `solver_metadatas`: dictionary mapping each problem type to solver traces (solution string, max weight, MUS indices, etc.).

Use the helper classes to inspect or transform instances:

```python
from satquest import CNF

row = cnf_eval[0]
cnf_unsat = CNF(dimacs=row["unsat_dimacs"])
print(cnf_unsat.nv, cnf_unsat.mc)
print(cnf_unsat.clauses[:2])
```

## Reproducing the Dataset

Both generation scripts draw random clauses, enforce deduplication, and attach solver statistics before uploading to Hugging Face. Set your own entity to publish results under your account:

```bash
uv run --group gen gen_cnf_dataset.py --hf-entity <your_org_or_handle> --seed 9527
uv run --group gen gen_cnf_rft_dataset.py --hf-entity <your_org_or_handle> --seed 9527
```

Key implementation details:

- Unsatisfiable formulas are produced first; satisfiable partners are created by flipping literals until a satisfying assignment emerges (`unsat2sat`).
- `post_process_fn` shuffles literals deterministically per seed, so different runs share difficulty profiles without leaking solutions.
- Solver metadata is recorded for every problem class (`SATSP`, `SATDP_SAT`, `SATDP_UNSAT`, `MaxSAT`, `MCS`, `MUS`) to support diverse reward functions.

## Customising Generation

- **Clause density**: tune the ratio `A` inside the scripts (`m = int(n * A)`) to target specific hardness regimes.
- **Variable range**: adjust the loop bounds for `N` to create larger instances.
- **Additional annotations**: extend `post_process_fn` to log heuristic statistics or include natural-language paraphrases so the same workflow can power new question generators.

Remember to keep seeds fixed when comparing models across experiments to maintain reproducibility.
