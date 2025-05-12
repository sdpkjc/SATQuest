import random

from pysat.formula import CNF as PysatCNF
from pysat.solvers import Solver

from satquest.constants import SAT_SOLVER_NAME


class CNF:
    def __init__(self, clauses: list = None, dimacs: str = None):
        assert clauses or dimacs
        if clauses:
            self.cnf = PysatCNF(from_clauses=clauses)
        else:
            self.cnf = PysatCNF(from_string=dimacs)
        self._is_sat = None

    @property
    def clauses(self) -> list:
        return self.cnf.clauses

    @property
    def nv(self) -> int:
        return self.cnf.nv

    @property
    def mc(self) -> int:
        return len(self.clauses)

    @property
    def dimacs(self) -> str:
        return self.cnf.to_dimacs()

    @property
    def is_sat(self) -> bool:
        if self._is_sat is None:
            with Solver(name=SAT_SOLVER_NAME, bootstrap_with=self.cnf) as solver:
                self._is_sat = solver.solve()
        return self._is_sat

    def shuffle(self, seed: int = None) -> None:
        self._is_sat = None
        _rng = random.Random(seed)
        for i in range(len(self.clauses)):
            _rng.shuffle(self.clauses[i])
        _rng.shuffle(self.clauses)

    def sort(self) -> None:
        self._is_sat = None
        for i in range(len(self.clauses)):
            self.clauses[i].sort(key=lambda x: abs(x))
        self.clauses.sort()


if __name__ == "__main__":
    clauses = [[1, 2], [-1, 2], [-3, -2, 1], [3], [-3, -1]]
    cnf = CNF(clauses=clauses)
    cnf = CNF(dimacs=cnf.dimacs)
    cnf.sort()
    cnf.shuffle()
    print(cnf.clauses, cnf.nv, cnf.is_sat)
