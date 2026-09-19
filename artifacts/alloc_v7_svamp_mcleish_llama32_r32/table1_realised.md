# Table 1 -- svamp (mcleish_llama32_r32), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 3002 layer passes over 200 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 69.0 | +0.0 |
| default_cell | n/a | n/a | 84.7 (36%) | 79.8 (60%) | -10.8 |
| default_at_budget | 9.0 | 9.0 | 39.0 | 52.5 | +16.5 |
| lookup | 25.0 | 49.5 | 58.5 | 65.0 | +4.0 |
| equation | 26.5 | 56.0 | 61.5 | 65.0 | +4.0 |
| equation_n100 | 26.5 | 56.0 | 61.5 | 65.0 | +4.0 |
| equation_n30 | 26.5 | 56.0 | 61.5 | 65.0 | +4.0 |
| equation_resolved | 25.0 | 49.5 | 58.5 | 65.0 | +4.0 |
| gated_equation | 26.5 | 49.5 | 38.0 | 52.5 | +16.5 |
| gated_equation_resolved | 25.0 | 49.5 | 38.0 | 52.5 | +16.5 |

The ORACLE GAP is the best single evaluation cell (depth 8 at cap 128, 69.0 points over 200 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3.

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
