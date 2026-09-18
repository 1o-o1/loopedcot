# Table 1 -- hellaswag (ouro_2_6b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 171164 layer passes over 1700 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 76.8 | +5.4 |
| default_cell | n/a | n/a | n/a | 74.6 (34%) | +7.5 |
| default_at_budget | n/a | n/a | 76.3 (16%) | 76.6 | +5.5 |
| lookup | 33.6 | 66.0 | 82.1 | 82.1 | +0.0 |
| equation | 33.6 | 58.2 | 74.9 | 76.2 | +5.9 |
| equation_n30 | 31.7 | 66.0 | 81.9 | 76.5 | +5.6 |
| equation_n100 | 33.6 | 58.2 | 74.9 | 76.5 | +5.6 |
| gated_equation | 33.6 | 58.2 | 74.9 | 82.1 | +0.0 |
| avg_lookup | 36.0 | 69.2 | 82.4 | 82.1 | +0.0 |
| avg_equation | 35.5 | 60.0 | 74.8 | 76.6 | +5.5 |
| avg_gated_lookup | 36.0 | 69.3 | 82.5 | 82.1 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 3 at cap 0, 82.1 points over 1700 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 41832 vs 42791 (-2.2%) | 85056 vs 85582 (-0.6%) | 128505 vs 128373 (+0.1%) | 147946 vs 171164 (-13.6%) |
| avg_equation | 41670 vs 42791 (-2.6%) | 84826 vs 85582 (-0.9%) | 127675 vs 128373 (-0.5%) | 158266 vs 171164 (-7.5%) |
| avg_gated_lookup | 41832 vs 42791 (-2.2%) | 85143 vs 85582 (-0.5%) | 128958 vs 128373 (+0.5%) | 147946 vs 171164 (-13.6%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 82.1 points at 86.4% of the default cost, 13.6% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 76.6 points at 92.5% of the default cost, 7.5% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 82.1 points at 86.4% of the default cost, 13.6% under the budget it was given.
- `avg_gated_lookup` at 1.00x: deviated from the default cell on family F0. Verification margin +2.2 points, sd 3.9, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 13.6% of the budget, 86.4% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
