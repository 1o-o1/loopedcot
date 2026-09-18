# Table 1 -- svamp (ouro_2_6b_think)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 249394 layer passes over 200 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 7.0 |
| default_at_budget | n/a | 5.6 (45%) | 7.0 |
| lookup | 68.0 | 68.5 | 68.5 |
| equation | 68.0 | 68.5 | 68.5 |
| equation_n30 | 68.0 | 68.5 | 68.5 |
| equation_n100 | 68.0 | 68.5 | 68.5 |
| gated_equation | 68.0 | 68.5 | 68.5 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
