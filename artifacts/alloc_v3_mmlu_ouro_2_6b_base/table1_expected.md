# Table 1 -- mmlu (ouro_2_6b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 118165 layer passes over 1900 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 74.6 |
| default_cell | n/a | n/a | n/a | 76.9 (82%) |
| default_at_budget | n/a | n/a | 79.9 (42%) | 76.4 (90%) |
| lookup | 52.3 (90%) | 65.9 | 73.2 | 74.8 |
| equation | 51.7 (90%) | 65.9 | 72.5 | 74.3 |
| equation_n30 | 51.7 (90%) | 65.9 | 68.5 | 73.4 |
| equation_n100 | 51.7 (90%) | 65.9 | 72.5 | 74.3 |
| gated_equation | 51.7 (90%) | 65.8 | 70.3 | 74.5 |
| avg_lookup | 55.7 | 69.3 | 73.2 | 74.6 |
| avg_equation | 54.8 | 68.2 | 72.3 | 74.6 |
| avg_gated_lookup | 52.9 | 68.5 | 72.6 | 74.6 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 28196 vs 29541 (-4.6%) | 58548 vs 59082 (-0.9%) | 87557 vs 88623 (-1.2%) | 107117 vs 118165 (-9.3%) |
| avg_equation | 28336 vs 29541 (-4.1%) | 58279 vs 59082 (-1.4%) | 87448 vs 88623 (-1.3%) | 107117 vs 118165 (-9.3%) |
| avg_gated_lookup | 29754 vs 29541 (+0.7%) | 58800 vs 59082 (-0.5%) | 88994 vs 88623 (+0.4%) | 107117 vs 118165 (-9.3%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 74.6 points at 90.7% of the default cost, 9.3% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 74.6 points at 90.7% of the default cost, 9.3% under the budget it was given.
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 50 that fit, out of 100 calibration); cost saving 9.3% of the budget, 90.7% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
