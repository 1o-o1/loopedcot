# Table 1 -- math500 (ouro_1_4b_think), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 205663 layer passes over 400 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 89.5 | +0.0 |
| default_cell | 100.0 (4%) | 100.0 (31%) | 99.5 (48%) | 99.2 (60%) | -9.7 |
| default_at_budget | 55.2 | 75.8 | 75.8 | 83.8 | +5.8 |
| lookup | 67.2 | 78.2 | 84.2 | 84.5 | +5.0 |
| equation | 67.2 | 78.2 | 83.8 | 83.2 | +6.2 |
| equation_n100 | 67.2 | 78.2 | 83.8 | 83.2 | +6.2 |
| equation_n30 | 67.2 | 77.8 | 78.5 | 77.2 | +12.2 |
| equation_resolved | 67.2 | 78.2 | 84.2 | 84.5 | +5.0 |
| gated_equation | 67.2 | 78.0 | 84.5 | 83.8 | +5.8 |
| gated_equation_resolved | 67.2 | 78.2 | 84.5 | 83.8 | +5.8 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 4096, 89.5 points over 400 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
