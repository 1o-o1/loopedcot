# Table 1 -- math500 (ouro_2_6b_think), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 369853 layer passes over 400 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 91.2 | +0.0 |
| default_cell | 100.0 (5%) | 100.0 (33%) | 99.5 (53%) | 99.6 (62%) | -8.3 |
| default_at_budget | 41.5 | 60.5 | 76.5 | 77.8 | +13.5 |
| lookup | 61.3 | 78.0 | 81.2 | 84.2 | +7.0 |
| equation | 61.0 | 78.0 | 81.8 | 84.8 | +6.5 |
| equation_n100 | 61.0 | 78.0 | 81.8 | 84.8 | +6.5 |
| equation_n30 | 60.8 | 78.0 | 80.5 | 82.2 | +9.0 |
| equation_resolved | 61.3 | 78.0 | 81.8 | 84.8 | +6.5 |
| gated_equation | 60.0 | 76.2 | 78.2 | 82.8 | +8.5 |
| gated_equation_resolved | 60.0 | 76.2 | 78.2 | 82.8 | +8.5 |

The ORACLE GAP is the best single evaluation cell (depth 3 at cap 4096, 91.2 points over 400 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
