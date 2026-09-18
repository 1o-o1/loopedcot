# Table 1 -- arc (ouro_1_4b_base), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 38812 layer passes over 1072 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 86.5 |
| default_cell | n/a | n/a | n/a | 86.7 (57%) |
| default_at_budget | n/a | n/a | n/a | 86.7 (94%) |
| lookup | 42.9 (94%) | 75.4 | 83.7 | 86.0 |
| equation | 43.8 (94%) | 72.5 | 81.8 | 85.7 |
| equation_n30 | 43.8 (94%) | 72.5 | 84.4 | 85.8 |
| equation_n100 | 43.8 (94%) | 72.5 | 81.8 | 85.7 |
| gated_equation | 43.8 (94%) | 72.6 | 83.9 | 85.8 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
