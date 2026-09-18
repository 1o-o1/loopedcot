# Table 1 -- bbh (mcleish_llama32_r32)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 69981 layer passes over 2337 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 43.5 |
| default_at_budget | 49.2 (10%) | 54.6 (31%) | 43.7 (99%) |
| lookup | 34.5 (99%) | 36.5 | 40.0 |
| equation | 34.6 (99%) | 37.6 | 43.7 |
| equation_n30 | 33.4 (99%) | 38.1 | 43.8 |
| equation_n100 | 34.6 (99%) | 37.6 | 43.7 |
| gated_equation | 34.6 (99%) | 37.6 | 43.7 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
