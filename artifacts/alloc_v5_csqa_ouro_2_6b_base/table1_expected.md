# Table 1 -- csqa (ouro_2_6b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 124188 layer passes over 977 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 80.3 | +1.6 |
| default_cell | n/a | n/a | n/a | 78.7 (55%) | +3.3 |
| default_at_budget | n/a | n/a | n/a | 81.1 (100%) | +0.8 |
| lookup | 36.8 (100%) | 75.5 | 81.2 | 82.0 | +0.0 |
| equation | 36.8 (100%) | 74.7 | 80.0 | 80.0 | +1.9 |
| equation_n30 | 36.8 (100%) | 74.7 | 80.2 | 80.0 | +1.9 |
| equation_n100 | 36.8 (100%) | 74.7 | 77.5 | 80.0 | +1.9 |
| gated_equation | 36.8 (100%) | 74.7 | 80.2 | 81.2 | +0.8 |
| avg_lookup | 40.3 | 76.0 | 81.2 | 82.0 | +0.0 |
| avg_equation | 40.3 | 74.6 | 79.6 | 80.3 | +1.6 |
| avg_gated_lookup | 40.2 | 76.0 | 81.2 | 82.0 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 0, 82.0 points over 977 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 31015 vs 31047 (-0.1%) | 61885 vs 62094 (-0.3%) | 93022 vs 93141 (-0.1%) | 117256 vs 124188 (-5.6%) |
| avg_equation | 31015 vs 31047 (-0.1%) | 62217 vs 62094 (+0.2%) | 93293 vs 93141 (+0.2%) | 124165 vs 124188 (-0.0%) |
| avg_gated_lookup | 30984 vs 31047 (-0.2%) | 61885 vs 62094 (-0.3%) | 93022 vs 93141 (-0.1%) | 117256 vs 124188 (-5.6%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 82.0 points at 94.4% of the default cost, 5.6% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 82.0 points at 94.4% of the default cost, 5.6% under the budget it was given.
- `avg_gated_lookup` at 1.00x: deviated from the default cell on family F0. Verification margin +4.1 points, sd 3.0, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 5.6% of the budget, 94.4% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
