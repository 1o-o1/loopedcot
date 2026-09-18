# Table 1 -- arc (mcleish_llama32_r32)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 22554 layer passes over 1072 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 44.5 |
| default_at_budget | n/a | n/a | 43.7 (95%) |
| lookup | 24.1 (95%) | 38.0 | 42.8 |
| equation | 24.7 (95%) | 38.1 | 42.4 |
| equation_n30 | 22.5 (95%) | 38.0 | 42.4 |
| equation_n100 | 24.7 (95%) | 38.1 | 42.4 |
| gated_equation | 24.7 (95%) | 38.1 | 42.4 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
