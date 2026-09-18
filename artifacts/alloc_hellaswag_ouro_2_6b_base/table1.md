# Table 1 -- hellaswag (ouro_2_6b_base)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 170694 layer passes over 1900 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 76.4 |
| default_at_budget | n/a | n/a | 76.4 (100%) |
| lookup | 32.1 (100%) | 66.4 | 81.8 |
| equation | 34.4 (100%) | 58.7 | 76.5 |
| equation_n30 | 34.4 (100%) | 58.7 | 76.5 |
| equation_n100 | 34.4 (100%) | 58.7 | 76.5 |
| gated_equation | 34.4 (100%) | 58.7 | 76.5 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
