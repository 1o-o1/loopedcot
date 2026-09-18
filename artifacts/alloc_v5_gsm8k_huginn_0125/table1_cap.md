# Table 1 -- gsm8k (huginn_0125), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 105638 layer passes over 1056 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 25.5 | +0.1 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | 2.8 (24%) | 22.1 | +3.5 |
| lookup | 5.9 | 19.0 | 20.9 | 22.0 | +3.6 |
| equation | 6.1 | 19.1 | 20.9 | 20.9 | +4.6 |
| equation_n30 | 6.1 | 19.0 | 15.0 | 22.1 | +3.5 |
| equation_n100 | 6.1 | 19.0 | 20.9 | 22.0 | +3.6 |
| gated_equation | 6.1 | 19.1 | 20.9 | 22.0 | +3.6 |
| avg_lookup | 10.9 | 20.1 | 22.9 | 24.1 | +1.5 |
| avg_equation | 12.5 | 19.9 | 22.9 | 24.1 | +1.5 |
| avg_gated_lookup | 10.9 | 20.1 | 23.0 | 24.1 | +1.5 |

The ORACLE GAP is the best single evaluation cell (depth 32 at cap 256, 25.6 points over 1056 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3.

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 25131 vs 26410 (-4.8%) | 51871 vs 52819 (-1.8%) | 77175 vs 79229 (-2.6%) | 103173 vs 105638 (-2.3%) |
| avg_equation | 25854 vs 26410 (-2.1%) | 52278 vs 52819 (-1.0%) | 77175 vs 79229 (-2.6%) | 103173 vs 105638 (-2.3%) |
| avg_gated_lookup | 25131 vs 26410 (-4.8%) | 51871 vs 52819 (-1.8%) | 78429 vs 79229 (-1.0%) | 103173 vs 105638 (-2.3%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
