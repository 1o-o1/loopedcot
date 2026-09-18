# Table 1 -- strategyqa (huginn_0125)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 119422 layer passes over 2190 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 55.5 |
| default_at_budget | n/a | 56.0 | 55.9 |
| lookup | 56.4 | 56.0 | 56.0 |
| equation | 56.4 | 56.0 | 55.9 |
| equation_n30 | 56.4 | 56.7 | 56.3 |
| equation_n100 | 56.4 | 56.0 | 55.9 |
| gated_equation | 56.4 | 56.0 | 55.9 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
