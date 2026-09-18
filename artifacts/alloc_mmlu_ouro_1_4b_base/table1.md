# Table 1 -- mmlu (ouro_1_4b_base)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 58295 layer passes over 1900 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 68.7 |
| default_at_budget | n/a | n/a | 70.1 (88%) |
| lookup | 41.3 (88%) | 56.2 | 67.3 |
| equation | 40.9 (88%) | 57.3 | 65.9 |
| equation_n30 | 40.9 (88%) | 57.3 | 66.1 |
| equation_n100 | 40.9 (88%) | 57.3 | 65.9 |
| gated_equation | 40.9 (88%) | 57.3 | 65.9 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
