# Table 1 -- strategyqa (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 59025 layer passes over 1990 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 66.5 | +1.9 |
| default_cell | n/a | n/a | n/a | 66.4 (100%) | +2.0 |
| default_at_budget | n/a | n/a | 66.8 | 66.5 | +1.9 |
| lookup | 55.5 | 64.4 | 68.1 | 68.1 | +0.3 |
| equation | 53.8 | 66.6 | 68.1 | 67.7 | +0.7 |
| equation_n30 | 53.8 | 52.7 | 52.0 | 52.0 | +16.4 |
| equation_n100 | 53.8 | 63.0 | 66.8 | 66.6 | +1.8 |
| gated_equation | 53.8 | 66.5 | 63.8 | 63.8 | +4.6 |
| avg_lookup | 61.2 | 68.0 | 68.1 | 68.1 | +0.3 |
| avg_equation | 55.1 | 67.0 | 68.0 | 67.7 | +0.7 |
| avg_gated_lookup | 61.2 | 67.8 | 68.1 | 63.8 | +4.6 |

The ORACLE GAP is the best single evaluation cell (depth 3 at cap 128, 68.4 points over 1990 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 14326 vs 14756 (-2.9%) | 29264 vs 29513 (-0.8%) | 30423 vs 44269 (-31.3%) | 30423 vs 59025 (-48.5%) |
| avg_equation | 13178 vs 14756 (-10.7%) | 29244 vs 29513 (-0.9%) | 44303 vs 44269 (+0.1%) | 48331 vs 59025 (-18.1%) |
| avg_gated_lookup | 14326 vs 14756 (-2.9%) | 29613 vs 29513 (+0.3%) | 30423 vs 44269 (-31.3%) | 35861 vs 59025 (-39.2%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 68.1 points at 51.5% of the default cost, 31.3% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.1 points at 51.5% of the default cost, 48.5% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 67.7 points at 81.9% of the default cost, 18.1% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 68.1 points at 51.5% of the default cost, 31.3% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 63.8 points at 60.8% of the default cost, 39.2% under the budget it was given.
- `avg_gated_lookup` at 1.00x: deviated from the default cell on family F0. Verification margin +13.3 points, sd 5.8, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 39.2% of the budget, 60.8% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
