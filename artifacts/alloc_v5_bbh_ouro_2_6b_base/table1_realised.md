# Table 1 -- bbh (ouro_2_6b_base), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 197416 layer passes over 2137 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 82.5 | +0.0 |
| default_cell | n/a | 89.5 (10%) | 89.3 (21%) | 88.2 (57%) | -5.8 |
| default_at_budget | 79.6 (10%) | 89.5 (10%) | 86.9 (25%) | 66.6 (85%) | +15.9 |
| lookup | 43.2 (85%) | 55.8 | 77.0 | 80.2 | +2.3 |
| equation | 41.4 (85%) | 57.3 | 77.1 | 80.2 | +2.2 |
| equation_n30 | 41.4 (85%) | 57.3 | 76.9 | 80.1 | +2.3 |
| equation_n100 | 41.4 (85%) | 57.3 | 77.1 | 80.2 | +2.2 |
| gated_equation | 41.4 (85%) | 57.4 | 77.2 | 80.2 (100%) | +2.3 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 2048, 82.5 points over 2137 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
