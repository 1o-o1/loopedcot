# Table 1 -- csqa (ouro_2_6b_think), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 115680 layer passes over 977 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 80.9 | +0.0 |
| default_cell | 100.0 (0%) | 93.7 (24%) | 89.6 (66%) | 86.7 (80%) | -5.8 |
| default_at_budget | 80.5 | 79.2 | 79.4 | 80.1 | +0.7 |
| lookup | 80.0 | 80.3 | 80.5 | 80.5 | +0.4 |
| equation | 80.3 | 77.9 | 79.3 | 81.0 | -0.1 |
| equation_n100 | 80.1 | 78.1 | 79.3 | 79.6 | +1.2 |
| equation_n30 | 75.1 | 77.0 | 77.1 | 76.5 | +4.4 |
| equation_resolved | 80.0 | 80.3 | 80.5 | 80.5 | +0.4 |
| gated_equation | 80.5 | 79.2 | 79.4 | 80.1 | +0.7 |
| gated_equation_resolved | 80.5 | 79.2 | 79.4 | 80.1 | +0.7 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 4096, 80.9 points over 977 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
