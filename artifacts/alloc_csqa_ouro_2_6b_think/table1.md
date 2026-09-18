# Table 1 -- csqa (ouro_2_6b_think)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 235620 layer passes over 1121 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 80.8 |
| default_at_budget | n/a | n/a | 79.9 |
| lookup | 27.4 | 77.4 | 79.2 |
| equation | 19.6 | 76.6 | 79.9 |
| equation_n30 | 27.4 | 80.3 | 78.2 |
| equation_n100 | 19.6 | 76.6 | 79.9 |
| gated_equation | 19.6 | 76.6 | 79.9 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
