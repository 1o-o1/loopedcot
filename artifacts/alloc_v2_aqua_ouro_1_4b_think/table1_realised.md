# Table 1 -- aqua (ouro_1_4b_think), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 223283 layer passes over 154 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 82.5 |
| default_cell | n/a | 100.0 (14%) | 97.8 (58%) | 98.1 (68%) |
| default_at_budget | n/a | 51.9 | 78.6 | 79.2 |
| lookup | 51.3 | 77.3 | 82.5 | 85.7 |
| equation | 50.6 | 77.3 | 83.8 | 85.7 |
| equation_n30 | 49.4 | 77.3 | 82.5 | 84.4 |
| equation_n100 | 50.6 | 77.3 | 83.8 | 85.7 |
| gated_equation | 50.6 | 77.3 | 83.1 | 85.7 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
