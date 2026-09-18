# Table 1 -- csqa (ouro_2_6b_base), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 124178 layer passes over 1121 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 80.0 |
| default_cell | n/a | n/a | n/a | 79.9 (53%) |
| default_at_budget | n/a | n/a | n/a | 81.0 |
| lookup | 37.4 | 75.2 | 80.6 | 80.6 |
| equation | 37.4 | 74.2 | 74.0 | 74.0 |
| equation_n30 | 37.4 | 74.2 | 74.0 | 74.0 |
| equation_n100 | 37.4 | 74.2 | 74.0 | 74.0 |
| gated_equation | 37.4 | 74.2 | 74.0 | 76.4 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
