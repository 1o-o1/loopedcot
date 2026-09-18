# Table 1 -- bbh (ouro_1_4b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 183913 layer passes over 2137 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 84.3 | +0.0 |
| default_cell | n/a | n/a | 68.2 (10%) | 83.3 (72%) | +1.0 |
| default_at_budget | 65.5 (10%) | 52.4 (72%) | 66.3 | 84.1 | +0.1 |
| lookup | 32.5 | 66.5 | 81.0 | 83.2 | +1.1 |
| equation | 40.1 | 66.7 | 80.9 | 83.3 | +1.0 |
| equation_n30 | 34.3 | 66.7 | 81.1 | 82.3 | +2.0 |
| equation_n100 | 34.3 | 66.5 | 81.0 | 83.3 | +0.9 |
| gated_equation | 35.0 | 49.4 (72%) | 81.1 | 84.1 | +0.1 |
| avg_lookup | 45.1 | 73.3 | 81.0 | 84.1 | +0.1 |
| avg_equation | 41.2 | 73.5 | 81.4 | 84.3 | +0.0 |
| avg_gated_lookup | 41.7 | 76.8 | 82.4 | 84.3 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 4096, 84.3 points over 2137 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0, F2.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 47495 vs 45978 (+3.3%) | 91032 vs 91957 (-1.0%) | 135467 vs 137935 (-1.8%) | 161449 vs 183913 (-12.2%) |
| avg_equation | 45951 vs 45978 (-0.1%) | 91248 vs 91957 (-0.8%) | 138414 vs 137935 (+0.3%) | 173159 vs 183913 (-5.8%) |
| avg_gated_lookup | 44126 vs 45978 (-4.0%) | 97844 vs 91957 (+6.4%) | 142908 vs 137935 (+3.6%) | 173159 vs 183913 (-5.8%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 84.1 points at 87.8% of the default cost, 12.2% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 84.3 points at 94.2% of the default cost, 5.8% under the budget it was given.
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin -2.2 points, sd 3.2, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 5.8% of the budget, 94.2% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
