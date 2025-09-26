# 🌟 Examples

Use these snippets to preview SATQuest prompts and work with the Python API.

## 🎯 Prompt Gallery

Each tab shows the exact prompt text produced by `Problem.accept(...)` for a small reference CNF. Pick a problem type on the outer tabs, then switch between question formats inside.

=== "`SATSP`"

    === "`Math`"

        ```text
        Given a CNF formula with 3 variables and 4 clauses in mathematical notation:
        
        (x_1 \lor \neg x_2 \lor x_3) \land (\neg x_1 \lor x_2 \lor x_3) \land (x_1 \lor x_2) \land (\neg x_3)

        Find a satisfying assignment for the formula.
        Output a binary string of length 3 ('1' for true, '0' for false).
        ```

    === "`DIMACS`"

        ```text
        Given a CNF formula with 3 variables and 4 clauses in DIMACS format:
        
        p cnf 3 4
        1 -2 3 0
        -1 2 3 0
        1 2 0
        -3 0

        Find a satisfying assignment for the formula.
        Output a binary string of length 3 ('1' for true, '0' for false).
        ```

    === "`Story`"

        ```text
        It's cookie day on Quirkwild Zoo!
        Chef Orion is baking 3 kinds of cookies (chocolate comet, maple moon, ginger nebula), each either crunchy or chewy.
        Each of his 4 friends will be happy if Orion bakes at least one cookie they prefer:
        
        
        1. Aquila wants: crunchy chocolate comet, chewy maple moon, crunchy ginger nebula
        2. Borealis wants: chewy chocolate comet, crunchy maple moon, crunchy ginger nebula
        3. Cygnus wants: crunchy chocolate comet, crunchy maple moon
        4. Draco wants: chewy ginger nebula

        Find a satisfying assignment for the formula.
        Output a binary string of length 3 ('1' for true, '0' for false).
        ```

    === "`DualStory`"

        ```text
        It's cookie day on Quirkwild Zoo!
        Chef Orion is baking 3 kinds of cookies (chocolate comet, maple moon, ginger nebula), each either crunchy or chewy.
        Each of his 4 friends will be unhappy only if every cookie in their disliked combination is baked:
        
        
        1. Aquila dislikes: chewy chocolate comet + crunchy maple moon + chewy ginger nebula
        2. Borealis dislikes: crunchy chocolate comet + chewy maple moon + chewy ginger nebula
        3. Cygnus dislikes: chewy chocolate comet + chewy maple moon
        4. Draco dislikes: crunchy ginger nebula

        Find a satisfying assignment for the formula.
        Output a binary string of length 3 ('1' for true, '0' for false).
        ```

=== "`SATDP (SAT)`"

    === "`Math`"

        ```text
        Given a CNF formula with 3 variables and 4 clauses in mathematical notation:
        
        (x_1 \lor \neg x_2 \lor x_3) \land (\neg x_1 \lor x_2 \lor x_3) \land (x_1 \lor x_2) \land (\neg x_3)

        Determine if the formula is satisfiable.
        Output a binary string of length 1 ('1' for satisfiable, '0' for unsatisfiable).
        ```

    === "`DIMACS`"

        ```text
        Given a CNF formula with 3 variables and 4 clauses in DIMACS format:
        
        p cnf 3 4
        1 -2 3 0
        -1 2 3 0
        1 2 0
        -3 0

        Determine if the formula is satisfiable.
        Output a binary string of length 1 ('1' for satisfiable, '0' for unsatisfiable).
        ```

    === "`Story`"

        ```text
        It's cookie day on Quirkwild Zoo!
        Chef Orion is baking 3 kinds of cookies (chocolate comet, maple moon, ginger nebula), each either crunchy or chewy.
        Each of his 4 friends will be happy if Orion bakes at least one cookie they prefer:
        
        
        1. Aquila wants: crunchy chocolate comet, chewy maple moon, crunchy ginger nebula
        2. Borealis wants: chewy chocolate comet, crunchy maple moon, crunchy ginger nebula
        3. Cygnus wants: crunchy chocolate comet, crunchy maple moon
        4. Draco wants: chewy ginger nebula

        Determine if the formula is satisfiable.
        Output a binary string of length 1 ('1' for satisfiable, '0' for unsatisfiable).
        ```

    === "`DualStory`"

        ```text
        It's cookie day on Quirkwild Zoo!
        Chef Orion is baking 3 kinds of cookies (chocolate comet, maple moon, ginger nebula), each either crunchy or chewy.
        Each of his 4 friends will be unhappy only if every cookie in their disliked combination is baked:
        
        
        1. Aquila dislikes: chewy chocolate comet + crunchy maple moon + chewy ginger nebula
        2. Borealis dislikes: crunchy chocolate comet + chewy maple moon + chewy ginger nebula
        3. Cygnus dislikes: chewy chocolate comet + chewy maple moon
        4. Draco dislikes: crunchy ginger nebula

        Determine if the formula is satisfiable.
        Output a binary string of length 1 ('1' for satisfiable, '0' for unsatisfiable).
        ```

