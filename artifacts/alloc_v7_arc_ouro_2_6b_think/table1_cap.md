# Table 1 -- arc (ouro_2_6b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 89582 layer passes over 938 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 96.8 | +0.0 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 92.2 | 92.6 | 94.0 | 94.0 | +2.8 |
| lookup | 92.2 | 92.2 | 92.2 | 96.5 | +0.3 |
| equation | 92.2 | 94.8 | 94.0 | 96.5 | +0.3 |
| equation_n100 | 92.2 | 94.8 | 94.8 | 96.5 | +0.3 |
| equation_n30 | 92.2 | 92.2 | 94.0 | 94.0 | +2.8 |
| equation_resolved | 92.2 | 92.2 | 92.2 | 96.5 | +0.3 |
| gated_equation | 92.2 | 92.6 | 94.0 | 94.0 | +2.8 |
| gated_equation_resolved | 92.2 | 92.6 | 94.0 | 94.0 | +2.8 |
| avg_gated_equation_resolved | 92.2 | 92.6 | 94.0 | 94.0 | +2.8 |
| avg_gated_lookup | 92.2 | 92.6 | 94.0 | 94.0 | +2.8 |
| avg_lookup | 92.2 | 92.2 | 92.2 | 92.2 | +4.6 |
| avg_equation | 92.2 | 92.2 | 92.2 | 96.5 | +0.3 |
| avg_equation_resolved | 92.2 | 92.2 | 92.2 | 92.2 | +4.6 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 4096, 96.8 points over 938 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 14976 vs 22396 (-33.1%) | 27264 vs 44791 (-39.1%) | 51840 vs 67187 (-22.8%) | 51840 vs 89582 (-42.1%) |
| avg_gated_lookup | 14976 vs 22396 (-33.1%) | 27264 vs 44791 (-39.1%) | 51840 vs 67187 (-22.8%) | 51840 vs 89582 (-42.1%) |
| avg_lookup | 11232 vs 22396 (-49.8%) | 11232 vs 44791 (-74.9%) | 11232 vs 67187 (-83.3%) | 11232 vs 89582 (-87.5%) |
| avg_equation | 11232 vs 22396 (-49.8%) | 11232 vs 44791 (-74.9%) | 11232 vs 67187 (-83.3%) | 75744 vs 89582 (-15.4%) |
| avg_equation_resolved | 11232 vs 22396 (-49.8%) | 11232 vs 44791 (-74.9%) | 11232 vs 67187 (-83.3%) | 11232 vs 89582 (-87.5%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T64: 938 | 14976 | 789120 (over) vs 789120 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T128: 938 | 27264 | 789120 (over) vs 789120 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T256: 938 | 51840 | 789120 (over) vs 789120 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T256: 938 | 51840 | 789120 (over) vs 789120 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T64: 938 | 14976 | 789120 (over) vs 789120 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T128: 938 | 27264 | 789120 (over) vs 789120 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T256: 938 | 51840 | 789120 (over) vs 789120 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T256: 938 | 51840 | 789120 (over) vs 789120 (over) |
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -1.4 points, sd 1.4, bar 0.50 sd (70 verification questions, the ids after the 164 that fit, out of 234 calibration); cost saving 33.1% of the budget, 16.7% of the default cost. Mirror fold -0.6 points, sd 1.1 on 164 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (70 verification questions, the ids after the 164 that fit, out of 234 calibration); cost saving 39.1% of the budget, 30.4% of the default cost. Mirror fold -0.6 points, sd 1.1 on 164 questions (fails).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -2.9 points, sd 2.0, bar 0.50 sd (70 verification questions, the ids after the 164 that fit, out of 234 calibration); cost saving 22.8% of the budget, 57.9% of the default cost. Mirror fold -0.6 points, sd 1.4 on 164 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -2.9 points, sd 2.0, bar 0.50 sd (70 verification questions, the ids after the 164 that fit, out of 234 calibration); cost saving 42.1% of the budget, 57.9% of the default cost. Mirror fold +0.0 points, sd 0.9 on 164 questions (fails).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -1.4 points, sd 1.4, bar 0.50 sd (70 verification questions, the ids after the 164 that fit, out of 234 calibration); cost saving 33.1% of the budget, 16.7% of the default cost. Mirror fold -0.6 points, sd 1.1 on 164 questions (fails).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (70 verification questions, the ids after the 164 that fit, out of 234 calibration); cost saving 39.1% of the budget, 30.4% of the default cost. Mirror fold -0.6 points, sd 1.1 on 164 questions (fails).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -2.9 points, sd 2.0, bar 0.50 sd (70 verification questions, the ids after the 164 that fit, out of 234 calibration); cost saving 22.8% of the budget, 57.9% of the default cost. Mirror fold -0.6 points, sd 1.4 on 164 questions (fails).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -2.9 points, sd 2.0, bar 0.50 sd (70 verification questions, the ids after the 164 that fit, out of 234 calibration); cost saving 42.1% of the budget, 57.9% of the default cost. Mirror fold +0.0 points, sd 0.9 on 164 questions (fails).

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
