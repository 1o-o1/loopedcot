# Table 1 -- math500 (ouro_1_4b_think)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 278580 layer passes over 400 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 89.8 |
| default_at_budget | n/a | 36.9 (99%) | 75.5 |
| lookup | 32.0 | 66.8 | 84.2 |
| equation | 32.0 | 66.8 | 77.2 |
| equation_n30 | 32.0 | 66.8 | 77.0 |
| equation_n100 | 32.0 | 66.8 | 77.2 |
| gated_equation | 32.0 | 66.8 | 77.2 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
