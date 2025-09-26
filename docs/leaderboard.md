# Leaderboard

SATQuest tracks LLM reasoning across 140 paired CNFs (5 problem types x 4 prompt formats) using the verifier described in the paper. Use this page to compare against published numbers and append new runs.

## Benchmark Results

| Model | Family | Overall accuracy | Notes | Source |
| --- | --- | --- | --- | --- |
| o3-mini | Closed reasoning | 0.56 | Highest average accuracy across all SATQuest tasks. | Paper Fig. 2 |
| DeepSeek-R1 | Open reasoning | 0.42 | Maintains the best open-weight curve as instance complexity rises. | Paper Fig. 2 / Sec. 3 |
| QwQ-32B | Open reasoning | 0.40 | Drops sharply when moving from math -> story prompts. | Paper Fig. 2 / Sec. 3 |
| DeepSeek-R1-Distill-Qwen-32B | Distilled reasoning | 0.39 | Retains most of DeepSeek-R1's strength with a smaller footprint. | Paper Fig. 2 |
| GPT-4.1 | Closed vanilla | 0.38 | Competitive baseline without specialised reasoning tuning. | Paper Fig. 2 |
| DeepSeek-V3-0324 | Open vanilla | 0.36 | Strongest open-weight vanilla baseline. | Paper Fig. 2 |
| Qwen2.5-7B-Instruct | Open vanilla | <0.10 | Illustrates the challenge for small instruction-tuned models. | Paper Sec. 3 |
| DeepSeek-R1-Distill-Qwen-7B | Distilled reasoning | - | Evaluated in Table 1; aggregate accuracy not disclosed. | Paper App. D |
| Qwen2.5-32B-Instruct | Open vanilla | - | Evaluated in Table 1; aggregate accuracy not disclosed. | Paper App. D |

_All numbers average across all problem types and prompt formats on `sdpkjc/SATQuest`._

## How to Submit Results

1. **Run the evaluator** - `uv run --group eval eval_model.py` with your model settings (see [Evaluate](evaluate.md)).
2. **Log to W&B** - we use the `SATQuest-Eval` project; keep `--cnf-shuffle` and dataset revisions explicit for reproducibility.
3. **Open a PR** - add a row to the table above (including accuracy, configuration, and a link to the run) or link to an external report. Qualitative examples or failure cases are welcome.

## Comparability Checklist

- Keep problem/question lists and `--cnf-shuffle` consistent across comparisons.
- Report the number of evaluated CNFs and repeats; include mean +/- stdev when sweeping sampling hyperparameters.
- Document any edits to prompt templates, regex extraction, or solver parameters.
- Mention environment details (solver version, SATQuest commit, dataset revision) so others can replicate your setup.

## Looking Ahead

Upcoming iterations will surface charts (accuracy vs. solver decisions, format heatmaps) directly in the docs. Until then, the markdown table keeps contributions lightweight, feel free to file issues with automation ideas if you want to help streamline reporting.
