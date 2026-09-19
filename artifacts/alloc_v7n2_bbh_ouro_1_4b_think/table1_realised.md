# Table 1 -- bbh (ouro_1_4b_think), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 123394 layer passes over 2137 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 83.8 | +0.0 |
| default_cell | 71.4 (0%) | 87.2 (26%) | 91.0 (57%) | 90.6 (72%) | -6.9 |
| default_at_budget | 55.3 | 79.2 | 79.3 | 82.8 | +1.0 |
| lookup | 58.7 | 79.6 | 81.1 | 83.2 | +0.5 |
| equation | 55.5 | 79.5 | 81.4 | 83.6 | +0.2 |
| equation_n100 | 55.5 | 79.5 | 81.4 | 83.6 | +0.2 |
| equation_n30 | 58.7 | 76.5 | 81.1 | 81.9 | +1.8 |
| equation_resolved | 58.7 | 79.6 | 81.1 | 83.2 | +0.5 |
| gated_equation | 55.7 | 79.2 | 79.3 | 82.8 | +1.0 |
| gated_equation_resolved | 55.7 | 79.2 | 79.3 | 82.8 | +1.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 4096, 83.8 points over 2137 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
