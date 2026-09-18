# Table 1 -- aqua (ouro_1_4b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 223283 layer passes over 154 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 82.5 | +2.6 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 58.4 | 78.6 | 83.1 | +1.9 |
| lookup | 52.6 | 81.2 | 84.4 | 83.1 | +1.9 |
| equation | 52.6 | 81.2 | 84.4 | 85.1 | +0.0 |
| equation_n30 | 52.6 | 81.2 | 84.4 | 85.1 | +0.0 |
| equation_n100 | 52.6 | 81.2 | 84.4 | 85.1 | +0.0 |
| gated_equation | 51.3 | 81.2 | 84.4 | 85.1 | +0.0 |
| avg_lookup | 64.9 | 81.2 | 82.5 | 85.1 | +0.0 |
| avg_equation | 64.9 | 79.9 | 85.1 | 85.1 | +0.0 |
| avg_gated_lookup | 64.3 | 81.2 | 84.4 | 81.8 | +3.2 |

The ORACLE GAP is the best single evaluation cell (depth 3 at cap 4096, 85.1 points over 154 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 52725 vs 55821 (-5.5%) | 113457 vs 111641 (+1.6%) | 168226 vs 167462 (+0.5%) | 217490 vs 223283 (-2.6%) |
| avg_equation | 52725 vs 55821 (-5.5%) | 112706 vs 111641 (+1.0%) | 166936 vs 167462 (-0.3%) | 219021 vs 223283 (-1.9%) |
| avg_gated_lookup | 53478 vs 55821 (-4.2%) | 118936 vs 111641 (+6.5%) | 163463 vs 167462 (-2.4%) | 216802 vs 223283 (-2.9%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
