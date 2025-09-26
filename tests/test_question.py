import re

import pytest

from satquest.cnf import CNF
from satquest.constants import CHEF_NAME, COOKIE_NAMES
from satquest.question import (
    QuestionDIMACS,
    QuestionDualStory,
    QuestionMath,
    QuestionStory,
    create_question,
)


def test_question_dimacs_satsp_mentions_dimacs_and_instruction():
    cnf = CNF(clauses=[[1, -2], [2]])
    text = QuestionDIMACS().visit_satsp(cnf)

    assert f"{cnf.nv} variables" in text
    assert cnf.dimacs.strip() in text
    assert "binary string of length 2" in text


def test_question_math_formats_clauses_in_math_notation():
    cnf = CNF(clauses=[[1, -2]])
    text = QuestionMath().visit_satsp(cnf)

    assert "x_1" in text
    assert "\\lor" in text
    assert "Given a CNF formula" in text


def test_question_dimacs_maxsat_emphasises_optimization_goal():
    cnf = CNF(clauses=[[1], [-1]])
    text = QuestionDIMACS().visit_maxsat(cnf)

    assert "maximizes the number of satisfied clauses" in text
    assert f"binary string of length {cnf.nv}" in text
    assert cnf.dimacs.strip() in text


def test_question_story_names_and_storytelling_details():
    cnf = CNF(clauses=[[1], [-2]])
    text = QuestionStory().visit_satdp(cnf)

    assert f"Chef {CHEF_NAME}" in text
    assert all(name in text for name in COOKIE_NAMES[: cnf.nv])
    assert "binary string of length 1" in text
    assert "wants" in text


def test_question_dualstory_switches_phrasing_and_textures():
    cnf = CNF(clauses=[[1, -2]])
    text = QuestionDualStory().visit_satsp(cnf)

    assert "dislikes" in text
    assert "binary string of length 2" in text
    assert "crunchy" in text and "chewy" in text
    assert text.count("crunchy") == text.count("chewy")


def test_question_math_uses_braced_indices_for_two_digit_variables():
    cnf = CNF(clauses=[[10, -11]])
    text = QuestionMath().visit_satsp(cnf)

    assert "x_{10}" in text
    assert "\\neg x_{11}" in text
    assert f"binary string of length {cnf.nv}" in text


def test_question_story_lists_friend_requirements_in_order():
    cnf = CNF(clauses=[[1, -2], [-1, 2]])
    text = QuestionStory().visit_satsp(cnf)

    assert "1." in text and "2." in text
    numbered_lines = [line for line in text.splitlines() if line.strip().startswith(("1.", "2."))]
    assert numbered_lines[0].startswith("1.")
    assert COOKIE_NAMES[0] in text and COOKIE_NAMES[1] in text


def test_question_dualstory_flips_literal_textures():
    cnf = CNF(clauses=[[1], [-2]])
    text = QuestionDualStory().visit_satdp(cnf)

    first_friend_line = next(line for line in text.splitlines() if line.strip().startswith("1."))
    second_friend_line = next(line for line in text.splitlines() if line.strip().startswith("2."))
    assert "chewy" in first_friend_line  # positive literal becomes chewy in dual story
    assert "crunchy" in second_friend_line  # negative literal becomes crunchy


def test_question_repr_and_factory_helper():
    story_question = QuestionStory()
    repr_text = repr(story_question)

    assert repr_text.startswith("QuestionStory_")
    assert re.match(r"QuestionStory_[A-Za-z0-9]+_[A-Za-z0-9]+", repr_text)

    assert isinstance(create_question("dimacs"), QuestionDIMACS)
    assert isinstance(create_question("math"), QuestionMath)
    assert isinstance(create_question("story"), QuestionStory)
    assert isinstance(create_question("dualstory"), QuestionDualStory)
    assert isinstance(create_question("StOrY"), QuestionStory)
    with pytest.raises(ValueError):
        create_question("unknown")
