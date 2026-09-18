# Table 1 -- gsm8k (huginn_0125), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 105638 layer passes over 1056 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 25.5 | +0.1 |
| default_cell | n/a | n/a | n/a | 25.6 (98%) | -0.1 |
| default_at_budget | n/a | n/a | 2.8 (24%) | 25.5 | +0.1 |
| lookup | 7.9 | 21.1 | 20.9 | 25.6 | +0.0 |
| equation | 8.1 | 21.0 | 20.8 | 25.5 | +0.1 |
| equation_n30 | 8.1 | 21.0 | 14.9 | 25.5 | +0.1 |
| equation_n100 | 8.1 | 21.0 | 20.8 | 25.5 | +0.1 |
| gated_equation | 8.1 | 21.0 | 20.8 | 25.5 | +0.1 |
| avg_lookup | 12.8 | 22.2 | 23.7 | 25.6 | +0.0 |
| avg_equation | 12.9 | 20.8 | 23.7 | 25.5 | +0.1 |
| avg_gated_lookup | 12.8 | 22.2 | 23.7 | 25.5 | +0.1 |

The ORACLE GAP is the best single evaluation cell (depth 32 at cap 256, 25.6 points over 1056 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3.

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 25134 vs 26410 (-4.8%) | 52601 vs 52819 (-0.4%) | 78966 vs 79229 (-0.3%) | 94848 vs 105638 (-10.2%) |
| avg_equation | 24959 vs 26410 (-5.5%) | 53520 vs 52819 (+1.3%) | 79458 vs 79229 (+0.3%) | 98118 vs 105638 (-7.1%) |
| avg_gated_lookup | 25134 vs 26410 (-4.8%) | 53401 vs 52819 (+1.1%) | 78966 vs 79229 (-0.3%) | 98118 vs 105638 (-7.1%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 25.6 points at 89.8% of the default cost, 10.2% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 25.5 points at 92.9% of the default cost, 7.1% under the budget it was given.
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 7.1% of the budget, 92.9% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
