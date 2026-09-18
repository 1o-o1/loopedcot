# Table 1 -- csqa (huginn_0125)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 87279 layer passes over 1121 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 43.6 |
| default_at_budget | n/a | n/a | 42.2 |
| lookup | 19.1 | 30.9 | 43.1 |
| equation | 19.1 | 31.4 | 42.6 |
| equation_n30 | 19.1 | 31.4 | 42.6 |
| equation_n100 | 19.1 | 31.4 | 42.6 |
| gated_equation | 19.1 | 31.4 | 43.1 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
