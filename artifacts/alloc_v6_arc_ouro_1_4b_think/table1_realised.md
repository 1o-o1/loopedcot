# Table 1 -- arc (ouro_1_4b_think), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 49996 layer passes over 938 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 93.7 | +0.4 |
| default_cell | n/a | 98.7 (16%) | 97.2 (57%) | 96.7 (83%) | -2.5 |
| default_at_budget | 88.6 | 86.5 | 89.9 | 91.4 | +2.8 |
| lookup | 88.8 | 89.8 | 91.5 | 93.3 | +0.9 |
| equation | 85.0 | 90.7 | 92.1 | 93.8 | +0.3 |
| equation_n100 | 85.0 | 90.6 | 92.0 | 93.6 | +0.5 |
| equation_n30 | 85.0 | 90.5 | 91.3 | 92.4 | +1.7 |
| equation_resolved | 88.8 | 89.8 | 91.5 | 93.3 | +0.9 |
| gated_equation | 88.6 | 87.7 | 91.5 | 93.3 | +0.9 |
| gated_equation_resolved | 88.6 | 87.7 | 91.5 | 90.9 | +3.2 |

The ORACLE GAP is the best single evaluation cell (depth 3 at cap 1024, 94.1 points over 938 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F1, F2, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
