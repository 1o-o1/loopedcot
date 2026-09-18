# Table 1 -- gsm8k (ouro_2_6b_base), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 151176 layer passes over 1056 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 82.8 | +0.0 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | n/a | 63.2 | +19.6 |
| lookup | 23.1 | 51.4 | 74.1 | 78.4 | +4.4 |
| equation | 23.1 | 51.6 | 74.1 | 78.4 | +4.4 |
| equation_n30 | 23.1 | 50.4 | 74.1 | 75.0 | +7.8 |
| equation_n100 | 23.1 | 50.4 | 74.1 | 78.4 | +4.4 |
| gated_equation | 23.1 | 50.4 | 74.1 | 78.4 | +4.4 |
| avg_lookup | 25.9 | 62.6 | 75.4 | 79.7 | +3.0 |
| avg_equation | 26.3 | 61.6 | 75.4 | 79.7 | +3.0 |
| avg_gated_lookup | 25.9 | 60.4 | 75.4 | 79.7 | +3.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 512, 82.8 points over 1056 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 37670 vs 37794 (-0.3%) | 75331 vs 75588 (-0.3%) | 112640 vs 113382 (-0.7%) | 150089 vs 151176 (-0.7%) |
| avg_equation | 38079 vs 37794 (+0.8%) | 74522 vs 75588 (-1.4%) | 112640 vs 113382 (-0.7%) | 150089 vs 151176 (-0.7%) |
| avg_gated_lookup | 37670 vs 37794 (-0.3%) | 73174 vs 75588 (-3.2%) | 112640 vs 113382 (-0.7%) | 150042 vs 151176 (-0.8%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
