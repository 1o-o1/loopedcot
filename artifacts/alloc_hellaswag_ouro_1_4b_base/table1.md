# Table 1 -- hellaswag (ouro_1_4b_base)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 94300 layer passes over 1900 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 57.4 |
| default_at_budget | n/a | n/a | 57.4 |
| lookup | 34.7 | 56.9 | 65.4 |
| equation | 31.6 | 46.8 | 57.4 |
| equation_n30 | 31.6 | 46.8 | 56.1 |
| equation_n100 | 31.6 | 46.8 | 57.4 |
| gated_equation | 31.6 | 46.8 | 57.4 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
