# Table 1 -- mmlu (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 58952 layer passes over 1700 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 68.4 | +0.0 |
| default_cell | n/a | n/a | n/a | 71.7 (79%) | -3.4 |
| default_at_budget | n/a | n/a | 74.3 (41%) | 70.5 (89%) | -2.1 |
| lookup | 40.3 (89%) | 59.2 | 65.6 | 66.8 | +1.6 |
| equation | 40.6 (89%) | 58.9 | 64.6 | 67.8 | +0.6 |
| equation_n30 | 40.6 (89%) | 58.9 | 64.9 | 67.8 | +0.6 |
| equation_n100 | 40.6 (89%) | 58.9 | 64.8 | 67.9 | +0.4 |
| gated_equation | 40.6 (89%) | 58.9 | 65.4 | 68.7 (89%) | -0.3 |
| avg_lookup | 43.6 | 61.4 | 66.4 | 67.4 | +1.0 |
| avg_equation | 42.9 | 61.6 | 65.5 | 68.4 | +0.0 |
| avg_gated_lookup | 44.5 | 61.1 | 66.6 | 67.4 | +1.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 128, 68.4 points over 1700 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 14821 vs 14738 (+0.6%) | 29297 vs 29476 (-0.6%) | 44279 vs 44214 (+0.1%) | 47957 vs 58952 (-18.7%) |
| avg_equation | 14756 vs 14738 (+0.1%) | 29502 vs 29476 (+0.1%) | 44472 vs 44214 (+0.6%) | 55207 vs 58952 (-6.4%) |
| avg_gated_lookup | 14675 vs 14738 (-0.4%) | 30152 vs 29476 (+2.3%) | 45275 vs 44214 (+2.4%) | 47957 vs 58952 (-18.7%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 67.4 points at 81.3% of the default cost, 18.7% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.4 points at 93.6% of the default cost, 6.4% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 67.4 points at 81.3% of the default cost, 18.7% under the budget it was given.
- `avg_gated_lookup` at 1.00x: deviated from the default cell on family F0. Verification margin +6.7 points, sd 4.6, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 18.7% of the budget, 81.3% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
