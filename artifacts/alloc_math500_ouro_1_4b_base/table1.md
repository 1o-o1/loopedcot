# Table 1 -- math500 (ouro_1_4b_base)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 178329 layer passes over 400 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 63.5 |
| default_at_budget | n/a | n/a | 56.9 (100%) |
| lookup | 24.1 (100%) | 53.0 | 65.5 |
| equation | 24.1 (100%) | 53.0 | 64.8 |
| equation_n30 | 24.1 (100%) | 53.0 | 65.5 |
| equation_n100 | 24.1 (100%) | 53.0 | 64.8 |
| gated_equation | 24.1 (100%) | 53.0 | 64.8 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
