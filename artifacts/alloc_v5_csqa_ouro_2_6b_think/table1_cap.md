# Table 1 -- csqa (ouro_2_6b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 234088 layer passes over 977 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 80.9 | +0.0 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | 79.2 | 80.1 | +0.7 |
| lookup | 18.1 | 80.3 | 80.0 | 80.0 | +0.8 |
| equation | 20.2 | 76.4 | 78.1 | 80.1 | +0.7 |
| equation_n30 | 28.9 | 76.4 | 76.5 | 76.5 | +4.4 |
| equation_n100 | 20.2 | 76.4 | 78.1 | 78.1 | +2.8 |
| gated_equation | 20.2 | 76.4 | 79.2 | 80.1 | +0.7 |
| avg_lookup | 67.3 | 80.6 | 79.8 | 80.2 | +0.6 |
| avg_equation | 67.3 | 76.8 | 78.0 | 80.2 | +0.6 |
| avg_gated_lookup | 65.8 | 80.6 | 80.3 | 80.1 | +0.7 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 4096, 80.9 points over 977 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 57914 vs 58522 (-1.0%) | 115832 vs 117044 (-1.0%) | 166525 vs 175566 (-5.1%) | 214482 vs 234088 (-8.4%) |
| avg_equation | 57914 vs 58522 (-1.0%) | 115382 vs 117044 (-1.4%) | 173023 vs 175566 (-1.4%) | 223324 vs 234088 (-4.6%) |
| avg_gated_lookup | 56752 vs 58522 (-3.0%) | 115832 vs 117044 (-1.0%) | 155608 vs 175566 (-11.4%) | 228518 vs 234088 (-2.4%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
