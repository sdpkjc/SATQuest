import traceback
from abc import ABC, abstractmethod
from typing import Any, Generator

from pysat.examples.lbx import LBX as MCSSolver
from pysat.examples.musx import MUSX as MUSSolver
from pysat.examples.rc2 import RC2 as MaxSATSolver
from pysat.solvers import Solver

from satquest.cnf import CNF
from satquest.constants import GIT_HASH, SAT_SOLVER_NAME
from satquest.question import Question
from satquest.satquest_utils import cnf2wcnf, get_class_source_hash


class Problem(ABC):
    def __init__(self, cnf: CNF):
        self.cnf = cnf

    @property
    @abstractmethod
    def solution(self) -> Any:
        pass

    @abstractmethod
    def solution_enumerate(self) -> Generator[str, None, None]:
        pass

    @property
    @abstractmethod
    def search_space_size(self) -> Any:
        pass

    @abstractmethod
    def check(self, answer: Any) -> bool:
        pass

    @abstractmethod
    def format_check(self, answer: Any) -> bool:
        pass

    @abstractmethod
    def accept(self, question: Question, *args, **kwargs) -> str:
        pass

    @property
    @abstractmethod
    def ANSWER_PATTERN(self) -> str:
        pass

    @property
    def solver_metadata(self):
        if not hasattr(self, "_solver_metadata"):
            _ = self.solution
        return self._solver_metadata

    def __repr__(self):
        return f"{self.__class__.__name__}_{GIT_HASH}_{get_class_source_hash(self.__class__)}"


class SATDP(Problem):
    @property
    def solution(self) -> bool:
        if not hasattr(self, "_solution"):
            self._solution, self._solver_metadata = "-1", None
            try:
                with Solver(name=SAT_SOLVER_NAME, bootstrap_with=self.cnf.clauses) as solver:
                    self._solution = str(int(solver.solve()))
                    self._solver_metadata = {**solver.accum_stats(), "solvers": (SAT_SOLVER_NAME,)}
            except Exception:
                traceback.print_exc()
        return self._solution

    def solution_enumerate(self) -> Generator[str, None, None]:
        yield self.solution

    @property
    def search_space_size(self) -> Any:
        return 2**self.cnf.nv

    def check(self, answer: str) -> bool:
        try:
            assert self.format_check(answer)
            return answer == str(self.solution)
        except Exception:
            traceback.print_exc()
        return False

    def format_check(self, answer: str) -> bool:
        return isinstance(answer, str) and len(answer) == 1 and set(answer).issubset({"0", "1"})

    def accept(self, question: Question, *args, **kwargs) -> str:
        return question.visit_satdp(self, *args, **kwargs)

    @property
    def ANSWER_PATTERN(self) -> str:
        return r"(?=([01]{%d}))" % 1


class SATSP(Problem):
    @property
    def solution(self) -> str:
        assert self.cnf.is_sat
        if not hasattr(self, "_solution"):
            self._solution, self._solver_metadata = None, None
            try:
                with Solver(name=SAT_SOLVER_NAME, bootstrap_with=self.cnf.clauses) as solver:
                    _is_sat = solver.solve()
                    if _is_sat:
                        self._solution = "".join(["1" if iv > 0 else "0" for iv in solver.get_model()])
                    self._solver_metadata = {**solver.accum_stats(), "solvers": (SAT_SOLVER_NAME,)}
            except Exception:
                traceback.print_exc()
        return self._solution

    def solution_enumerate(self) -> Generator[str, None, None]:
        assert self.cnf.is_sat
        with Solver(name=SAT_SOLVER_NAME, bootstrap_with=self.cnf.clauses) as solver:
            for s in solver.enum_models():
                yield "".join(["1" if iv > 0 else "0" for iv in s])

    @property
    def search_space_size(self) -> Any:
        return 2**self.cnf.nv

    def check(self, answer: str) -> bool:
        assert self.cnf.is_sat
        try:
            assert self.format_check(answer)
            with Solver(name=SAT_SOLVER_NAME, bootstrap_with=self.cnf.clauses) as solver:
                return solver.solve(assumptions=[(i + 1) if ai == "1" else -(i + 1) for i, ai in enumerate(answer)])
        except Exception:
            traceback.print_exc()
        return False

    def format_check(self, answer: str) -> bool:
        return isinstance(answer, str) and len(answer) == self.cnf.nv and set(answer).issubset({"0", "1"})

    def accept(self, question: Question, *args, **kwargs) -> str:
        return question.visit_satsp(self, *args, **kwargs)

    @property
    def ANSWER_PATTERN(self) -> str:
        return r"(?=([01]{%d}))" % self.cnf.nv


