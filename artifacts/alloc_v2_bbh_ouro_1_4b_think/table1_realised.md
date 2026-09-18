# Table 1 -- bbh (ouro_1_4b_think), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 182991 layer passes over 2337 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 84.4 |
| default_cell | 90.9 (0%) | 83.0 (13%) | 89.2 (37%) | 90.6 (70%) |
| default_at_budget | 66.2 (10%) | 52.8 (72%) | 66.5 | 82.0 |
| lookup | 36.5 | 65.7 | 80.2 | 83.6 |
| equation | 35.7 | 65.3 | 80.1 | 82.8 |
| equation_n30 | 35.6 | 65.2 | 80.3 | 82.7 |
| equation_n100 | 35.7 | 65.3 | 80.1 | 82.8 |
| gated_equation | 35.7 | 65.3 | 80.1 | 83.7 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
