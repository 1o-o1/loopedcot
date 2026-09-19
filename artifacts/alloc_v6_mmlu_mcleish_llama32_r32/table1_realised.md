# Table 1 -- mmlu (mcleish_llama32_r32), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 16072 layer passes over 1700 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 37.4 | +1.1 |
| default_cell | 37.6 (77%) | 38.4 (93%) | 38.3 (94%) | 38.3 (94%) | +0.2 |
| default_at_budget | 35.5 | 37.7 | 37.8 | 37.7 | +0.8 |
| lookup | 36.6 | 36.7 | 36.7 | 36.7 | +1.8 |
| equation | 36.6 | 36.5 | 36.5 | 36.5 | +1.9 |
| equation_n100 | 36.6 | 36.5 | 36.5 | 36.5 | +1.9 |
| equation_n30 | 36.6 | 36.5 | 36.5 | 36.5 | +1.9 |
| equation_resolved | 36.6 | 36.7 | 36.7 | 36.7 | +1.8 |
| gated_equation | 36.6 | 36.5 | 36.5 | 36.5 | +1.9 |
| gated_equation_resolved | 37.1 | 36.7 | 36.7 | 36.7 | +1.8 |

The ORACLE GAP is the best single evaluation cell (depth 8 at cap 0, 38.5 points over 1700 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2.

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
