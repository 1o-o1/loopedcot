# Table 1 -- svamp (ouro_1_4b_think)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 129897 layer passes over 200 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 89.5 |
| default_at_budget | n/a | 59.5 (98%) | 89.0 |
| lookup | 47.5 | 85.5 | 87.0 |
| equation | 52.5 | 85.5 | 84.5 |
| equation_n30 | 52.5 | 85.0 | 86.5 |
| equation_n100 | 52.5 | 85.5 | 84.5 |
| gated_equation | 52.5 | 85.5 | 84.5 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
