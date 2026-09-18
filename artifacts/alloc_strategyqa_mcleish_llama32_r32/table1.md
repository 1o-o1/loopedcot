# Table 1 -- strategyqa (mcleish_llama32_r32)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 59637 layer passes over 2190 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 50.3 |
| default_at_budget | n/a | 50.9 | 51.0 |
| lookup | 52.3 | 52.3 | 52.3 |
| equation | 50.9 | 50.0 | 49.9 |
| equation_n30 | 50.9 | 50.0 | 49.9 |
| equation_n100 | 50.9 | 50.0 | 49.9 |
| gated_equation | 50.9 | 50.0 | 49.9 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
