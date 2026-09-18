# Table 1 -- aqua (ouro_2_6b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 158694 layer passes over 154 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 73.4 | +1.9 |
| default_cell | n/a | n/a | n/a | 73.4 | +1.9 |
| default_at_budget | n/a | n/a | 73.5 (22%) | 73.4 | +1.9 |
| lookup | 40.3 | 68.2 | 68.2 | 68.2 | +7.1 |
| equation | 50.6 | 65.6 | 66.2 | 66.2 | +9.1 |
| equation_n30 | 37.7 | 65.6 | 66.2 | 75.3 | +0.0 |
| equation_n100 | 50.6 | 65.6 | 66.2 | 66.2 | +9.1 |
| gated_equation | 37.7 | 65.6 | 66.2 | 73.4 | +1.9 |
| avg_lookup | 47.4 | 68.2 | 68.2 | 68.2 | +7.1 |
| avg_equation | 54.5 | 66.2 | 66.2 | 66.2 | +9.1 |
| avg_gated_lookup | 48.7 | 69.5 | 71.4 | 72.1 | +3.2 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 256, 75.3 points over 154 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F1, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 40712 vs 39674 (+2.6%) | 69931 vs 79347 (-11.9%) | 69931 vs 119021 (-41.2%) | 69931 vs 158694 (-55.9%) |
| avg_equation | 41923 vs 39674 (+5.7%) | 80006 vs 79347 (+0.8%) | 88368 vs 119021 (-25.8%) | 88368 vs 158694 (-44.3%) |
| avg_gated_lookup | 41720 vs 39674 (+5.2%) | 82512 vs 79347 (+4.0%) | 114151 vs 119021 (-4.1%) | 137161 vs 158694 (-13.6%) |
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 68.2 points at 44.1% of the default cost, 11.9% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 68.2 points at 44.1% of the default cost, 41.2% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.2 points at 44.1% of the default cost, 55.9% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 66.2 points at 55.7% of the default cost, 25.8% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 66.2 points at 55.7% of the default cost, 44.3% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 72.1 points at 86.4% of the default cost, 13.6% under the budget it was given.
- `avg_gated_lookup` at 1.00x: deviated from the default cell on family F1. Verification margin +3.3 points, sd 3.3, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 13.6% of the budget, 86.4% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
