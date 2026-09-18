# Table 1 -- aqua (huginn_0125), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 142485 layer passes over 154 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 24.7 |
| default_cell | n/a | 50.0 (1%) | 23.3 (86%) | 23.9 (87%) |
| default_at_budget | n/a | 13.0 (15%) | 22.7 | 23.4 |
| lookup | 24.7 | 24.7 | 24.7 | 24.7 |
| equation | 25.3 | 24.7 | 20.8 | 20.8 |
| equation_n30 | 25.3 | 24.7 | 20.8 | 20.8 |
| equation_n100 | 25.3 | 24.7 | 20.8 | 20.8 |
| gated_equation | 25.3 | 24.7 | 20.8 | 20.8 |

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