=== "`SATDP (UNSAT)`"

    === "`Math`"

        ```text
        Given a CNF formula with 2 variables and 3 clauses in mathematical notation:
        
        (x_1 \lor x_2) \land (\neg x_1) \land (\neg x_2)

        Determine if the formula is satisfiable.
        Output a binary string of length 1 ('1' for satisfiable, '0' for unsatisfiable).
        ```

    === "`DIMACS`"

        ```text
        Given a CNF formula with 2 variables and 3 clauses in DIMACS format:
        
        p cnf 2 3
        1 2 0
        -1 0
        -2 0

        Determine if the formula is satisfiable.
        Output a binary string of length 1 ('1' for satisfiable, '0' for unsatisfiable).
        ```

    === "`Story`"

        ```text
        It's cookie day on Quirkwild Zoo!
        Chef Orion is baking 2 kinds of cookies (chocolate comet, maple moon), each either crunchy or chewy.
        Each of his 3 friends will be happy if Orion bakes at least one cookie they prefer:
        
        
        1. Aquila wants: crunchy chocolate comet, crunchy maple moon
        2. Borealis wants: chewy chocolate comet
        3. Cygnus wants: chewy maple moon

        Determine if the formula is satisfiable.
        Output a binary string of length 1 ('1' for satisfiable, '0' for unsatisfiable).
        ```

    === "`DualStory`"

        ```text
        It's cookie day on Quirkwild Zoo!
        Chef Orion is baking 2 kinds of cookies (chocolate comet, maple moon), each either crunchy or chewy.
        Each of his 3 friends will be unhappy only if every cookie in their disliked combination is baked:
        
        
        1. Aquila dislikes: chewy chocolate comet + chewy maple moon
        2. Borealis dislikes: crunchy chocolate comet
        3. Cygnus dislikes: crunchy maple moon

        Determine if the formula is satisfiable.
        Output a binary string of length 1 ('1' for satisfiable, '0' for unsatisfiable).
        ```

=== "`MaxSAT`"

    === "`Math`"

        ```text
        Given a CNF formula with 2 variables and 3 clauses in mathematical notation:
        
        (x_1 \lor x_2) \land (\neg x_1) \land (\neg x_2)

        Find an assignment that maximizes the number of satisfied clauses.
        Output a binary string of length 2 ('1' for true, '0' for false).
        ```

    === "`DIMACS`"

        ```text
        Given a CNF formula with 2 variables and 3 clauses in DIMACS format:
        
        p cnf 2 3
        1 2 0
        -1 0
        -2 0

        Find an assignment that maximizes the number of satisfied clauses.
        Output a binary string of length 2 ('1' for true, '0' for false).
        ```

    === "`Story`"

        ```text
        It's cookie day on Quirkwild Zoo!
        Chef Orion is baking 2 kinds of cookies (chocolate comet, maple moon), each either crunchy or chewy.
        Each of his 3 friends will be happy if Orion bakes at least one cookie they prefer:
        
        
        1. Aquila wants: crunchy chocolate comet, crunchy maple moon
        2. Borealis wants: chewy chocolate comet
        3. Cygnus wants: chewy maple moon

        Find an assignment that maximizes the number of satisfied clauses.
        Output a binary string of length 2 ('1' for true, '0' for false).
        ```

    === "`DualStory`"

        ```text
        It's cookie day on Quirkwild Zoo!
        Chef Orion is baking 2 kinds of cookies (chocolate comet, maple moon), each either crunchy or chewy.
        Each of his 3 friends will be unhappy only if every cookie in their disliked combination is baked:
        
        
        1. Aquila dislikes: chewy chocolate comet + chewy maple moon
        2. Borealis dislikes: crunchy chocolate comet
        3. Cygnus dislikes: crunchy maple moon

        Find an assignment that maximizes the number of satisfied clauses.
        Output a binary string of length 2 ('1' for true, '0' for false).
        ```

