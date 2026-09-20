# Table 1 -- csqa (ouro_1_4b_think), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 112642 layer passes over 977 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 76.0 | +0.6 |
| default_cell | 86.7 (5%) | 86.0 (68%) | 82.9 (79%) | 81.2 (84%) | -4.6 |
| default_at_budget | 75.2 | 75.2 | 75.2 | 76.5 | +0.2 |
| lookup | 74.1 | 75.2 | 75.2 | 76.5 | +0.2 |
| equation | 75.3 | 76.2 | 76.3 | 76.5 | +0.2 |
| equation_n100 | 75.3 | 76.2 | 76.3 | 76.5 | +0.2 |
| equation_n30 | 73.9 | 76.7 | 75.9 | 75.9 | +0.7 |
| equation_resolved | 74.1 | 76.2 | 76.3 | 76.5 | +0.2 |
| gated_equation | 75.2 | 75.2 | 75.2 | 76.5 | +0.2 |
| gated_equation_resolved | 75.2 | 75.2 | 75.2 | 76.5 | +0.2 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 2048, 76.7 points over 977 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none.

`default_cell` is the default operating point (depth 4 at cap 8192) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
