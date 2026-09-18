# Table 1 -- math500 (ouro_1_4b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 278580 layer passes over 400 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 89.8 | +0.0 |
| default_cell | n/a | n/a | n/a | 92.2 (90%) | -2.5 |
| default_at_budget | n/a | 36.9 (99%) | 75.8 | 88.0 | +1.8 |
| lookup | 32.2 | 76.8 | 86.2 | 89.8 | +0.0 |
| equation | 32.2 | 76.8 | 85.5 | 89.8 | +0.0 |
| equation_n30 | 32.2 | 76.8 | 77.0 | 77.0 | +12.8 |
| equation_n100 | 32.2 | 76.8 | 85.5 | 89.8 | +0.0 |
| gated_equation | 32.2 | 73.5 | 86.8 | 87.8 | +2.0 |
| avg_lookup | 58.8 | 77.5 | 87.2 | 89.8 | +0.0 |
| avg_equation | 59.0 | 76.8 | 80.5 | 89.8 | +0.0 |
| avg_gated_lookup | 50.7 | 77.5 | 87.2 | 89.8 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 4096, 89.8 points over 400 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 72388 vs 69645 (+3.9%) | 135279 vs 139290 (-2.9%) | 210098 vs 208935 (+0.6%) | 270654 vs 278580 (-2.8%) |
| avg_equation | 71867 vs 69645 (+3.2%) | 139407 vs 139290 (+0.1%) | 212413 vs 208935 (+1.7%) | 270654 vs 278580 (-2.8%) |
| avg_gated_lookup | 68953 vs 69645 (-1.0%) | 133540 vs 139290 (-4.1%) | 210964 vs 208935 (+1.0%) | 270654 vs 278580 (-2.8%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 89.8 points at 97.2% of the default cost, 2.8% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 89.8 points at 97.2% of the default cost, 2.8% under the budget it was given.
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 2.8% of the budget, 97.2% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
