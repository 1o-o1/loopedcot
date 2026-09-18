# Table 1 -- aqua (huginn_0125)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 142485 layer passes over 154 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 24.7 |
| default_at_budget | n/a | 13.0 (15%) | 23.4 |
| lookup | 23.4 | 24.7 | 24.7 |
| equation | 25.3 | 24.7 | 20.8 |
| equation_n30 | 25.3 | 24.7 | 20.8 |
| equation_n100 | 25.3 | 24.7 | 20.8 |
| gated_equation | 25.3 | 24.7 | 20.8 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
