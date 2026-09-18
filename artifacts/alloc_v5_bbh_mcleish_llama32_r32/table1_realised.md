# Table 1 -- bbh (mcleish_llama32_r32), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 69931 layer passes over 2137 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 43.5 | +0.2 |
| default_cell | 50.0 (10%) | 54.6 (16%) | 56.8 (45%) | 47.3 (88%) | -3.6 |
| default_at_budget | 50.0 (10%) | 55.6 (31%) | 42.9 (72%) | 43.5 (99%) | +0.3 |
| lookup | 32.5 (99%) | 40.7 | 42.7 | 43.5 | +0.2 |
| equation | 33.9 (99%) | 41.7 | 43.1 | 43.4 | +0.3 |
| equation_n30 | 34.0 (99%) | 34.3 | 35.4 | 43.9 | -0.2 |
| equation_n100 | 34.1 (99%) | 38.7 | 42.3 | 43.4 | +0.3 |
| gated_equation | 33.9 (99%) | 41.7 | 42.7 | 42.7 | +1.0 |

The ORACLE GAP is the best single evaluation cell (depth 8 at cap 512, 43.7 points over 2137 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3.

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
