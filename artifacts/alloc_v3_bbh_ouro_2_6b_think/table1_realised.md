# Table 1 -- bbh (ouro_2_6b_think), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 322452 layer passes over 2337 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 91.1 |
| default_cell | n/a | 85.8 (10%) | 92.9 (26%) | 93.9 (65%) |
| default_at_budget | 85.4 (10%) | 78.5 (40%) | 62.8 (97%) | 83.8 |
| lookup | 48.5 | 76.7 | 84.9 | 87.2 |
| equation | 48.9 | 76.7 | 84.9 | 88.0 |
| equation_n30 | 42.3 | 76.0 | 83.6 | 84.2 |
| equation_n100 | 48.9 | 76.7 | 84.9 | 88.0 |
| gated_equation | 48.6 | 76.6 | 84.4 | 83.7 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
