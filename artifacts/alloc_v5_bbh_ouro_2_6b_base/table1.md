# Table 1 -- bbh (ouro_2_6b_base), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 197416 layer passes over 2137 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 82.5 | +0.0 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 79.6 (10%) | 89.5 (10%) | 86.7 (25%) | 65.3 (85%) | +17.2 |
| lookup | 43.0 (85%) | 55.7 | 74.4 | 77.2 | +5.3 |
| equation | 41.6 (85%) | 57.3 | 74.4 | 77.2 | +5.3 |
| equation_n30 | 41.7 (85%) | 57.2 | 76.0 | 77.2 | +5.2 |
| equation_n100 | 41.7 (85%) | 57.2 | 74.4 | 77.2 | +5.3 |
| gated_equation | 40.8 (85%) | 57.3 | 74.5 | 77.3 (100%) | +5.2 |
| avg_lookup | 43.6 | 64.5 | 78.0 | 80.9 | +1.6 |
| avg_equation | 42.3 | 64.5 | 77.2 | 80.7 | +1.7 |
| avg_gated_lookup | 42.4 | 70.0 | 78.9 | 80.7 | +1.7 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 2048, 82.5 points over 2137 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 49253 vs 49354 (-0.2%) | 97513 vs 98708 (-1.2%) | 146748 vs 148062 (-0.9%) | 196272 vs 197416 (-0.6%) |
| avg_equation | 49685 vs 49354 (+0.7%) | 97513 vs 98708 (-1.2%) | 147518 vs 148062 (-0.4%) | 196617 vs 197416 (-0.4%) |
| avg_gated_lookup | 49800 vs 49354 (+0.9%) | 105161 vs 98708 (+6.5%) | 150883 vs 148062 (+1.9%) | 203690 vs 197416 (+3.2%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
