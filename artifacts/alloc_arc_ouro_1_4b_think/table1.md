# Table 1 -- arc (ouro_1_4b_think)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 85662 layer passes over 1072 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 93.4 |
| default_at_budget | n/a | 87.2 (98%) | 90.6 |
| lookup | 74.4 | 86.3 | 89.6 |
| equation | 74.6 | 84.2 | 93.1 |
| equation_n30 | 74.6 | 84.1 | 93.1 |
| equation_n100 | 74.6 | 84.2 | 93.1 |
| gated_equation | 74.6 | 84.2 | 93.1 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
