# Table 1 -- arc (ouro_1_4b_think), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 62974 layer passes over 938 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 93.7 | +0.4 |
| default_cell | n/a | 100.0 (6%) | 96.9 (45%) | 96.5 (79%) | -2.4 |
| default_at_budget | 86.2 | 89.8 | 90.0 | 91.9 | +2.2 |
| lookup | 86.2 | 89.8 | 93.0 | 93.0 | +1.2 |
| equation | 86.6 | 90.2 | 93.7 | 93.7 | +0.4 |
| equation_n100 | 84.9 | 90.2 | 93.5 | 93.6 | +0.5 |
| equation_n30 | 82.2 | 88.9 | 93.5 | 92.5 | +1.6 |
| equation_resolved | 86.2 | 89.8 | 93.0 | 93.0 | +1.2 |
| gated_equation | 86.2 | 90.1 | 93.3 | 92.9 | +1.3 |
| gated_equation_resolved | 86.2 | 90.1 | 93.3 | 92.9 | +1.3 |

The ORACLE GAP is the best single evaluation cell (depth 3 at cap 1024, 94.1 points over 938 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
