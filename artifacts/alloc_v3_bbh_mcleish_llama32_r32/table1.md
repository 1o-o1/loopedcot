# Table 1 -- bbh (mcleish_llama32_r32), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 69981 layer passes over 2337 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 43.5 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | 49.2 (10%) | 54.6 (31%) | 43.2 (72%) | 43.7 (99%) |
| lookup | 34.5 (99%) | 36.5 | 39.7 | 40.0 |
| equation | 34.6 (99%) | 37.6 | 42.8 | 43.7 |
| equation_n30 | 33.4 (99%) | 38.1 | 42.8 | 43.8 |
| equation_n100 | 34.6 (99%) | 37.6 | 42.8 | 43.7 |
| gated_equation | 34.4 (99%) | 38.1 | 42.9 | 43.8 |
| avg_lookup | 35.6 | 37.9 | 40.1 | 40.1 |
| avg_equation | 35.9 | 39.6 | 44.3 | 43.6 |
| avg_gated_lookup | 31.9 | 35.6 | 34.6 | 34.6 |

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 17462 vs 17495 (-0.2%) | 34688 vs 34990 (-0.9%) | 49535 vs 52485 (-5.6%) | 49535 vs 69981 (-29.2%) |
| avg_equation | 16983 vs 17495 (-2.9%) | 35970 vs 34990 (+2.8%) | 51285 vs 52485 (-2.3%) | 69800 vs 69981 (-0.3%) |
| avg_gated_lookup | 17209 vs 17495 (-1.6%) | 31449 vs 34990 (-10.1%) | 45951 vs 52485 (-12.5%) | 45951 vs 69981 (-34.3%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 40.1 points at 70.8% of the default cost, 5.6% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 40.1 points at 70.8% of the default cost, 29.2% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 34.6 points at 65.7% of the default cost, 12.5% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 34.6 points at 65.7% of the default cost, 34.3% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
