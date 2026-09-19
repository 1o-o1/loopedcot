# Table 1 -- strategyqa (mcleish_llama32_r32), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 41981 layer passes over 1990 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 49.7 | +1.6 |
| default_cell | 50.8 (83%) | 50.8 (83%) | 50.8 (83%) | 50.8 (83%) | +0.5 |
| default_at_budget | 50.6 | 50.8 | 50.7 | 50.7 | +0.7 |
| lookup | 50.5 | 50.6 | 50.7 | 50.7 | +0.7 |
| equation | 50.6 | 50.8 | 50.7 | 50.7 | +0.7 |
| equation_n100 | 50.6 | 50.8 | 50.7 | 50.7 | +0.7 |
| equation_n30 | 50.6 | 50.8 | 50.7 | 50.7 | +0.7 |
| equation_resolved | 50.5 | 50.8 | 50.7 | 50.7 | +0.7 |
| gated_equation | 50.6 | 50.8 | 50.7 | 50.7 | +0.7 |
| gated_equation_resolved | 50.6 | 50.8 | 50.7 | 50.7 | +0.7 |

The ORACLE GAP is the best single evaluation cell (depth 8 at cap 0, 51.3 points over 1990 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none.

`default_cell` is the default operating point (depth 8 at cap 8192) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