=== "`MCS`"

    === "`Math`"

        ```text
        Given a CNF formula with 2 variables and 3 clauses in mathematical notation:
        
        (x_1 \lor x_2) \land (\neg x_1) \land (\neg x_2)

        Find a minimal subset of clauses whose removal makes the formula satisfiable (no proper subset has this property).
        Output a binary string of length 3 ('1' if the clause is in the subset, '0' otherwise), following the order of clauses in the formula.
        ```

    === "`DIMACS`"

        ```text
        Given a CNF formula with 2 variables and 3 clauses in DIMACS format:
        
        p cnf 2 3
        1 2 0
        -1 0
        -2 0

        Find a minimal subset of clauses whose removal makes the formula satisfiable (no proper subset has this property).
        Output a binary string of length 3 ('1' if the clause is in the subset, '0' otherwise), following the order of clauses in the formula.
        ```

    === "`Story`"

        ```text
        It's cookie day on Quirkwild Zoo!
        Chef Orion is baking 2 kinds of cookies (chocolate comet, maple moon), each either crunchy or chewy.
        Each of his 3 friends will be happy if Orion bakes at least one cookie they prefer:        
        
        1. Aquila wants: crunchy chocolate comet, crunchy maple moon
        2. Borealis wants: chewy chocolate comet
        3. Cygnus wants: chewy maple moon

        Find a minimal subset of clauses whose removal makes the formula satisfiable (no proper subset has this property).
        Output a binary string of length 3 ('1' if the clause is in the subset, '0' otherwise), following the order of clauses in the formula.
        ```

    === "`DualStory`"

        ```text
        It's cookie day on Quirkwild Zoo!
        Chef Orion is baking 2 kinds of cookies (chocolate comet, maple moon), each either crunchy or chewy.
        Each of his 3 friends will be unhappy only if every cookie in their disliked combination is baked:
        
        1. Aquila dislikes: chewy chocolate comet + chewy maple moon
        2. Borealis dislikes: crunchy chocolate comet
        3. Cygnus dislikes: crunchy maple moon

        Find a minimal subset of clauses whose removal makes the formula satisfiable (no proper subset has this property).
        Output a binary string of length 3 ('1' if the clause is in the subset, '0' otherwise), following the order of clauses in the formula.
        ```

