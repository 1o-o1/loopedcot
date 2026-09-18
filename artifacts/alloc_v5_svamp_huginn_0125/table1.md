# Table 1 -- svamp (huginn_0125), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 84875 layer passes over 200 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 44.5 | +0.0 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | n/a | 27.0 | +17.5 |
| lookup | 4.5 | 26.5 | 39.5 | 39.5 | +5.0 |
| equation | 3.5 | 26.5 | 39.5 | 39.5 | +5.0 |
| equation_n30 | 4.5 | 20.0 | 20.0 | 20.0 | +24.5 |
| equation_n100 | 3.5 | 26.5 | 39.5 | 39.5 | +5.0 |
| gated_equation | 3.5 | 20.0 | 39.5 | 28.5 | +16.0 |
| avg_lookup | 18.0 | 38.5 | 39.5 | 39.5 | +5.0 |
| avg_equation | 19.5 | 39.0 | 41.0 | 45.0 | -0.5 |
| avg_gated_lookup | 19.0 | 38.0 | 39.5 | 39.5 | +5.0 |

The ORACLE GAP is the best single evaluation cell (depth 32 at cap 128, 44.5 points over 200 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F3.

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 21811 vs 21219 (+2.8%) | 43908 vs 42438 (+3.5%) | 48954 vs 63657 (-23.1%) | 48954 vs 84875 (-42.3%) |
| avg_equation | 22169 vs 21219 (+4.5%) | 44241 vs 42438 (+4.2%) | 68286 vs 63657 (+7.3%) | 86770 vs 84875 (+2.2%) |
| avg_gated_lookup | 21501 vs 21219 (+1.3%) | 43268 vs 42438 (+2.0%) | 48954 vs 63657 (-23.1%) | 48954 vs 84875 (-42.3%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 39.5 points at 57.7% of the default cost, 23.1% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 39.5 points at 57.7% of the default cost, 42.3% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 39.5 points at 57.7% of the default cost, 23.1% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 39.5 points at 57.7% of the default cost, 42.3% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
