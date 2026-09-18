# Table 1 -- bbh (ouro_1_4b_base)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 100844 layer passes over 2337 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 75.6 |
| default_at_budget | 76.7 (10%) | 79.6 (10%) | 59.8 (86%) |
| lookup | 33.8 (86%) | 46.8 | 65.4 |
| equation | 34.3 (86%) | 46.5 | 68.4 |
| equation_n30 | 35.6 (86%) | 46.5 | 68.1 |
| equation_n100 | 34.3 (86%) | 46.5 | 68.4 |
| gated_equation | 34.3 (86%) | 46.5 | 68.4 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
