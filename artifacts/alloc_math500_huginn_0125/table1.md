# Table 1 -- math500 (huginn_0125)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 224131 layer passes over 400 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 15.0 |
| default_at_budget | n/a | n/a | 15.4 (99%) |
| lookup | 8.2 | 15.2 | 15.8 |
| equation | 7.5 | 14.5 | 15.2 |
| equation_n30 | 7.5 | 6.8 | 15.2 |
| equation_n100 | 7.5 | 14.5 | 15.2 |
| gated_equation | 7.5 | 14.5 | 15.2 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
