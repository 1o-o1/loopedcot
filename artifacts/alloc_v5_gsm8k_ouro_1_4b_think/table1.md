# Table 1 -- gsm8k (ouro_1_4b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 127642 layer passes over 1056 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 93.0 | +0.0 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 26.9 (31%) | 59.6 | 88.5 | +4.5 |
| lookup | 32.4 | 81.0 | 86.8 | 90.7 | +2.3 |
| equation | 32.4 | 81.0 | 86.8 | 90.7 | +2.3 |
| equation_n30 | 32.4 | 81.0 | 86.8 | 90.6 | +2.4 |
| equation_n100 | 32.4 | 81.0 | 86.8 | 90.7 | +2.3 |
| gated_equation | 32.4 | 26.6 (31%) | 86.8 | 90.7 | +2.3 |
| avg_lookup | 38.4 | 81.2 | 88.1 | 90.8 | +2.2 |
| avg_equation | 34.5 | 81.2 | 88.1 | 90.8 | +2.2 |
| avg_gated_lookup | 38.4 | 81.2 | 87.7 | 90.8 | +2.2 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 4096, 93.0 points over 1056 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0, F2.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 32145 vs 31910 (+0.7%) | 64049 vs 63821 (+0.4%) | 94602 vs 95731 (-1.2%) | 127901 vs 127642 (+0.2%) |
| avg_equation | 31088 vs 31910 (-2.6%) | 64049 vs 63821 (+0.4%) | 97535 vs 95731 (+1.9%) | 127702 vs 127642 (+0.0%) |
| avg_gated_lookup | 32145 vs 31910 (+0.7%) | 64049 vs 63821 (+0.4%) | 95894 vs 95731 (+0.2%) | 127702 vs 127642 (+0.0%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
