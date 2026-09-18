# Table 1 -- bbh (mcleish_llama32_r32), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 69981 layer passes over 2337 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 43.5 |
| default_cell | n/a | n/a | 49.2 (10%) | 55.9 (46%) |
| default_at_budget | 49.2 (10%) | 57.5 (31%) | 44.1 (72%) | 43.4 (99%) |
| lookup | 34.4 (99%) | 37.7 | 40.2 | 40.0 |
| equation | 33.8 (99%) | 37.3 | 40.9 | 43.4 |
| equation_n30 | 33.3 (99%) | 42.1 | 43.4 | 43.4 |
| equation_n100 | 33.8 (99%) | 37.3 | 40.9 | 43.4 |
| gated_equation | 33.7 (99%) | 37.4 | 40.9 | 43.4 |
| avg_lookup | 36.3 | 40.3 | 40.1 | 40.1 |
| avg_equation | 36.5 | 40.2 | 43.5 | 43.5 |
| avg_gated_lookup | 36.3 | 40.3 | 40.1 | 43.5 |

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 18026 vs 17495 (+3.0%) | 35010 vs 34990 (+0.1%) | 47666 vs 52485 (-9.2%) | 47666 vs 69981 (-31.9%) |
| avg_equation | 17333 vs 17495 (-0.9%) | 34984 vs 34990 (-0.0%) | 52080 vs 52485 (-0.8%) | 66969 vs 69981 (-4.3%) |
| avg_gated_lookup | 18026 vs 17495 (+3.0%) | 35010 vs 34990 (+0.1%) | 47666 vs 52485 (-9.2%) | 66969 vs 69981 (-4.3%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 40.1 points at 68.1% of the default cost, 9.2% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 40.1 points at 68.1% of the default cost, 31.9% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 43.5 points at 95.7% of the default cost, 4.3% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 40.1 points at 68.1% of the default cost, 9.2% under the budget it was given.
- `avg_gated_lookup` reverted to the default cell for every question at 1.00x: the predicted calibration margin did not clear 0.50 of its own SD.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
