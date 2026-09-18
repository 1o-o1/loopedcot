# Table 1 -- gsm8k (ouro_1_4b_think)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 127112 layer passes over 1219 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 93.1 |
| default_at_budget | n/a | 25.7 (28%) | 88.7 |
| lookup | 31.7 | 80.6 | 91.1 |
| equation | 31.7 | 80.6 | 91.1 |
| equation_n30 | 31.7 | 80.6 | 91.1 |
| equation_n100 | 31.7 | 80.6 | 91.1 |
| gated_equation | 31.7 | 80.6 | 91.1 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
