# Table 1 -- aqua (mcleish_llama32_r32)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 41537 layer passes over 154 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 53.2 |
| default_at_budget | n/a | n/a | 53.9 |
| lookup | 23.4 | 43.5 | 53.2 |
| equation | 24.0 | 42.9 | 55.8 |
| equation_n30 | 24.0 | 42.9 | 55.8 |
| equation_n100 | 24.0 | 42.9 | 55.8 |
| gated_equation | 24.0 | 42.9 | 55.8 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
