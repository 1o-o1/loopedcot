# Table 1 -- mmlu (huginn_0125)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 85934 layer passes over 1900 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 36.4 |
| default_at_budget | n/a | n/a | 37.6 (92%) |
| lookup | 24.8 | 35.5 | 35.8 |
| equation | 24.2 | 35.8 | 36.2 |
| equation_n30 | 24.2 | 35.8 | 36.2 |
| equation_n100 | 24.2 | 35.8 | 36.2 |
| gated_equation | 24.2 | 35.8 | 36.2 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
