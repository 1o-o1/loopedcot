# Table 1 -- gsm8k (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 15588 layer passes over 1056 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 76.7 | +0.1 |
| default_cell | n/a | n/a | n/a | 76.7 | +0.1 |
| default_at_budget | 11.6 | 39.9 | 66.4 | 76.7 | +0.1 |
| lookup | 26.5 | 64.9 | 74.1 | 76.7 | +0.1 |
| equation | 26.5 | 64.9 | 74.3 | 76.7 | +0.1 |
| equation_n100 | 26.5 | 64.9 | 74.3 | 76.7 | +0.1 |
| equation_n30 | 26.5 | 64.9 | 74.3 | 76.7 | +0.1 |
| equation_resolved | 26.5 | 64.9 | 74.3 | 76.7 | +0.1 |
| gated_equation | 15.2 | 64.9 | 74.3 | 76.7 | +0.1 |
| gated_equation_resolved | 26.5 | 64.9 | 74.3 | 76.7 | +0.1 |
| avg_gated_equation_resolved | 15.8 | 64.9 | 74.3 | 76.7 | +0.1 |
| avg_gated_lookup | 15.8 | 64.9 | 74.1 | 76.7 | +0.1 |
| avg_lookup | 11.6 | 64.9 | 73.5 | 76.7 | +0.1 |
| avg_equation | 11.6 | 64.3 | 74.1 | 76.7 | +0.1 |
| avg_equation_resolved | 11.6 | 64.3 | 74.1 | 76.7 | +0.1 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 1024, 76.8 points over 1056 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 1536 vs 3897 (-60.6%) | 7158 vs 7794 (-8.2%) | 11361 vs 11691 (-2.8%) | 14793 vs 15588 (-5.1%) |
| avg_gated_lookup | 1536 vs 3897 (-60.6%) | 7158 vs 7794 (-8.2%) | 10099 vs 11691 (-13.6%) | 14793 vs 15588 (-5.1%) |
| avg_lookup | 768 vs 3897 (-80.3%) | 7158 vs 7794 (-8.2%) | 9824 vs 11691 (-16.0%) | 13485 vs 15588 (-13.5%) |
| avg_equation | 768 vs 3897 (-80.3%) | 6699 vs 7794 (-14.1%) | 10099 vs 11691 (-13.6%) | 14793 vs 15588 (-5.1%) |
| avg_equation_resolved | 768 vs 3897 (-80.3%) | 6699 vs 7794 (-14.1%) | 10099 vs 11691 (-13.6%) | 14793 vs 15588 (-5.1%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T0: 1056 | 1536 | 14793 (over) vs 14793 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T0: 1056 | 1536 | 14793 (over) vs 14793 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T0: 1056 | 1536 | 14793 (over) vs 14793 (over) |
| 1.00x | default_cell | 4 | k4_T4096: 1056 | 14793 | 14793 (fits) vs 14793 (fits) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T0: 1056 | 1536 | 14793 (over) vs 14793 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T0: 1056 | 1536 | 14793 (over) vs 14793 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T0: 1056 | 1536 | 14793 (over) vs 14793 (over) |
| 1.00x | default_cell | 4 | k4_T4096: 1056 | 14793 | 14793 (fits) vs 14793 (fits) |
- `avg_gated_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 74.3 points at 72.9% of the default cost, 2.8% under the budget it was given.
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin -3.8 points, sd 4.2, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 60.6% of the budget, 9.9% of the default cost. Mirror fold -3.8 points, sd 2.4 on 184 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F3. Verification margin +51.9 points, sd 7.2, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 8.2% of the budget, 45.9% of the default cost. Mirror fold +48.4 points, sd 4.2 on 184 questions (clears).
- `avg_gated_equation_resolved` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F2. Verification margin +57.0 points, sd 6.2, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 2.8% of the budget, 72.9% of the default cost. Mirror fold +57.6 points, sd 4.0 on 184 questions (clears).
- `avg_gated_equation_resolved` at 1.00x: reverted to the default cell for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 5.1% of the budget, 94.9% of the default cost. Mirror fold +0.0 points, sd 0.0 on 184 questions (fails).
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 74.1 points at 64.8% of the default cost, 13.6% under the budget it was given.
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin -3.8 points, sd 4.2, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 60.6% of the budget, 9.9% of the default cost. Mirror fold -1.6 points, sd 1.9 on 184 questions (fails).
- `avg_gated_lookup` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F3. Verification margin +51.9 points, sd 7.2, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 8.2% of the budget, 45.9% of the default cost. Mirror fold +50.5 points, sd 4.1 on 184 questions (clears).
- `avg_gated_lookup` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F2. Verification margin +57.0 points, sd 6.2, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 13.6% of the budget, 64.8% of the default cost. Mirror fold +57.1 points, sd 4.0 on 184 questions (clears).
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 5.1% of the budget, 94.9% of the default cost. Mirror fold +0.0 points, sd 0.0 on 184 questions (fails).
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 76.7 points at 86.5% of the default cost, 13.5% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 76.7 points at 94.9% of the default cost, 5.1% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 76.7 points at 94.9% of the default cost, 5.1% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
