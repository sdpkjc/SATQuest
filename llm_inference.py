import time

from dotenv import load_dotenv
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_random

load_dotenv()
MAX_DURATION = 900

client = OpenAI()


@retry(
    stop=stop_after_attempt(20),
    wait=wait_random(min=3, max=10),
    before_sleep=lambda s: print(f"======= retry {s.attempt_number} {s.outcome.exception()} ======="),
)
def llm_inference(
    question_w_template: str,
    system_prompt: str = None,
    model: str = "gpt-4o-mini",
    temperature: float = 0.6,
    max_tokens: int = 16384,
    reasoning_effort: str = None,
    stream: bool = False,
    v: bool = False,
):
    if v:
        print(question_w_template)
        print("\n==================\n")
    is_reasoning_model = any(token in model for token in ["r1", "o1", "o3", "o4", "qwq", "reasoner"])
    call_params = {"model": model, "stream": stream}
    if stream:
        call_params["stream_options"] = {"include_usage": True}
    if is_reasoning_model:
        call_params["reasoning_effort"] = reasoning_effort
    if is_reasoning_model:
        call_params["messages"] = [{"role": "user", "content": question_w_template}]
    else:
        call_params["temperature"] = temperature
        call_params["max_tokens"] = max_tokens
        call_params["messages"] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question_w_template},
        ]
    response_obj = client.chat.completions.create(**call_params)

    content_output, reasoning_content_output, usage = "", "", {}
    if stream:
        start = time.time()
        for chunk in response_obj:
            if time.time() - start > MAX_DURATION:
                print("stream timeout! break.")
                break
            if chunk.usage:
                usage = chunk.usage.dict()
            if not chunk.choices or not chunk.choices[0].delta:
                continue
            delta = chunk.choices[0].delta
            if delta.content:
                content_output += delta.content
                if v:
                    print(delta.content, end="")
            if hasattr(delta, "reasoning_content") and delta.reasoning_content:
                reasoning_content_output += delta.reasoning_content
                if v:
                    print(delta.reasoning_content, end="")
    else:
        message = response_obj.choices[0].message
        content_output = message.content
        usage = response_obj.usage
        if hasattr(message, "reasoning_content") and message.reasoning_content:
            reasoning_content_output = message.reasoning_content
        if v:
            print(reasoning_content_output)
            print(content_output)

    assert content_output is not None and len(content_output) > 0 and len(usage) > 0
    return {"reasoning_content_output": reasoning_content_output, "content_output": content_output, "usage": usage}


if __name__ == "__main__":
    from datasets import load_dataset

    from satquest import CNF, create_problem, create_question
    from satquest.satquest_utils import (
        ANSWER_PATTERN,
        QUERY_TEMPLATE,
        SYSTEM_PROMPT,
        re_matcher,
    )

    model = "gpt-4o"

    cnf_idx = 10
    dataset_cnf = load_dataset("sdpkjc/SATQuest")["test"]
    cnf_dimacs = dataset_cnf[cnf_idx]["sat_dimacs"]

    problem = create_problem("SATSP", CNF(dimacs=cnf_dimacs))
    question = create_question("math")
    question_str = problem.accept(question)

    question_w_template = QUERY_TEMPLATE.format(Question=question_str)
    output_dict = llm_inference(
        question_w_template,
        system_prompt=SYSTEM_PROMPT,
        model=model,
        temperature=0.6,
        max_tokens=16384,
        stream=True,
        v=True,
    )

    content_output = output_dict["content_output"]
    final_answer = re_matcher(re_matcher(content_output, ANSWER_PATTERN), problem.ANSWER_PATTERN)

    print("\n==================\n")

    print(final_answer)
    print(problem.solution)
    print(problem.check(final_answer))
    # print(problem.check(problem.solution))
    for i, s in enumerate(problem.solution_enumerate()):
        print(i, s)
