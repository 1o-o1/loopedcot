# Table 1 -- mmlu (ouro_2_6b_think), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 242015 layer passes over 1900 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 80.1 |
| default_cell | n/a | 95.8 (1%) | 90.4 (47%) | 86.8 (75%) |
| default_at_budget | n/a | 75.2 (90%) | 75.3 | 78.8 |
| lookup | 65.9 | 74.5 | 78.1 | 80.8 |
| equation | 45.9 | 75.5 | 78.0 | 80.8 |
| equation_n30 | 45.9 | 75.6 | 78.0 | 80.8 |
| equation_n100 | 45.9 | 75.5 | 78.0 | 80.8 |
| gated_equation | 45.9 | 75.7 | 78.0 | 81.1 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
