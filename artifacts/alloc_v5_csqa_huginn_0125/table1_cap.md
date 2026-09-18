# Table 1 -- csqa (huginn_0125), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 87288 layer passes over 977 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 42.8 | +0.0 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | n/a | 41.5 (100%) | +1.3 |
| lookup | 19.5 | 36.7 | 41.7 | 42.4 | +0.4 |
| equation | 18.9 | 32.4 | 41.7 | 41.7 | +1.1 |
| equation_n30 | 20.5 | 32.7 | 41.7 | 41.7 | +1.1 |
| equation_n100 | 19.4 | 31.7 | 41.7 | 41.7 | +1.1 |
| gated_equation | 18.9 | 32.4 | 41.7 | 41.5 | +1.3 |
| avg_lookup | 26.0 | 40.0 | 41.4 | 42.0 | +0.8 |
| avg_equation | 23.6 | 39.4 | 42.2 | 43.1 | -0.3 |
| avg_gated_lookup | 24.5 | 39.0 | 41.4 | 42.0 | +0.8 |

The ORACLE GAP is the best single evaluation cell (depth 32 at cap 64, 42.8 points over 977 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none.

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 20640 vs 21822 (-5.4%) | 42601 vs 43644 (-2.4%) | 62791 vs 65466 (-4.1%) | 86335 vs 87288 (-1.1%) |
| avg_equation | 19660 vs 21822 (-9.9%) | 42562 vs 43644 (-2.5%) | 64525 vs 65466 (-1.4%) | 85975 vs 87288 (-1.5%) |
| avg_gated_lookup | 20384 vs 21822 (-6.6%) | 41710 vs 43644 (-4.4%) | 62791 vs 65466 (-4.1%) | 86335 vs 87288 (-1.1%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 42.0 points at 98.9% of the default cost, 1.1% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 42.0 points at 98.9% of the default cost, 1.1% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
