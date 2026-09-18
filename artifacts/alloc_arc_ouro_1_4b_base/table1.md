# Table 1 -- arc (ouro_1_4b_base)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 38812 layer passes over 1072 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 86.5 |
| default_at_budget | n/a | n/a | 86.6 (94%) |
| lookup | 42.9 (94%) | 75.4 | 86.0 |
| equation | 43.4 (94%) | 72.2 | 85.6 |
| equation_n30 | 43.4 (94%) | 72.2 | 84.9 |
| equation_n100 | 43.4 (94%) | 72.2 | 85.6 |
| gated_equation | 43.4 (94%) | 72.2 | 85.6 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
