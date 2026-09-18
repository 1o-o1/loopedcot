# Table 1 -- aqua (ouro_2_6b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 401640 layer passes over 154 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 89.0 | +0.0 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 55.8 | 75.3 | 85.1 | +3.9 |
| lookup | 50.0 | 79.2 | 83.1 | 85.1 | +3.9 |
| equation | 48.1 | 79.2 | 83.1 | 85.1 | +3.9 |
| equation_n30 | 50.6 | 73.4 | 83.1 | 85.1 | +3.9 |
| equation_n100 | 48.1 | 79.2 | 83.1 | 85.1 | +3.9 |
| gated_equation | 51.3 | 53.2 | 83.1 | 85.7 | +3.2 |
| avg_lookup | 63.6 | 81.8 | 83.8 | 87.7 | +1.3 |
| avg_equation | 63.0 | 81.8 | 83.8 | 85.1 | +3.9 |
| avg_gated_lookup | 64.3 | 81.8 | 83.8 | 87.0 | +1.9 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 4096, 89.0 points over 154 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0, F2.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 94558 vs 100410 (-5.8%) | 203324 vs 200820 (+1.2%) | 293935 vs 301230 (-2.4%) | 426006 vs 401640 (+6.1%) |
| avg_equation | 94722 vs 100410 (-5.7%) | 203324 vs 200820 (+1.2%) | 293935 vs 301230 (-2.4%) | 387705 vs 401640 (-3.5%) |
| avg_gated_lookup | 100383 vs 100410 (-0.0%) | 205418 vs 200820 (+2.3%) | 295514 vs 301230 (-1.9%) | 409409 vs 401640 (+1.9%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
