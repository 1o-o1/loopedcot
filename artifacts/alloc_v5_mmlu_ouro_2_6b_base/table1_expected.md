# Table 1 -- mmlu (ouro_2_6b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 119579 layer passes over 1700 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 74.7 | +0.1 |
| default_cell | n/a | n/a | 100.0 (0%) | 76.8 (82%) | -1.9 |
| default_at_budget | n/a | n/a | 79.2 (46%) | 76.4 (90%) | -1.6 |
| lookup | 54.2 (90%) | 66.3 | 73.1 | 74.0 | +0.8 |
| equation | 52.1 (90%) | 65.9 | 72.4 | 74.1 | +0.8 |
| equation_n30 | 54.2 (90%) | 66.5 | 72.4 | 74.1 | +0.8 |
| equation_n100 | 52.1 (90%) | 65.9 | 72.4 | 74.1 | +0.7 |
| gated_equation | 52.1 (90%) | 65.9 | 80.2 (46%) | 75.4 (90%) | -0.6 |
| avg_lookup | 56.5 | 69.4 | 73.8 | 74.5 | +0.4 |
| avg_equation | 52.0 | 68.3 | 73.6 | 74.7 | +0.1 |
| avg_gated_lookup | 57.2 | 69.4 | 73.8 | 74.5 | +0.4 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 128, 74.8 points over 1700 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 29156 vs 29895 (-2.5%) | 59413 vs 59790 (-0.6%) | 89604 vs 89684 (-0.1%) | 95913 vs 119579 (-19.8%) |
| avg_equation | 29551 vs 29895 (-1.1%) | 59243 vs 59790 (-0.9%) | 90336 vs 89684 (+0.7%) | 107798 vs 119579 (-9.9%) |
| avg_gated_lookup | 30268 vs 29895 (+1.2%) | 59575 vs 59790 (-0.4%) | 89634 vs 89684 (-0.1%) | 95913 vs 119579 (-19.8%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 74.5 points at 80.2% of the default cost, 19.8% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 74.7 points at 90.1% of the default cost, 9.9% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 74.5 points at 80.2% of the default cost, 19.8% under the budget it was given.
- `avg_gated_lookup` at 1.00x: deviated from the default cell on family F0. Verification margin +2.2 points, sd 4.2, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 19.8% of the budget, 80.2% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
