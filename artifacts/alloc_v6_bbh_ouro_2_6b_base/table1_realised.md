# Table 1 -- bbh (ouro_2_6b_base), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 42462 layer passes over 2137 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 82.5 | +0.0 |
| default_cell | 89.8 (12%) | 78.5 (26%) | 87.1 (61%) | 85.5 (79%) | -3.0 |
| default_at_budget | 56.9 | 56.5 | 67.5 | 69.8 | +12.6 |
| lookup | 58.3 | 66.9 | 77.9 | 77.8 | +4.6 |
| equation | 57.2 | 66.9 | 77.9 | 77.8 | +4.6 |
| equation_n100 | 57.2 | 66.8 | 78.1 | 78.0 | +4.5 |
| equation_n30 | 57.2 | 66.4 | 69.2 | 77.9 | +4.5 |
| equation_resolved | 57.3 | 66.6 | 77.8 | 78.2 | +4.3 |
| gated_equation | 56.9 | 67.0 | 69.0 | 77.7 | +4.8 |
| gated_equation_resolved | 56.9 | 57.4 | 69.0 | 77.7 | +4.8 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 2048, 82.5 points over 2137 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F1, F2, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
