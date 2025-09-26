# Finetuning

SATQuest provides a reinforcement learning workflow powered by GRPO that encourages models to produce well-structured reasoning traces (`<think>...</think>`) and exact binary answers (`<answer>...</answer>`). This page explains how to launch the reference setup and how to adapt it to your infrastructure.

## Requirements

- 8 GPUs (the reference run uses two groups of four for VLLM serving and GRPO training). Adjust device mappings if you have fewer cards.
- CUDA-ready environment with the `uv` dependencies from the `rft` group installed (`uv sync --group rft`).
- Access to the `sdpkjc/SATQuest-RFT-3k` dataset or your own regeneration.
- A base instruction-tuned model. We test with `Qwen/Qwen2.5-7B-Instruct`, but any chat model with `<think>/<answer>` style outputs works if you update the reward functions.

## Launch the VLLM Server

Start an inference server that the trainer will query for rollout generation:

```bash
CUDA_VISIBLE_DEVICES=0,1,2,3 nohup uv run --group rft trl vllm-serve \
  --model Qwen/Qwen2.5-7B-Instruct \
  --tensor_parallel_size 4 \
  --max_model_len 16384 \
  --gpu_memory_utilization 0.9 \
  --enable_prefix_caching True &
```

- `tensor_parallel_size` should match the number of GPUs allocated to serving.
- `max_model_len` must accommodate the longest prompt + completion you expect (GRPO defaults to 2048+8192 tokens).
- Run the command inside `nohup` or a process manager so the server remains available when you start training.

## Run the GRPO Trainer

In a separate shell, launch the trainer against the server:

```bash
CUDA_VISIBLE_DEVICES=4,5,6,7 uv run --group rft accelerate launch \
  --num-processes 4 --config-file zero3.yaml \
  rft.py --model-id Qwen/Qwen2.5-7B-Instruct \
  --p-list SATSP --q-list math \
  --exp-name qwen2p5_satsp_math \
  --server-ip 0.0.0.0
```

`rft.py` loads the RFT dataset, expands it across specified problem/question types, shuffles examples, and feeds them into a `GRPOTrainer`. The configuration in code sets:

- `num_generations=16` rollouts per prompt,
- `per_device_train_batch_size=2` with `gradient_accumulation_steps=16`,
- cosine LR schedule with `learning_rate=2e-6`, and
- reward weights `[1.0, 0.05, 0.05]` for correctness, tag coverage, and format matching.

Modify `zero3.yaml` if you need a different parallelism strategy.

## Reward Functions

Three reward components are applied to each completion:

1. **`score_reward`**: extracts `<answer>...</answer>`, normalises it with `re_matcher`, and checks correctness via the SATQuest verifier.
2. **`tag_count_reward`**: encourages exactly one `<think>` and `<answer>` pair to avoid degenerate outputs.
3. **`format_reward`**: measures how much of the completion falls inside the desired tag structure.

Adjust the weights or implement new reward callables if you want to include latency penalties, reasoning-length bonuses, or other task-specific signals.

## Customising the Training Dataset

- Use `--p-list` / `--q-list` to control which problem classes appear in the rollout queue. Mixing `SATSP` with `SATDP_UNSAT`, for example, teaches the model to output both satisfying assignments and UNSAT certificates.
- Regenerate data with `gen_cnf_rft_dataset.py` to explore other clause densities. The trainer only reads `cnf_dimacs`, `prompt`, and `p_type`, so you can augment records with extra metadata without code changes.

## Monitoring and Checkpoints

Training logs are written to the directory named after `exp_name`. Because `save_only_model=True`, checkpoints contain only the model weights—use the same tokenizer when you resume. Keep an eye on rollout rewards to catch API failures from the VLLM server; flat reward curves usually indicate parsing errors or truncated completions, so consider lowering `max_completion_length` or increasing server timeout.

## Next Steps

- Plug the finetuned model into the [evaluation](evaluate.md) script for a side-by-side comparison with the base model.
- Extend `make_process_fn` in `rft.py` if you want to insert chain-of-thought exemplars or additional instructions before reinforcement learning.
