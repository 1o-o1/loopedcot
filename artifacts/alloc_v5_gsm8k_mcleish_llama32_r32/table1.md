# Table 1 -- gsm8k (mcleish_llama32_r32), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 141339 layer passes over 1056 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 48.9 | +0.6 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | 8.8 (6%) | 45.5 | +3.9 |
| lookup | 45.6 | 49.4 | 49.4 | 49.4 | +0.0 |
| equation | 45.6 | 49.4 | 49.4 | 49.4 | +0.0 |
| equation_n30 | 45.6 | 49.6 | 48.9 | 48.9 | +0.6 |
| equation_n100 | 45.6 | 49.6 | 48.9 | 48.9 | +0.6 |
| gated_equation | 45.6 | 49.4 | 48.9 | 48.9 | +0.6 |
| avg_lookup | 47.5 | 49.3 | 49.7 | 50.1 | -0.7 |
| avg_equation | 48.2 | 49.4 | 49.4 | 49.4 | +0.0 |
| avg_gated_lookup | 47.3 | 49.4 | 49.4 | 49.4 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 8 at cap 256, 49.4 points over 1056 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2.

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 34871 vs 35335 (-1.3%) | 70980 vs 70670 (+0.4%) | 97332 vs 106005 (-8.2%) | 136498 vs 141339 (-3.4%) |
| avg_equation | 34501 vs 35335 (-2.4%) | 69548 vs 70670 (-1.6%) | 106773 vs 106005 (+0.7%) | 135608 vs 141339 (-4.1%) |
| avg_gated_lookup | 34442 vs 35335 (-2.5%) | 45519 vs 70670 (-35.6%) | 45519 vs 106005 (-57.1%) | 45519 vs 141339 (-67.8%) |
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 49.4 points at 32.2% of the default cost, 35.6% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 49.4 points at 32.2% of the default cost, 57.1% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 49.4 points at 32.2% of the default cost, 67.8% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
