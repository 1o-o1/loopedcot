# Table 1 -- math500 (ouro_1_4b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 205663 layer passes over 400 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 89.5 | +0.0 |
| default_cell | n/a | n/a | n/a | 89.5 | +0.0 |
| default_at_budget | 36.8 | 75.5 | 83.8 | 89.5 | +0.0 |
| lookup | 66.8 | 76.8 | 87.8 | 89.5 | +0.0 |
| equation | 66.8 | 76.8 | 87.8 | 89.5 | +0.0 |
| equation_n100 | 66.8 | 76.8 | 87.8 | 89.5 | +0.0 |
| equation_n30 | 66.8 | 76.8 | 77.2 | 77.2 | +12.2 |
| equation_resolved | 66.8 | 76.8 | 87.8 | 89.5 | +0.0 |
| gated_equation | 59.5 | 76.8 | 83.8 | 89.5 | +0.0 |
| gated_equation_resolved | 59.5 | 76.8 | 83.8 | 89.5 | +0.0 |
| avg_gated_equation_resolved | 59.5 | 76.8 | 83.8 | 89.5 | +0.0 |
| avg_gated_lookup | 66.8 | 76.8 | 83.8 | 89.5 | +0.0 |
| avg_lookup | 66.8 | 76.8 | 87.8 | 89.5 | +0.0 |
| avg_equation | 66.8 | 76.8 | 77.2 | 89.5 | +0.0 |
| avg_equation_resolved | 66.8 | 76.8 | 87.8 | 89.5 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 4096, 89.5 points over 400 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 39177 vs 51416 (-23.8%) | 71648 vs 102832 (-30.3%) | 141930 vs 154248 (-8.0%) | 197228 vs 205663 (-4.1%) |
| avg_gated_lookup | 46306 vs 51416 (-9.9%) | 71648 vs 102832 (-30.3%) | 141930 vs 154248 (-8.0%) | 197228 vs 205663 (-4.1%) |
| avg_lookup | 46306 vs 51416 (-9.9%) | 71648 vs 102832 (-30.3%) | 144199 vs 154248 (-6.5%) | 197228 vs 205663 (-4.1%) |
| avg_equation | 46306 vs 51416 (-9.9%) | 71648 vs 102832 (-30.3%) | 104300 vs 154248 (-32.4%) | 197228 vs 205663 (-4.1%) |
| avg_equation_resolved | 46306 vs 51416 (-9.9%) | 71648 vs 102832 (-30.3%) | 144199 vs 154248 (-6.5%) | 197228 vs 205663 (-4.1%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T256: 400 | 28224 | 197228 (over) vs 197228 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T1024: 400 | 92331 | 197228 (over) vs 197228 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T2048: 400 | 141930 | 197228 (over) vs 197228 (over) |
| 1.00x | default_cell | 4 | k4_T4096: 400 | 197228 | 197228 (fits) vs 197228 (fits) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T256: 400 | 28224 | 197228 (over) vs 197228 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T1024: 400 | 92331 | 197228 (over) vs 197228 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T2048: 400 | 141930 | 197228 (over) vs 197228 (over) |
| 1.00x | default_cell | 4 | k4_T4096: 400 | 197228 | 197228 (fits) vs 197228 (fits) |
- `avg_gated_equation_resolved` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +26.7 points, sd 8.2, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 23.8% of the budget, 19.0% of the default cost. Mirror fold +21.4 points, sd 5.3 on 70 questions (clears).
- `avg_gated_equation_resolved` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F3. Verification margin +6.7 points, sd 8.2, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 30.3% of the budget, 34.8% of the default cost. Mirror fold +7.1 points, sd 4.2 on 70 questions (clears).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -3.3 points, sd 3.2, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 8.0% of the budget, 69.0% of the default cost. Mirror fold +0.0 points, sd 0.0 on 70 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: reverted to the default cell for every question. Verification margin -3.3 points, sd 3.2, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 4.1% of the budget, 95.9% of the default cost. Mirror fold +0.0 points, sd 0.0 on 70 questions (fails).
- `avg_gated_lookup` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F3. Verification margin +46.7 points, sd 9.2, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 9.9% of the budget, 22.5% of the default cost. Mirror fold +35.7 points, sd 6.3 on 70 questions (clears).
- `avg_gated_lookup` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F3. Verification margin +6.7 points, sd 8.2, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 30.3% of the budget, 34.8% of the default cost. Mirror fold +7.1 points, sd 4.2 on 70 questions (clears).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -3.3 points, sd 3.2, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 8.0% of the budget, 69.0% of the default cost. Mirror fold +0.0 points, sd 0.0 on 70 questions (fails).
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 4.1% of the budget, 95.9% of the default cost. Mirror fold -5.7 points, sd 3.4 on 70 questions (fails).
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 89.5 points at 95.9% of the default cost, 4.1% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 89.5 points at 95.9% of the default cost, 4.1% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 89.5 points at 95.9% of the default cost, 4.1% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
