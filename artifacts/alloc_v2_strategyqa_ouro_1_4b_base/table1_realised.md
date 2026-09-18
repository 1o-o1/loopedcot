# Table 1 -- strategyqa (ouro_1_4b_base), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 58978 layer passes over 2190 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 66.3 |
| default_cell | n/a | n/a | 67.5 (86%) | 66.8 (95%) |
| default_at_budget | n/a | n/a | 66.5 | 66.5 |
| lookup | 55.6 | 63.9 | 65.8 | 65.8 |
| equation | 53.8 | 66.8 | 67.4 | 66.4 |
| equation_n30 | 55.3 | 66.8 | 66.5 | 66.4 |
| equation_n100 | 53.8 | 66.8 | 67.4 | 66.4 |
| gated_equation | 53.8 | 66.8 | 66.5 | 66.5 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
