# Table 1 -- arc (ouro_2_6b_base), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 77524 layer passes over 938 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 93.1 | +0.0 |
| default_cell | n/a | n/a | n/a | 92.8 (56%) | +0.3 |
| default_at_budget | n/a | n/a | n/a | 92.8 (93%) | +0.3 |
| lookup | 63.3 (93%) | 86.8 | 91.0 | 92.0 | +1.1 |
| equation | 56.9 (93%) | 85.7 | 91.0 | 91.7 | +1.4 |
| equation_n30 | 56.9 (93%) | 85.7 | 91.0 | 92.0 | +1.1 |
| equation_n100 | 56.9 (93%) | 85.7 | 91.0 | 91.7 | +1.4 |
| gated_equation | 56.9 (93%) | 85.9 | 91.0 | 92.2 (93%) | +0.9 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 128, 93.1 points over 938 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