class MaxSAT(Problem):
    @property
    def solution(self) -> str:
        assert not self.cnf.is_sat
        if not hasattr(self, "_solution"):
            self._solution, self._solver_metadata = None, None
            try:
                with MaxSATSolver(cnf2wcnf(self.cnf.cnf), solver=SAT_SOLVER_NAME, verbose=0) as solver:
                    solver.compute()
                    self._solver_metadata = {**solver.oracle.accum_stats(), "solvers": (SAT_SOLVER_NAME, "RC2")}
                    self._solution = "".join(["1" if iv > 0 else "0" for iv in solver.model])
            except Exception:
                traceback.print_exc()
        return self._solution

    def solution_enumerate(self) -> Generator[str, None, None]:
        assert not self.cnf.is_sat
        from pysat.examples.rc2 import RC2

        with RC2(cnf2wcnf(self.cnf.cnf), solver=SAT_SOLVER_NAME, verbose=0) as solver:
            pre_cost = None
            for s in solver.enumerate():
                if pre_cost is None:
                    pre_cost = solver.cost
                if solver.cost != pre_cost:
                    break
                yield "".join(["1" if iv > 0 else "0" for iv in s])

    @property
    def search_space_size(self) -> Any:
        return 2**self.cnf.nv

    def check(self, answer: str) -> bool:
        assert not self.cnf.is_sat
        try:
            assert self.format_check(answer)
            from pysat.examples.lsu import LSU as MaxSATSolver

            with MaxSATSolver(cnf2wcnf(self.cnf.cnf), solver=SAT_SOLVER_NAME, verbose=0) as solver:
                solver.solve()
                answer_cost = solver._get_model_cost(
                    cnf2wcnf(self.cnf.cnf), [(i + 1) if ai == "1" else -(i + 1) for i, ai in enumerate(answer)]
                )
                return answer_cost == solver.cost
        except Exception:
            traceback.print_exc()
        return False

    def format_check(self, answer: str) -> bool:
        return isinstance(answer, str) and len(answer) == self.cnf.nv and set(answer).issubset({"0", "1"})

    def accept(self, question: Question, *args, **kwargs) -> str:
        return question.visit_maxsat(self, *args, **kwargs)

    @property
    def ANSWER_PATTERN(self) -> str:
        return r"(?=([01]{%d}))" % self.cnf.nv


class MCS(Problem):
    @property
    def solution(self) -> str:
        assert not self.cnf.is_sat
        if not hasattr(self, "_solution"):
            with MCSSolver(cnf2wcnf(self.cnf.cnf), use_cld=False, solver_name=SAT_SOLVER_NAME) as solver:
                _solution_model = solver.compute()
                self._solution = "".join(["1" if i in _solution_model else "0" for i in range(1, self.cnf.mc + 1)])
                self._solver_metadata = {**solver.oracle.accum_stats(), "solvers": (SAT_SOLVER_NAME, "LBX")}
        return self._solution

    def solution_enumerate(self) -> Generator[str, None, None]:
        assert not self.cnf.is_sat
        with MCSSolver(cnf2wcnf(self.cnf.cnf), use_cld=False, solver_name=SAT_SOLVER_NAME) as solver:
            for mcs in solver.enumerate():
                solver.block(mcs)
                yield "".join(["1" if i in mcs else "0" for i in range(1, len(self.cnf.clauses) + 1)])

    @property
    def search_space_size(self) -> Any:
        return 2**self.cnf.mc

    def check(self, answer: str) -> bool:
        assert not self.cnf.is_sat
        try:
            assert self.format_check(answer)
            unmcs_clauses = [self.cnf.clauses[i] for i in range(self.cnf.mc) if answer[i] == "0"]
            mcs_clauses = [self.cnf.clauses[i] for i in range(self.cnf.mc) if answer[i] == "1"]
            with Solver(name=SAT_SOLVER_NAME, bootstrap_with=CNF(unmcs_clauses).cnf) as solver:
                if not solver.solve():
                    return False
            for i in range(len(mcs_clauses)):
                add_mcs_clauses = unmcs_clauses + [mcs_clauses[i]]
                with Solver(name=SAT_SOLVER_NAME, bootstrap_with=CNF(add_mcs_clauses).cnf) as solver:
                    if solver.solve():
                        return False
            return True
        except Exception:
            traceback.print_exc()
        return False

    def format_check(self, answer: str) -> bool:
        return isinstance(answer, str) and len(answer) == self.cnf.mc and set(answer).issubset({"0", "1"})

    def accept(self, question: Question, *args, **kwargs) -> str:
        return question.visit_mcs(self, *args, **kwargs)

    @property
    def ANSWER_PATTERN(self) -> str:
        return r"(?=([01]{%d}))" % self.cnf.mc


