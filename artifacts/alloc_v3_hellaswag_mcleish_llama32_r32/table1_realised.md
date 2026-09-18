# Table 1 -- hellaswag (mcleish_llama32_r32), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 45831 layer passes over 1900 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 28.9 |
| default_cell | n/a | n/a | 50.0 (0%) | 29.6 (70%) |
| default_at_budget | n/a | n/a | 40.3 (16%) | 29.2 (99%) |
| lookup | 24.8 (99%) | 30.9 | 31.5 | 28.6 |
| equation | 24.8 (99%) | 26.3 | 27.2 | 29.2 |
| equation_n30 | 25.4 (99%) | 25.4 | 27.7 | 29.1 |
| equation_n100 | 24.8 (99%) | 26.3 | 27.2 | 29.2 |
| gated_equation | 24.8 (99%) | 27.4 | 28.1 | 29.1 |

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
