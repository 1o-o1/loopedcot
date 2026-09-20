# Table 1 -- aqua (ouro_1_4b_think), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 257269 layer passes over 154 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 82.5 | +2.6 |
| default_cell | 100.0 (12%) | 97.6 (55%) | 98.1 (68%) | 98.3 (75%) | -13.2 |
| default_at_budget | 66.2 | 78.6 | 79.2 | 83.1 | +1.9 |
| lookup | 67.5 | 82.5 | 85.7 | 86.4 | -1.3 |
| equation | 67.5 | 82.5 | 85.7 | 86.4 | -1.3 |
| equation_n100 | 67.5 | 82.5 | 85.7 | 86.4 | -1.3 |
| equation_n30 | 67.5 | 82.5 | 85.7 | 86.4 | -1.3 |
| equation_resolved | 67.5 | 82.5 | 85.7 | 83.1 | +1.9 |
| gated_equation | 67.5 | 81.2 | 84.4 | 83.1 | +1.9 |
| gated_equation_resolved | 67.5 | 80.5 | 85.7 | 83.1 | +1.9 |

The ORACLE GAP is the best single evaluation cell (depth 3 at cap 4096, 85.1 points over 154 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3.

`default_cell` is the default operating point (depth 4 at cap 8192) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
