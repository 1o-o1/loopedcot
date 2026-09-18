# Table 1 -- aqua (huginn_0125), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 142485 layer passes over 154 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 24.7 | +3.2 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 13.0 (15%) | 21.4 | 23.4 | +4.5 |
| lookup | 23.4 | 24.7 | 24.7 | 24.7 | +3.2 |
| equation | 25.3 | 24.7 | 20.8 | 20.8 | +7.1 |
| equation_n30 | 25.3 | 24.7 | 20.8 | 20.8 | +7.1 |
| equation_n100 | 25.3 | 24.7 | 20.8 | 20.8 | +7.1 |
| gated_equation | 22.1 | 24.7 | 21.4 | 23.4 | +4.5 |
| avg_lookup | 24.0 | 24.7 | 24.7 | 24.7 | +3.2 |
| avg_equation | 26.0 | 23.4 | 20.8 | 20.8 | +7.1 |
| avg_gated_lookup | 23.4 | 23.4 | 23.4 | 23.4 | +4.5 |

The ORACLE GAP is the best single evaluation cell (depth 2 at cap 0, 27.9 points over 154 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F3.

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 35018 vs 35621 (-1.7%) | 52204 vs 71242 (-26.7%) | 52204 vs 106863 (-51.1%) | 52204 vs 142485 (-63.4%) |
| avg_equation | 35314 vs 35621 (-0.9%) | 69758 vs 71242 (-2.1%) | 93164 vs 106863 (-12.8%) | 93164 vs 142485 (-34.6%) |
| avg_gated_lookup | 7514 vs 35621 (-78.9%) | 7514 vs 71242 (-89.5%) | 7514 vs 106863 (-93.0%) | 7514 vs 142485 (-94.7%) |
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 24.7 points at 36.6% of the default cost, 26.7% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 24.7 points at 36.6% of the default cost, 51.1% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 24.7 points at 36.6% of the default cost, 63.4% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 20.8 points at 65.4% of the default cost, 12.8% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 20.8 points at 65.4% of the default cost, 34.6% under the budget it was given.
- `avg_gated_lookup` at 0.25x: the multiplier is 0, so the budget never binds. The row is the same 23.4 points at 5.3% of the default cost, 78.9% under the budget it was given.
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 23.4 points at 5.3% of the default cost, 89.5% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 23.4 points at 5.3% of the default cost, 93.0% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 23.4 points at 5.3% of the default cost, 94.7% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
