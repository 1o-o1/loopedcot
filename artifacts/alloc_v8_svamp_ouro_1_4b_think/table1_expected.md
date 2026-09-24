# Table 1 -- svamp (ouro_1_4b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 68624 layer passes over 200 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 89.5 | +0.5 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 75.0 | 87.0 | 89.5 | 90.0 | +0.0 |
| lookup | 78.0 | 87.0 | 87.5 | 87.5 | +2.5 |
| equation | 78.0 | 86.5 | 87.5 | 87.5 | +2.5 |
| equation_n100 | 78.0 | 86.5 | 87.5 | 87.5 | +2.5 |
| equation_n30 | 69.5 | 86.0 | 87.5 | 87.5 | +2.5 |
| equation_resolved | 78.0 | 86.0 | 87.5 | 87.5 | +2.5 |
| gated_equation | 75.0 | 86.0 | 87.5 | 87.5 | +2.5 |
| gated_equation_resolved | 75.0 | 86.0 | 87.5 | 87.5 | +2.5 |
| avg_gated_equation_resolved | 75.0 | 86.0 | 87.5 | 87.5 | +2.5 |
| avg_gated_lookup | 75.0 | 86.0 | 89.5 | 90.0 | +0.0 |
| avg_lookup | 64.5 | 87.0 | 87.5 | 87.5 | +2.5 |
| avg_equation | 78.0 | 86.5 | 87.5 | 87.5 | +2.5 |
| avg_equation_resolved | 64.5 | 86.0 | 87.5 | 87.5 | +2.5 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 2048, 90.0 points over 200 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2. Of the families that CLEAR the bar the one that RUNS is set by `policy.GATE_FAMILY_RULE` = `best`: the cleared family with the largest mean verified margin over the folds, ties to the smaller family. The folds, the bar, the reference and the pricing are the same test under either rule; only which cleared family is taken differs.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 13617 vs 17156 (-20.6%) | 26727 vs 34312 (-22.1%) | 44871 vs 51468 (-12.8%) | 44871 vs 68624 (-34.6%) |
| avg_gated_lookup | 13617 vs 17156 (-20.6%) | 26727 vs 34312 (-22.1%) | 45849 vs 51468 (-10.9%) | 56388 vs 68624 (-17.8%) |
| avg_lookup | 7488 vs 17156 (-56.4%) | 23485 vs 34312 (-31.6%) | 44871 vs 51468 (-12.8%) | 44871 vs 68624 (-34.6%) |
| avg_equation | 12103 vs 17156 (-29.5%) | 31464 vs 34312 (-8.3%) | 44871 vs 51468 (-12.8%) | 44871 vs 68624 (-34.6%) |
| avg_equation_resolved | 7488 vs 17156 (-56.4%) | 26727 vs 34312 (-22.1%) | 44871 vs 51468 (-12.8%) | 44871 vs 68624 (-34.6%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 200 | 13617 | 68772 (over) vs 68772 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T256: 200 | 24187 | 68772 (over) vs 68772 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T1024: 200 | 45849 | 68772 (over) vs 68772 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T2048: 200 | 56388 | 68772 (over) vs 68772 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 200 | 13617 | 68772 (over) vs 68772 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T256: 200 | 24187 | 68772 (over) vs 68772 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T1024: 200 | 45849 | 68772 (over) vs 68772 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T2048: 200 | 56388 | 68772 (over) vs 68772 (over) |
- `avg_gated_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 87.5 points at 65.4% of the default cost, 12.8% under the budget it was given.
- `avg_gated_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 87.5 points at 65.4% of the default cost, 34.6% under the budget it was given.
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -13.3 points, sd 6.1, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 20.6% of the budget, 19.8% of the default cost. Mirror fold +0.0 points, sd 2.0 on 70 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +16.7 points, sd 7.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 22.1% of the budget, 38.9% of the default cost. Mirror fold +10.0 points, sd 4.5 on 70 questions (clears).
- `avg_gated_equation_resolved` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +6.7 points, sd 6.5, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 12.8% of the budget, 65.4% of the default cost. Mirror fold +4.3 points, sd 3.8 on 70 questions (clears).
- `avg_gated_equation_resolved` at 1.00x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +6.7 points, sd 6.5, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 34.6% of the budget, 65.4% of the default cost. Mirror fold +2.9 points, sd 3.5 on 70 questions (clears).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -13.3 points, sd 6.1, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 20.6% of the budget, 19.8% of the default cost. Mirror fold +0.0 points, sd 2.0 on 70 questions (fails).
- `avg_gated_lookup` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +16.7 points, sd 7.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 22.1% of the budget, 38.9% of the default cost. Mirror fold +10.0 points, sd 4.5 on 70 questions (clears).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 8.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 10.9% of the budget, 66.8% of the default cost. Mirror fold +1.4 points, sd 4.3 on 70 questions (fails).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 8.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 17.8% of the budget, 82.2% of the default cost. Mirror fold +0.0 points, sd 4.1 on 70 questions (fails).
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 87.5 points at 65.4% of the default cost, 12.8% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 87.5 points at 65.4% of the default cost, 34.6% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 87.5 points at 65.4% of the default cost, 12.8% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 87.5 points at 65.4% of the default cost, 34.6% under the budget it was given.
- `avg_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 87.5 points at 65.4% of the default cost, 12.8% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 87.5 points at 65.4% of the default cost, 34.6% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
