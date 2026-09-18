# Table 1 -- csqa (ouro_1_4b_base)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 61952 layer passes over 1121 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 72.3 |
| default_at_budget | n/a | n/a | 72.1 |
| lookup | 30.4 | 65.6 | 73.1 |
| equation | 31.8 | 61.4 | 72.0 |
| equation_n30 | 32.3 | 61.4 | 73.1 |
| equation_n100 | 31.8 | 61.4 | 72.0 |
| gated_equation | 31.8 | 61.4 | 72.2 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
