from satquest.cnf import CNF


def test_init_from_clauses_exposes_basic_properties():
    clauses = [[1, -2, 3], [-1, 2]]
    cnf = CNF(clauses=clauses)

    assert cnf.clauses == clauses
    assert cnf.nv == 3
    assert cnf.mc == len(clauses)


def test_init_from_dimacs_round_trips_clauses():
    original = CNF(clauses=[[1, -2], [2, -3]])
    clone = CNF(dimacs=original.dimacs)

    assert clone.clauses == original.clauses
    assert clone.nv == original.nv
    assert clone.mc == original.mc


def test_shuffle_with_seed_is_deterministic_and_resets_cache():
    base = [[1, 2, -3], [3, -1], [-2, 4]]
    cnf_one = CNF(clauses=[clause[:] for clause in base])
    cnf_two = CNF(clauses=[clause[:] for clause in base])

    cnf_one._is_sat = True
    cnf_one.shuffle(seed=7)
    cnf_two.shuffle(seed=7)

    assert cnf_one.clauses == cnf_two.clauses
    assert cnf_one._is_sat is None


def test_sort_orders_literals_and_clauses_globally():
    cnf = CNF(clauses=[[3, -1, 2], [-3, 1], [2, -2, 1]])
    cnf.sort()

    assert cnf.clauses == [[-1, 2, 3], [1, -3], [1, 2, -2]]


def test_is_sat_handles_sat_and_unsat_instances():
    sat_cnf = CNF(clauses=[[1, -2], [2]])
    unsat_cnf = CNF(clauses=[[1], [-1]])

    assert sat_cnf.is_sat is True
    assert unsat_cnf.is_sat is False
