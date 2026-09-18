# Table 1 -- strategyqa (ouro_2_6b_think)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 194662 layer passes over 2190 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 77.8 |
| default_at_budget | n/a | 74.6 | 78.0 |
| lookup | 59.5 | 74.9 | 74.9 |
| equation | 59.9 | 77.4 | 78.0 |
| equation_n30 | 59.9 | 77.4 | 78.0 |
| equation_n100 | 59.9 | 77.4 | 78.0 |
| gated_equation | 59.9 | 77.4 | 78.0 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
