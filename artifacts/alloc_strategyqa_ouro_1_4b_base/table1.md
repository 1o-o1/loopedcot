# Table 1 -- strategyqa (ouro_1_4b_base)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 58978 layer passes over 2190 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 66.3 |
| default_at_budget | n/a | n/a | 66.4 |
| lookup | 55.6 | 63.9 | 65.8 |
| equation | 53.9 | 66.8 | 66.4 |
| equation_n30 | 55.3 | 66.8 | 66.4 |
| equation_n100 | 53.9 | 66.8 | 66.4 |
| gated_equation | 53.9 | 66.8 | 66.4 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
