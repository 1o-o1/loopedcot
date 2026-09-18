# Table 1 -- mmlu (huginn_0125), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 85913 layer passes over 1700 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 36.3 | +3.1 |
| default_cell | n/a | n/a | 44.3 (37%) | 37.8 (84%) | +1.5 |
| default_at_budget | n/a | n/a | 39.3 (70%) | 37.2 (91%) | +2.2 |
| lookup | 28.9 | 35.2 | 35.5 | 35.5 | +3.9 |
| equation | 29.4 | 35.4 | 35.9 | 36.1 | +3.2 |
| equation_n30 | 26.4 | 35.7 | 35.9 | 36.1 | +3.2 |
| equation_n100 | 29.2 | 35.2 | 35.9 | 36.1 | +3.2 |
| gated_equation | 29.9 | 35.4 | 37.3 | 36.5 | +2.8 |

The ORACLE GAP is the best single evaluation cell (depth 16 at cap 0, 39.4 points over 1700 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F3.

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
