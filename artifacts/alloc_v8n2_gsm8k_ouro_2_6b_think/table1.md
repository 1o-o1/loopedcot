# Table 1 -- gsm8k (ouro_2_6b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 142194 layer passes over 1056 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 87.7 | +2.0 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 14.3 | 27.6 | 71.0 | 71.0 | +18.7 |
| lookup | 58.7 | 82.5 | 88.8 | 88.8 | +0.9 |
| equation | 58.7 | 82.5 | 88.8 | 88.8 | +0.9 |
| equation_n100 | 58.7 | 82.5 | 88.8 | 88.8 | +0.9 |
| equation_n30 | 50.9 | 82.5 | 88.8 | 88.8 | +0.9 |
| equation_resolved | 58.7 | 82.5 | 88.8 | 88.8 | +0.9 |
| gated_equation | 58.7 | 33.7 | 74.0 | 74.0 | +15.7 |
| gated_equation_resolved | 58.7 | 33.7 | 74.0 | 74.0 | +15.7 |
| avg_gated_equation_resolved | 58.7 | 82.5 | 88.8 | 88.8 | +0.9 |
| avg_gated_lookup | 58.7 | 82.5 | 88.8 | 88.8 | +0.9 |
| avg_lookup | 58.7 | 82.5 | 88.8 | 88.8 | +0.9 |
| avg_equation | 58.7 | 82.5 | 88.8 | 88.8 | +0.9 |
| avg_equation_resolved | 58.7 | 82.5 | 88.8 | 88.8 | +0.9 |

The ORACLE GAP is the best single evaluation cell (depth 2 at cap 2048, 89.7 points over 1056 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3. Of the families that CLEAR the bar the one that RUNS is set by `policy.GATE_FAMILY_RULE` = `best`: the cleared family with the largest mean verified margin over the folds, ties to the smaller family. The folds, the bar, the reference and the pricing are the same test under either rule; only which cleared family is taken differs.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 25440 vs 35549 (-28.4%) | 50880 vs 71097 (-28.4%) | 100032 vs 106646 (-6.2%) | 100032 vs 142194 (-29.7%) |
| avg_gated_lookup | 25440 vs 35549 (-28.4%) | 50880 vs 71097 (-28.4%) | 100032 vs 106646 (-6.2%) | 100032 vs 142194 (-29.7%) |
| avg_lookup | 25440 vs 35549 (-28.4%) | 50880 vs 71097 (-28.4%) | 100032 vs 106646 (-6.2%) | 100032 vs 142194 (-29.7%) |
| avg_equation | 25440 vs 35549 (-28.4%) | 50880 vs 71097 (-28.4%) | 100032 vs 106646 (-6.2%) | 100032 vs 142194 (-29.7%) |
| avg_equation_resolved | 25440 vs 35549 (-28.4%) | 50880 vs 71097 (-28.4%) | 100032 vs 106646 (-6.2%) | 100032 vs 142194 (-29.7%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 1056 | 28032 | 789888 (over) vs 789888 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T256: 1056 | 52608 | 789888 (over) vs 789888 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T512: 1056 | 101760 | 789888 (over) vs 789888 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T512: 1056 | 101760 | 789888 (over) vs 789888 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 1056 | 28032 | 789888 (over) vs 789888 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T256: 1056 | 52608 | 789888 (over) vs 789888 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T512: 1056 | 101760 | 789888 (over) vs 789888 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T512: 1056 | 101760 | 789888 (over) vs 789888 (over) |
- `avg_gated_equation_resolved` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F3. Verification margin +38.0 points, sd 6.1, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 28.4% of the budget, 17.9% of the default cost. Mirror fold +48.9 points, sd 4.4 on 184 questions (clears).
- `avg_gated_equation_resolved` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F3. Verification margin +54.4 points, sd 5.7, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 28.4% of the budget, 35.8% of the default cost. Mirror fold +62.5 points, sd 3.7 on 184 questions (clears).
- `avg_gated_equation_resolved` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F3. Verification margin +22.8 points, sd 5.0, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 6.2% of the budget, 70.3% of the default cost. Mirror fold +21.2 points, sd 3.2 on 184 questions (clears).
- `avg_gated_equation_resolved` at 1.00x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F3. Verification margin +22.8 points, sd 5.0, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 29.7% of the budget, 70.3% of the default cost. Mirror fold +21.2 points, sd 3.2 on 184 questions (clears).
- `avg_gated_lookup` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F3. Verification margin +38.0 points, sd 6.1, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 28.4% of the budget, 17.9% of the default cost. Mirror fold +33.2 points, sd 3.8 on 184 questions (clears).
- `avg_gated_lookup` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F3. Verification margin +54.4 points, sd 5.7, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 28.4% of the budget, 35.8% of the default cost. Mirror fold +62.5 points, sd 3.7 on 184 questions (clears).
- `avg_gated_lookup` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F3. Verification margin +22.8 points, sd 5.0, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 6.2% of the budget, 70.3% of the default cost. Mirror fold +21.2 points, sd 3.2 on 184 questions (clears).
- `avg_gated_lookup` at 1.00x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F3. Verification margin +22.8 points, sd 5.0, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 29.7% of the budget, 70.3% of the default cost. Mirror fold +21.2 points, sd 3.2 on 184 questions (clears).

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
