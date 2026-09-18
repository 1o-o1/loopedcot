# Table 1 -- arc (ouro_2_6b_base)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 77503 layer passes over 1072 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 93.3 |
| default_at_budget | n/a | n/a | 93.0 (93%) |
| lookup | 63.0 (93%) | 86.6 | 88.1 |
| equation | 52.7 (93%) | 85.5 | 91.9 |
| equation_n30 | 52.7 (93%) | 85.9 | 92.4 |
| equation_n100 | 52.7 (93%) | 85.5 | 91.9 |
| gated_equation | 52.7 (93%) | 85.5 | 91.9 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
