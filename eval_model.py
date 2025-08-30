# import os
# os.environ["WEAVE_PARALLELISM"] = "1"
import asyncio
import time
from dataclasses import dataclass, field

import tyro
import weave
from datasets import load_dataset
from weave import Evaluation

from llm_inference import llm_inference
from satquest import CNF, Problem, create_problem, create_question
from satquest.satquest_utils import (  # noqa
    ANSWER_PATTERN,
    QUERY_TEMPLATE,
    SYSTEM_PROMPT,
    re_matcher,
)


@dataclass
class Args:
    exp_name: str | None = None
    wandb_project: str = "SATQuest-Eval"
    hf_dataset_name: str = "sdpkjc/SATQuest"
    p_type_list: list[str] = field(default_factory=lambda: ["SATSP"])
    # p_type_list: list[str] = field(default_factory=lambda: ["SATSP", "MaxSAT", "MCS", "MUS", "SATDP_SAT", "SATDP_UNSAT"])
    q_type_list: list[str] = field(default_factory=lambda: ["math"])
    # q_type_list: list[str] = field(default_factory=lambda: ["math", "dimacs", "story", "dualstory"])
    llm_model: str = "gpt-4o"
    max_tokens: int = 16384
    temperature: float = 0.6
    num_example: int | None = None
    stream: bool = True
    cnf_shuffle: bool = False
    n_repeat: int = 1  # 16


if __name__ == "__main__":
    args = tyro.cli(Args)
    dataset_cnf = load_dataset(args.hf_dataset_name)["test"]
    num_example = min(args.num_example, len(dataset_cnf)) if args.num_example else len(dataset_cnf)
    dataset_cnf = dataset_cnf.select(range(num_example))

    examples = []
    for p_type in args.p_type_list:
        assert p_type in ["SATSP", "SATDP_SAT", "SATDP_UNSAT", "MaxSAT", "MCS", "MUS"], f"Unknown problem type: {p_type}"
        sat_flag = True if p_type in ["SATSP", "SATDP_SAT"] else False
        for q_type in args.q_type_list:
            assert q_type in ["math", "dimacs", "story", "dualstory"], f"Unknown question type: {q_type}"

            for i, d_item in enumerate(dataset_cnf):
                cnf = CNF(dimacs=d_item["sat_dimacs"]) if sat_flag else CNF(dimacs=d_item["unsat_dimacs"])
                if args.cnf_shuffle:
                    cnf.shuffle()
                _problem, _question = create_problem(p_type, cnf), create_question(q_type)
                for r in range(args.n_repeat):
                    _example = {
                        "cnf_id": d_item["id"],
                        "problem": _problem,
                        "question": _question,
                        "problem_type": p_type,
                        "question_type": q_type,
                        "num_literal": d_item["num_literal"],
                        "question_str": _problem.accept(_question),
                    }
                    if args.n_repeat > 1:
                        _example["repeat_i"] = r
                    examples.append(_example)

    @weave.op()
    def match_score(problem: Problem, output: dict) -> dict:
        return {
            "is_correct": problem.check(output["final_answer"]),
            "is_format_correct": problem.format_check(output["final_answer"]),
        }

    @weave.op()
    def function_to_evaluate(problem: Problem, question_str: str):
        question_w_template = QUERY_TEMPLATE.format(Question=question_str)
        output_dict = llm_inference(
            question_w_template,
            system_prompt=SYSTEM_PROMPT,
            model=args.llm_model,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
            reasoning_effort="high",
            stream=True,
            v=True,
        )
        output_dict["final_answer"] = None
        try:
            content_output = output_dict["content_output"]
            output_dict["final_answer"] = re_matcher(re_matcher(content_output, ANSWER_PATTERN), problem.ANSWER_PATTERN)
        except Exception as e:
            print(f"Error while matching answer: {e}")
        return output_dict

    eval_run_name = f"{args.llm_model}_{'-'.join([pt.replace('_', '') for pt in args.p_type_list])}_{'-'.join(args.q_type_list)}_ne{len(examples)}_t{int(time.time())}"
    if args.exp_name:
        eval_run_name = f"{args.exp_name}_{eval_run_name}"
    if args.n_repeat > 1:
        eval_run_name = f"R{args.n_repeat}_" + eval_run_name
    print(eval_run_name)

    evaluation = Evaluation(evaluation_name=eval_run_name, dataset=examples, scorers=[match_score])
    weave.init(
        args.wandb_project, autopatch_settings={"disable_autopatch": True}
    )  # autopatch_settings={"openai": {"enabled": False}}
    asyncio.run(evaluation.evaluate(function_to_evaluate))
