# Table 1 -- bbh (ouro_1_4b_base), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 100521 layer passes over 2137 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 75.8 | +0.0 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 75.5 (10%) | 79.1 (10%) | 79.4 (30%) | 59.8 (87%) | +16.0 |
| lookup | 34.1 (87%) | 46.6 | 58.5 | 65.4 | +10.4 |
| equation | 34.1 (87%) | 46.6 | 63.4 | 68.6 | +7.2 |
| equation_n30 | 34.1 (87%) | 46.3 | 57.3 | 58.9 | +16.9 |
| equation_n100 | 34.1 (87%) | 46.6 | 63.4 | 68.6 | +7.2 |
| gated_equation | 35.3 (87%) | 46.3 | 57.8 | 56.2 | +19.7 |
| avg_lookup | 31.8 | 53.9 | 63.5 | 70.7 | +5.1 |
| avg_equation | 34.9 | 50.4 | 63.7 | 70.7 | +5.1 |
| avg_gated_lookup | 36.2 | 54.7 | 68.2 | 70.8 | +5.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 2048, 75.8 points over 2137 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 23791 vs 25130 (-5.3%) | 49723 vs 50261 (-1.1%) | 75377 vs 75391 (-0.0%) | 99620 vs 100521 (-0.9%) |
| avg_equation | 24963 vs 25130 (-0.7%) | 49212 vs 50261 (-2.1%) | 74094 vs 75391 (-1.7%) | 99620 vs 100521 (-0.9%) |
| avg_gated_lookup | 25664 vs 25130 (+2.1%) | 52992 vs 50261 (+5.4%) | 79519 vs 75391 (+5.5%) | 103330 vs 100521 (+2.8%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
