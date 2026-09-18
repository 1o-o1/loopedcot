# Table 1 -- arc (huginn_0125), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 53783 layer passes over 938 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 40.5 | +1.3 |
| default_cell | n/a | n/a | n/a | 41.4 (53%) | +0.4 |
| default_at_budget | n/a | n/a | n/a | 40.8 (94%) | +1.0 |
| lookup | 29.2 | 39.9 | 41.8 | 41.9 | -0.1 |
| equation | 28.0 | 39.0 | 39.4 | 39.8 | +2.0 |
| equation_n30 | 26.0 | 26.0 | 26.0 | 39.3 | +2.5 |
| equation_n100 | 23.9 | 37.8 | 39.4 | 40.8 | +1.0 |
| gated_equation | 27.5 | 38.8 | 39.4 | 40.6 (94%) | +1.2 |
| avg_lookup | 32.4 | 41.9 | 42.6 | 40.6 | +1.2 |
| avg_equation | 32.2 | 38.7 | 39.6 | 40.6 | +1.2 |
| avg_gated_lookup | 33.2 | 38.6 | 39.6 | 40.5 | +1.3 |

The ORACLE GAP is the best single evaluation cell (depth 16 at cap 0, 41.8 points over 938 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0.

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 13466 vs 13446 (+0.1%) | 26702 vs 26892 (-0.7%) | 40736 vs 40337 (+1.0%) | 53850 vs 53783 (+0.1%) |
| avg_equation | 13586 vs 13446 (+1.0%) | 26930 vs 26892 (+0.1%) | 40622 vs 40337 (+0.7%) | 53619 vs 53783 (-0.3%) |
| avg_gated_lookup | 13246 vs 13446 (-1.5%) | 26925 vs 26892 (+0.1%) | 40622 vs 40337 (+0.7%) | 53856 vs 53783 (+0.1%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
