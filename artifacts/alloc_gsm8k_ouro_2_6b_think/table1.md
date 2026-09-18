# Table 1 -- gsm8k (ouro_2_6b_think)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 237574 layer passes over 1219 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 21.7 |
| default_at_budget | n/a | n/a | 24.6 |
| lookup | 57.3 | 63.1 | 65.1 |
| equation | 57.3 | 63.1 | 64.8 |
| equation_n30 | 57.3 | 63.1 | 64.8 |
| equation_n100 | 57.3 | 63.1 | 64.8 |
| gated_equation | 57.3 | 63.1 | 64.8 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
