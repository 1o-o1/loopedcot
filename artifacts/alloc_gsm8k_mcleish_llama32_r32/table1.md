# Table 1 -- gsm8k (mcleish_llama32_r32)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 140290 layer passes over 1219 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 49.2 |
| default_at_budget | n/a | n/a | 44.5 |
| lookup | 45.4 | 48.4 | 47.9 |
| equation | 45.4 | 49.8 | 49.1 |
| equation_n30 | 45.4 | 49.9 | 49.1 |
| equation_n100 | 45.4 | 49.8 | 49.1 |
| gated_equation | 45.4 | 49.8 | 49.1 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
