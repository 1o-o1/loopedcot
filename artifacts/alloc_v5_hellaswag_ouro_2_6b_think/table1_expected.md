# Table 1 -- hellaswag (ouro_2_6b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 280620 layer passes over 1700 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 81.2 | +0.9 |
| default_cell | n/a | n/a | n/a | 76.8 (34%) | +5.3 |
| default_at_budget | n/a | 74.6 (30%) | 81.2 | 81.4 | +0.7 |
| lookup | 39.9 | 80.4 | 81.3 | 81.2 | +0.8 |
| equation | 39.9 | 74.4 | 78.9 | 78.9 | +3.1 |
| equation_n30 | 39.9 | 74.4 | 73.9 | 81.2 | +0.9 |
| equation_n100 | 39.9 | 74.4 | 73.9 | 80.7 | +1.4 |
| gated_equation | 39.9 | 74.9 | 80.7 | 81.4 | +0.7 |
| avg_lookup | 63.1 | 81.4 | 81.2 | 81.2 | +0.8 |
| avg_equation | 63.2 | 73.6 | 78.9 | 78.9 | +3.1 |
| avg_gated_lookup | 62.8 | 79.1 | 79.1 | 81.2 | +0.9 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 64, 82.1 points over 1700 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 69126 vs 70155 (-1.5%) | 137722 vs 140310 (-1.8%) | 199558 vs 210465 (-5.2%) | 199558 vs 280620 (-28.9%) |
| avg_equation | 69009 vs 70155 (-1.6%) | 141100 vs 140310 (+0.6%) | 196012 vs 210465 (-6.9%) | 196012 vs 280620 (-30.2%) |
| avg_gated_lookup | 68656 vs 70155 (-2.1%) | 112832 vs 140310 (-19.6%) | 112832 vs 210465 (-46.4%) | 281530 vs 280620 (+0.3%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 81.2 points at 71.1% of the default cost, 5.2% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 81.2 points at 71.1% of the default cost, 28.9% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 78.9 points at 69.8% of the default cost, 6.9% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 78.9 points at 69.8% of the default cost, 30.2% under the budget it was given.
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 79.1 points at 40.2% of the default cost, 19.6% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 79.1 points at 40.2% of the default cost, 46.4% under the budget it was given.
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin -3.3 points, sd 3.7, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving -0.3% of the budget, 100.3% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
