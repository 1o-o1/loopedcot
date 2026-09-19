# Table 1 -- gsm8k (ouro_1_4b_base), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 15588 layer passes over 1056 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 76.7 | +0.1 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 11.6 | 39.9 | 39.9 | 66.4 | +10.4 |
| lookup | 26.5 | 54.4 | 62.7 | 66.4 | +10.4 |
| equation | 26.5 | 54.4 | 62.7 | 66.4 | +10.4 |
| equation_n100 | 26.5 | 54.4 | 62.7 | 66.4 | +10.4 |
| equation_n30 | 26.5 | 54.4 | 62.7 | 66.4 | +10.4 |
| equation_resolved | 26.5 | 54.4 | 62.7 | 66.4 | +10.4 |
| gated_equation | 15.2 | 54.4 | 62.7 | 66.4 | +10.4 |
| gated_equation_resolved | 26.5 | 54.4 | 62.7 | 66.4 | +10.4 |
| avg_gated_equation_resolved | 11.6 | 54.4 | 62.7 | 66.4 | +10.4 |
| avg_gated_lookup | 11.6 | 54.4 | 62.7 | 66.4 | +10.4 |
| avg_lookup | 11.6 | 54.4 | 62.7 | 62.7 | +14.1 |
| avg_equation | 11.6 | 54.4 | 62.7 | 62.7 | +14.1 |
| avg_equation_resolved | 11.6 | 54.4 | 62.7 | 62.7 | +14.1 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 1024, 76.8 points over 1056 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 3072 vs 3897 (-21.2%) | 6912 vs 7794 (-11.3%) | 10368 vs 11691 (-11.3%) | 13824 vs 15588 (-11.3%) |
| avg_gated_lookup | 3072 vs 3897 (-21.2%) | 6912 vs 7794 (-11.3%) | 10368 vs 11691 (-11.3%) | 13824 vs 15588 (-11.3%) |
| avg_lookup | 768 vs 3897 (-80.3%) | 6912 vs 7794 (-11.3%) | 10368 vs 11691 (-11.3%) | 10368 vs 15588 (-33.5%) |
| avg_equation | 768 vs 3897 (-80.3%) | 6912 vs 7794 (-11.3%) | 10368 vs 11691 (-11.3%) | 10368 vs 15588 (-33.5%) |
| avg_equation_resolved | 768 vs 3897 (-80.3%) | 6912 vs 7794 (-11.3%) | 10368 vs 11691 (-11.3%) | 10368 vs 15588 (-33.5%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T16: 1056 | 3072 | 394752 (over) vs 394752 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T64: 1056 | 7680 | 394752 (over) vs 394752 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T64: 1056 | 7680 | 394752 (over) vs 394752 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T128: 1056 | 13824 | 394752 (over) vs 394752 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T16: 1056 | 3072 | 394752 (over) vs 394752 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T64: 1056 | 7680 | 394752 (over) vs 394752 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T64: 1056 | 7680 | 394752 (over) vs 394752 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T128: 1056 | 13824 | 394752 (over) vs 394752 (over) |
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +3.8 points, sd 4.2, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 21.2% of the budget, 19.7% of the default cost. Mirror fold -3.3 points, sd 2.9 on 184 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F3. Verification margin +25.3 points, sd 6.1, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 11.3% of the budget, 44.3% of the default cost. Mirror fold +16.3 points, sd 4.0 on 184 questions (clears).
- `avg_gated_equation_resolved` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +38.0 points, sd 6.1, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 11.3% of the budget, 66.5% of the default cost. Mirror fold +26.1 points, sd 3.5 on 184 questions (clears).
- `avg_gated_equation_resolved` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 11.3% of the budget, 88.7% of the default cost. Mirror fold -6.5 points, sd 3.6 on 184 questions (fails).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +3.8 points, sd 4.2, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 21.2% of the budget, 19.7% of the default cost. Mirror fold -1.1 points, sd 3.0 on 184 questions (fails).
- `avg_gated_lookup` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F3. Verification margin +25.3 points, sd 6.1, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 11.3% of the budget, 44.3% of the default cost. Mirror fold +16.3 points, sd 4.0 on 184 questions (clears).
- `avg_gated_lookup` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +38.0 points, sd 6.1, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 11.3% of the budget, 66.5% of the default cost. Mirror fold +26.1 points, sd 3.5 on 184 questions (clears).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 11.3% of the budget, 88.7% of the default cost. Mirror fold -4.9 points, sd 2.8 on 184 questions (fails).

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
