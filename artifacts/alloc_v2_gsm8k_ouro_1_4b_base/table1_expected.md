# Table 1 -- gsm8k (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 77130 layer passes over 1219 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 76.9 |
| default_cell | n/a | n/a | n/a | 79.4 (86%) |
| default_at_budget | n/a | n/a | n/a | 73.3 |
| lookup | 22.1 | 61.9 | 71.7 | 76.8 |
| equation | 22.2 | 61.9 | 71.7 | 76.2 |
| equation_n30 | 22.2 | 61.6 | 70.7 | 73.7 |
| equation_n100 | 22.2 | 61.9 | 71.7 | 76.2 |
| gated_equation | 22.2 | 61.9 | 71.7 | 76.2 |
| avg_lookup | 24.0 | 64.9 | 70.1 | 76.9 |
| avg_equation | 24.0 | 65.2 | 73.7 | 76.9 |
| avg_gated_lookup | 24.0 | 64.9 | 70.1 | 76.9 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 19484 vs 19283 (+1.0%) | 38404 vs 38565 (-0.4%) | 57797 vs 57848 (-0.1%) | 74850 vs 77130 (-3.0%) |
| avg_equation | 19484 vs 19283 (+1.0%) | 38704 vs 38565 (+0.4%) | 57697 vs 57848 (-0.3%) | 74850 vs 77130 (-3.0%) |
| avg_gated_lookup | 19484 vs 19283 (+1.0%) | 38404 vs 38565 (-0.4%) | 57797 vs 57848 (-0.1%) | 74850 vs 77130 (-3.0%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 76.9 points at 97.0% of the default cost, 3.0% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 76.9 points at 97.0% of the default cost, 3.0% under the budget it was given.
- `avg_gated_lookup` reverted to the default cell for every question at 1.00x: the predicted calibration margin did not clear 0.50 of its own SD.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
