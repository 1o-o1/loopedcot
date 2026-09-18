# Table 1 -- svamp (mcleish_llama32_r32), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 32123 layer passes over 200 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 69.0 | +0.0 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | n/a | 50.0 | +19.0 |
| lookup | 22.5 | 33.0 | 62.0 | 62.0 | +7.0 |
| equation | 22.5 | 39.0 | 63.0 | 63.0 | +6.0 |
| equation_n30 | 22.5 | 39.0 | 63.0 | 63.0 | +6.0 |
| equation_n100 | 22.5 | 39.0 | 63.0 | 63.0 | +6.0 |
| gated_equation | 22.5 | 39.0 | 63.0 | 50.5 | +18.5 |
| avg_lookup | 25.0 | 50.5 | 66.0 | 68.0 | +1.0 |
| avg_equation | 24.0 | 54.0 | 63.0 | 68.5 | +0.5 |
| avg_gated_lookup | 26.5 | 51.5 | 65.5 | 68.0 | +1.0 |

The ORACLE GAP is the best single evaluation cell (depth 8 at cap 128, 69.0 points over 200 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F3.

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 8046 vs 8031 (+0.2%) | 16743 vs 16062 (+4.2%) | 25664 vs 24092 (+6.5%) | 33352 vs 32123 (+3.8%) |
| avg_equation | 8039 vs 8031 (+0.1%) | 16390 vs 16062 (+2.0%) | 24900 vs 24092 (+3.4%) | 33671 vs 32123 (+4.8%) |
| avg_gated_lookup | 8179 vs 8031 (+1.8%) | 16547 vs 16062 (+3.0%) | 25215 vs 24092 (+4.7%) | 33262 vs 32123 (+3.5%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
