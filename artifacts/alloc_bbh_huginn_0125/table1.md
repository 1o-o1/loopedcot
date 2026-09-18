# Table 1 -- bbh (huginn_0125)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 142666 layer passes over 2337 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 35.7 |
| default_at_budget | 55.8 (10%) | 61.0 (21%) | 35.9 (88%) |
| lookup | 30.6 | 31.4 | 35.4 |
| equation | 28.3 | 24.7 | 35.4 |
| equation_n30 | 31.8 | 34.4 | 34.5 |
| equation_n100 | 28.3 | 24.7 | 35.4 |
| gated_equation | 28.3 | 24.7 | 35.6 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
