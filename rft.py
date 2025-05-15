import re
from dataclasses import dataclass, field

import tyro
from datasets import concatenate_datasets, load_dataset
from transformers import AutoTokenizer
from trl import GRPOConfig, GRPOTrainer

from satquest import CNF, create_problem, create_question
from satquest.satquest_utils import re_matcher


def make_process_fn(p_type, q_type):
    def process_fn(example):
        cnf = CNF(dimacs=example["sat_dimacs"] if p_type in ["SATSP", "SATDP_SAT"] else example["unsat_dimacs"])
        cnf.shuffle()
        _problem, _question = create_problem(p_type, cnf), create_question(q_type)
        question_str, exp_s = _problem.accept(_question), "0" * (len(_problem.solution) - 1) + "1"
        prompt = [
            {
                "role": "system",
                "content": "You are a helpful AI Assistant that provides well-reasoned and detailed responses. You first think about the reasoning process as an internal monologue and then provide the user with the answer. Respond in the following format: <think>\n...\n</think>\n<answer>\n...\n</answer>",
            },
            {
                "role": "user",
                "content": question_str
                + f"\nShow your work in <think> </think> tags. And return the final answer in <answer> </answer> tags, for example <answer> {exp_s} </answer>.",
            },
        ]
        return {
            "cnf_dimacs": cnf.dimacs,
            "prompt": prompt,
            "p_type": p_type,
        }

    return process_fn


def tag_count_reward(completions, **kwargs) -> list[float]:
    """Reward function that checks if we produce the desired number of think and answer tags associated with `format_reward()`.

    Adapted from: https://gist.github.com/willccbb/4676755236bb08cab5f4e54a0475d6fb#file-grpo_demo-py-L90
    """

    def count_tags(text: str) -> float:
        count = 0.0
        if text.count("<think>") == 1:
            count += 0.25
        if text.count("</think>") == 1:
            count += 0.25
        if text.count("<answer>") == 1:
            count += 0.25
        if text.count("</answer>") == 1:
            count += 0.25
        return count

    contents = [completion[0]["content"] for completion in completions]
    return [count_tags(c) for c in contents]


_PATTERN = re.compile(r"<think>.*?</think>\s?<answer>.*?</answer>", flags=re.DOTALL)


def format_reward(completions, **kwargs):
    completion_contents = [completion[0]["content"] for completion in completions]
    rewards = []
    for c in completion_contents:
        text = str(c)
        total_len = len(text)
        if total_len == 0:
            rewards.append(0.0)
            continue

        m = _PATTERN.search(text)
        match_len = len(m.group()) if m else 0
        rewards.append(match_len / total_len)

    return rewards


def extract_answer(solution_str):
    answer_pattern = r"<answer>(.*?)</answer>"
    match = re.finditer(answer_pattern, solution_str, re.DOTALL)
    matches = list(match)
    if matches:
        final_answer = matches[-1].group(1).strip()
    else:
        final_answer = None
    return final_answer


def compute_score(solution_str, cnf_dimacs, p_type, score=1.0):
    problem = create_problem(p_type, CNF(dimacs=cnf_dimacs))
    try:
        answer_str = extract_answer(solution_str=solution_str)
        answer_01_str = re_matcher(answer_str, problem.ANSWER_PATTERN)
        if problem.check(answer_01_str):
            return score
    except Exception:
        pass
    return 0.0


def score_reward(completions, **kwargs):
    completion_contents = [completion[0]["content"] for completion in completions]
    rews = []
    for i, c in enumerate(completion_contents):
        ka = {k: v[i] for k, v in kwargs.items()}
        rews.append(compute_score(c, ka["cnf_dimacs"], ka["p_type"]))
    return rews


@dataclass
class Args:
    model_id: str = "Qwen/Qwen2.5-7B-Instruct"
    p_list: list = field(default_factory=lambda: ["SATSP"])
    q_list: list = field(default_factory=lambda: ["math"])  # ["math", "story"]
    exp_name: str = None
    server_ip: str = "0.0.0.0"


if __name__ == "__main__":
    args = tyro.cli(Args)
    exp_name = args.model_id.split("/")[-1] + "_" + "-".join(args.p_list) + "_" + "-".join(args.q_list)
    if args.exp_name is not None:
        exp_name = exp_name + "_" + args.exp_name
    print(exp_name)

    dataset = load_dataset("sdpkjc/SATQuest-RFT-3k", split="train")
    dataset_list = []
    for pt in args.p_list:
        for qt in args.q_list:
            dataset_list.append(dataset.map(function=make_process_fn(pt, qt)))
    dataset = concatenate_datasets(dataset_list)
    dataset = dataset.shuffle(seed=9527).select_columns(["cnf_dimacs", "prompt", "p_type"])

    training_args = GRPOConfig(
        output_dir=exp_name,
        logging_steps=1,
        log_on_each_node=False,
        log_completions=True,
        warmup_steps=10,
        max_prompt_length=2048,
        max_completion_length=8192,
        use_vllm=True,
        vllm_server_host=args.server_ip,
        vllm_server_timeout=1000,
        num_generations=16,
        per_device_train_batch_size=2,
        gradient_accumulation_steps=16,
        gradient_checkpointing=True,
        save_strategy="steps",
        save_steps=50,
        save_total_limit=20,
        save_only_model=True,
        bf16=True,
        num_train_epochs=1,
        max_steps=500,
        max_grad_norm=0.3,
        num_iterations=1,
        learning_rate=2e-6,
        lr_scheduler_type="cosine",
        beta=0.01,
        loss_type="grpo",
        scale_rewards=True,
        mask_truncated_completions=True,
        temperature=1.0,
        reward_weights=[1.0, 0.05, 0.05],
    )

    tokenizer = AutoTokenizer.from_pretrained(
        args.model_id,
        revision="main",
        trust_remote_code=True,
    )
    trainer = GRPOTrainer(
        model=args.model_id,
        reward_funcs=[score_reward, tag_count_reward, format_reward],
        args=training_args,
        train_dataset=dataset,
        processing_class=tokenizer,
    )
    trainer.train()
