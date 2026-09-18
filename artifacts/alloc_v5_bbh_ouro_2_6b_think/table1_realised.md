# Table 1 -- bbh (ouro_2_6b_think), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 320368 layer passes over 2137 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 91.2 | +0.0 |
| default_cell | n/a | 85.9 (10%) | 92.6 (26%) | 93.7 (64%) | -2.5 |
| default_at_budget | 85.9 (10%) | 79.3 (38%) | 62.5 (95%) | 83.9 | +7.4 |
| lookup | 48.3 | 76.5 | 84.9 | 87.4 | +3.8 |
| equation | 48.1 | 76.5 | 84.9 | 88.2 | +3.1 |
| equation_n30 | 48.7 | 76.4 | 85.9 | 87.5 | +3.7 |
| equation_n100 | 48.0 | 76.3 | 85.1 | 88.4 | +2.8 |
| gated_equation | 48.0 | 76.5 | 83.2 | 87.1 | +4.1 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 4096, 91.2 points over 2137 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
