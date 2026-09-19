# Table 1 -- bbh (huginn_0125), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 37633 layer passes over 2137 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 35.6 | +0.1 |
| default_cell | 50.7 (13%) | 37.6 (46%) | 42.6 (73%) | 41.4 (84%) | -5.8 |
| default_at_budget | 30.7 | 33.5 | 34.4 | 35.2 | +0.4 |
| lookup | 31.9 | 33.2 | 34.3 | 35.1 | +0.6 |
| equation | 30.9 | 35.1 | 35.3 | 35.2 | +0.4 |
| equation_n100 | 30.7 | 33.5 | 34.4 | 35.2 | +0.4 |
| equation_n30 | 31.8 | 31.8 | 31.8 | 31.8 | +3.8 |
| equation_resolved | 31.9 | 33.2 | 34.3 | 35.3 | +0.4 |
| gated_equation | 30.7 | 33.5 | 34.4 | 35.2 | +0.4 |
| gated_equation_resolved | 30.7 | 33.5 | 34.4 | 35.2 | +0.4 |

The ORACLE GAP is the best single evaluation cell (depth 32 at cap 512, 35.7 points over 2137 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none.

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
