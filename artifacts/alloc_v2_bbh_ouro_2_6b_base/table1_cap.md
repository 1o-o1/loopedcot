# Table 1 -- bbh (ouro_2_6b_base), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 197932 layer passes over 2337 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 82.6 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | 81.0 (10%) | 90.4 (10%) | 86.9 (26%) | 65.8 (85%) |
| lookup | 43.4 (85%) | 56.2 | 74.7 | 77.3 |
| equation | 41.9 (85%) | 57.7 | 74.7 | 77.3 |
| equation_n30 | 41.9 (85%) | 57.6 | 74.7 | 77.3 |
| equation_n100 | 41.9 (85%) | 57.7 | 74.7 | 77.3 |
| gated_equation | 41.9 (85%) | 57.7 | 74.7 | 77.3 |
| avg_lookup | 44.2 | 65.1 | 77.4 | 80.9 |
| avg_equation | 44.2 | 64.0 | 77.2 | 80.8 |
| avg_gated_lookup | 44.2 | 65.1 | 77.4 | 80.9 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 49247 vs 49483 (-0.5%) | 97386 vs 98966 (-1.6%) | 147789 vs 148449 (-0.4%) | 194993 vs 197932 (-1.5%) |
| avg_equation | 49247 vs 49483 (-0.5%) | 96638 vs 98966 (-2.4%) | 147271 vs 148449 (-0.8%) | 194709 vs 197932 (-1.6%) |
| avg_gated_lookup | 49247 vs 49483 (-0.5%) | 97386 vs 98966 (-1.6%) | 147789 vs 148449 (-0.4%) | 194993 vs 197932 (-1.5%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
