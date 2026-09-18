# Table 1 -- mmlu (mcleish_llama32_r32), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 40492 layer passes over 1900 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 37.3 |
| default_cell | n/a | n/a | n/a | 39.4 (83%) |
| default_at_budget | n/a | n/a | 39.1 (86%) | 38.1 (98%) |
| lookup | 26.4 (98%) | 36.1 | 36.7 | 36.7 |
| equation | 28.2 (98%) | 36.8 | 36.8 | 36.6 |
| equation_n30 | 32.9 (98%) | 36.4 | 36.8 | 36.6 |
| equation_n100 | 28.2 (98%) | 36.8 | 36.8 | 36.6 |
| gated_equation | 28.2 (98%) | 36.8 | 36.8 | 36.6 |
| avg_lookup | 32.5 | 36.7 | 36.7 | 36.7 |
| avg_equation | 32.2 | 36.9 | 36.6 | 36.6 |
| avg_gated_lookup | 32.4 | 37.1 | 37.1 | 37.1 |

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 10018 vs 10123 (-1.0%) | 16424 vs 20246 (-18.9%) | 16424 vs 30369 (-45.9%) | 16424 vs 40492 (-59.4%) |
| avg_equation | 9951 vs 10123 (-1.7%) | 20235 vs 20246 (-0.1%) | 25026 vs 30369 (-17.6%) | 25026 vs 40492 (-38.2%) |
| avg_gated_lookup | 9706 vs 10123 (-4.1%) | 16119 vs 20246 (-20.4%) | 16119 vs 30369 (-46.9%) | 16119 vs 40492 (-60.2%) |
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 40.6% of the default cost, 18.9% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 40.6% of the default cost, 45.9% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 40.6% of the default cost, 59.4% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 36.6 points at 61.8% of the default cost, 17.6% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 36.6 points at 61.8% of the default cost, 38.2% under the budget it was given.
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 37.1 points at 39.8% of the default cost, 20.4% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 37.1 points at 39.8% of the default cost, 46.9% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 37.1 points at 39.8% of the default cost, 60.2% under the budget it was given.
- `avg_gated_lookup` at 1.00x: deviated from the default cell. Verification margin +13.3 points, sd 10.3, bar 0.50 sd (30 verification questions, the ids after the 50 that fit, out of 100 calibration); cost saving 60.2% of the budget, 39.8% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
