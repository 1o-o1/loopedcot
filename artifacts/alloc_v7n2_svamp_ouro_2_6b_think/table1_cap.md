# Table 1 -- svamp (ouro_2_6b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 146673 layer passes over 200 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 83.0 | +0.0 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 14.0 | 30.5 | 76.0 | 76.0 | +7.0 |
| lookup | 64.5 | 79.0 | 79.0 | 79.0 | +4.0 |
| equation | 67.5 | 79.0 | 79.5 | 79.5 | +3.5 |
| equation_n100 | 67.5 | 79.0 | 79.5 | 79.5 | +3.5 |
| equation_n30 | 67.5 | 79.0 | 79.5 | 79.5 | +3.5 |
| equation_resolved | 64.5 | 79.0 | 79.0 | 79.0 | +4.0 |
| gated_equation | 21.5 | 36.5 | 76.0 | 76.0 | +7.0 |
| gated_equation_resolved | 21.5 | 36.5 | 76.0 | 76.0 | +7.0 |
| avg_gated_equation_resolved | 16.5 | 79.0 | 76.0 | 76.0 | +7.0 |
| avg_gated_lookup | 16.5 | 79.0 | 76.0 | 76.0 | +7.0 |
| avg_lookup | 53.0 | 79.0 | 79.0 | 79.0 | +4.0 |
| avg_equation | 67.5 | 79.0 | 79.5 | 79.5 | +3.5 |
| avg_equation_resolved | 64.5 | 79.0 | 79.0 | 79.0 | +4.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 4096, 83.0 points over 200 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 4320 vs 36668 (-88.2%) | 50496 vs 73336 (-31.1%) | 100992 vs 110004 (-8.2%) | 100992 vs 146673 (-31.1%) |
| avg_gated_lookup | 4320 vs 36668 (-88.2%) | 50496 vs 73336 (-31.1%) | 100992 vs 110004 (-8.2%) | 100992 vs 146673 (-31.1%) |
| avg_lookup | 12960 vs 36668 (-64.7%) | 50496 vs 73336 (-31.1%) | 50496 vs 110004 (-54.1%) | 50496 vs 146673 (-65.6%) |
| avg_equation | 25248 vs 36668 (-31.1%) | 50496 vs 73336 (-31.1%) | 99648 vs 110004 (-9.4%) | 99648 vs 146673 (-32.1%) |
| avg_equation_resolved | 25920 vs 36668 (-29.3%) | 50496 vs 73336 (-31.1%) | 50496 vs 110004 (-54.1%) | 50496 vs 146673 (-65.6%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 200 | 27264 | 789120 (over) vs 789120 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T256: 200 | 51840 | 789120 (over) vs 789120 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T512: 200 | 100992 | 789120 (over) vs 789120 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T512: 200 | 100992 | 789120 (over) vs 789120 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 200 | 27264 | 789120 (over) vs 789120 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T256: 200 | 51840 | 789120 (over) vs 789120 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T512: 200 | 100992 | 789120 (over) vs 789120 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T512: 200 | 100992 | 789120 (over) vs 789120 (over) |
- `avg_gated_equation_resolved` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +6.7 points, sd 4.5, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 88.2% of the budget, 2.9% of the default cost. Mirror fold +2.9 points, sd 5.6 on 70 questions (clears).
- `avg_gated_equation_resolved` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F3. Verification margin +30.0 points, sd 8.4, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 31.1% of the budget, 34.4% of the default cost. Mirror fold +64.3 points, sd 5.8 on 70 questions (clears).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 6.8, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 8.2% of the budget, 68.9% of the default cost. Mirror fold +12.9 points, sd 5.7 on 70 questions (clears).
- `avg_gated_equation_resolved` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 6.8, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 31.1% of the budget, 68.9% of the default cost. Mirror fold +12.9 points, sd 5.7 on 70 questions (clears).
- `avg_gated_lookup` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +6.7 points, sd 4.5, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 88.2% of the budget, 2.9% of the default cost. Mirror fold +2.9 points, sd 5.6 on 70 questions (clears).
- `avg_gated_lookup` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F3. Verification margin +30.0 points, sd 8.4, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 31.1% of the budget, 34.4% of the default cost. Mirror fold +64.3 points, sd 5.8 on 70 questions (clears).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 6.8, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 8.2% of the budget, 68.9% of the default cost. Mirror fold +12.9 points, sd 5.7 on 70 questions (clears).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 6.8, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 31.1% of the budget, 68.9% of the default cost. Mirror fold +12.9 points, sd 5.7 on 70 questions (clears).

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
