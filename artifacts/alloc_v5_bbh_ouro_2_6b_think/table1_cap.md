# Table 1 -- bbh (ouro_2_6b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 320368 layer passes over 2137 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 91.2 | +0.0 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 85.9 (10%) | 79.3 (38%) | 62.3 (95%) | 83.1 | +8.1 |
| lookup | 48.0 | 74.4 | 82.7 | 86.7 | +4.5 |
| equation | 47.9 | 74.4 | 82.2 | 83.2 | +8.0 |
| equation_n30 | 47.6 | 75.2 | 82.3 | 87.1 | +4.1 |
| equation_n100 | 47.6 | 74.4 | 82.7 | 86.7 | +4.5 |
| gated_equation | 47.9 | 75.0 | 82.5 | 87.1 | +4.1 |
| avg_lookup | 49.8 | 79.4 | 85.9 | 87.2 | +4.0 |
| avg_equation | 49.8 | 80.0 | 83.4 | 84.8 | +6.5 |
| avg_gated_lookup | 50.0 | 80.2 | 86.0 | 88.1 | +3.2 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 4096, 91.2 points over 2137 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 80582 vs 80092 (+0.6%) | 150865 vs 160184 (-5.8%) | 240346 vs 240276 (+0.0%) | 294619 vs 320368 (-8.0%) |
| avg_equation | 80582 vs 80092 (+0.6%) | 160732 vs 160184 (+0.3%) | 241392 vs 240276 (+0.5%) | 308316 vs 320368 (-3.8%) |
| avg_gated_lookup | 80910 vs 80092 (+1.0%) | 160180 vs 160184 (-0.0%) | 237916 vs 240276 (-1.0%) | 319276 vs 320368 (-0.3%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
