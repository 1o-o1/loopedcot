# Table 1 -- aqua (ouro_2_6b_base), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 158694 layer passes over 154 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 73.4 | +1.9 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | 73.5 (22%) | 72.1 | +3.2 |
| lookup | 40.3 | 66.2 | 68.2 | 68.2 | +7.1 |
| equation | 50.6 | 66.2 | 67.5 | 66.9 | +8.4 |
| equation_n30 | 37.7 | 66.2 | 67.5 | 72.1 | +3.2 |
| equation_n100 | 50.6 | 66.2 | 67.5 | 66.9 | +8.4 |
| gated_equation | 37.7 | 66.2 | 67.5 | 72.1 | +3.2 |
| avg_lookup | 44.8 | 59.7 | 68.2 | 68.2 | +7.1 |
| avg_equation | 46.1 | 66.9 | 70.8 | 70.8 | +4.5 |
| avg_gated_lookup | 45.5 | 63.6 | 71.4 | 72.1 | +3.2 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 256, 75.3 points over 154 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 40224 vs 39674 (+1.4%) | 75596 vs 79347 (-4.7%) | 85649 vs 119021 (-28.0%) | 85649 vs 158694 (-46.0%) |
| avg_equation | 41283 vs 39674 (+4.1%) | 79665 vs 79347 (+0.4%) | 119455 vs 119021 (+0.4%) | 158234 vs 158694 (-0.3%) |
| avg_gated_lookup | 41397 vs 39674 (+4.3%) | 73681 vs 79347 (-7.1%) | 122149 vs 119021 (+2.6%) | 146723 vs 158694 (-7.5%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 68.2 points at 54.0% of the default cost, 28.0% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.2 points at 54.0% of the default cost, 46.0% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 72.1 points at 92.5% of the default cost, 7.5% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
