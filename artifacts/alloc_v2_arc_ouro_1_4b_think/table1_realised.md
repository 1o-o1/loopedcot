# Table 1 -- arc (ouro_1_4b_think), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 85662 layer passes over 1072 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 93.4 |
| default_cell | n/a | n/a | 97.2 (27%) | 96.6 (82%) |
| default_at_budget | n/a | 87.2 (98%) | 88.9 | 91.2 |
| lookup | 74.4 | 86.8 | 89.6 | 89.6 |
| equation | 74.6 | 87.8 | 92.3 | 93.6 |
| equation_n30 | 74.6 | 85.6 | 91.0 | 91.6 |
| equation_n100 | 74.6 | 87.8 | 92.3 | 93.6 |
| gated_equation | 74.6 | 87.8 | 91.8 | 93.6 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
