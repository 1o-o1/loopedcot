# Table 1 -- hellaswag (ouro_1_4b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 145921 layer passes over 1700 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 74.8 | +2.9 |
| default_cell | n/a | n/a | n/a | 73.4 (44%) | +4.2 |
| default_at_budget | n/a | 68.6 (32%) | 72.4 | 74.8 | +2.9 |
| lookup | 37.9 | 76.6 | 77.6 | 77.6 | +0.0 |
| equation | 37.4 | 69.3 | 72.0 | 71.9 | +5.7 |
| equation_n30 | 36.4 | 69.3 | 72.0 | 74.8 | +2.9 |
| equation_n100 | 37.4 | 69.3 | 72.0 | 71.9 | +5.7 |
| gated_equation | 37.4 | 69.3 (32%) | 77.6 | 77.6 | +0.0 |
| avg_lookup | 56.3 | 77.5 | 77.6 | 77.6 | +0.0 |
| avg_equation | 56.7 | 75.0 | 71.9 | 71.9 | +5.7 |
| avg_gated_lookup | 54.9 | 77.2 | 76.6 | 77.6 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 0, 77.6 points over 1700 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 36074 vs 36480 (-1.1%) | 73178 vs 72960 (+0.3%) | 75221 vs 109441 (-31.3%) | 75221 vs 145921 (-48.5%) |
| avg_equation | 35956 vs 36480 (-1.4%) | 66902 vs 72960 (-8.3%) | 108830 vs 109441 (-0.6%) | 108830 vs 145921 (-25.4%) |
| avg_gated_lookup | 35939 vs 36480 (-1.5%) | 73202 vs 72960 (+0.3%) | 81365 vs 109441 (-25.7%) | 75221 vs 145921 (-48.5%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 77.6 points at 51.5% of the default cost, 31.3% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 77.6 points at 51.5% of the default cost, 48.5% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 71.9 points at 74.6% of the default cost, 25.4% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 76.6 points at 55.8% of the default cost, 25.7% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 77.6 points at 51.5% of the default cost, 48.5% under the budget it was given.
- `avg_gated_lookup` at 1.00x: deviated from the default cell on family F0. Verification margin +8.9 points, sd 4.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 48.5% of the budget, 51.5% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
