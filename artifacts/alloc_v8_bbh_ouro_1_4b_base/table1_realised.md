# Table 1 -- bbh (ouro_1_4b_base), realised accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 23044 layer passes over 2137 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 75.8 | +0.0 |
| default_cell | 81.3 (12%) | 77.4 (33%) | 80.9 (68%) | 79.6 (79%) | -3.8 |
| default_at_budget | 45.4 | 51.6 | 61.8 | 64.6 | +11.2 |
| lookup | 45.5 | 60.4 | 63.9 | 74.0 | +1.8 |
| equation | 45.6 | 60.5 | 64.0 | 74.0 | +1.8 |
| equation_n100 | 45.5 | 60.5 | 64.0 | 74.0 | +1.8 |
| equation_n30 | 42.4 | 59.7 | 71.2 | 73.8 | +2.0 |
| equation_resolved | 45.5 | 60.4 | 63.9 | 74.0 | +1.8 |
| gated_equation | 45.4 | 51.6 | 61.8 | 64.6 | +11.2 |
| gated_equation_resolved | 45.4 | 51.6 | 61.8 | 64.6 | +11.2 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 2048, 75.8 points over 2137 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none. Of the families that CLEAR the bar the one that RUNS is set by `policy.GATE_FAMILY_RULE` = `best`: the cleared family with the largest mean verified margin over the folds, ties to the smaller family. The folds, the bar, the reference and the pricing are the same test under either rule; only which cleared family is taken differs.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under realised accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
