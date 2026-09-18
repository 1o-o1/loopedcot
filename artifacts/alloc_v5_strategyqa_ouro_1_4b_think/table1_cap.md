# Table 1 -- strategyqa (ouro_1_4b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 108565 layer passes over 1990 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 72.4 | +0.2 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 69.7 | 71.0 | 72.2 | +0.5 |
| lookup | 61.0 | 69.7 | 71.0 | 70.9 | +1.7 |
| equation | 61.0 | 69.7 | 71.1 | 72.2 | +0.5 |
| equation_n30 | 61.0 | 66.1 | 67.5 | 72.2 | +0.5 |
| equation_n100 | 61.0 | 66.1 | 71.0 | 72.2 | +0.5 |
| gated_equation | 61.0 | 69.7 | 71.0 | 72.2 | +0.5 |
| avg_lookup | 63.3 | 68.4 | 71.7 | 71.8 | +0.8 |
| avg_equation | 63.0 | 70.9 | 72.1 | 71.9 | +0.7 |
| avg_gated_lookup | 63.4 | 68.4 | 71.6 | 71.8 | +0.8 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 2048, 72.6 points over 1990 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 27276 vs 27141 (+0.5%) | 53442 vs 54283 (-1.5%) | 77305 vs 81424 (-5.1%) | 102412 vs 108565 (-5.7%) |
| avg_equation | 26688 vs 27141 (-1.7%) | 54436 vs 54283 (+0.3%) | 80509 vs 81424 (-1.1%) | 105724 vs 108565 (-2.6%) |
| avg_gated_lookup | 26721 vs 27141 (-1.5%) | 53442 vs 54283 (-1.5%) | 72058 vs 81424 (-11.5%) | 102412 vs 108565 (-5.7%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