=== "`MUS`"

    === "`Math`"

        ```text
        Given a CNF formula with 2 variables and 3 clauses in mathematical notation:
        
        (x_1 \lor x_2) \land (\neg x_1) \land (\neg x_2)

        Find a minimal subset of clauses that is unsatisfiable (no proper subset is unsatisfiable).
        Output a binary string of length 3 ('1' if the clause is in the subset, '0' otherwise), following the order of clauses in the formula.
        ```

    === "`DIMACS`"

        ```text
        Given a CNF formula with 2 variables and 3 clauses in DIMACS format:
        
        p cnf 2 3
        1 2 0
        -1 0
        -2 0

        Find a minimal subset of clauses that is unsatisfiable (no proper subset is unsatisfiable).
        Output a binary string of length 3 ('1' if the clause is in the subset, '0' otherwise), following the order of clauses in the formula.
        ```

    === "`Story`"

        ```text
        It's cookie day on Quirkwild Zoo!
        Chef Orion is baking 2 kinds of cookies (chocolate comet, maple moon), each either crunchy or chewy.
        Each of his 3 friends will be happy if Orion bakes at least one cookie they prefer:        
        
        1. Aquila wants: crunchy chocolate comet, crunchy maple moon
        2. Borealis wants: chewy chocolate comet
        3. Cygnus wants: chewy maple moon

        Find a minimal subset of clauses that is unsatisfiable (no proper subset is unsatisfiable).
        Output a binary string of length 3 ('1' if the clause is in the subset, '0' otherwise), following the order of clauses in the formula.
        ```

    === "`DualStory`"

        ```text
        It's cookie day on Quirkwild Zoo!
        Chef Orion is baking 2 kinds of cookies (chocolate comet, maple moon), each either crunchy or chewy.
        Each of his 3 friends will be unhappy only if every cookie in their disliked combination is baked:
        
        1. Aquila dislikes: chewy chocolate comet + chewy maple moon
        2. Borealis dislikes: crunchy chocolate comet
        3. Cygnus dislikes: crunchy maple moon

        Find a minimal subset of clauses that is unsatisfiable (no proper subset is unsatisfiable).
        Output a binary string of length 3 ('1' if the clause is in the subset, '0' otherwise), following the order of clauses in the formula.
        ```

## 🛠️ API Recipes

### ✅ Verify a Candidate Assignment

```python
from datasets import load_dataset

from satquest import CNF, create_problem, create_question

item = load_dataset("sdpkjc/SATQuest", split="test")[12]
cnf = CNF(dimacs=item["sat_dimacs"])
problem = create_problem("SATSP", cnf)
question = create_question("math")

prompt = problem.accept(question)
print(prompt)

candidate = "001"
print("correct?", problem.check(candidate))
print("format ok?", problem.format_check(candidate))
```

`check` returns `1` for fully correct assignments, `0` for wrong answers, and fractional values for partially correct optimisation tasks.

### 🔄 Switch Prompt Styles

```python
cnf = CNF(dimacs=item["sat_dimacs"])
problem = create_problem("SATSP", cnf)

for q_type in ["math", "dimacs", "story", "dualstory"]:
    question = create_question(q_type)
    preview = problem.accept(question)
    print("---", q_type, "---")
    print(preview.splitlines()[0])
```

Different question types emphasise either natural-language reasoning (`story`) or raw DIMACS literals (`dimacs`). Use this pattern to create mixed evaluation batches.

### 🧪 Evaluate Multiple CNFs Locally

```python
from datasets import load_dataset

from satquest import CNF, create_problem, create_question

rows = load_dataset("sdpkjc/SATQuest", split="test").select(range(5))
question = create_question("math")

for row in rows:
    cnf = CNF(dimacs=row["sat_dimacs"])
    problem = create_problem("SATSP", cnf)
    prompt = problem.accept(question)
    reference = problem.solution
    print(f"CNF {row['id']} -> ground truth {reference}")
```

This loop mimics the behaviour of `eval_model.py` without involving an LLM, which is handy for debugging prompt templates or solver expectations.

### 🗂️ Use Solver Metadata for Filtering

```python
from datasets import load_dataset

dataset = load_dataset("sdpkjc/SATQuest", split="test")

def is_hard(example):
    mus_size = len(example["solver_metadatas"]["MUS"]["decisions"])
    return mus_size >= 2

hard_examples = dataset.filter(is_hard)
print("hard instances:", len(hard_examples))
```

Metadata includes MUS indices, MaxSAT scores, and satisfying assignments. Combine these signals with your evaluation metrics to build targeted test suites.

### 🤖 Prepare Prompts for Custom RL Pipelines

```python
from satquest import CNF, create_problem, create_question

cnf = CNF(dimacs=item["sat_dimacs"])
problem = create_problem("SATSP", cnf)
question = create_question("story")

prompt_messages = [
    {"role": "system", "content": "You are a careful reasoning assistant."},
    {"role": "user", "content": problem.accept(question)},
]
```

The reinforcement learning script (`rft.py`) follows a similar structure but augments the user message with tags such as `<think>` to guide the model. Reuse this scaffolding in your own trainers or adapters.
