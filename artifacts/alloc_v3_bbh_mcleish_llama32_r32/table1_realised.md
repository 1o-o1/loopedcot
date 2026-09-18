# Table 1 -- bbh (mcleish_llama32_r32), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 69981 layer passes over 2337 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 43.5 |
| default_cell | 49.2 (10%) | 53.9 (16%) | 57.0 (45%) | 47.3 (88%) |
| default_at_budget | 49.2 (10%) | 55.4 (31%) | 43.5 (72%) | 43.5 (99%) |
| lookup | 33.8 (99%) | 37.8 | 39.9 | 40.0 |
| equation | 34.1 (99%) | 38.9 | 41.2 | 43.4 |
| equation_n30 | 34.0 (99%) | 39.2 | 43.0 | 43.6 |
| equation_n100 | 34.1 (99%) | 38.9 | 41.2 | 43.4 |
| gated_equation | 34.0 (99%) | 39.4 | 43.1 | 43.6 |

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
