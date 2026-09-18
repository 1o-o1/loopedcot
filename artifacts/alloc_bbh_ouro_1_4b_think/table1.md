# Table 1 -- bbh (ouro_1_4b_think)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 182991 layer passes over 2337 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 84.4 |
| default_at_budget | 66.2 (10%) | 52.8 (72%) | 81.3 |
| lookup | 35.1 | 64.4 | 81.3 |
| equation | 35.5 | 62.0 | 80.5 |
| equation_n30 | 35.5 | 62.0 | 80.5 |
| equation_n100 | 35.5 | 62.0 | 80.5 |
| gated_equation | 35.5 | 62.0 | 81.7 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
