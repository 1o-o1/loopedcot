# Table 1 -- gsm8k (ouro_1_4b_base)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 77130 layer passes over 1219 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 76.9 |
| default_at_budget | n/a | n/a | 61.6 |
| lookup | 20.3 | 50.8 | 73.3 |
| equation | 20.3 | 50.8 | 73.3 |
| equation_n30 | 20.3 | 49.9 | 73.3 |
| equation_n100 | 20.3 | 50.8 | 73.3 |
| gated_equation | 20.3 | 50.8 | 73.3 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
