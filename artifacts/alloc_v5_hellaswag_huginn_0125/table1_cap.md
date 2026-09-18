# Table 1 -- hellaswag (huginn_0125), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 116818 layer passes over 1700 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 34.0 | +5.6 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | 59.0 (11%) | 34.6 (99%) | +5.0 |
| lookup | 24.2 | 38.2 | 38.7 | 39.6 | +0.0 |
| equation | 24.2 | 38.2 | 38.6 | 38.6 | +1.0 |
| equation_n30 | 24.8 | 38.6 | 38.7 | 39.6 | +0.0 |
| equation_n100 | 23.5 | 38.4 | 38.6 | 38.6 | +1.0 |
| gated_equation | 24.5 | 38.6 | 38.7 | 34.4 | +5.2 |
| avg_lookup | 32.9 | 38.8 | 39.2 | 39.6 | +0.0 |
| avg_equation | 32.9 | 38.6 | 38.6 | 38.6 | +1.0 |
| avg_gated_lookup | 32.9 | 38.8 | 39.2 | 39.6 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 32 at cap 0, 39.6 points over 1700 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none.

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 27478 vs 29204 (-5.9%) | 57752 vs 58409 (-1.1%) | 86653 vs 87613 (-1.1%) | 102451 vs 116818 (-12.3%) |
| avg_equation | 27478 vs 29204 (-5.9%) | 52778 vs 58409 (-9.6%) | 52778 vs 87613 (-39.8%) | 52778 vs 116818 (-54.8%) |
| avg_gated_lookup | 27478 vs 29204 (-5.9%) | 57752 vs 58409 (-1.1%) | 86653 vs 87613 (-1.1%) | 102451 vs 116818 (-12.3%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 39.6 points at 87.7% of the default cost, 12.3% under the budget it was given.
- `avg_equation` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 38.6 points at 45.2% of the default cost, 9.6% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 38.6 points at 45.2% of the default cost, 39.8% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 38.6 points at 45.2% of the default cost, 54.8% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 39.6 points at 87.7% of the default cost, 12.3% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
