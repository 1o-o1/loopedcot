# Table 1 -- math500 (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 178329 layer passes over 400 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 63.5 | +2.5 |
| default_cell | n/a | n/a | n/a | 67.5 (92%) | -1.5 |
| default_at_budget | n/a | n/a | 56.3 (99%) | 63.9 (100%) | +2.1 |
| lookup | 24.1 (100%) | 64.8 | 65.8 | 65.5 | +0.5 |
| equation | 25.6 (100%) | 64.2 | 66.2 | 66.0 | +0.0 |
| equation_n30 | 25.6 (100%) | 64.2 | 66.0 | 66.0 | +0.0 |
| equation_n100 | 25.6 (100%) | 64.2 | 66.2 | 66.0 | +0.0 |
| gated_equation | 25.6 (100%) | 64.2 | 66.2 (100%) | 63.5 | +2.5 |
| avg_lookup | 30.2 | 66.2 | 65.5 | 65.5 | +0.5 |
| avg_equation | 29.5 | 64.5 | 66.0 | 66.0 | +0.0 |
| avg_gated_lookup | 29.2 | 66.2 | 65.5 | 63.5 | +2.5 |

The ORACLE GAP is the best single evaluation cell (depth 3 at cap 4096, 66.0 points over 400 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 43608 vs 44582 (-2.2%) | 88144 vs 89164 (-1.1%) | 109654 vs 133746 (-18.0%) | 109654 vs 178329 (-38.5%) |
| avg_equation | 44948 vs 44582 (+0.8%) | 89988 vs 89164 (+0.9%) | 132753 vs 133746 (-0.7%) | 132753 vs 178329 (-25.6%) |
| avg_gated_lookup | 42499 vs 44582 (-4.7%) | 87700 vs 89164 (-1.6%) | 109654 vs 133746 (-18.0%) | 167182 vs 178329 (-6.3%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 65.5 points at 61.5% of the default cost, 18.0% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 65.5 points at 61.5% of the default cost, 38.5% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 66.0 points at 74.4% of the default cost, 25.6% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 65.5 points at 61.5% of the default cost, 18.0% under the budget it was given.
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin -3.3 points, sd 10.1, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 6.3% of the budget, 93.7% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
