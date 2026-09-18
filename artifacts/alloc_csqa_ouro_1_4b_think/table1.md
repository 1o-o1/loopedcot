# Table 1 -- csqa (ouro_1_4b_think)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 131275 layer passes over 1121 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 77.4 |
| default_at_budget | n/a | 70.9 | 76.1 |
| lookup | 55.8 | 70.2 | 74.2 |
| equation | 55.6 | 74.0 | 76.3 |
| equation_n30 | 55.6 | 74.0 | 76.1 |
| equation_n100 | 55.6 | 74.0 | 76.3 |
| gated_equation | 55.6 | 74.0 | 76.1 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
