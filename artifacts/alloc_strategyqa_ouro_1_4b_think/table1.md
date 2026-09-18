# Table 1 -- strategyqa (ouro_1_4b_think)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 109309 layer passes over 2190 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 72.5 |
| default_at_budget | n/a | 69.5 | 72.2 |
| lookup | 61.0 | 69.5 | 69.5 |
| equation | 61.0 | 69.4 | 71.1 |
| equation_n30 | 61.0 | 69.4 | 71.1 |
| equation_n100 | 61.0 | 69.4 | 71.1 |
| gated_equation | 61.0 | 69.4 | 71.1 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
