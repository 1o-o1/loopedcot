# Table 1 -- math500 (ouro_2_6b_base), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 338737 layer passes over 400 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 56.0 |
| default_cell | n/a | n/a | 72.4 (68%) | 65.0 (84%) |
| default_at_budget | n/a | n/a | 53.3 (98%) | 55.9 (100%) |
| lookup | 31.3 (100%) | 52.2 | 53.8 | 53.5 |
| equation | 33.6 (100%) | 52.0 | 56.8 | 57.0 |
| equation_n30 | 33.6 (100%) | 51.2 | 53.2 | 53.2 |
| equation_n100 | 33.6 (100%) | 52.0 | 56.8 | 57.0 |
| gated_equation | 33.6 (100%) | 52.0 | 56.8 | 57.0 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
