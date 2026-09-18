# Table 1 -- bbh (ouro_2_6b_think)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 322452 layer passes over 2337 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 91.1 |
| default_at_budget | 85.4 (10%) | 78.5 (40%) | 83.1 |
| lookup | 48.0 | 75.3 | 86.7 |
| equation | 47.5 | 75.3 | 84.2 |
| equation_n30 | 42.1 | 74.7 | 83.4 |
| equation_n100 | 47.5 | 75.3 | 84.2 |
| gated_equation | 47.5 | 75.3 | 82.8 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
