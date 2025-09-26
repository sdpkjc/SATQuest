from datasets import load_dataset

from satquest import CNF, create_problem, create_question

item = load_dataset("sdpkjc/SATQuest", split="test")[0]
cnf = CNF(dimacs=item["sat_dimacs"])
# cnf.shuffle()

problem = create_problem("SATSP", cnf)  # or 'SATDP', 'MaxSAT', 'MCS', 'MUS'
question = create_question("math")  # or 'dimacs', 'story', 'dualstory'

prompt = problem.accept(question)
print(f"===== Prompt =====\n{prompt}\n")
"""
Given a CNF formula with 3 variables and 12 clauses in mathematical notation:

(x_1 \lor x_2 \lor x_3) \land (x_3 \lor \neg x_1 \lor x_2) \land (x_1 \lor x_3 \lor \neg x_2) \land (x_1 \lor \neg x_2) \land (x_3 \lor x_1 \lor \neg x_2) \land (x_3 \lor \neg x_1 \lor x_2) \land (\neg x_3 \lor \neg x_1) \land (\neg x_1 \lor x_2 \lor x_3) \land (\neg x_2 \lor \neg x_3) \land (\neg x_2 \lor x_3 \lor x_1) \land (x_1 \lor \neg x_3) \land (\neg x_3 \lor \neg x_2 \lor \neg x_1)

Find a satisfying assignment for the formula.
Output a binary string of length 3 ('1' for true, '0' for false).
"""

answer = problem.solution  # reference answer
print(f"===== Answer =====\n{answer}\n")
# 110

reward = int(problem.check(answer))  # 1 if answer is correct, 0 otherwise, 0.5 if answer is partial
print(f"===== Reward =====\n{reward}\n")
# 1
