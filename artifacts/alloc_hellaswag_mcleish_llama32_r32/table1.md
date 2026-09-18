# Table 1 -- hellaswag (mcleish_llama32_r32)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 45831 layer passes over 1900 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 28.9 |
| default_at_budget | n/a | n/a | 29.0 (99%) |
| lookup | 24.8 (99%) | 30.9 | 28.6 |
| equation | 24.8 (99%) | 26.3 | 28.9 |
| equation_n30 | 25.3 (99%) | 27.6 | 28.9 |
| equation_n100 | 24.8 (99%) | 26.3 | 28.9 |
| gated_equation | 24.8 (99%) | 26.3 | 28.9 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
