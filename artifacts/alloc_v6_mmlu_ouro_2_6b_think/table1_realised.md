# Table 1 -- mmlu (ouro_2_6b_think), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 144919 layer passes over 1700 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 79.6 | +1.9 |
| default_cell | 100.0 (1%) | 93.3 (30%) | 89.2 (65%) | 85.7 (76%) | -4.1 |
| default_at_budget | 73.9 | 75.8 | 78.3 | 78.4 | +3.2 |
| lookup | 73.8 | 76.2 | 78.2 | 79.6 | +1.9 |
| equation | 71.2 | 76.0 | 78.2 | 79.6 | +1.9 |
| equation_n100 | 71.2 | 75.4 | 78.2 | 79.6 | +1.9 |
| equation_n30 | 71.2 | 76.2 | 79.2 | 79.6 | +1.9 |
| equation_resolved | 73.8 | 76.0 | 78.2 | 79.6 | +1.9 |
| gated_equation | 74.0 | 77.2 | 79.2 | 79.6 | +1.9 |
| gated_equation_resolved | 74.0 | 77.2 | 79.2 | 79.6 | +1.9 |

The ORACLE GAP is the best single evaluation cell (depth 3 at cap 4096, 81.6 points over 1700 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
