from abc import ABC, abstractmethod

from satquest.cnf import CNF
from satquest.constants import CHARACTERS, CHEF_NAME, COOKIE_NAMES, GIT_HASH
from satquest.satquest_utils import get_class_source_hash


class Question(ABC):
    @abstractmethod
    def visit_satdp(self, cnf: CNF) -> str:
        # SAT Decision Problem
        pass

    @abstractmethod
    def visit_satsp(self, cnf: CNF) -> str:
        # SAT Solve Problem
        pass

    @abstractmethod
    def visit_maxsat(self, cnf: CNF) -> str:
        # MaxSAT
        pass

    @abstractmethod
    def visit_mcs(self, cnf: CNF) -> str:
        # Minimal Correction Subset (MCS)
        pass

    @abstractmethod
    def visit_mus(self, cnf: CNF) -> str:
        # Minimal Unsatisfiable Subset (MUS)
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}_{GIT_HASH}_{get_class_source_hash(self.__class__)}"


class QuestionDIMACS(Question):
    def visit_satdp(self, cnf: CNF) -> str:
        Q = self._get_q_prefix(cnf)
        Q += """
Determine if the formula is satisfiable.
Output a binary string of length 1 ('1' for satisfiable, '0' for unsatisfiable)."""
        return Q

    def visit_satsp(self, cnf: CNF) -> str:
        Q = self._get_q_prefix(cnf)
        Q += f"""
Find a satisfying assignment for the formula.
Output a binary string of length {cnf.nv} ('1' for true, '0' for false)."""
        return Q

    def visit_maxsat(self, cnf: CNF) -> str:
        Q = self._get_q_prefix(cnf)
        Q += f"""
Find an assignment that maximizes the number of satisfied clauses.
Output a binary string of length {cnf.nv} ('1' for true, '0' for false)."""
        return Q

    def visit_mcs(self, cnf: CNF) -> str:
        Q = self._get_q_prefix(cnf)
        Q += f"""
Find a minimal subset of clauses whose removal makes the formula satisfiable (no proper subset has this property).
Output a binary string of length {cnf.mc} ('1' if the clause is in the subset, '0' otherwise), following the order of clauses in the formula."""
        return Q

    def visit_mus(self, cnf: CNF) -> str:
        Q = self._get_q_prefix(cnf)
        Q += f"""
Find a minimal subset of clauses that is unsatisfiable (no proper subset is unsatisfiable).
Output a binary string of length {cnf.mc} ('1' if the clause is in the subset, '0' otherwise), following the order of clauses in the formula."""
        return Q

    def _get_q_prefix(self, cnf: CNF) -> str:
        Q_prefix = f"""\
Given a CNF formula with {cnf.nv} variables and {cnf.mc} clauses in DIMACS format:

{cnf.dimacs}
"""
        return Q_prefix


class QuestionMath(QuestionDIMACS):
    def _clauses2mathformula(self, clauses: list) -> str:
        return " \\land ".join(
            "("
            + " \\lor ".join(
                (f"x_{{{abs(lit)}}}" if lit > 0 else f"\\neg x_{{{abs(lit)}}}")
                if abs(lit) > 9
                else (f"x_{abs(lit)}" if lit > 0 else f"\\neg x_{abs(lit)}")
                for lit in clause
            )
            + ")"
            for clause in clauses
        )

    def _get_q_prefix(self, cnf: CNF) -> str:
        Q_prefix = f"""\
Given a CNF formula with {cnf.nv} variables and {cnf.mc} clauses in mathematical notation:

{self._clauses2mathformula(cnf.clauses)}
"""
        return Q_prefix


