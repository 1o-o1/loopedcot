# Table 1 -- math500 (huginn_0125), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 224131 layer passes over 400 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 15.0 | +0.8 |
| default_cell | n/a | n/a | n/a | 17.1 (84%) | -1.3 |
| default_at_budget | n/a | n/a | 15.5 (98%) | 15.1 (99%) | +0.6 |
| lookup | 8.2 | 15.2 | 15.5 | 15.8 | +0.0 |
| equation | 7.2 | 13.5 | 15.5 | 15.0 | +0.8 |
| equation_n30 | 7.2 | 6.2 | 15.2 | 15.0 | +0.8 |
| equation_n100 | 7.2 | 13.5 | 15.5 | 15.0 | +0.8 |
| gated_equation | 7.2 | 6.2 | 13.5 | 13.5 | +2.2 |
| avg_lookup | 13.2 | 15.5 | 15.8 | 15.8 | +0.0 |
| avg_equation | 12.8 | 15.5 | 15.2 | 15.0 | +0.8 |
| avg_gated_lookup | 10.8 | 14.5 | 15.2 | 15.0 | +0.8 |

The ORACLE GAP is the best single evaluation cell (depth 16 at cap 256, 15.8 points over 400 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2.

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 56995 vs 56033 (+1.7%) | 111911 vs 112065 (-0.1%) | 155466 vs 168098 (-7.5%) | 155466 vs 224131 (-30.6%) |
| avg_equation | 57531 vs 56033 (+2.7%) | 112240 vs 112065 (+0.2%) | 156677 vs 168098 (-6.8%) | 221433 vs 224131 (-1.2%) |
| avg_gated_lookup | 57977 vs 56033 (+3.5%) | 114051 vs 112065 (+1.8%) | 146866 vs 168098 (-12.6%) | 221433 vs 224131 (-1.2%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 15.8 points at 69.4% of the default cost, 7.5% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 15.8 points at 69.4% of the default cost, 30.6% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 15.0 points at 98.8% of the default cost, 1.2% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 15.2 points at 65.5% of the default cost, 12.6% under the budget it was given.
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin -3.3 points, sd 3.4, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 1.2% of the budget, 98.8% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
