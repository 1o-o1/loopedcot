# Table 1 -- bbh (ouro_1_4b_think), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 158425 layer passes over 2137 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 83.7 | +0.1 |
| default_cell | 76.7 (3%) | 90.6 (45%) | 90.5 (71%) | 89.8 (81%) | -6.1 |
| default_at_budget | 55.2 | 79.2 | 82.7 | 83.0 | +0.8 |
| lookup | 76.0 | 80.4 | 83.1 | 83.2 | +0.5 |
| equation | 76.0 | 80.7 | 83.4 | 84.0 | -0.2 |
| equation_n100 | 76.0 | 80.7 | 83.4 | 84.0 | -0.2 |
| equation_n30 | 76.0 | 80.4 | 81.7 | 83.2 | +0.5 |
| equation_resolved | 76.0 | 80.4 | 83.1 | 83.2 | +0.5 |
| gated_equation | 75.9 | 79.2 | 82.7 | 83.0 | +0.8 |
| gated_equation_resolved | 75.9 | 79.2 | 82.7 | 83.0 | +0.8 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 4096, 83.8 points over 2137 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2.

`default_cell` is the default operating point (depth 4 at cap 8192) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
