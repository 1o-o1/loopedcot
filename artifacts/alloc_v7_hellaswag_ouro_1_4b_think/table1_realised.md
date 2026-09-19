# Table 1 -- hellaswag (ouro_1_4b_think), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 72044 layer passes over 1700 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 74.8 | +2.9 |
| default_cell | n/a | 87.8 (16%) | 81.3 (69%) | 79.3 (82%) | -1.6 |
| default_at_budget | 71.9 | 70.6 | 75.0 | 74.9 | +2.7 |
| lookup | 77.6 | 77.6 | 77.6 | 77.6 | +0.0 |
| equation | 71.8 | 71.9 | 72.1 | 72.9 | +4.8 |
| equation_n100 | 70.6 | 68.9 | 71.2 | 71.4 | +6.2 |
| equation_n30 | 71.8 | 72.1 | 75.3 | 75.0 | +2.6 |
| equation_resolved | 76.9 | 76.9 | 76.9 | 76.9 | +0.7 |
| gated_equation | 77.6 | 77.6 | 74.1 | 73.5 | +4.2 |
| gated_equation_resolved | 77.6 | 77.6 | 72.9 | 72.2 | +5.5 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 0, 77.6 points over 1700 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
