# Table 1 -- csqa (mcleish_llama32_r32)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 35104 layer passes over 1121 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 38.1 |
| default_at_budget | n/a | n/a | 39.9 (100%) |
| lookup | 21.4 (100%) | 30.0 | 42.2 |
| equation | 21.4 (100%) | 32.7 | 42.2 |
| equation_n30 | 21.4 (100%) | 28.0 | 42.2 |
| equation_n100 | 21.4 (100%) | 32.7 | 42.2 |
| gated_equation | 21.4 (100%) | 32.7 | 42.2 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
