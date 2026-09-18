# Table 1 -- csqa (ouro_1_4b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 133929 layer passes over 977 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 76.7 | +0.0 |
| default_cell | n/a | n/a | n/a | 76.7 | +0.0 |
| default_at_budget | n/a | 72.9 | 75.2 | 76.7 | +0.0 |
| lookup | 61.1 | 73.5 | 75.2 | 76.5 | +0.2 |
| equation | 61.1 | 73.9 | 75.2 | 76.7 | +0.0 |
| equation_n30 | 61.1 | 73.9 | 76.4 | 76.4 | +0.3 |
| equation_n100 | 61.1 | 73.9 | 75.2 | 76.7 | +0.0 |
| gated_equation | 61.1 | 72.9 | 75.2 | 76.7 | +0.0 |
| avg_lookup | 60.7 | 73.9 | 77.0 | 76.5 | +0.2 |
| avg_equation | 60.8 | 71.5 | 75.7 | 76.7 | +0.0 |
| avg_gated_lookup | 60.8 | 73.8 | 75.6 | 76.7 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 2048, 76.7 points over 977 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 33346 vs 33482 (-0.4%) | 66923 vs 66964 (-0.1%) | 98418 vs 100446 (-2.0%) | 104309 vs 133929 (-22.1%) |
| avg_equation | 33456 vs 33482 (-0.1%) | 66470 vs 66964 (-0.7%) | 99895 vs 100446 (-0.5%) | 111070 vs 133929 (-17.1%) |
| avg_gated_lookup | 33466 vs 33482 (-0.0%) | 66800 vs 66964 (-0.2%) | 98695 vs 100446 (-1.7%) | 119145 vs 133929 (-11.0%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 76.5 points at 77.9% of the default cost, 22.1% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 76.7 points at 82.9% of the default cost, 17.1% under the budget it was given.
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 11.0% of the budget, 89.0% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
