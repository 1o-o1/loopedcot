# Table 1 -- mmlu (mcleish_llama32_r32)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 40492 layer passes over 1900 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 37.3 |
| default_at_budget | n/a | n/a | 38.1 (98%) |
| lookup | 26.8 (98%) | 36.6 | 36.7 |
| equation | 28.2 (98%) | 36.9 | 37.1 |
| equation_n30 | 31.8 (98%) | 36.4 | 37.1 |
| equation_n100 | 28.2 (98%) | 36.9 | 37.1 |
| gated_equation | 28.2 (98%) | 36.9 | 37.1 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
