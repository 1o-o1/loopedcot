# Table 1 -- gsm8k (ouro_2_6b_base)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 151460 layer passes over 1219 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 82.7 |
| default_at_budget | n/a | n/a | 63.7 |
| lookup | 23.4 | 52.7 | 78.4 |
| equation | 23.5 | 52.8 | 78.4 |
| equation_n30 | 23.5 | 52.8 | 78.4 |
| equation_n100 | 23.5 | 52.8 | 78.4 |
| gated_equation | 23.5 | 52.8 | 78.4 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
