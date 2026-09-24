# Table 1 -- arc (ouro_1_4b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 49996 layer passes over 938 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 93.7 | +0.4 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 88.6 | 86.2 | 89.9 | 89.9 | +4.3 |
| lookup | 88.6 | 89.7 | 89.7 | 93.3 | +0.9 |
| equation | 84.5 | 89.7 | 89.7 | 93.3 | +0.9 |
| equation_n100 | 84.5 | 89.7 | 89.7 | 93.3 | +0.9 |
| equation_n30 | 84.5 | 89.7 | 88.1 | 89.6 | +4.6 |
| equation_resolved | 88.6 | 89.7 | 89.7 | 93.3 | +0.9 |
| gated_equation | 88.6 | 86.2 | 89.9 | 93.3 | +0.9 |
| gated_equation_resolved | 88.6 | 86.2 | 89.9 | 93.3 | +0.9 |
| avg_gated_equation_resolved | 88.6 | 86.2 | 89.9 | 93.3 | +0.9 |
| avg_gated_lookup | 88.6 | 86.2 | 89.9 | 93.3 | +0.9 |
| avg_lookup | 87.0 | 89.7 | 89.7 | 93.3 | +0.9 |
| avg_equation | 87.0 | 89.7 | 89.7 | 93.3 | +0.9 |
| avg_equation_resolved | 87.0 | 89.7 | 89.7 | 93.3 | +0.9 |

The ORACLE GAP is the best single evaluation cell (depth 3 at cap 1024, 94.1 points over 938 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2. Of the families that CLEAR the bar the one that RUNS is set by `policy.GATE_FAMILY_RULE` = `best`: the cleared family with the largest mean verified margin over the folds, ties to the smaller family. The folds, the bar, the reference and the pricing are the same test under either rule; only which cleared family is taken differs.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 7488 vs 12499 (-40.1%) | 13632 vs 24998 (-45.5%) | 25920 vs 37497 (-30.9%) | 37872 vs 49996 (-24.2%) |
| avg_gated_lookup | 7488 vs 12499 (-40.1%) | 13632 vs 24998 (-45.5%) | 25920 vs 37497 (-30.9%) | 37872 vs 49996 (-24.2%) |
| avg_lookup | 1344 vs 12499 (-89.2%) | 19440 vs 24998 (-22.2%) | 19440 vs 37497 (-48.2%) | 37872 vs 49996 (-24.2%) |
| avg_equation | 1344 vs 12499 (-89.2%) | 19440 vs 24998 (-22.2%) | 19440 vs 37497 (-48.2%) | 37872 vs 49996 (-24.2%) |
| avg_equation_resolved | 1344 vs 12499 (-89.2%) | 19440 vs 24998 (-22.2%) | 19440 vs 37497 (-48.2%) | 37872 vs 49996 (-24.2%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T64: 938 | 7488 | 394560 (over) vs 394560 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T128: 938 | 13632 | 394560 (over) vs 394560 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T256: 938 | 25920 | 394560 (over) vs 394560 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T256: 938 | 25920 | 394560 (over) vs 394560 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T64: 938 | 7488 | 394560 (over) vs 394560 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T128: 938 | 13632 | 394560 (over) vs 394560 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T256: 938 | 25920 | 394560 (over) vs 394560 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T256: 938 | 25920 | 394560 (over) vs 394560 (over) |
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +1.4 points, sd 1.5, bar 0.50 sd (70 verification questions, the ids after the 164 that fit, out of 234 calibration); cost saving 40.1% of the budget, 15.0% of the default cost. Mirror fold -1.2 points, sd 1.9 on 164 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +1.4 points, sd 3.7, bar 0.50 sd (70 verification questions, the ids after the 164 that fit, out of 234 calibration); cost saving 45.5% of the budget, 27.3% of the default cost. Mirror fold -3.0 points, sd 2.4 on 164 questions (fails).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +1.4 points, sd 3.1, bar 0.50 sd (70 verification questions, the ids after the 164 that fit, out of 234 calibration); cost saving 30.9% of the budget, 51.8% of the default cost. Mirror fold -2.4 points, sd 2.5 on 164 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +5.7 points, sd 4.0, bar 0.50 sd (70 verification questions, the ids after the 164 that fit, out of 234 calibration); cost saving 24.2% of the budget, 75.8% of the default cost. Mirror fold +3.7 points, sd 1.7 on 164 questions (clears).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +1.4 points, sd 1.5, bar 0.50 sd (70 verification questions, the ids after the 164 that fit, out of 234 calibration); cost saving 40.1% of the budget, 15.0% of the default cost. Mirror fold -1.2 points, sd 1.9 on 164 questions (fails).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +1.4 points, sd 3.7, bar 0.50 sd (70 verification questions, the ids after the 164 that fit, out of 234 calibration); cost saving 45.5% of the budget, 27.3% of the default cost. Mirror fold -3.0 points, sd 2.4 on 164 questions (fails).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +1.4 points, sd 3.1, bar 0.50 sd (70 verification questions, the ids after the 164 that fit, out of 234 calibration); cost saving 30.9% of the budget, 51.8% of the default cost. Mirror fold -2.4 points, sd 2.5 on 164 questions (fails).
- `avg_gated_lookup` at 1.00x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +5.7 points, sd 4.0, bar 0.50 sd (70 verification questions, the ids after the 164 that fit, out of 234 calibration); cost saving 24.2% of the budget, 75.8% of the default cost. Mirror fold +3.7 points, sd 1.7 on 164 questions (clears).
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 93.3 points at 75.8% of the default cost, 24.2% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 93.3 points at 75.8% of the default cost, 24.2% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
