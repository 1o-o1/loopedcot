# Table 1 -- arc (ouro_2_6b_think)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 161239 layer passes over 1072 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 96.5 |
| default_at_budget | n/a | 92.0 (91%) | 94.0 |
| lookup | 83.8 | 92.4 | 92.4 |
| equation | 74.3 | 91.9 | 96.3 |
| equation_n30 | 74.3 | 91.8 | 94.0 |
| equation_n100 | 74.3 | 91.9 | 96.3 |
| gated_equation | 74.3 | 91.9 | 96.3 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
