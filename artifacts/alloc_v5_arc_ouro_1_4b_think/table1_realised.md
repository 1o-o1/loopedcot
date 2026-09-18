# Table 1 -- arc (ouro_1_4b_think), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 85664 layer passes over 938 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 93.7 | +0.4 |
| default_cell | n/a | n/a | 96.9 (28%) | 96.7 (82%) | -2.6 |
| default_at_budget | n/a | 87.5 (98%) | 88.9 | 91.5 | +2.7 |
| lookup | 74.5 | 89.7 | 92.0 | 93.3 | +0.9 |
| equation | 74.9 | 88.5 | 92.6 | 93.9 | +0.2 |
| equation_n30 | 74.9 | 85.5 | 92.4 | 93.2 | +1.0 |
| equation_n100 | 74.9 | 88.5 | 92.4 | 93.7 | +0.4 |
| gated_equation | 74.9 | 86.9 (98%) | 87.0 | 93.3 | +0.9 |

The ORACLE GAP is the best single evaluation cell (depth 3 at cap 1024, 94.1 points over 938 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0, F2.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
