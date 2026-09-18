# Table 1 -- arc (ouro_2_6b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 160919 layer passes over 938 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 96.8 | +0.0 |
| default_cell | n/a | n/a | n/a | 95.9 (42%) | +0.9 |
| default_at_budget | n/a | 91.9 (91%) | 93.3 | 96.7 | +0.1 |
| lookup | 83.5 | 92.2 | 96.5 | 96.7 | +0.1 |
| equation | 70.0 | 92.2 | 96.5 | 96.7 | +0.1 |
| equation_n30 | 70.0 | 91.7 | 94.7 | 96.6 | +0.2 |
| equation_n100 | 70.0 | 88.1 | 96.5 | 96.7 | +0.1 |
| gated_equation | 70.0 | 91.7 | 91.0 | 96.4 | +0.4 |
| avg_lookup | 87.7 | 93.4 | 96.7 | 96.7 | +0.1 |
| avg_equation | 87.5 | 93.5 | 96.7 | 96.7 | +0.1 |
| avg_gated_lookup | 87.7 | 94.1 | 96.7 | 96.7 | +0.1 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 4096, 96.8 points over 938 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0, F1.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 40114 vs 40230 (-0.3%) | 80009 vs 80459 (-0.6%) | 117024 vs 120689 (-3.0%) | 117024 vs 160919 (-27.3%) |
| avg_equation | 39968 vs 40230 (-0.6%) | 79786 vs 80459 (-0.8%) | 117024 vs 120689 (-3.0%) | 117024 vs 160919 (-27.3%) |
| avg_gated_lookup | 39384 vs 40230 (-2.1%) | 81514 vs 80459 (+1.3%) | 117024 vs 120689 (-3.0%) | 117024 vs 160919 (-27.3%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 96.7 points at 72.7% of the default cost, 3.0% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 96.7 points at 72.7% of the default cost, 27.3% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 96.7 points at 72.7% of the default cost, 3.0% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 96.7 points at 72.7% of the default cost, 27.3% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 96.7 points at 72.7% of the default cost, 3.0% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 96.7 points at 72.7% of the default cost, 27.3% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
