# Table 1 -- bbh (ouro_2_6b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 197932 layer passes over 2337 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 82.6 |
| default_cell | n/a | 90.4 (10%) | 90.2 (21%) | 84.4 (53%) |
| default_at_budget | 81.0 (10%) | 90.4 (10%) | 87.1 (26%) | 70.0 (85%) |
| lookup | 43.4 (85%) | 56.5 | 79.6 | 81.0 |
| equation | 40.3 (85%) | 57.8 | 79.6 | 81.2 |
| equation_n30 | 40.3 (85%) | 57.8 | 79.6 | 81.2 |
| equation_n100 | 40.3 (85%) | 57.8 | 79.6 | 81.2 |
| gated_equation | 40.4 (85%) | 57.9 | 79.1 | 78.9 |
| avg_lookup | 44.1 | 74.3 | 81.3 | 81.3 |
| avg_equation | 44.1 | 74.3 | 81.4 | 81.4 |
| avg_gated_lookup | 44.0 | 66.5 | 67.8 | 82.6 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 49558 vs 49483 (+0.2%) | 97272 vs 98966 (-1.7%) | 143429 vs 148449 (-3.4%) | 143429 vs 197932 (-27.5%) |
| avg_equation | 49558 vs 49483 (+0.2%) | 97294 vs 98966 (-1.7%) | 143648 vs 148449 (-3.2%) | 143648 vs 197932 (-27.4%) |
| avg_gated_lookup | 48191 vs 49483 (-2.6%) | 106775 vs 98966 (+7.9%) | 133683 vs 148449 (-9.9%) | 190187 vs 197932 (-3.9%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 81.3 points at 72.5% of the default cost, 3.4% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 81.3 points at 72.5% of the default cost, 27.5% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 81.4 points at 72.6% of the default cost, 3.2% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 81.4 points at 72.6% of the default cost, 27.4% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 67.8 points at 67.5% of the default cost, 9.9% under the budget it was given.
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin -30.0 points, sd 8.5, bar 0.50 sd (30 verification questions, the ids after the 50 that fit, out of 100 calibration); cost saving 3.9% of the budget, 96.1% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
