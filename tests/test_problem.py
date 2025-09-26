import pytest

from satquest.cnf import CNF
from satquest.problem import MCS, MUS, SATDP, SATSP, MaxSAT, create_problem


@pytest.mark.parametrize(
    "kind,expected",
    [
        ("satdp", SATDP),
        ("SATDP_unsat", SATDP),
        ("satsp", SATSP),
        ("maxsat", MaxSAT),
        ("mcs", MCS),
        ("mus", MUS),
        ("unknown", type(None)),
    ],
)
def test_create_problem_dispatches_to_expected_type(kind, expected):
    cnf = CNF(clauses=[[1]])
    problem = create_problem(kind, cnf)

    if expected is type(None):
        assert problem is None
    else:
        assert isinstance(problem, expected)


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
