# Table 1 -- math500 (mcleish_llama32_r32), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 80576 layer passes over 400 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 30.0 | +0.2 |
| default_cell | 36.6 (77%) | 34.7 (84%) | 34.7 (84%) | 34.7 (84%) | -4.5 |
| default_at_budget | 29.5 | 30.0 | 29.8 | 29.8 | +0.5 |
| lookup | 28.7 | 28.7 | 28.7 | 28.7 | +1.5 |
| equation | 29.5 | 30.0 | 29.8 | 29.8 | +0.5 |
| equation_n100 | 29.5 | 30.0 | 29.8 | 29.8 | +0.5 |
| equation_n30 | 29.5 | 30.0 | 29.8 | 29.8 | +0.5 |
| equation_resolved | 28.7 | 28.7 | 28.7 | 28.7 | +1.5 |
| gated_equation | 29.5 | 30.0 | 29.8 | 29.8 | +0.5 |
| gated_equation_resolved | 29.5 | 30.0 | 29.8 | 29.8 | +0.5 |

The ORACLE GAP is the best single evaluation cell (depth 8 at cap 4096, 30.2 points over 400 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none.

`default_cell` is the default operating point (depth 8 at cap 8192) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
