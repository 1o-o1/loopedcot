# Table 1 -- math500 (ouro_1_4b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 181887 layer passes over 400 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 89.8 | +0.0 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 36.8 | 59.0 | 75.8 | 75.8 | +14.0 |
| lookup | 59.5 | 75.8 | 76.8 | 84.5 | +5.2 |
| equation | 59.5 | 75.8 | 76.8 | 84.5 | +5.2 |
| equation_n100 | 59.5 | 75.8 | 76.8 | 84.5 | +5.2 |
| equation_n30 | 59.5 | 75.8 | 76.8 | 76.8 | +13.0 |
| equation_resolved | 59.5 | 75.8 | 76.8 | 84.5 | +5.2 |
| gated_equation | 59.5 | 75.8 | 76.8 | 84.5 | +5.2 |
| gated_equation_resolved | 59.5 | 75.8 | 76.8 | 84.5 | +5.2 |
| avg_gated_equation_resolved | 59.5 | 75.8 | 76.8 | 84.5 | +5.2 |
| avg_gated_lookup | 59.5 | 75.8 | 76.8 | 84.5 | +5.2 |
| avg_lookup | 52.0 | 66.8 | 76.8 | 76.8 | +13.0 |
| avg_equation | 52.0 | 66.8 | 76.8 | 76.8 | +13.0 |
| avg_equation_resolved | 52.0 | 66.8 | 76.8 | 76.8 | +13.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 4096, 89.8 points over 400 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3. Of the families that CLEAR the bar the one that RUNS is set by `policy.GATE_FAMILY_RULE` = `best`: the cleared family with the largest mean verified margin over the folds, ties to the smaller family. The folds, the bar, the reference and the pricing are the same test under either rule; only which cleared family is taken differs.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 39600 vs 45472 (-12.9%) | 76464 vs 90943 (-15.9%) | 100128 vs 136415 (-26.6%) | 150192 vs 181887 (-17.4%) |
| avg_gated_lookup | 39600 vs 45472 (-12.9%) | 76464 vs 90943 (-15.9%) | 100128 vs 136415 (-26.6%) | 150192 vs 181887 (-17.4%) |
| avg_lookup | 26400 vs 45472 (-41.9%) | 50976 vs 90943 (-43.9%) | 100128 vs 136415 (-26.6%) | 100128 vs 181887 (-45.0%) |
| avg_equation | 26400 vs 45472 (-41.9%) | 50976 vs 90943 (-43.9%) | 100128 vs 136415 (-26.6%) | 100128 vs 181887 (-45.0%) |
| avg_equation_resolved | 26400 vs 45472 (-41.9%) | 50976 vs 90943 (-43.9%) | 100128 vs 136415 (-26.6%) | 100128 vs 181887 (-45.0%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T256: 400 | 28224 | 396864 (over) vs 396864 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T512: 400 | 52800 | 396864 (over) vs 396864 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T1024: 400 | 101952 | 396864 (over) vs 396864 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T1024: 400 | 101952 | 396864 (over) vs 396864 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T256: 400 | 28224 | 396864 (over) vs 396864 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T512: 400 | 52800 | 396864 (over) vs 396864 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T1024: 400 | 101952 | 396864 (over) vs 396864 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T1024: 400 | 101952 | 396864 (over) vs 396864 (over) |
- `avg_gated_equation_resolved` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +26.7 points, sd 8.2, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 12.9% of the budget, 21.8% of the default cost. Mirror fold +21.4 points, sd 5.3 on 70 questions (clears).
- `avg_gated_equation_resolved` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +26.7 points, sd 7.9, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 15.9% of the budget, 42.0% of the default cost. Mirror fold +10.0 points, sd 4.1 on 70 questions (clears).
- `avg_gated_equation_resolved` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F3. Verification margin +6.7 points, sd 8.2, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 26.6% of the budget, 55.0% of the default cost. Mirror fold +5.7 points, sd 4.0 on 70 questions (clears).
- `avg_gated_equation_resolved` at 1.00x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +6.7 points, sd 8.1, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 17.4% of the budget, 82.6% of the default cost. Mirror fold +7.1 points, sd 3.0 on 70 questions (clears).
- `avg_gated_lookup` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +26.7 points, sd 8.2, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 12.9% of the budget, 21.8% of the default cost. Mirror fold +21.4 points, sd 5.3 on 70 questions (clears).
- `avg_gated_lookup` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +26.7 points, sd 7.9, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 15.9% of the budget, 42.0% of the default cost. Mirror fold +10.0 points, sd 4.1 on 70 questions (clears).
- `avg_gated_lookup` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F3. Verification margin +6.7 points, sd 8.2, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 26.6% of the budget, 55.0% of the default cost. Mirror fold +5.7 points, sd 4.0 on 70 questions (clears).
- `avg_gated_lookup` at 1.00x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +6.7 points, sd 8.1, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 17.4% of the budget, 82.6% of the default cost. Mirror fold +7.1 points, sd 3.0 on 70 questions (clears).

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
