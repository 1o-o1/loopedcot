# Table 1 -- gsm8k (ouro_2_6b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 142031 layer passes over 1056 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 87.1 | +2.6 |
| default_cell | n/a | n/a | n/a | 87.1 | +2.6 |
| default_at_budget | 14.3 | 27.6 | 71.0 | 87.7 | +2.0 |
| lookup | 65.2 | 88.8 | 89.3 | 89.3 | +0.4 |
| equation | 65.2 | 89.7 | 89.3 | 89.3 | +0.4 |
| equation_n100 | 65.2 | 89.7 | 89.3 | 89.3 | +0.4 |
| equation_n30 | 65.2 | 89.7 | 89.3 | 89.3 | +0.4 |
| equation_resolved | 65.2 | 89.7 | 89.3 | 89.3 | +0.4 |
| gated_equation | 65.2 | 74.0 | 87.0 | 89.3 | +0.4 |
| gated_equation_resolved | 65.2 | 74.0 | 87.0 | 89.3 | +0.4 |
| avg_gated_equation_resolved | 58.7 | 74.0 | 87.0 | 89.3 | +0.4 |
| avg_gated_lookup | 58.7 | 74.0 | 87.2 | 89.3 | +0.4 |
| avg_lookup | 58.7 | 88.8 | 89.3 | 89.3 | +0.4 |
| avg_equation | 58.7 | 88.8 | 89.3 | 89.3 | +0.4 |
| avg_equation_resolved | 58.7 | 88.8 | 89.3 | 89.3 | +0.4 |

The ORACLE GAP is the best single evaluation cell (depth 2 at cap 2048, 89.7 points over 1056 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 22850 vs 35508 (-35.6%) | 70681 vs 71015 (-0.5%) | 99123 vs 106523 (-6.9%) | 74012 vs 142031 (-47.9%) |
| avg_gated_lookup | 22850 vs 35508 (-35.6%) | 70681 vs 71015 (-0.5%) | 94644 vs 106523 (-11.2%) | 74012 vs 142031 (-47.9%) |
| avg_lookup | 22850 vs 35508 (-35.6%) | 61071 vs 71015 (-14.0%) | 74012 vs 106523 (-30.5%) | 74012 vs 142031 (-47.9%) |
| avg_equation | 22850 vs 35508 (-35.6%) | 61071 vs 71015 (-14.0%) | 74012 vs 106523 (-30.5%) | 74012 vs 142031 (-47.9%) |
| avg_equation_resolved | 22850 vs 35508 (-35.6%) | 61071 vs 71015 (-14.0%) | 74012 vs 106523 (-30.5%) | 74012 vs 142031 (-47.9%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 1056 | 28032 | 130258 (over) vs 130258 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T256: 1056 | 52602 | 130258 (over) vs 130258 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T512: 1056 | 93216 | 130258 (over) vs 130258 (over) |
| 1.00x | default_cell | 4 | k4_T4096: 1056 | 130258 | 130258 (fits) vs 130258 (fits) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 1056 | 28032 | 130258 (over) vs 130258 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T256: 1056 | 52602 | 130258 (over) vs 130258 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T512: 1056 | 93216 | 130258 (over) vs 130258 (over) |
| 1.00x | default_cell | 4 | k4_T4096: 1056 | 130258 | 130258 (fits) vs 130258 (fits) |
- `avg_gated_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 87.0 points at 69.8% of the default cost, 6.9% under the budget it was given.
- `avg_gated_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 89.3 points at 52.1% of the default cost, 47.9% under the budget it was given.
- `avg_gated_equation_resolved` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F3. Verification margin +38.0 points, sd 6.1, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 35.6% of the budget, 16.1% of the default cost. Mirror fold +48.9 points, sd 4.4 on 184 questions (clears).
- `avg_gated_equation_resolved` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +40.5 points, sd 6.3, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 0.5% of the budget, 49.8% of the default cost. Mirror fold +52.7 points, sd 3.9 on 184 questions (clears).
- `avg_gated_equation_resolved` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +17.7 points, sd 5.5, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 6.9% of the budget, 69.8% of the default cost. Mirror fold +21.7 points, sd 3.5 on 184 questions (clears).
- `avg_gated_equation_resolved` at 1.00x: deviated from the default cell on family F3. Verification margin +6.3 points, sd 3.2, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 47.9% of the budget, 52.1% of the default cost. Mirror fold +2.2 points, sd 2.7 on 184 questions (clears).
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 87.2 points at 66.6% of the default cost, 11.2% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 89.3 points at 52.1% of the default cost, 47.9% under the budget it was given.
- `avg_gated_lookup` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F3. Verification margin +38.0 points, sd 6.1, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 35.6% of the budget, 16.1% of the default cost. Mirror fold +48.9 points, sd 4.4 on 184 questions (clears).
- `avg_gated_lookup` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +40.5 points, sd 6.3, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 0.5% of the budget, 49.8% of the default cost. Mirror fold +52.7 points, sd 3.9 on 184 questions (clears).
- `avg_gated_lookup` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +17.7 points, sd 5.5, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 11.2% of the budget, 66.6% of the default cost. Mirror fold +20.1 points, sd 3.4 on 184 questions (clears).
- `avg_gated_lookup` at 1.00x: deviated from the default cell on family F3. Verification margin +6.3 points, sd 3.2, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 47.9% of the budget, 52.1% of the default cost. Mirror fold +2.2 points, sd 2.7 on 184 questions (clears).
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 89.3 points at 52.1% of the default cost, 30.5% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 89.3 points at 52.1% of the default cost, 47.9% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 89.3 points at 52.1% of the default cost, 30.5% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 89.3 points at 52.1% of the default cost, 47.9% under the budget it was given.
- `avg_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 89.3 points at 52.1% of the default cost, 30.5% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 89.3 points at 52.1% of the default cost, 47.9% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
