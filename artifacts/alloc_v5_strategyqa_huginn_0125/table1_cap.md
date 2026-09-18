# Table 1 -- strategyqa (huginn_0125), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 118487 layer passes over 1990 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 55.5 | +1.3 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 55.8 | 56.3 | 55.6 | +1.2 |
| lookup | 56.1 | 56.4 | 56.4 | 56.4 | +0.4 |
| equation | 56.1 | 56.2 | 56.5 | 55.8 | +1.0 |
| equation_n30 | 56.1 | 56.2 | 56.5 | 55.8 | +1.0 |
| equation_n100 | 56.1 | 56.2 | 56.5 | 55.8 | +1.0 |
| gated_equation | 56.1 | 56.0 | 56.0 | 55.8 | +1.0 |
| avg_lookup | 55.9 | 56.4 | 56.4 | 56.4 | +0.4 |
| avg_equation | 56.2 | 56.0 | 56.1 | 56.1 | +0.7 |
| avg_gated_lookup | 55.8 | 55.8 | 55.8 | 55.6 | +1.2 |

The ORACLE GAP is the best single evaluation cell (depth 32 at cap 1024, 56.8 points over 1990 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2.

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 29320 vs 29622 (-1.0%) | 41488 vs 59244 (-30.0%) | 41488 vs 88865 (-53.3%) | 41488 vs 118487 (-65.0%) |
| avg_equation | 29414 vs 29622 (-0.7%) | 32919 vs 59244 (-44.4%) | 84986 vs 88865 (-4.4%) | 107765 vs 118487 (-9.0%) |
| avg_gated_lookup | 29411 vs 29622 (-0.7%) | 55191 vs 59244 (-6.8%) | 89930 vs 88865 (+1.2%) | 114327 vs 118487 (-3.5%) |
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 56.4 points at 35.0% of the default cost, 30.0% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 56.4 points at 35.0% of the default cost, 53.3% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 56.4 points at 35.0% of the default cost, 65.0% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 55.6 points at 96.5% of the default cost, 3.5% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
