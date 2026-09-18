# Table 1 -- strategyqa (ouro_1_4b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 109309 layer passes over 2190 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 72.5 |
| default_cell | n/a | n/a | n/a | 72.5 |
| default_at_budget | n/a | 69.5 | 72.2 | 72.5 |
| lookup | 61.0 | 69.5 | 69.5 | 69.5 |
| equation | 61.0 | 69.4 | 71.2 | 71.2 |
| equation_n30 | 61.0 | 69.4 | 71.2 | 71.2 |
| equation_n100 | 61.0 | 69.4 | 71.2 | 71.2 |
| gated_equation | 61.0 | 69.5 | 71.2 | 72.5 |
| avg_lookup | 62.3 | 69.5 | 69.5 | 69.5 |
| avg_equation | 61.3 | 70.7 | 71.2 | 71.2 |
| avg_gated_lookup | 61.0 | 69.5 | 69.5 | 72.5 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 25330 vs 27327 (-7.3%) | 49399 vs 54655 (-9.6%) | 49399 vs 81982 (-39.7%) | 49399 vs 109309 (-54.8%) |
| avg_equation | 26098 vs 27327 (-4.5%) | 52772 vs 54655 (-3.4%) | 71784 vs 81982 (-12.4%) | 71784 vs 109309 (-34.3%) |
| avg_gated_lookup | 25072 vs 27327 (-8.3%) | 49399 vs 54655 (-9.6%) | 49399 vs 81982 (-39.7%) | 107291 vs 109309 (-1.8%) |
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 69.5 points at 45.2% of the default cost, 9.6% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 69.5 points at 45.2% of the default cost, 39.7% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 69.5 points at 45.2% of the default cost, 54.8% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 71.2 points at 65.7% of the default cost, 12.4% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 71.2 points at 65.7% of the default cost, 34.3% under the budget it was given.
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 69.5 points at 45.2% of the default cost, 9.6% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 69.5 points at 45.2% of the default cost, 39.7% under the budget it was given.
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin +0.0 points, sd 9.5, bar 0.50 sd (30 verification questions, the ids after the 50 that fit, out of 100 calibration); cost saving 1.8% of the budget, 98.2% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
