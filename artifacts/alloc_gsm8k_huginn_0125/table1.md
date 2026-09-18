# Table 1 -- gsm8k (huginn_0125)

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 104580 layer passes over 1219 questions (0.0% of them counted at the horizon).

| arm | 0.25 x default | 0.50 x default | 1.00 x default |
|---|---|---|---|
| default | not feasible | not feasible | 26.3 |
| default_at_budget | n/a | n/a | 22.8 |
| lookup | 5.2 | 18.9 | 22.9 |
| equation | 5.3 | 18.8 | 21.3 |
| equation_n30 | 5.1 | 18.9 | 22.9 |
| equation_n100 | 5.3 | 18.8 | 21.3 |
| gated_equation | 5.3 | 18.8 | 22.9 |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
