# Table 1 -- gsm8k (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 77105 layer passes over 1056 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 76.7 | +0.1 |
| default_cell | n/a | n/a | n/a | 81.6 (71%) | -4.8 |
| default_at_budget | n/a | n/a | n/a | 73.0 | +3.8 |
| lookup | 22.1 | 62.2 | 72.0 | 76.4 | +0.4 |
| equation | 22.2 | 62.2 | 72.2 | 76.4 | +0.4 |
| equation_n30 | 22.2 | 61.9 | 71.1 | 76.4 | +0.4 |
| equation_n100 | 22.2 | 62.2 | 72.2 | 76.2 | +0.6 |
| gated_equation | 22.2 | 62.2 | 72.2 | 76.4 | +0.4 |
| avg_lookup | 23.7 | 65.4 | 74.1 | 76.7 | +0.1 |
| avg_equation | 24.3 | 65.4 | 74.3 | 76.7 | +0.1 |
| avg_gated_lookup | 24.2 | 65.4 | 74.1 | 76.7 | +0.1 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 1024, 76.8 points over 1056 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 19482 vs 19276 (+1.1%) | 38596 vs 38552 (+0.1%) | 57997 vs 57829 (+0.3%) | 75002 vs 77105 (-2.7%) |
| avg_equation | 19615 vs 19276 (+1.8%) | 38596 vs 38552 (+0.1%) | 58078 vs 57829 (+0.4%) | 76310 vs 77105 (-1.0%) |
| avg_gated_lookup | 19794 vs 19276 (+2.7%) | 38596 vs 38552 (+0.1%) | 57997 vs 57829 (+0.3%) | 76310 vs 77105 (-1.0%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 76.7 points at 97.3% of the default cost, 2.7% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 76.7 points at 99.0% of the default cost, 1.0% under the budget it was given.
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 1.0% of the budget, 99.0% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
