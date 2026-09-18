# Table 1 -- bbh (ouro_2_6b_base)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 197932 layer passes over 2337 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 82.6 |
| default_at_budget | 81.0 (10%) | 90.4 (10%) | 65.8 (85%) |
| lookup | 43.4 (85%) | 56.2 | 77.3 |
| equation | 41.9 (85%) | 57.7 | 77.3 |
| equation_n30 | 41.9 (85%) | 57.6 | 77.3 |
| equation_n100 | 41.9 (85%) | 57.7 | 77.3 |
| gated_equation | 41.9 (85%) | 57.7 | 77.3 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
