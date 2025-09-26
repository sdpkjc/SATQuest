# 🏆 Leaderboard

SATQuest tracks LLM reasoning across 140 paired CNFs (5 problem types x 4 prompt formats) using the verifier described in the paper. Use this page to compare against published numbers and append new runs.

## 📊 Benchmark Results

| Model                  | Model Type       | Overall accuracy |
| ---------------------- | ---------------- | ---------------- |
| 🏆 `o3-mini`           | Closed Reasoning | 0.56             |
| `DeepSeek-R1`         | Open Reasoning   | 0.42             |
| `QwQ-32B`             | Open Reasoning   | 0.40             |
| `DS-R1-Distill-Qwen-32B` | Open Reasoning   | 0.36             |
| `GPT-4.1`             | Closed vanilla | 0.26             |
| `DeepSeek-V3-0324`     | Open vanilla   | 0.18             |
| `DS-R1-Distill-Qwen-7B` | Open Reasoning   | 0.08             |
| `Qwen2.5-32B-Instruct` | Open Vanilla   | 0.07             |
| `Qwen2.5-7B-Instruct`  | Open Vanilla   | 0.06             |

_All numbers average across all problem types and prompt formats on `sdpkjc/SATQuest`._
_For more details, see our [paper](https://arxiv.org/abs/2509.00930)._

## 📝 How to Submit Results

1. **Run the evaluator** - `uv run --group eval eval_model.py` with your model settings (see [Evaluate](evaluate.md)).
2. **Log to W&B** - we use the `SATQuest-Eval` project; keep `--cnf-shuffle` and dataset revisions explicit for reproducibility.
3. **Open a PR** - add a row to the table above (including accuracy, configuration, and a link to the run) or link to an external report. Qualitative examples or failure cases are welcome.

## 📝 Comparability Checklist

- Keep problem/question lists and `--cnf-shuffle` consistent across comparisons.
- Report the number of evaluated CNFs and repeats; include mean +/- stdev when sweeping sampling hyperparameters.
- Document any edits to prompt templates, regex extraction, or solver parameters.
- Mention environment details (solver version, SATQuest commit, dataset revision) so others can replicate your setup.

## 🔮 Looking Ahead

Upcoming iterations will surface charts (accuracy vs. solver decisions, format heatmaps) directly in the docs. Until then, the markdown table keeps contributions lightweight, feel free to file issues with automation ideas if you want to help streamline reporting.