class MUS(Problem):
    @property
    def solution(self) -> str:
        assert not self.cnf.is_sat
        if not hasattr(self, "_solution"):
            with MUSSolver(self.cnf.cnf, solver=SAT_SOLVER_NAME, verbosity=0) as solver:
                _solution_model = solver.compute()
                self._solution = "".join(["1" if i in _solution_model else "0" for i in range(1, self.cnf.mc + 1)])
                self._solver_metadata = {**solver.oracle.accum_stats(), "solvers": (SAT_SOLVER_NAME, "MUSX")}
        return self._solution

    def solution_enumerate(self) -> Generator[str, None, None]:
        assert not self.cnf.is_sat
        from pysat.examples.hitman import Hitman

        with Hitman(solver="m22") as hitman_solver:
            with MCSSolver(cnf2wcnf(self.cnf.cnf), use_cld=False, solver_name=SAT_SOLVER_NAME) as solver:
                for mcs in solver.enumerate():
                    solver.block(mcs)
                    hitman_solver.hit(mcs)
            for mus in hitman_solver.enumerate():
                yield "".join(["1" if i in mus else "0" for i in range(1, len(self.cnf.clauses) + 1)])

    @property
    def search_space_size(self) -> Any:
        return 2**self.cnf.mc

    def check(self, answer: str) -> bool:
        assert not self.cnf.is_sat
        try:
            assert self.format_check(answer)
            mus_clauses = [self.cnf.clauses[i] for i in range(self.cnf.mc) if answer[i] == "1"]
            with Solver(name=SAT_SOLVER_NAME, bootstrap_with=CNF(mus_clauses).cnf) as solver:
                if solver.solve():
                    return False
            for i in range(len(mus_clauses)):
                sub_mus_clauses = mus_clauses[:i] + mus_clauses[i + 1 :]
                with Solver(name=SAT_SOLVER_NAME, bootstrap_with=CNF(sub_mus_clauses).cnf) as solver:
                    if not solver.solve():
                        return False
            return True
        except Exception:
            traceback.print_exc()
        return False

    def format_check(self, answer: str) -> bool:
        return isinstance(answer, str) and len(answer) == self.cnf.mc and set(answer).issubset({"0", "1"})

    def accept(self, question: Question, *args, **kwargs) -> str:
        return question.visit_mus(self, *args, **kwargs)

    @property
    def ANSWER_PATTERN(self) -> str:
        return r"(?=([01]{%d}))" % self.cnf.mc


def create_problem(problem_type: str, cnf: CNF) -> Problem:
    problem_type = problem_type.lower()
    match problem_type:
        case "satdp" | "satdp_sat" | "satdp_unsat":
            return SATDP(cnf)
        case "satsp":
            return SATSP(cnf)
        case "maxsat":
            return MaxSAT(cnf)
        case "mcs":
            return MCS(cnf)
        case "mus":
            return MUS(cnf)
    return None
