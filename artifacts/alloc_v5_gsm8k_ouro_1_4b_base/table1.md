# Table 1 -- gsm8k (ouro_1_4b_base), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 77105 layer passes over 1056 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 76.7 | +0.1 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | n/a | 61.4 | +15.4 |
| lookup | 20.1 | 50.7 | 64.8 | 73.5 | +3.3 |
| equation | 20.1 | 50.7 | 64.8 | 73.5 | +3.3 |
| equation_n30 | 20.1 | 50.7 | 63.9 | 73.5 | +3.3 |
| equation_n100 | 20.1 | 50.7 | 64.8 | 73.5 | +3.3 |
| gated_equation | 20.1 | 50.7 | 64.8 | 73.5 | +3.3 |
| avg_lookup | 21.7 | 54.8 | 68.9 | 73.5 | +3.3 |
| avg_equation | 21.7 | 54.4 | 68.9 | 73.5 | +3.3 |
| avg_gated_lookup | 21.7 | 54.9 | 68.9 | 73.5 | +3.3 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 1024, 76.8 points over 1056 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 19415 vs 19276 (+0.7%) | 38022 vs 38552 (-1.4%) | 57464 vs 57829 (-0.6%) | 76674 vs 77105 (-0.6%) |
| avg_equation | 19415 vs 19276 (+0.7%) | 37670 vs 38552 (-2.3%) | 57464 vs 57829 (-0.6%) | 76674 vs 77105 (-0.6%) |
| avg_gated_lookup | 19415 vs 19276 (+0.7%) | 38148 vs 38552 (-1.1%) | 56694 vs 57829 (-2.0%) | 76674 vs 77105 (-0.6%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
