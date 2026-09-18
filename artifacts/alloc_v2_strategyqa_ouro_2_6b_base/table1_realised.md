# Table 1 -- strategyqa (ouro_2_6b_base), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 99332 layer passes over 2190 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 74.7 |
| default_cell | n/a | n/a | 76.2 (1%) | 74.8 (97%) |
| default_at_budget | n/a | n/a | 72.9 (100%) | 74.9 |
| lookup | 59.5 | 66.9 | 73.5 | 75.0 |
| equation | 59.3 | 69.8 | 73.5 | 74.9 |
| equation_n30 | 59.3 | 66.4 | 73.3 | 74.9 |
| equation_n100 | 59.3 | 69.8 | 73.5 | 74.9 |
| gated_equation | 59.3 | 69.8 | 73.6 | 74.9 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
