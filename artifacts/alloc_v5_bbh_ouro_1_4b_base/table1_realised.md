# Table 1 -- bbh (ouro_1_4b_base), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 100521 layer passes over 2137 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 75.8 | +0.0 |
| default_cell | n/a | 79.1 (10%) | 84.2 (20%) | 82.7 (61%) | -6.9 |
| default_at_budget | 75.5 (10%) | 79.1 (10%) | 80.5 (30%) | 62.8 (87%) | +13.0 |
| lookup | 35.1 (87%) | 48.5 | 64.3 | 71.9 | +3.9 |
| equation | 35.2 (87%) | 48.3 | 64.5 | 72.0 | +3.8 |
| equation_n30 | 35.2 (87%) | 48.2 | 64.3 | 72.2 | +3.6 |
| equation_n100 | 35.2 (87%) | 48.3 | 64.5 | 72.0 | +3.8 |
| gated_equation | 35.0 (87%) | 48.1 | 64.2 | 62.0 | +13.8 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 2048, 75.8 points over 2137 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
