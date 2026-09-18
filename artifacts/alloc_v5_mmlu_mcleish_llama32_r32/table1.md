# Table 1 -- mmlu (mcleish_llama32_r32), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 40743 layer passes over 1700 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 37.4 | +1.1 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | 38.9 (86%) | 38.3 (98%) | +0.2 |
| lookup | 33.1 (98%) | 36.8 | 36.7 | 36.7 | +1.8 |
| equation | 33.3 (98%) | 36.3 | 36.6 | 36.2 | +2.3 |
| equation_n30 | 26.7 (98%) | 36.4 | 36.6 | 36.2 | +2.3 |
| equation_n100 | 33.4 (98%) | 36.2 | 36.6 | 36.2 | +2.3 |
| gated_equation | 26.7 (98%) | 36.4 | 38.5 (86%) | 36.2 | +2.3 |
| avg_lookup | 33.2 | 36.7 | 36.7 | 36.7 | +1.8 |
| avg_equation | 31.6 | 36.7 | 36.2 | 36.2 | +2.3 |
| avg_gated_lookup | 33.4 | 36.7 | 36.7 | 36.7 | +1.8 |

The ORACLE GAP is the best single evaluation cell (depth 8 at cap 0, 38.5 points over 1700 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0, F2.

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 10037 vs 10186 (-1.5%) | 18610 vs 20371 (-8.6%) | 18610 vs 30557 (-39.1%) | 18610 vs 40743 (-54.3%) |
| avg_equation | 10111 vs 10186 (-0.7%) | 20527 vs 20371 (+0.8%) | 30526 vs 30557 (-0.1%) | 40073 vs 40743 (-1.6%) |
| avg_gated_lookup | 10142 vs 10186 (-0.4%) | 18610 vs 20371 (-8.6%) | 18610 vs 30557 (-39.1%) | 18610 vs 40743 (-54.3%) |
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 45.7% of the default cost, 8.6% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 45.7% of the default cost, 39.1% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 45.7% of the default cost, 54.3% under the budget it was given.
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 45.7% of the default cost, 8.6% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 45.7% of the default cost, 39.1% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 45.7% of the default cost, 54.3% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
