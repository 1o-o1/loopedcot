# Table 1 -- aqua (ouro_2_6b_think), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 278149 layer passes over 154 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 89.0 | +0.0 |
| default_cell | 100.0 (5%) | 100.0 (39%) | 98.9 (60%) | 98.2 (73%) | -9.3 |
| default_at_budget | 55.8 | 76.0 | 85.1 | 85.7 | +3.2 |
| lookup | 67.5 | 81.8 | 85.1 | 85.7 | +3.2 |
| equation | 67.5 | 81.8 | 85.1 | 85.7 | +3.2 |
| equation_n100 | 67.5 | 81.8 | 85.1 | 85.7 | +3.2 |
| equation_n30 | 67.5 | 79.2 | 85.1 | 85.7 | +3.2 |
| equation_resolved | 67.5 | 81.8 | 85.1 | 85.7 | +3.2 |
| gated_equation | 67.5 | 79.2 | 85.1 | 85.7 | +3.2 |
| gated_equation_resolved | 67.5 | 79.2 | 85.1 | 85.7 | +3.2 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 4096, 89.0 points over 154 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F3. Of the families that CLEAR the bar the one that RUNS is set by `policy.GATE_FAMILY_RULE` = `best`: the cleared family with the largest mean verified margin over the folds, ties to the smaller family. The folds, the bar, the reference and the pricing are the same test under either rule; only which cleared family is taken differs.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
