# Table 1 -- hellaswag (ouro_2_6b_think)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 280144 layer passes over 1900 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 81.2 |
| default_at_budget | n/a | 74.9 (31%) | 81.4 |
| lookup | 40.5 | 80.8 | 79.8 |
| equation | 39.9 | 74.4 | 79.6 |
| equation_n30 | 39.9 | 74.1 | 74.1 |
| equation_n100 | 39.9 | 74.4 | 79.6 |
| gated_equation | 39.9 | 74.4 | 79.6 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
