# Table 1 -- aqua (ouro_2_6b_base)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 158694 layer passes over 154 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 73.4 |
| default_at_budget | n/a | n/a | 72.1 |
| lookup | 40.3 | 66.2 | 68.2 |
| equation | 50.6 | 66.2 | 66.9 |
| equation_n30 | 37.7 | 66.2 | 72.1 |
| equation_n100 | 50.6 | 66.2 | 66.9 |
| gated_equation | 50.6 | 66.2 | 69.5 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
