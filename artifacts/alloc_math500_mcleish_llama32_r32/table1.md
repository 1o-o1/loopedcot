# Table 1 -- math500 (mcleish_llama32_r32)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 96379 layer passes over 400 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 30.2 |
| default_at_budget | n/a | n/a | 30.0 |
| lookup | 23.2 | 32.0 | 28.7 |
| equation | 26.5 | 30.5 | 30.8 |
| equation_n30 | 26.5 | 30.5 | 30.0 |
| equation_n100 | 26.5 | 30.5 | 30.8 |
| gated_equation | 26.5 | 30.5 | 30.8 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