class QuestionStory(Question):
    # Cookie Challenge (Wishes)

    def visit_satdp(self, cnf: CNF) -> str:
        self._cookie_names, self._character_names = self._get_names(cnf.nv, cnf.mc)
        Q = self._get_q_prefix(cnf)
        Q += f"""
Is it possible for Chef {CHEF_NAME} to bake cookies so every friend is happy?
Output a binary string of length 1 ('1' for yes, '0' for no)."""
        return Q

    def visit_satsp(self, cnf: CNF) -> str:
        self._cookie_names, self._character_names = self._get_names(cnf.nv, cnf.mc)
        Q = self._get_q_prefix(cnf)
        Q += f"""
Help Chef {CHEF_NAME} find a cookie recipe that makes everyone happy.
Output a binary string of length {cnf.nv} for cookies ({', '.join(self._cookie_names)}): '1' for crunchy, '0' for chewy."""
        return Q

    def visit_maxsat(self, cnf: CNF) -> str:
        self._cookie_names, self._character_names = self._get_names(cnf.nv, cnf.mc)
        Q = self._get_q_prefix(cnf)
        Q += f"""
Help Chef {CHEF_NAME} find a cookie recipe that makes as many friends happy as possible.
Output a binary string of length {cnf.nv} for cookies ({', '.join(self._cookie_names)}): '1' for crunchy, '0' for chewy."""
        return Q

    def visit_mcs(self, cnf: CNF) -> str:
        self._cookie_names, self._character_names = self._get_names(cnf.nv, cnf.mc)
        Q = self._get_q_prefix(cnf)
        Q += f"""
Sadly, Chef {CHEF_NAME} can't make everyone happy. Find a minimal group of friends whose requirements Chef {CHEF_NAME} must ignore to keep the others happy. (This group is minimal: removing all requirements in this group is necessary to allow all other friends' requirements to be met, and removing only a part of this group is not sufficient.)
Output a binary string of length {cnf.mc} ({', '.join(self._character_names)}): '1' to ignore their requirements, '0' otherwise."""
        return Q

    def visit_mus(self, cnf: CNF) -> str:
        self._cookie_names, self._character_names = self._get_names(cnf.nv, cnf.mc)
        Q = self._get_q_prefix(cnf)
        Q += f"""
Sadly, Chef {CHEF_NAME} can't make everyone happy. Find a minimal group of friends such that Chef {CHEF_NAME} cannot possibly accommodate all their requirements at the same time. (This group is minimal: removing any single requirement from this group makes it possible to accommodate all the other requirements within this group.)
Output a binary string of length {cnf.mc} ({', '.join(self._character_names)}): '1' if their requirements is part of this core group, '0' otherwise."""
        return Q

    def _get_q_prefix(self, cnf: CNF) -> str:
        Q_prefix = f"""It's cookie day on Quirkwild Zoo!
Chef {CHEF_NAME} is baking {cnf.nv} kinds of cookies ({', '.join(self._cookie_names)}), each either crunchy or chewy.
Each of his {cnf.mc} friends will be happy if {CHEF_NAME} bakes at least one cookie they prefer:

{self._clauses2story_conditions(cnf.clauses)}
"""
        return Q_prefix

    def _clauses2story_conditions(self, clauses: list) -> str:
        friends_texts = []
        for friend_idx, clause in enumerate(clauses):
            friend_name = self._character_names[friend_idx]
            conditions = []
            for lit in clause:
                cookie_name = self._cookie_names[(abs(lit) - 1)]
                texture = "crunchy" if lit > 0 else "chewy"
                conditions.append(f"{texture} {cookie_name}")
            conditions_text = ", ".join(conditions)
            friends_texts.append(f"{friend_idx+1}. {friend_name} wants: {conditions_text}")
        friends_text = "\n".join(friends_texts)
        return friends_text

    def _get_names(self, n: int, m: int) -> tuple[list, list]:
        assert n <= len(COOKIE_NAMES)
        assert m <= len(CHARACTERS)
        return COOKIE_NAMES[:n], CHARACTERS[:m]


class QuestionDualStory(QuestionStory):
    # Cookie Challenge (Dislikes)

    def _get_q_prefix(self, cnf: CNF) -> str:
        Q_prefix = f"""It's cookie day on Quirkwild Zoo!
Chef {CHEF_NAME} is baking {cnf.nv} kinds of cookies ({', '.join(self._cookie_names)}), each either crunchy or chewy.
Each of his {cnf.mc} friends will be unhappy only if every cookie in their disliked combination is baked:

{self._clauses2story_conditions(cnf.clauses)}
"""
        return Q_prefix

    def _clauses2story_conditions(self, clauses: list) -> str:
        friends_text = super()._clauses2story_conditions(clauses)
        friends_text = friends_text.replace("wants", "dislikes").replace(", ", " + ")
        # Reversed: positive -> chewy, negative -> crunchy
        friends_text = friends_text.replace("chewy", "==9527==").replace("crunchy", "chewy").replace("==9527==", "crunchy")
        return friends_text


def create_question(question_type: str) -> Question:
    question_type = question_type.lower()
    match question_type:
        case "dimacs":
            return QuestionDIMACS()
        case "math":
            return QuestionMath()
        case "story":
            return QuestionStory()
        case "dualstory":
            return QuestionDualStory()
    raise ValueError(f"Invalid question type: {question_type}")
