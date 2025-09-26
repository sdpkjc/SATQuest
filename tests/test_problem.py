import pytest

from satquest.cnf import CNF
from satquest.constants import SAT_SOLVER_NAME
from satquest.problem import MCS, MUS, SATDP, SATSP, MaxSAT, create_problem
from satquest.question import Question


@pytest.mark.parametrize(
    "kind,expected",
    [
        ("satdp", SATDP),
        ("SATDP_unsat", SATDP),
        ("satsp", SATSP),
        ("maxsat", MaxSAT),
        ("mcs", MCS),
        ("mus", MUS),
    ],
)
def test_create_problem_dispatches_to_expected_type(kind, expected):
    cnf = CNF(clauses=[[1]])
    problem = create_problem(kind, cnf)

    if expected is type(None):
        assert problem is None
    else:
        assert isinstance(problem, expected)


def test_create_problem_raises_value_error_for_unknown_problem_type():
    with pytest.raises(ValueError):
        create_problem("unknown", CNF(clauses=[[1]]))


def test_satdp_solution_and_check_cover_sat_and_unsat():
    sat_problem = SATDP(CNF(clauses=[[1]]))
    unsat_problem = SATDP(CNF(clauses=[[1], [-1]]))

    assert sat_problem.solution == "1"
    assert sat_problem.check("1") is True
    assert sat_problem.check("0") is False

    assert unsat_problem.solution == "0"
    assert unsat_problem.check("0") is True
    assert unsat_problem.check("1") is False
    assert unsat_problem.format_check("10") is False
    assert unsat_problem.solver_metadata["solvers"] == (sat_problem.solver_metadata["solvers"][0],)


def test_satsp_solution_enumeration_and_validation():
    cnf = CNF(clauses=[[1, -2], [2]])
    problem = SATSP(cnf)

    solution = problem.solution
    assert problem.format_check(solution) is True
    assert solution == "11"
    assert problem.check(solution) is True
    assert problem.check("10") is False
    assert list(problem.solution_enumerate()) == [solution]
    assert problem.search_space_size == 2**cnf.nv
    assert problem.solver_metadata["solvers"][0]


def test_maxsat_mcs_mus_share_expected_behaviour_on_unsat_instance():
    cnf = CNF(clauses=[[1], [-1]])

    maxsat = MaxSAT(cnf)
    assert maxsat.format_check(maxsat.solution) is True
    assert maxsat.check(maxsat.solution) is True
    assert set(maxsat.solution_enumerate()) == {"1", "0"}

    mcs = MCS(cnf)
    assert mcs.solution in {"10", "01"}
    assert mcs.check(mcs.solution) is True
    assert set(mcs.solution_enumerate()) == {"10", "01"}
    assert mcs.check("00") is False
    assert mcs.search_space_size == 2**cnf.mc

    mus = MUS(cnf)
    assert mus.solution == "11"
    assert mus.check(mus.solution) is True
    assert list(mus.solution_enumerate()) == ["11"]
    assert mus.check("10") is False

    for problem in (maxsat, mcs, mus):
        assert problem.solver_metadata["solvers"][0]


def test_accept_delegates_to_question_visitor():
    class RecordingQuestion(Question):
        def __init__(self) -> None:
            self.calls: list[tuple[str, CNF]] = []

        def _record(self, name: str, cnf: CNF) -> str:
            self.calls.append((name, cnf))
            return f"{name}-response"

        def visit_satdp(self, cnf: CNF) -> str:
            return self._record("satdp", cnf)

        def visit_satsp(self, cnf: CNF) -> str:
            return self._record("satsp", cnf)

        def visit_maxsat(self, cnf: CNF) -> str:
            return self._record("maxsat", cnf)

        def visit_mcs(self, cnf: CNF) -> str:
            return self._record("mcs", cnf)

        def visit_mus(self, cnf: CNF) -> str:
            return self._record("mus", cnf)

    question = RecordingQuestion()
    factories = [
        (lambda: SATDP(CNF(clauses=[[1]])), "satdp"),
        (lambda: SATSP(CNF(clauses=[[1]])), "satsp"),
        (lambda: MaxSAT(CNF(clauses=[[1], [-1]])), "maxsat"),
        (lambda: MCS(CNF(clauses=[[1], [-1]])), "mcs"),
        (lambda: MUS(CNF(clauses=[[1], [-1]])), "mus"),
    ]

    for factory, expected in factories:
        question.calls.clear()
        problem = factory()
        response = problem.accept(question)
        assert response == f"{expected}-response"
        assert question.calls == [(expected, problem.cnf)]


@pytest.mark.parametrize(
    "problem_factory, expected_length",
    [
        (lambda: SATDP(CNF(clauses=[[1]])), 1),
        (lambda: SATSP(CNF(clauses=[[1, -2], [2]])), 2),
        (lambda: MaxSAT(CNF(clauses=[[1], [-1]])), 1),
        (lambda: MCS(CNF(clauses=[[1], [-1]])), 2),
        (lambda: MUS(CNF(clauses=[[1], [-1]])), 2),
    ],
)
def test_answer_pattern_matches_problem_dimensions(problem_factory, expected_length):
    problem = problem_factory()
    assert problem.ANSWER_PATTERN == f"(?=([01]{{{expected_length}}}))"


@pytest.mark.parametrize(
    "problem_factory, invalid_values",
    [
        (lambda: SATDP(CNF(clauses=[[1]])), ["", "2", "01", 1, None]),
        (lambda: SATSP(CNF(clauses=[[1]])), ["", "2", "01", 1, None]),
        (lambda: MaxSAT(CNF(clauses=[[1], [-1]])), ["", "2", "01", 1, None]),
        (lambda: MCS(CNF(clauses=[[1], [-1]])), ["", "2", "1", "000", 1, None]),
        (lambda: MUS(CNF(clauses=[[1], [-1]])), ["", "2", "1", "000", 1, None]),
    ],
)
def test_format_check_rejects_invalid_values(problem_factory, invalid_values):
    problem = problem_factory()
    for value in invalid_values:
        assert problem.format_check(value) is False


@pytest.mark.parametrize(
    "problem_factory, expected",
    [
        (lambda: SATDP(CNF(clauses=[[1]])), (SAT_SOLVER_NAME,)),
        (lambda: SATSP(CNF(clauses=[[1]])), (SAT_SOLVER_NAME,)),
        (lambda: MaxSAT(CNF(clauses=[[1], [-1]])), (SAT_SOLVER_NAME, "RC2")),
        (lambda: MCS(CNF(clauses=[[1], [-1]])), (SAT_SOLVER_NAME, "LBX")),
        (lambda: MUS(CNF(clauses=[[1], [-1]])), (SAT_SOLVER_NAME, "MUSX")),
    ],
)
def test_solver_metadata_reports_solver_names(problem_factory, expected):
    problem = problem_factory()
    _ = problem.solution
    assert problem.solver_metadata is not None
    assert problem.solver_metadata["solvers"] == expected
