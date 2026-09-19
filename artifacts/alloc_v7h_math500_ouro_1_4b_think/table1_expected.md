# Table 1 -- math500 (ouro_1_4b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 205663 layer passes over 400 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 89.5 | +0.5 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 36.8 | 75.5 | 83.8 | 89.5 | +0.5 |
| lookup | 59.5 | 75.5 | 87.8 | 89.2 | +0.8 |
| equation | 59.5 | 75.8 | 87.8 | 89.2 | +0.8 |
| equation_n100 | 59.5 | 75.8 | 87.8 | 89.2 | +0.8 |
| equation_n30 | 59.5 | 75.8 | 87.8 | 89.2 | +0.8 |
| equation_resolved | 59.5 | 75.5 | 87.8 | 89.2 | +0.8 |
| gated_equation | 59.5 | 75.5 | 83.8 | 89.5 | +0.5 |
| gated_equation_resolved | 59.5 | 75.5 | 83.8 | 89.5 | +0.5 |
| avg_gated_equation_resolved | 36.8 | 75.5 | 83.8 | 89.5 | +0.5 |
| avg_gated_lookup | 36.8 | 75.5 | 83.8 | 89.5 | +0.5 |
| avg_lookup | 59.5 | 75.8 | 87.8 | 89.2 | +0.8 |
| avg_equation | 59.5 | 75.8 | 87.8 | 89.2 | +0.8 |
| avg_equation_resolved | 59.5 | 75.8 | 87.8 | 89.2 | +0.8 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 8192, 90.0 points over 400 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2.

`default_cell` is the default operating point (depth 4 at cap 8192) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 28224 vs 51416 (-45.1%) | 92331 vs 102832 (-10.2%) | 141930 vs 154248 (-8.0%) | 197228 vs 205663 (-4.1%) |
| avg_gated_lookup | 28224 vs 51416 (-45.1%) | 92331 vs 102832 (-10.2%) | 141930 vs 154248 (-8.0%) | 197228 vs 205663 (-4.1%) |
| avg_lookup | 39177 vs 51416 (-23.8%) | 68964 vs 102832 (-32.9%) | 144199 vs 154248 (-6.5%) | 194948 vs 205663 (-5.2%) |
| avg_equation | 39177 vs 51416 (-23.8%) | 68964 vs 102832 (-32.9%) | 144199 vs 154248 (-6.5%) | 194948 vs 205663 (-5.2%) |
| avg_equation_resolved | 39177 vs 51416 (-23.8%) | 68964 vs 102832 (-32.9%) | 144199 vs 154248 (-6.5%) | 194948 vs 205663 (-5.2%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T256: 400 | 28224 | 266586 (over) vs 266586 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T1024: 400 | 92331 | 266586 (over) vs 266586 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T2048: 400 | 141930 | 266586 (over) vs 266586 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T4096: 400 | 197228 | 266586 (over) vs 266586 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T256: 400 | 28224 | 266586 (over) vs 266586 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T1024: 400 | 92331 | 266586 (over) vs 266586 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T2048: 400 | 141930 | 266586 (over) vs 266586 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T4096: 400 | 197228 | 266586 (over) vs 266586 (over) |
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +26.7 points, sd 8.2, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 45.1% of the budget, 13.7% of the default cost. Mirror fold -12.9 points, sd 4.4 on 70 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -3.3 points, sd 5.7, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 10.2% of the budget, 44.9% of the default cost. Mirror fold +0.0 points, sd 3.4 on 70 questions (fails).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -3.3 points, sd 3.2, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 8.0% of the budget, 69.0% of the default cost. Mirror fold +0.0 points, sd 0.0 on 70 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -3.3 points, sd 3.2, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 4.1% of the budget, 95.9% of the default cost. Mirror fold -5.7 points, sd 3.4 on 70 questions (fails).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +26.7 points, sd 8.2, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 45.1% of the budget, 13.7% of the default cost. Mirror fold -12.9 points, sd 4.4 on 70 questions (fails).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -3.3 points, sd 5.7, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 10.2% of the budget, 44.9% of the default cost. Mirror fold +0.0 points, sd 3.4 on 70 questions (fails).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -10.0 points, sd 5.5, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 8.0% of the budget, 69.0% of the default cost. Mirror fold +0.0 points, sd 0.0 on 70 questions (fails).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -3.3 points, sd 3.2, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 4.1% of the budget, 95.9% of the default cost. Mirror fold -5.7 points, sd 3.4 on 70 questions (fails).

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
