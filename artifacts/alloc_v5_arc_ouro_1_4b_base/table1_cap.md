# Table 1 -- arc (ouro_1_4b_base), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 38814 layer passes over 938 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 86.4 | +0.0 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | n/a | 86.6 (93%) | -0.3 |
| lookup | 42.7 (93%) | 75.3 | 83.7 | 85.6 | +0.7 |
| equation | 42.7 (93%) | 72.3 | 83.4 | 85.3 | +1.1 |
| equation_n30 | 42.7 (93%) | 72.3 | 84.3 | 84.4 | +1.9 |
| equation_n100 | 42.7 (93%) | 72.3 | 83.4 | 84.4 | +1.9 |
| gated_equation | 42.7 (93%) | 72.3 | 84.3 | 86.4 (93%) | -0.1 |
| avg_lookup | 45.2 | 78.1 | 85.3 | 85.9 | +0.4 |
| avg_equation | 42.1 | 75.1 | 84.1 | 86.1 | +0.2 |
| avg_gated_lookup | 45.2 | 79.1 | 84.1 | 85.9 | +0.4 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 128, 86.4 points over 938 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 9593 vs 9704 (-1.1%) | 19232 vs 19407 (-0.9%) | 28874 vs 29111 (-0.8%) | 38164 vs 38814 (-1.7%) |
| avg_equation | 9707 vs 9704 (+0.0%) | 19315 vs 19407 (-0.5%) | 29021 vs 29111 (-0.3%) | 38691 vs 38814 (-0.3%) |
| avg_gated_lookup | 9498 vs 9704 (-2.1%) | 19204 vs 19407 (-1.0%) | 29078 vs 29111 (-0.1%) | 38164 vs 38814 (-1.7%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 85.9 points at 98.3% of the default cost, 1.7% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 85.9 points at 98.3% of the default cost, 1.7% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
