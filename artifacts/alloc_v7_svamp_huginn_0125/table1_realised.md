# Table 1 -- svamp (huginn_0125), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 8195 layer passes over 200 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 44.5 | +0.0 |
| default_cell | n/a | 100.0 (2%) | 63.0 (36%) | 52.2 (57%) | -7.7 |
| default_at_budget | 2.0 | 20.0 | 30.0 | 33.0 | +11.5 |
| lookup | 16.0 | 31.0 | 40.0 | 40.0 | +4.5 |
| equation | 19.0 | 31.0 | 42.5 | 42.0 | +2.5 |
| equation_n100 | 19.0 | 31.0 | 42.5 | 42.0 | +2.5 |
| equation_n30 | 19.0 | 20.5 | 20.0 | 20.0 | +24.5 |
| equation_resolved | 19.0 | 31.0 | 40.0 | 40.0 | +4.5 |
| gated_equation | 16.5 | 30.5 | 30.0 | 33.0 | +11.5 |
| gated_equation_resolved | 16.5 | 30.5 | 30.0 | 33.0 | +11.5 |

The ORACLE GAP is the best single evaluation cell (depth 32 at cap 128, 44.5 points over 200 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2.

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
