# Table 1 -- arc (huginn_0125)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 53810 layer passes over 1072 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 41.3 |
| default_at_budget | n/a | n/a | 42.3 (94%) |
| lookup | 25.8 | 39.6 | 41.5 |
| equation | 26.7 | 39.0 | 41.4 |
| equation_n30 | 26.7 | 33.6 | 42.4 |
| equation_n100 | 26.7 | 39.0 | 41.4 |
| gated_equation | 26.7 | 39.0 | 42.4 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
