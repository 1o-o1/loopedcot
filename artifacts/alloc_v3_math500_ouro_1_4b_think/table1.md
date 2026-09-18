# Table 1 -- math500 (ouro_1_4b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 278580 layer passes over 400 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 89.8 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 36.9 (99%) | 75.2 | 75.5 |
| lookup | 32.0 | 66.8 | 76.8 | 84.2 |
| equation | 32.0 | 66.8 | 76.8 | 77.2 |
| equation_n30 | 32.0 | 66.8 | 76.8 | 77.0 |
| equation_n100 | 32.0 | 66.8 | 76.8 | 77.2 |
| gated_equation | 32.0 | 66.8 | 76.8 | 77.0 |
| avg_lookup | 51.0 | 75.0 | 77.5 | 79.8 |
| avg_equation | 50.2 | 75.2 | 77.2 | 77.2 |
| avg_gated_lookup | 50.2 | 74.5 | 78.5 | 81.0 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 68404 vs 69645 (-1.8%) | 139382 vs 139290 (+0.1%) | 200264 vs 208935 (-4.2%) | 284214 vs 278580 (+2.0%) |
| avg_equation | 68097 vs 69645 (-2.2%) | 136556 vs 139290 (-2.0%) | 212373 vs 208935 (+1.6%) | 282157 vs 278580 (+1.3%) |
| avg_gated_lookup | 68643 vs 69645 (-1.4%) | 139628 vs 139290 (+0.2%) | 218685 vs 208935 (+4.7%) | 273867 vs 278580 (-1.7%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
