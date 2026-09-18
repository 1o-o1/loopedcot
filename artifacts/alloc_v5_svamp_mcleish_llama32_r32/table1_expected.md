# Table 1 -- svamp (mcleish_llama32_r32), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 32123 layer passes over 200 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 69.0 | +0.0 |
| default_cell | n/a | n/a | n/a | 77.2 (50%) | -8.2 |
| default_at_budget | n/a | n/a | n/a | 56.5 | +12.5 |
| lookup | 22.5 | 33.0 | 62.0 | 66.5 | +2.5 |
| equation | 24.0 | 39.0 | 63.0 | 67.0 | +2.0 |
| equation_n30 | 24.0 | 39.0 | 63.0 | 67.0 | +2.0 |
| equation_n100 | 24.0 | 39.0 | 63.0 | 67.0 | +2.0 |
| gated_equation | 24.0 | 39.0 | 63.0 | 57.0 | +12.0 |
| avg_lookup | 26.5 | 53.5 | 66.5 | 68.5 | +0.5 |
| avg_equation | 25.5 | 56.5 | 67.0 | 68.5 | +0.5 |
| avg_gated_lookup | 25.5 | 52.5 | 66.5 | 68.5 | +0.5 |

The ORACLE GAP is the best single evaluation cell (depth 8 at cap 128, 69.0 points over 200 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F3.

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 8144 vs 8031 (+1.4%) | 16543 vs 16062 (+3.0%) | 25213 vs 24092 (+4.7%) | 32048 vs 32123 (-0.2%) |
| avg_equation | 7994 vs 8031 (-0.5%) | 16737 vs 16062 (+4.2%) | 25471 vs 24092 (+5.7%) | 32062 vs 32123 (-0.2%) |
| avg_gated_lookup | 8260 vs 8031 (+2.9%) | 16437 vs 16062 (+2.3%) | 25213 vs 24092 (+4.7%) | 32048 vs 32123 (-0.2%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
