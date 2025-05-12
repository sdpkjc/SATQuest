import hashlib
import inspect
import re

from pysat.formula import WCNF


def cnf2wcnf(cnf):
    wcnf = WCNF()
    wcnf.nv = cnf.nv
    for clause in cnf.clauses:
        wcnf.append(clause, weight=1)
    return wcnf


def get_class_source_hash(cls):
    try:
        source = inspect.getsource(cls)
        source_hash = hashlib.md5(source.encode("utf-8")).hexdigest()[:8]
    except Exception:
        source_hash = "unknown"

    return source_hash


def re_matcher(content_output: str, pattern: str) -> str:
    final_answer = None
    try:
        match = re.finditer(pattern, content_output, re.DOTALL)
        matches = list(match)
        if matches:
            final_answer = matches[-1].group(1)
    except Exception as e:
        print(f"Error while matching answer: {e}")
    return final_answer


SYSTEM_PROMPT = "You are a helpful assistant."
QUERY_TEMPLATE = """\
Solve the following problem step by step. The last line of your response should be of the form Answer: $ANSWER (without quotes) where $ANSWER is the answer to the problem.

{Question}

Remember to put your answer on its own line after "Answer:", and you do not need to use a \\boxed command.
""".strip()

ANSWER_PATTERN = r"(?i)answer:\s*([^\n]+)"
