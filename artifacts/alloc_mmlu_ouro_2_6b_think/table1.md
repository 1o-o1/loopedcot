# Table 1 -- mmlu (ouro_2_6b_think)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 242015 layer passes over 1900 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 80.1 |
| default_at_budget | n/a | 75.2 (90%) | 78.7 |
| lookup | 65.9 | 73.9 | 80.6 |
| equation | 45.8 | 75.3 | 80.6 |
| equation_n30 | 45.8 | 75.3 | 80.6 |
| equation_n100 | 45.8 | 75.3 | 80.6 |
| gated_equation | 45.8 | 75.4 | 80.6 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
