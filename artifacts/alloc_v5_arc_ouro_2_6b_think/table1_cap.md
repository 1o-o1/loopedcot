# Table 1 -- arc (ouro_2_6b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 160919 layer passes over 938 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 96.8 | +0.0 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 91.9 (91%) | 92.5 | 94.0 | +2.8 |
| lookup | 83.5 | 92.2 | 92.2 | 96.5 | +0.3 |
| equation | 70.0 | 92.2 | 94.0 | 96.5 | +0.3 |
| equation_n30 | 70.0 | 91.7 | 92.2 | 94.0 | +2.8 |
| equation_n100 | 70.0 | 92.2 | 94.8 | 96.5 | +0.3 |
| gated_equation | 70.0 | 91.7 | 91.0 | 96.5 | +0.3 |
| avg_lookup | 87.7 | 92.6 | 93.9 | 95.8 | +1.0 |
| avg_equation | 87.5 | 92.8 | 95.2 | 96.6 | +0.2 |
| avg_gated_lookup | 87.7 | 92.8 | 92.8 | 93.7 | +3.1 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 4096, 96.8 points over 938 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0, F2.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 40114 vs 40230 (-0.3%) | 81714 vs 80459 (+1.6%) | 122447 vs 120689 (+1.5%) | 162122 vs 160919 (+0.7%) |
| avg_equation | 39968 vs 40230 (-0.6%) | 79521 vs 80459 (-1.2%) | 117142 vs 120689 (-2.9%) | 160766 vs 160919 (-0.1%) |
| avg_gated_lookup | 39384 vs 40230 (-2.1%) | 80877 vs 80459 (+0.5%) | 107985 vs 120689 (-10.5%) | 169815 vs 160919 (+5.5%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
