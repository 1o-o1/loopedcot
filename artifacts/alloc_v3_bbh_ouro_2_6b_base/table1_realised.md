# Table 1 -- bbh (ouro_2_6b_base), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 197932 layer passes over 2337 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 82.6 |
| default_cell | n/a | 90.4 (10%) | 90.2 (21%) | 88.6 (57%) |
| default_at_budget | 81.0 (10%) | 90.4 (10%) | 87.1 (26%) | 67.3 (85%) |
| lookup | 43.7 (85%) | 56.4 | 77.4 | 80.4 |
| equation | 41.6 (85%) | 57.8 | 77.5 | 80.4 |
| equation_n30 | 41.6 (85%) | 57.8 | 77.5 | 80.4 |
| equation_n100 | 41.6 (85%) | 57.8 | 77.5 | 80.4 |
| gated_equation | 41.6 (85%) | 57.9 | 77.7 | 78.0 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
