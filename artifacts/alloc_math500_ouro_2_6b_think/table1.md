# Table 1 -- math500 (ouro_2_6b_think)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 563241 layer passes over 400 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 91.2 |
| default_at_budget | n/a | 41.7 (99%) | 76.2 |
| lookup | 43.2 | 72.8 | 83.8 |
| equation | 43.2 | 72.8 | 81.8 |
| equation_n30 | 43.2 | 45.5 | 82.0 |
| equation_n100 | 43.2 | 72.8 | 81.8 |
| gated_equation | 43.2 | 72.8 | 81.8 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
