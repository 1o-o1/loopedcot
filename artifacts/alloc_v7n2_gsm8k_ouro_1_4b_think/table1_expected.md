# Table 1 -- gsm8k (ouro_1_4b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 78375 layer passes over 1056 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 92.9 | +0.0 |
| default_cell | n/a | n/a | n/a | 92.9 | +0.0 |
| default_at_budget | 27.2 | 59.8 | 88.2 | 92.9 | +0.0 |
| lookup | 55.0 | 86.1 | 91.4 | 92.8 | +0.1 |
| equation | 55.0 | 86.1 | 91.4 | 92.9 | +0.0 |
| equation_n100 | 55.0 | 86.1 | 91.4 | 92.9 | +0.0 |
| equation_n30 | 55.0 | 83.6 | 91.4 | 92.9 | +0.0 |
| equation_resolved | 55.0 | 86.1 | 91.4 | 92.9 | +0.0 |
| gated_equation | 55.0 | 86.1 | 91.4 | 92.9 | +0.0 |
| gated_equation_resolved | 55.0 | 86.1 | 91.4 | 92.9 | +0.0 |
| avg_gated_equation_resolved | 55.0 | 86.1 | 91.4 | 92.9 | +0.0 |
| avg_gated_lookup | 55.0 | 86.1 | 91.4 | 92.9 | +0.0 |
| avg_lookup | 55.0 | 86.1 | 91.3 | 92.8 | +0.1 |
| avg_equation | 55.0 | 86.1 | 91.4 | 92.9 | +0.0 |
| avg_equation_resolved | 55.0 | 86.1 | 91.3 | 92.9 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 4096, 92.9 points over 1056 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 13141 vs 19594 (-32.9%) | 35351 vs 39188 (-9.8%) | 57928 vs 58782 (-1.5%) | 74401 vs 78375 (-5.1%) |
| avg_gated_lookup | 13141 vs 19594 (-32.9%) | 35351 vs 39188 (-9.8%) | 57928 vs 58782 (-1.5%) | 74401 vs 78375 (-5.1%) |
| avg_lookup | 13141 vs 19594 (-32.9%) | 35351 vs 39188 (-9.8%) | 51192 vs 58782 (-12.9%) | 67487 vs 78375 (-13.9%) |
| avg_equation | 13141 vs 19594 (-32.9%) | 35351 vs 39188 (-9.8%) | 57928 vs 58782 (-1.5%) | 74401 vs 78375 (-5.1%) |
| avg_equation_resolved | 13141 vs 19594 (-32.9%) | 35351 vs 39188 (-9.8%) | 51192 vs 58782 (-12.9%) | 74401 vs 78375 (-5.1%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 1056 | 14016 | 74401 (over) vs 74401 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T256: 1056 | 26304 | 74401 (over) vs 74401 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T512: 1056 | 47064 | 74401 (over) vs 74401 (over) |
| 1.00x | default_cell | 4 | k4_T4096: 1056 | 74401 | 74401 (fits) vs 74401 (fits) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 1056 | 14016 | 74401 (over) vs 74401 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T256: 1056 | 26304 | 74401 (over) vs 74401 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T512: 1056 | 47064 | 74401 (over) vs 74401 (over) |
| 1.00x | default_cell | 4 | k4_T4096: 1056 | 74401 | 74401 (fits) vs 74401 (fits) |
- `avg_gated_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 91.4 points at 73.9% of the default cost, 1.5% under the budget it was given.
- `avg_gated_equation_resolved` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F3. Verification margin +27.8 points, sd 6.2, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 32.9% of the budget, 16.8% of the default cost. Mirror fold +28.3 points, sd 3.7 on 184 questions (clears).
- `avg_gated_equation_resolved` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +32.9 points, sd 5.4, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 9.8% of the budget, 45.1% of the default cost. Mirror fold +24.5 points, sd 3.7 on 184 questions (clears).
- `avg_gated_equation_resolved` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +7.6 points, sd 3.5, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 1.5% of the budget, 73.9% of the default cost. Mirror fold +7.1 points, sd 2.6 on 184 questions (clears).
- `avg_gated_equation_resolved` at 1.00x: reverted to the default cell for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 5.1% of the budget, 94.9% of the default cost. Mirror fold -1.6 points, sd 1.6 on 184 questions (fails).
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 91.4 points at 73.9% of the default cost, 1.5% under the budget it was given.
- `avg_gated_lookup` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F3. Verification margin +27.8 points, sd 6.2, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 32.9% of the budget, 16.8% of the default cost. Mirror fold +28.3 points, sd 3.7 on 184 questions (clears).
- `avg_gated_lookup` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +32.9 points, sd 5.4, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 9.8% of the budget, 45.1% of the default cost. Mirror fold +24.5 points, sd 3.7 on 184 questions (clears).
- `avg_gated_lookup` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +7.6 points, sd 3.5, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 1.5% of the budget, 73.9% of the default cost. Mirror fold +6.5 points, sd 2.5 on 184 questions (clears).
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 5.1% of the budget, 94.9% of the default cost. Mirror fold -2.2 points, sd 1.7 on 184 questions (fails).
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 92.8 points at 86.1% of the default cost, 13.9% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 92.9 points at 94.9% of the default cost, 5.1% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 92.9 points at 94.9% of the default cost, 5.1% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
