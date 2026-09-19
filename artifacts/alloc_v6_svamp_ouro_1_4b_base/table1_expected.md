# Table 1 -- svamp (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 6421 layer passes over 200 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 86.5 | +0.0 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 44.5 | 53.0 | 58.0 | 78.0 | +8.5 |
| lookup | 44.5 | 62.0 | 77.5 | 84.0 | +2.5 |
| equation | 38.0 | 62.0 | 77.5 | 85.5 | +1.0 |
| equation_n100 | 38.0 | 62.0 | 77.5 | 85.5 | +1.0 |
| equation_n30 | 44.5 | 51.0 | 77.5 | 85.5 | +1.0 |
| equation_resolved | 44.5 | 62.0 | 77.5 | 85.5 | +1.0 |
| gated_equation | 44.5 | 62.0 | 77.5 | 85.5 | +1.0 |
| gated_equation_resolved | 44.5 | 62.0 | 77.5 | 85.5 | +1.0 |
| avg_gated_equation_resolved | 44.5 | 44.5 | 77.5 | 85.5 | +1.0 |
| avg_gated_lookup | 44.5 | 62.0 | 72.0 | 84.0 | +2.5 |
| avg_lookup | 44.5 | 62.0 | 72.0 | 84.0 | +2.5 |
| avg_equation | 31.0 | 31.0 | 31.0 | 85.5 | +1.0 |
| avg_equation_resolved | 44.5 | 62.0 | 77.5 | 85.5 | +1.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 256, 86.5 points over 200 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 1056 vs 1605 (-34.2%) | 1056 vs 3210 (-67.1%) | 4367 vs 4816 (-9.3%) | 5126 vs 6421 (-20.2%) |
| avg_gated_lookup | 1056 vs 1605 (-34.2%) | 2926 vs 3210 (-8.9%) | 3408 vs 4816 (-29.2%) | 5056 vs 6421 (-21.3%) |
| avg_lookup | 1056 vs 1605 (-34.2%) | 2926 vs 3210 (-8.9%) | 3408 vs 4816 (-29.2%) | 5056 vs 6421 (-21.3%) |
| avg_equation | 528 vs 1605 (-67.1%) | 528 vs 3210 (-83.6%) | 528 vs 4816 (-89.0%) | 5126 vs 6421 (-20.2%) |
| avg_equation_resolved | 1056 vs 1605 (-34.2%) | 2926 vs 3210 (-8.9%) | 4367 vs 4816 (-9.3%) | 5126 vs 6421 (-20.2%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T0: 200 | 1056 | 6926 (over) vs 6926 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T0: 200 | 1056 | 6926 (over) vs 6926 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T0: 200 | 1056 | 6926 (over) vs 6926 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T0: 200 | 1056 | 6926 (over) vs 6926 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T0: 200 | 1056 | 6926 (over) vs 6926 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T0: 200 | 1056 | 6926 (over) vs 6926 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T0: 200 | 1056 | 6926 (over) vs 6926 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T0: 200 | 1056 | 6926 (over) vs 6926 (over) |
- `avg_gated_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 85.5 points at 79.8% of the default cost, 20.2% under the budget it was given.
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 34.2% of the budget, 16.4% of the default cost. Mirror fold -7.1 points, sd 3.6 on 70 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 67.1% of the budget, 16.4% of the default cost. Mirror fold +17.1 points, sd 6.2 on 70 questions (clears).
- `avg_gated_equation_resolved` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F2. Verification margin +33.3 points, sd 8.6, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 9.3% of the budget, 68.0% of the default cost. Mirror fold +27.1 points, sd 5.8 on 70 questions (clears).
- `avg_gated_equation_resolved` at 1.00x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F2. Verification margin +40.0 points, sd 9.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 20.2% of the budget, 79.8% of the default cost. Mirror fold +32.9 points, sd 6.0 on 70 questions (clears).
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 84.0 points at 78.7% of the default cost, 21.3% under the budget it was given.
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 34.2% of the budget, 16.4% of the default cost. Mirror fold -10.0 points, sd 5.8 on 70 questions (fails).
- `avg_gated_lookup` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F3. Verification margin +26.7 points, sd 8.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 8.9% of the budget, 45.6% of the default cost. Mirror fold +17.1 points, sd 6.2 on 70 questions (clears).
- `avg_gated_lookup` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F3. Verification margin +30.0 points, sd 8.3, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 29.2% of the budget, 53.1% of the default cost. Mirror fold +21.4 points, sd 6.1 on 70 questions (clears).
- `avg_gated_lookup` at 1.00x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F2. Verification margin +40.0 points, sd 9.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 21.3% of the budget, 78.7% of the default cost. Mirror fold +32.9 points, sd 6.0 on 70 questions (clears).
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 84.0 points at 78.7% of the default cost, 21.3% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 85.5 points at 79.8% of the default cost, 20.2% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
