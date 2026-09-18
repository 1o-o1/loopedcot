# Table 1 -- mmlu (ouro_2_6b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 240640 layer passes over 1700 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 79.6 | +1.9 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 75.2 (89%) | 75.5 | 78.3 | +3.3 |
| lookup | 65.4 | 72.9 | 78.0 | 80.2 | +1.4 |
| equation | 45.3 | 75.2 | 77.8 | 80.2 | +1.4 |
| equation_n30 | 45.3 | 74.2 | 77.9 | 80.2 | +1.4 |
| equation_n100 | 45.3 | 74.2 | 77.8 | 80.2 | +1.4 |
| gated_equation | 46.0 | 75.5 (99%) | 77.9 | 80.2 | +1.4 |
| avg_lookup | 69.8 | 76.1 | 79.2 | 80.8 | +0.8 |
| avg_equation | 62.7 | 75.5 | 79.2 | 80.8 | +0.8 |
| avg_gated_lookup | 67.6 | 74.8 | 79.6 | 81.1 | +0.5 |

The ORACLE GAP is the best single evaluation cell (depth 3 at cap 4096, 81.6 points over 1700 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 60156 vs 60160 (-0.0%) | 122478 vs 120320 (+1.8%) | 180105 vs 180480 (-0.2%) | 234881 vs 240640 (-2.4%) |
| avg_equation | 58248 vs 60160 (-3.2%) | 119800 vs 120320 (-0.4%) | 178717 vs 180480 (-1.0%) | 239912 vs 240640 (-0.3%) |
| avg_gated_lookup | 62320 vs 60160 (+3.6%) | 115968 vs 120320 (-3.6%) | 177156 vs 180480 (-1.8%) | 250754 vs 240640 (+4.2%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
