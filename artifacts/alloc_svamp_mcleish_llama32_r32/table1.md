# Table 1 -- svamp (mcleish_llama32_r32)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 32123 layer passes over 200 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 69.0 |
| default_at_budget | n/a | n/a | 50.0 |
| lookup | 22.5 | 33.0 | 62.0 |
| equation | 22.5 | 39.0 | 63.0 |
| equation_n30 | 22.5 | 39.0 | 63.0 |
| equation_n100 | 22.5 | 39.0 | 63.0 |
| gated_equation | 22.5 | 39.0 | 63.0 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
