# Table 1 -- math500 (ouro_2_6b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 563241 layer passes over 400 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 91.2 |
| default_cell | n/a | n/a | n/a | 92.8 (93%) |
| default_at_budget | n/a | 41.7 (99%) | 75.8 | 90.0 |
| lookup | 44.2 | 78.8 | 83.8 | 90.0 |
| equation | 44.2 | 78.8 | 87.8 | 91.5 |
| equation_n30 | 44.2 | 78.8 | 81.8 | 89.8 |
| equation_n100 | 44.2 | 78.8 | 87.8 | 91.5 |
| gated_equation | 44.2 | 78.8 | 87.8 | 91.5 |
| avg_lookup | 51.0 | 79.8 | 85.0 | 91.2 |
| avg_equation | 48.2 | 81.2 | 84.5 | 91.2 |
| avg_gated_lookup | 51.0 | 79.8 | 85.0 | 91.2 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 134887 vs 140810 (-4.2%) | 282470 vs 281621 (+0.3%) | 438666 vs 422431 (+3.8%) | 537649 vs 563241 (-4.5%) |
| avg_equation | 143080 vs 140810 (+1.6%) | 279695 vs 281621 (-0.7%) | 431373 vs 422431 (+2.1%) | 537649 vs 563241 (-4.5%) |
| avg_gated_lookup | 134887 vs 140810 (-4.2%) | 282470 vs 281621 (+0.3%) | 438666 vs 422431 (+3.8%) | 537649 vs 563241 (-4.5%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 91.2 points at 95.5% of the default cost, 4.5% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 91.2 points at 95.5% of the default cost, 4.5% under the budget it was given.
- `avg_gated_lookup` reverted to the default cell for every question at 1.00x: the predicted calibration margin did not clear 0.50 of its own SD.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
