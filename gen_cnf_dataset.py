import random
from dataclasses import dataclass

import numpy as np
import tyro
from datasets import Dataset, DatasetDict
from pysat.solvers import Solver

from satquest import CNF, create_problem
from satquest.constants import SAT_SOLVER_NAME


@dataclass
class Args:
    hf_entity: str = "sdpkjc"
    dataset_name: str = "SATQuest"
    seed: int = 9527


def solve_sat(clause_set):
    if not clause_set:
        return True
    with Solver(name=SAT_SOLVER_NAME, bootstrap_with=clause_set) as solver:
        return solver.solve()


def generate_random_clause(n, clause_len):
    assert clause_len <= n
    variables = random.sample(range(1, n + 1), clause_len)
    return sorted([v * random.choice([-1, 1]) for v in variables], key=abs)


def generate_random_unsat_cnf(n, m, p_k_2=0.3, p_geo=0.7):
    generated_formula = []
    while solve_sat(generated_formula):
        generated_formula_set = set()
        while len(generated_formula_set) < m:
            k_base = 1 if random.random() < p_k_2 else 2
            k = k_base + np.random.geometric(p_geo)
            k = min(k, n)
            clause = generate_random_clause(n, k)
            generated_formula_set.add(tuple(clause))
        generated_formula = list(map(list, generated_formula_set))
    return generated_formula


def unsat2sat(clauses):
    def random_flip_clause(clauses):
        return [[-literal if random.random() < 0.5 else literal for literal in clause] for clause in clauses]

    while not solve_sat(clauses):
        clauses = random_flip_clause(clauses)
    return clauses


def post_process_fn(cnf_item, seed=0):
    _rng = random.Random(seed)
    unsat_cnf, sat_cnf = CNF(dimacs=cnf_item["unsat_dimacs"]), CNF(dimacs=cnf_item["sat_dimacs"])
    sat_cnf.shuffle(seed=_rng.getrandbits(_rng.randint(1, 2048)))
    unsat_cnf.shuffle(seed=_rng.getrandbits(_rng.randint(1, 2048)))

    solver_metadatas = {}
    for P_NAME in ["SATDP_SAT", "SATSP", "SATDP_UNSAT", "MaxSAT", "MCS", "MUS"]:
        p = create_problem(P_NAME, sat_cnf if P_NAME in ["SATDP_SAT", "SATSP"] else unsat_cnf)
        solver_metadatas[P_NAME] = p.solver_metadata

    cnf_item["unsat_dimacs"], cnf_item["sat_dimacs"] = unsat_cnf.dimacs, sat_cnf.dimacs
    return {
        **cnf_item,
        "num_variable": unsat_cnf.nv,
        "num_clause": unsat_cnf.mc,
        "solver_metadatas": solver_metadatas,
    }


if __name__ == "__main__":
    args = tyro.cli(Args)
    random.seed(args.seed)

    A, REPEAT = 4, 10
    S_dedu = set()
    pair_cnfs = []
    for N in sorted(list(range(3, 16 + 1, 1)) * REPEAT):
        M = int(N * A)
        print(N, M, A)
        while True:
            unsat_clauses = generate_random_unsat_cnf(N, M)
            assert unsat_clauses
            unsat_cnf = CNF(clauses=unsat_clauses)
            unsat_cnf.sort()
            if unsat_cnf.dimacs not in S_dedu:
                break
        S_dedu.add(unsat_cnf.dimacs)
        sat_clauses = unsat2sat(unsat_clauses)
        pair_cnfs.append((CNF(clauses=unsat_clauses), CNF(clauses=sat_clauses)))

    cnf_item_list = []
    for unsat_cnf, sat_cnf in pair_cnfs:
        assert not unsat_cnf.is_sat and sat_cnf.is_sat
        unsat_dimacs, sat_dimacs = unsat_cnf.dimacs, sat_cnf.dimacs
        cnf_item = {
            "id": len(cnf_item_list),
            "num_literal": sum([len(c) for c in unsat_cnf.clauses]),
            "sat_dimacs": sat_dimacs,
            "unsat_dimacs": unsat_dimacs,
        }
        cnf_item_list.append(post_process_fn(cnf_item, seed=args.seed))
        print(
            cnf_item_list[-1]["id"],
            cnf_item_list[-1]["num_variable"],
            cnf_item_list[-1]["num_clause"],
            cnf_item_list[-1]["num_literal"],
        )
    print(len(cnf_item_list))

    dataset_dict = DatasetDict(
        {
            "test": Dataset.from_list(cnf_item_list),
        }
    )
    print(args.dataset_name)
    # dataset_dict.save_to_disk(f"./{args.dataset_name}-{args.seed}")
    dataset_dict.push_to_hub(f"{args.hf_entity}/{args.dataset_name}")
