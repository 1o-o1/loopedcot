# Table 1 -- csqa (ouro_2_6b_base)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 124178 layer passes over 1121 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 80.0 |
| default_at_budget | n/a | n/a | 81.0 |
| lookup | 33.7 | 75.2 | 80.6 |
| equation | 33.7 | 74.2 | 74.0 |
| equation_n30 | 33.7 | 74.2 | 74.0 |
| equation_n100 | 33.7 | 74.2 | 74.0 |
| gated_equation | 33.7 | 74.2 | 74.0 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
