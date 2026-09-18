# Table 1 -- strategyqa (huginn_0125), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 118487 layer passes over 1990 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 55.5 | +1.3 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 56.3 | 56.8 | 56.4 | +0.4 |
| lookup | 56.0 | 56.4 | 56.4 | 56.4 | +0.4 |
| equation | 56.0 | 56.0 | 56.2 | 56.2 | +0.6 |
| equation_n30 | 56.0 | 56.0 | 56.2 | 56.2 | +0.6 |
| equation_n100 | 56.0 | 56.0 | 56.2 | 56.2 | +0.6 |
| gated_equation | 56.0 | 56.0 | 56.8 | 56.4 | +0.4 |
| avg_lookup | 56.2 | 56.4 | 56.4 | 56.4 | +0.4 |
| avg_equation | 56.0 | 56.2 | 56.2 | 56.2 | +0.6 |
| avg_gated_lookup | 56.1 | 55.5 | 55.6 | 55.6 | +1.2 |

The ORACLE GAP is the best single evaluation cell (depth 32 at cap 1024, 56.8 points over 1990 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2.

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 29540 vs 29622 (-0.3%) | 30168 vs 59244 (-49.1%) | 30168 vs 88865 (-66.1%) | 30168 vs 118487 (-74.5%) |
| avg_equation | 28560 vs 29622 (-3.6%) | 55798 vs 59244 (-5.8%) | 72592 vs 88865 (-18.3%) | 72592 vs 118487 (-38.7%) |
| avg_gated_lookup | 29285 vs 29622 (-1.1%) | 59762 vs 59244 (+0.9%) | 62338 vs 88865 (-29.9%) | 62338 vs 118487 (-47.4%) |
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 56.4 points at 25.5% of the default cost, 49.1% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 56.4 points at 25.5% of the default cost, 66.1% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 56.4 points at 25.5% of the default cost, 74.5% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 56.2 points at 61.3% of the default cost, 18.3% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 56.2 points at 61.3% of the default cost, 38.7% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 55.6 points at 52.6% of the default cost, 29.9% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 55.6 points at 52.6% of the default cost, 47.4% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
