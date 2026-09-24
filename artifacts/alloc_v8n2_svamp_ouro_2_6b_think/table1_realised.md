# Table 1 -- svamp (ouro_2_6b_think), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 146673 layer passes over 200 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 83.0 | +0.0 |
| default_cell | n/a | 96.4 (42%) | 94.6 (74%) | 91.6 (83%) | -8.6 |
| default_at_budget | 14.0 | 52.5 | 76.0 | 78.5 | +4.5 |
| lookup | 70.0 | 80.5 | 77.5 | 77.0 | +6.0 |
| equation | 69.0 | 79.5 | 79.5 | 80.0 | +3.0 |
| equation_n100 | 69.0 | 79.5 | 79.5 | 80.0 | +3.0 |
| equation_n30 | 69.0 | 78.5 | 79.5 | 79.5 | +3.5 |
| equation_resolved | 70.0 | 81.0 | 82.5 | 83.0 | +0.0 |
| gated_equation | 27.0 | 71.0 | 76.5 | 76.5 | +6.5 |
| gated_equation_resolved | 27.0 | 71.0 | 76.5 | 76.5 | +6.5 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 4096, 83.0 points over 200 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2. Of the families that CLEAR the bar the one that RUNS is set by `policy.GATE_FAMILY_RULE` = `best`: the cleared family with the largest mean verified margin over the folds, ties to the smaller family. The folds, the bar, the reference and the pricing are the same test under either rule; only which cleared family is taken differs.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
