# Table 1 -- bbh (huginn_0125), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 142482 layer passes over 2137 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 35.6 | +0.1 |
| default_cell | 60.0 (2%) | 54.1 (10%) | 53.0 (30%) | 46.9 (63%) | -11.2 |
| default_at_budget | 57.3 (10%) | 60.1 (21%) | 52.4 (42%) | 36.3 (88%) | -0.7 |
| lookup | 31.6 | 34.5 | 32.7 | 33.7 | +2.0 |
| equation | 29.0 | 34.3 | 35.2 | 35.9 | -0.2 |
| equation_n30 | 31.4 | 34.5 | 32.0 | 32.2 | +3.5 |
| equation_n100 | 29.1 | 27.5 | 31.6 | 35.8 | -0.2 |
| gated_equation | 30.2 | 33.9 | 34.7 | 34.8 | +0.8 |

The ORACLE GAP is the best single evaluation cell (depth 32 at cap 512, 35.7 points over 2137 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none.

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
