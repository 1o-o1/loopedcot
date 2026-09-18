# Table 1 -- mmlu (ouro_2_6b_base)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 118165 layer passes over 1900 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 74.6 |
| default_at_budget | n/a | n/a | 76.1 (90%) |
| lookup | 53.2 (90%) | 65.9 | 74.2 |
| equation | 51.9 (90%) | 64.9 | 73.8 |
| equation_n30 | 51.9 (90%) | 64.9 | 73.2 |
| equation_n100 | 51.9 (90%) | 64.9 | 73.8 |
| gated_equation | 51.9 (90%) | 64.9 | 74.0 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
