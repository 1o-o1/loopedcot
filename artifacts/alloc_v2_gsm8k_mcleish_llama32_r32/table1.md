# Table 1 -- gsm8k (mcleish_llama32_r32), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 140290 layer passes over 1219 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 49.2 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | 6.7 (2%) | 44.5 |
| lookup | 45.4 | 48.4 | 47.9 | 47.9 |
| equation | 45.4 | 49.8 | 49.1 | 49.1 |
| equation_n30 | 45.4 | 49.9 | 49.1 | 49.1 |
| equation_n100 | 45.4 | 49.8 | 49.1 | 49.1 |
| gated_equation | 45.4 | 49.8 | 49.1 | 49.1 |
| avg_lookup | 48.0 | 48.2 | 48.0 | 48.4 |
| avg_equation | 48.0 | 49.6 | 49.4 | 49.5 |
| avg_gated_lookup | 48.0 | 48.2 | 48.0 | 48.4 |

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 34520 vs 35073 (-1.6%) | 68990 vs 70145 (-1.6%) | 88762 vs 105218 (-15.6%) | 133808 vs 140290 (-4.6%) |
| avg_equation | 34520 vs 35073 (-1.6%) | 69159 vs 70145 (-1.4%) | 114705 vs 105218 (+9.0%) | 144938 vs 140290 (+3.3%) |
| avg_gated_lookup | 34520 vs 35073 (-1.6%) | 68990 vs 70145 (-1.6%) | 88762 vs 105218 (-15.6%) | 133808 vs 140290 (-4.6%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
