# Table 1 -- strategyqa (ouro_2_6b_think), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 194101 layer passes over 1990 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 77.8 | +1.3 |
| default_cell | n/a | n/a | 86.9 (29%) | 83.0 (74%) | -3.9 |
| default_at_budget | n/a | 74.7 | 78.1 | 78.2 | +0.9 |
| lookup | 59.7 | 77.8 | 78.7 | 78.4 | +0.7 |
| equation | 59.7 | 77.5 | 78.8 | 78.5 | +0.6 |
| equation_n30 | 59.7 | 77.5 | 78.8 | 78.2 | +0.9 |
| equation_n100 | 59.7 | 77.5 | 78.8 | 78.5 | +0.6 |
| gated_equation | 59.7 | 77.5 | 79.1 | 78.7 | +0.4 |

The ORACLE GAP is the best single evaluation cell (depth 3 at cap 512, 79.1 points over 1990 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
