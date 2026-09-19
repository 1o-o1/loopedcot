# Table 1 -- math500 (huginn_0125), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 96956 layer passes over 400 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 15.0 | +0.8 |
| default_cell | 25.0 (45%) | 20.5 (70%) | 19.9 (72%) | 19.7 (72%) | -4.0 |
| default_at_budget | 15.2 | 15.5 | 15.2 | 15.2 | +0.5 |
| lookup | 15.2 | 15.8 | 15.8 | 15.8 | +0.0 |
| equation | 16.0 | 15.5 | 15.2 | 15.2 | +0.5 |
| equation_n100 | 16.0 | 15.5 | 15.2 | 15.2 | +0.5 |
| equation_n30 | 14.0 | 15.5 | 15.2 | 15.2 | +0.5 |
| equation_resolved | 15.2 | 15.8 | 15.8 | 15.8 | +0.0 |
| gated_equation | 15.2 | 15.5 | 15.2 | 15.2 | +0.5 |
| gated_equation_resolved | 15.2 | 15.5 | 15.2 | 15.2 | +0.5 |

The ORACLE GAP is the best single evaluation cell (depth 16 at cap 256, 15.8 points over 400 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none.

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
