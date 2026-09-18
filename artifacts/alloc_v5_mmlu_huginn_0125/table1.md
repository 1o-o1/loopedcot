# Table 1 -- mmlu (huginn_0125), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 85913 layer passes over 1700 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 36.3 | +3.1 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | 39.0 (70%) | 37.3 (91%) | +2.0 |
| lookup | 29.0 | 35.2 | 35.5 | 35.5 | +3.9 |
| equation | 29.5 | 35.4 | 36.0 | 36.1 | +3.2 |
| equation_n30 | 26.4 | 35.7 | 36.0 | 36.1 | +3.2 |
| equation_n100 | 26.4 | 35.7 | 36.0 | 36.1 | +3.2 |
| gated_equation | 30.0 | 35.4 | 36.5 | 36.8 | +2.5 |
| avg_lookup | 32.3 | 35.5 | 35.5 | 35.5 | +3.9 |
| avg_equation | 32.8 | 36.3 | 36.2 | 36.1 | +3.3 |
| avg_gated_lookup | 32.3 | 35.5 | 35.5 | 35.5 | +3.9 |

The ORACLE GAP is the best single evaluation cell (depth 16 at cap 0, 39.4 points over 1700 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F3.

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 20337 vs 21478 (-5.3%) | 37751 vs 42956 (-12.1%) | 37751 vs 64435 (-41.4%) | 37751 vs 85913 (-56.1%) |
| avg_equation | 20816 vs 21478 (-3.1%) | 43536 vs 42956 (+1.4%) | 65706 vs 64435 (+2.0%) | 85787 vs 85913 (-0.1%) |
| avg_gated_lookup | 20077 vs 21478 (-6.5%) | 37751 vs 42956 (-12.1%) | 37751 vs 64435 (-41.4%) | 37751 vs 85913 (-56.1%) |
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 35.5 points at 43.9% of the default cost, 12.1% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 35.5 points at 43.9% of the default cost, 41.4% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 35.5 points at 43.9% of the default cost, 56.1% under the budget it was given.
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 35.5 points at 43.9% of the default cost, 12.1% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 35.5 points at 43.9% of the default cost, 41.4% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 35.5 points at 43.9% of the default cost, 56.1% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
