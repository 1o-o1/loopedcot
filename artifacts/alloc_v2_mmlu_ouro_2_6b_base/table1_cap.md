# Table 1 -- mmlu (ouro_2_6b_base), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 118165 layer passes over 1900 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 74.6 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | 80.1 (42%) | 76.1 (90%) |
| lookup | 53.2 (90%) | 65.9 | 73.2 | 74.2 |
| equation | 51.9 (90%) | 64.9 | 70.7 | 73.8 |
| equation_n30 | 51.9 (90%) | 64.9 | 67.9 | 73.2 |
| equation_n100 | 51.9 (90%) | 64.9 | 70.7 | 73.8 |
| gated_equation | 51.9 (90%) | 64.9 | 71.0 | 74.0 |
| avg_lookup | 55.7 | 69.3 | 74.2 | 74.8 |
| avg_equation | 54.7 | 67.1 | 71.4 | 74.8 |
| avg_gated_lookup | 55.7 | 69.3 | 74.2 | 74.8 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 28196 vs 29541 (-4.6%) | 58548 vs 59082 (-0.9%) | 89094 vs 88623 (+0.5%) | 116774 vs 118165 (-1.2%) |
| avg_equation | 28456 vs 29541 (-3.7%) | 58993 vs 59082 (-0.2%) | 88079 vs 88623 (-0.6%) | 116392 vs 118165 (-1.5%) |
| avg_gated_lookup | 28196 vs 29541 (-4.6%) | 58548 vs 59082 (-0.9%) | 89094 vs 88623 (+0.5%) | 116774 vs 118165 (-1.2%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
