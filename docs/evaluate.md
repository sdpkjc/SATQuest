# 📈 Evaluate

The evaluation harness wraps SATQuest problems, calls a target LLM, and uses the package verifier to score responses. Results are logged through Weave into your Weights & Biases project so you can compare multiple model runs side by side.

## Prerequisites

- Install dependencies with `uv sync --group eval` or ensure `weave`, `tyro`, `datasets`, and your target LLM client are available.
- Authenticate with Weights & Biases (`wandb login`) if you want metrics to upload automatically.
- Set any provider-specific environment variables required by `llm_inference.py` (for example, OpenAI API keys).

## Running an Evaluation

```bash
uv run --group eval eval_model.py \
  --exp-name qwen_math_satsp \
  --wandb-project SATQuest-Eval \
  --hf-dataset-name sdpkjc/SATQuest \
  --p-type-list SATSP \
  --q-type-list math \
  --llm-model gpt-4o \
  --max-tokens 16384 \
  --temperature 0.6 \
  --num-example 50 \
  --stream True \
  --cnf-shuffle False \
  --n-repeat 1
```

The command prints a run name derived from your flags (e.g., `gpt-4o_SATSP_math_ne50_t1699999999`) and streams progress as Weave evaluates each prompt.

## Key Arguments

- `--exp-name`: Optional prefix added to the generated run name. Use this to group sweeps.
- `--wandb-project`: W&B project slug. Defaults to `SATQuest-Eval`.
- `--hf-dataset-name`: Dataset identifier. Provide a custom path if you regenerated the benchmark under your namespace.
- `--p-type-list`: Comma-separated problem types. Mix decision (`SATSP`, `SATDP_*`) and optimisation (`MaxSAT`, `MCS`, `MUS`) tasks to test different reasoning behaviours.
- `--q-type-list`: Prompt styles (`math`, `dimacs`, `story`, `dualstory`). Multiple values trigger a Cartesian product with problem types.
- `--llm-model`: Model identifier handled by `llm_inference.py`. Extend that file if you need to call a new provider.
- `--max-tokens`, `--temperature`: Sampling controls forwarded to the LLM client.
- `--num-example`: Limit the number of CNFs per run (default is the entire split).
- `--stream`: When `True`, requests streaming responses from the LLM.
- `--cnf-shuffle`: Shuffle literals before generating the prompt to reduce positional bias.
- `--n-repeat`: Repeat the same (problem, question) pair multiple times; useful for sampling variance studies.

Invalid problem or question types raise assertions early, so you can catch typos immediately.

## Outputs and Logging

For every example the script stores:

- `question_str`: final prompt presented to the LLM.
- `final_answer`: answer extracted via regex from the model's response (if parsing succeeds).
- `is_correct`: boolean verifying correctness against the SATQuest oracle.
- `is_format_correct`: whether the answer matched the expected binary pattern.

Weave batches these results and forwards them to W&B. Inspect per-example tables, aggregate accuracies, and response traces in the W&B UI. Logs also print locally for quick debugging.

## Tips

- Use `--cnf-shuffle True` when evaluating models prone to memorising literal order.
- Pair `--n-repeat > 1` with a small `--num-example` to estimate variance before scaling up.
- When experimenting with alternative datasets, confirm that solver metadata exists—custom problem types may require updating `create_problem` or the reward functions.
