# Table 1 -- arc (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 38814 layer passes over 938 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 86.4 | +0.0 |
| default_cell | n/a | n/a | n/a | 85.7 (57%) | +0.7 |
| default_at_budget | n/a | n/a | n/a | 86.6 (93%) | -0.3 |
| lookup | 42.7 (93%) | 75.3 | 83.9 | 85.6 | +0.7 |
| equation | 43.7 (93%) | 73.0 | 83.6 | 85.3 | +1.1 |
| equation_n30 | 43.7 (93%) | 73.0 | 84.5 | 84.4 | +1.9 |
| equation_n100 | 43.7 (93%) | 73.0 | 83.6 | 84.4 | +1.9 |
| gated_equation | 43.7 (93%) | 73.0 | 84.5 | 86.4 (93%) | -0.1 |
| avg_lookup | 45.2 | 78.1 | 84.4 | 85.9 | +0.4 |
| avg_equation | 43.3 | 75.2 | 84.4 | 86.2 | +0.1 |
| avg_gated_lookup | 45.2 | 79.1 | 84.4 | 85.9 | +0.4 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 128, 86.4 points over 938 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 9593 vs 9704 (-1.1%) | 19232 vs 19407 (-0.9%) | 29051 vs 29111 (-0.2%) | 38122 vs 38814 (-1.8%) |
| avg_equation | 9587 vs 9704 (-1.2%) | 19433 vs 19407 (+0.1%) | 29055 vs 29111 (-0.2%) | 38707 vs 38814 (-0.3%) |
| avg_gated_lookup | 9498 vs 9704 (-2.1%) | 19278 vs 19407 (-0.7%) | 29051 vs 29111 (-0.2%) | 38122 vs 38814 (-1.8%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 85.9 points at 98.2% of the default cost, 1.8% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 85.9 points at 98.2% of the default cost, 1.8% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
