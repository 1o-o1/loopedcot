# Table 1 -- math500 (ouro_2_6b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 563241 layer passes over 400 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 91.2 | +0.0 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 41.7 (99%) | 75.2 | 76.2 | +15.0 |
| lookup | 43.2 | 72.8 | 78.8 | 83.8 | +7.5 |
| equation | 43.2 | 72.8 | 78.8 | 81.8 | +9.5 |
| equation_n30 | 43.2 | 45.5 | 76.0 | 82.0 | +9.2 |
| equation_n100 | 43.2 | 72.8 | 78.8 | 81.8 | +9.5 |
| gated_equation | 43.2 | 60.0 | 78.8 | 84.0 | +7.2 |
| avg_lookup | 51.7 | 76.2 | 80.0 | 82.5 | +8.8 |
| avg_equation | 51.2 | 76.2 | 80.2 | 82.0 | +9.2 |
| avg_gated_lookup | 59.0 | 75.0 | 82.0 | 84.2 | +7.0 |

The ORACLE GAP is the best single evaluation cell (depth 3 at cap 4096, 91.2 points over 400 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 138436 vs 140810 (-1.7%) | 245586 vs 281621 (-12.8%) | 411654 vs 422431 (-2.6%) | 552246 vs 563241 (-2.0%) |
| avg_equation | 140264 vs 140810 (-0.4%) | 257137 vs 281621 (-8.7%) | 406067 vs 422431 (-3.9%) | 570420 vs 563241 (+1.3%) |
| avg_gated_lookup | 146663 vs 140810 (+4.2%) | 229120 vs 281621 (-18.6%) | 420091 vs 422431 (-0.6%) | 558583 vs 563241 (-0.8%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
