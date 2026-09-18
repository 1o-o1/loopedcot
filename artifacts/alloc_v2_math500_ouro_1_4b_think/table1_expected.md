# Table 1 -- math500 (ouro_1_4b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 278580 layer passes over 400 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 89.8 |
| default_cell | n/a | n/a | n/a | 92.2 (90%) |
| default_at_budget | n/a | 36.9 (99%) | 75.8 | 88.0 |
| lookup | 32.2 | 76.8 | 86.2 | 89.8 |
| equation | 32.2 | 76.8 | 85.5 | 89.8 |
| equation_n30 | 32.2 | 76.8 | 77.0 | 77.0 |
| equation_n100 | 32.2 | 76.8 | 85.5 | 89.8 |
| gated_equation | 32.2 | 76.8 | 85.5 | 89.8 |
| avg_lookup | 58.8 | 77.5 | 87.2 | 89.8 |
| avg_equation | 59.0 | 76.8 | 80.5 | 89.8 |
| avg_gated_lookup | 58.8 | 77.5 | 87.2 | 89.8 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 72388 vs 69645 (+3.9%) | 135279 vs 139290 (-2.9%) | 210098 vs 208935 (+0.6%) | 270654 vs 278580 (-2.8%) |
| avg_equation | 71867 vs 69645 (+3.2%) | 139407 vs 139290 (+0.1%) | 212413 vs 208935 (+1.7%) | 270654 vs 278580 (-2.8%) |
| avg_gated_lookup | 72388 vs 69645 (+3.9%) | 135279 vs 139290 (-2.9%) | 210098 vs 208935 (+0.6%) | 270654 vs 278580 (-2.8%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 89.8 points at 97.2% of the default cost, 2.8% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 89.8 points at 97.2% of the default cost, 2.8% under the budget it was given.
- `avg_gated_lookup` reverted to the default cell for every question at 1.00x: the predicted calibration margin did not clear 0.50 of its own SD.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
