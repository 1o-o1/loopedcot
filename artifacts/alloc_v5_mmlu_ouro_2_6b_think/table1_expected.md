# Table 1 -- mmlu (ouro_2_6b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 240640 layer passes over 1700 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 79.6 | +1.9 |
| default_cell | n/a | n/a | n/a | 82.6 (21%) | -1.0 |
| default_at_budget | n/a | 75.2 (89%) | 77.2 | 79.4 | +2.2 |
| lookup | 65.4 | 72.9 | 81.2 | 81.6 | +0.0 |
| equation | 45.5 | 74.8 | 81.3 | 81.6 | +0.0 |
| equation_n30 | 45.5 | 67.7 | 81.5 | 79.9 | +1.7 |
| equation_n100 | 45.5 | 67.7 | 81.5 | 81.6 | +0.0 |
| gated_equation | 46.2 | 75.5 (99%) | 81.1 | 79.5 | +2.1 |
| avg_lookup | 69.8 | 75.8 | 81.6 | 81.6 | +0.0 |
| avg_equation | 62.7 | 76.2 | 81.6 | 81.6 | +0.0 |
| avg_gated_lookup | 67.9 | 75.4 | 81.5 | 81.5 | +0.1 |

The ORACLE GAP is the best single evaluation cell (depth 3 at cap 4096, 81.6 points over 1700 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 60156 vs 60160 (-0.0%) | 116982 vs 120320 (-2.8%) | 177720 vs 180480 (-1.5%) | 177720 vs 240640 (-26.1%) |
| avg_equation | 58248 vs 60160 (-3.2%) | 120402 vs 120320 (+0.1%) | 177720 vs 180480 (-1.5%) | 177720 vs 240640 (-26.1%) |
| avg_gated_lookup | 61495 vs 60160 (+2.2%) | 115377 vs 120320 (-4.1%) | 164435 vs 180480 (-8.9%) | 164435 vs 240640 (-31.7%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 81.6 points at 73.9% of the default cost, 1.5% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 81.6 points at 73.9% of the default cost, 26.1% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 81.6 points at 73.9% of the default cost, 1.5% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 81.6 points at 73.9% of the default cost, 26.1% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 81.5 points at 68.3% of the default cost, 8.9% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 81.5 points at 68.3% of the default cost, 31.7% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
