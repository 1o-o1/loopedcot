# Table 1 -- aqua (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 78835 layer passes over 154 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 67.5 | +1.3 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | 80.8 (17%) | 67.5 | +1.3 |
| lookup | 29.2 | 52.6 | 68.8 | 68.8 | +0.0 |
| equation | 24.0 | 52.6 | 68.8 | 68.2 | +0.6 |
| equation_n30 | 24.0 | 52.6 | 68.8 | 68.2 | +0.6 |
| equation_n100 | 24.0 | 52.6 | 68.8 | 68.2 | +0.6 |
| gated_equation | 24.0 | 52.6 | 80.8 (17%) | 68.2 | +0.6 |
| avg_lookup | 36.4 | 56.5 | 68.8 | 68.8 | +0.0 |
| avg_equation | 35.7 | 56.5 | 68.2 | 68.2 | +0.6 |
| avg_gated_lookup | 36.4 | 56.5 | 68.8 | 68.8 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 3 at cap 256, 68.8 points over 154 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0, F2.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 20737 vs 19709 (+5.2%) | 39745 vs 39418 (+0.8%) | 52245 vs 59126 (-11.6%) | 52245 vs 78835 (-33.7%) |
| avg_equation | 20357 vs 19709 (+3.3%) | 39745 vs 39418 (+0.8%) | 59882 vs 59126 (+1.3%) | 60706 vs 78835 (-23.0%) |
| avg_gated_lookup | 20943 vs 19709 (+6.3%) | 40476 vs 39418 (+2.7%) | 52245 vs 59126 (-11.6%) | 52245 vs 78835 (-33.7%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 68.8 points at 66.3% of the default cost, 11.6% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.8 points at 66.3% of the default cost, 33.7% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.2 points at 77.0% of the default cost, 23.0% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 68.8 points at 66.3% of the default cost, 11.6% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.8 points at 66.3% of the default cost, 33.7% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
