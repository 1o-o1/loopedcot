# Table 1 -- aqua (ouro_2_6b_think)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 401640 layer passes over 154 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 89.0 |
| default_at_budget | n/a | 55.8 | 85.1 |
| lookup | 50.0 | 79.2 | 85.1 |
| equation | 48.1 | 79.2 | 85.1 |
| equation_n30 | 50.6 | 73.4 | 85.1 |
| equation_n100 | 48.1 | 79.2 | 85.1 |
| gated_equation | 48.1 | 79.2 | 85.1 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
