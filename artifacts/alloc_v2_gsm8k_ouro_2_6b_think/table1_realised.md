# Table 1 -- gsm8k (ouro_2_6b_think), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 237574 layer passes over 1219 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 21.7 |
| default_cell | n/a | n/a | 8.9 (11%) | 16.9 (74%) |
| default_at_budget | n/a | n/a | 16.6 | 24.1 |
| lookup | 57.4 | 63.5 | 65.1 | 65.1 |
| equation | 57.4 | 63.5 | 65.1 | 64.8 |
| equation_n30 | 57.4 | 63.5 | 65.1 | 64.8 |
| equation_n100 | 57.4 | 63.5 | 65.1 | 64.8 |
| gated_equation | 57.4 | 63.5 | 65.1 | 64.8 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
