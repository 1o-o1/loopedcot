# Table 1 -- svamp (ouro_2_6b_base)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 131236 layer passes over 200 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 83.0 |
| default_at_budget | n/a | n/a | 56.5 |
| lookup | 26.5 | 51.5 | 82.5 |
| equation | 28.5 | 44.5 | 82.5 |
| equation_n30 | 28.5 | 52.0 | 82.0 |
| equation_n100 | 28.5 | 44.5 | 82.5 |
| gated_equation | 28.5 | 44.5 | 82.5 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
