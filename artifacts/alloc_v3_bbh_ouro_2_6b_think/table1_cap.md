# Table 1 -- bbh (ouro_2_6b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 322452 layer passes over 2337 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 91.1 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | 85.4 (10%) | 78.5 (40%) | 62.6 (97%) | 83.1 |
| lookup | 48.0 | 75.3 | 82.9 | 86.7 |
| equation | 47.5 | 75.3 | 82.3 | 84.2 |
| equation_n30 | 42.1 | 74.7 | 82.2 | 83.4 |
| equation_n100 | 47.5 | 75.3 | 82.3 | 84.2 |
| gated_equation | 48.3 | 75.3 | 82.8 | 82.8 |
| avg_lookup | 50.7 | 79.1 | 86.0 | 87.7 |
| avg_equation | 50.7 | 80.2 | 83.4 | 87.4 |
| avg_gated_lookup | 49.9 | 82.1 | 82.8 | 83.2 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 79984 vs 80613 (-0.8%) | 149268 vs 161226 (-7.4%) | 241504 vs 241839 (-0.1%) | 320323 vs 322452 (-0.7%) |
| avg_equation | 79984 vs 80613 (-0.8%) | 155325 vs 161226 (-3.7%) | 246584 vs 241839 (+2.0%) | 314174 vs 322452 (-2.6%) |
| avg_gated_lookup | 76820 vs 80613 (-4.7%) | 176252 vs 161226 (+9.3%) | 211633 vs 241839 (-12.5%) | 264315 vs 322452 (-18.0%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
