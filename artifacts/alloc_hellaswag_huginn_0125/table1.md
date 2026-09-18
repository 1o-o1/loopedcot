# Table 1 -- hellaswag (huginn_0125)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 116966 layer passes over 1900 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 34.4 |
| default_at_budget | n/a | n/a | 34.9 (100%) |
| lookup | 27.8 | 39.1 | 40.3 |
| equation | 28.1 | 33.6 | 33.1 |
| equation_n30 | 28.1 | 33.6 | 33.1 |
| equation_n100 | 28.1 | 33.6 | 33.1 |
| gated_equation | 28.1 | 33.6 | 34.6 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
