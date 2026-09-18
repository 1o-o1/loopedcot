# Table 1 -- svamp (ouro_1_4b_base)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 65870 layer passes over 200 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 86.5 |
| default_at_budget | n/a | n/a | 63.0 |
| lookup | 24.5 | 50.5 | 84.0 |
| equation | 28.0 | 50.5 | 85.5 |
| equation_n30 | 28.0 | 50.5 | 85.5 |
| equation_n100 | 28.0 | 50.5 | 85.5 |
| gated_equation | 28.0 | 50.5 | 85.5 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
