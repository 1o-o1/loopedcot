# Table 1 -- aqua (ouro_1_4b_base), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 78835 layer passes over 154 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 67.5 | +1.3 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | 80.8 (17%) | 68.8 | +0.0 |
| lookup | 29.2 | 53.2 | 65.6 | 68.8 | +0.0 |
| equation | 24.0 | 53.2 | 65.6 | 68.8 | +0.0 |
| equation_n30 | 24.0 | 53.2 | 66.2 | 68.8 | +0.0 |
| equation_n100 | 24.0 | 53.2 | 65.6 | 68.8 | +0.0 |
| gated_equation | 24.0 | 53.2 | 80.8 (17%) | 68.8 | +0.0 |
| avg_lookup | 37.0 | 55.8 | 68.8 | 68.8 | +0.0 |
| avg_equation | 35.1 | 55.8 | 66.2 | 68.8 | +0.0 |
| avg_gated_lookup | 37.0 | 55.8 | 66.9 | 68.8 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 3 at cap 256, 68.8 points over 154 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0, F2.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 21053 vs 19709 (+6.8%) | 40590 vs 39418 (+3.0%) | 59868 vs 59126 (+1.3%) | 64237 vs 78835 (-18.5%) |
| avg_equation | 20402 vs 19709 (+3.5%) | 40590 vs 39418 (+3.0%) | 57894 vs 59126 (-2.1%) | 69623 vs 78835 (-11.7%) |
| avg_gated_lookup | 21053 vs 19709 (+6.8%) | 40590 vs 39418 (+3.0%) | 58253 vs 59126 (-1.5%) | 64237 vs 78835 (-18.5%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.8 points at 81.5% of the default cost, 18.5% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.8 points at 81.5% of the default cost, 18.5% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
