# Table 1 -- hellaswag (ouro_1_4b_think)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 145803 layer passes over 1900 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 74.5 |
| default_at_budget | n/a | 69.4 (33%) | 75.0 |
| lookup | 38.3 | 76.9 | 76.3 |
| equation | 37.8 | 69.5 | 71.9 |
| equation_n30 | 37.8 | 69.6 | 71.9 |
| equation_n100 | 37.8 | 69.5 | 71.9 |
| gated_equation | 37.8 | 69.5 | 75.0 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
