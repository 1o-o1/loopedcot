# Table 1 -- mmlu (ouro_1_4b_think)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 134109 layer passes over 1900 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 73.7 |
| default_at_budget | n/a | 65.3 (95%) | 70.7 |
| lookup | 58.4 | 64.7 | 72.5 |
| equation | 56.9 | 65.4 | 70.7 |
| equation_n30 | 56.3 | 65.4 | 72.6 |
| equation_n100 | 56.9 | 65.4 | 70.7 |
| gated_equation | 56.9 | 64.8 | 70.7 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
