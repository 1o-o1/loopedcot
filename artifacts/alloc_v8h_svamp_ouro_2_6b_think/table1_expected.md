# Table 1 -- svamp (ouro_2_6b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 193859 layer passes over 200 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 83.5 | +0.0 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 14.0 | 76.0 | 82.5 | 83.0 | +0.5 |
| lookup | 36.5 | 77.0 | 77.0 | 77.0 | +6.5 |
| equation | 36.5 | 78.0 | 78.0 | 79.0 | +4.5 |
| equation_n100 | 36.5 | 78.0 | 78.0 | 79.0 | +4.5 |
| equation_n30 | 36.5 | 78.0 | 78.0 | 79.0 | +4.5 |
| equation_resolved | 36.5 | 78.0 | 82.5 | 82.5 | +1.0 |
| gated_equation | 36.5 | 78.0 | 82.5 | 83.0 | +0.5 |
| gated_equation_resolved | 36.5 | 78.0 | 82.5 | 83.0 | +0.5 |
| avg_gated_equation_resolved | 16.5 | 78.0 | 82.5 | 83.0 | +0.5 |
| avg_gated_lookup | 16.5 | 77.0 | 82.5 | 83.0 | +0.5 |
| avg_lookup | 16.5 | 77.0 | 77.0 | 77.0 | +6.5 |
| avg_equation | 2.5 | 78.0 | 78.0 | 78.0 | +5.5 |
| avg_equation_resolved | 16.5 | 78.0 | 82.5 | 82.5 | +1.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 8192, 83.5 points over 200 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3. Of the families that CLEAR the bar the one that RUNS is set by `policy.GATE_FAMILY_RULE` = `best`: the cleared family with the largest mean verified margin over the folds, ties to the smaller family. The folds, the bar, the reference and the pricing are the same test under either rule; only which cleared family is taken differs.

`default_cell` is the default operating point (depth 4 at cap 8192) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 4320 vs 48465 (-91.1%) | 96202 vs 96929 (-0.8%) | 129909 vs 145394 (-10.7%) | 173902 vs 193859 (-10.3%) |
| avg_gated_lookup | 4320 vs 48465 (-91.1%) | 77592 vs 96929 (-20.0%) | 129909 vs 145394 (-10.7%) | 173902 vs 193859 (-10.3%) |
| avg_lookup | 4320 vs 48465 (-91.1%) | 77592 vs 96929 (-20.0%) | 77592 vs 145394 (-46.6%) | 77592 vs 193859 (-60.0%) |
| avg_equation | 2016 vs 48465 (-95.8%) | 96202 vs 96929 (-0.8%) | 96202 vs 145394 (-33.8%) | 96202 vs 193859 (-50.4%) |
| avg_equation_resolved | 4320 vs 48465 (-91.1%) | 96202 vs 96929 (-0.8%) | 129909 vs 145394 (-10.7%) | 129909 vs 193859 (-33.0%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 200 | 27264 | 252545 (over) vs 252545 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T512: 200 | 80567 | 252545 (over) vs 252545 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T2048: 200 | 129909 | 252545 (over) vs 252545 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T4096: 200 | 173902 | 252545 (over) vs 252545 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 200 | 27264 | 252545 (over) vs 252545 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T512: 200 | 80567 | 252545 (over) vs 252545 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T2048: 200 | 129909 | 252545 (over) vs 252545 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T4096: 200 | 173902 | 252545 (over) vs 252545 (over) |
- `avg_gated_equation_resolved` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +6.7 points, sd 4.5, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 91.1% of the budget, 2.2% of the default cost. Mirror fold +2.9 points, sd 5.6 on 70 questions (clears).
- `avg_gated_equation_resolved` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F3. Verification margin +10.0 points, sd 5.5, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 0.8% of the budget, 49.6% of the default cost. Mirror fold +12.9 points, sd 5.4 on 70 questions (clears).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -3.3 points, sd 5.7, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 10.7% of the budget, 67.0% of the default cost. Mirror fold +0.0 points, sd 0.0 on 70 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -3.3 points, sd 5.7, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 10.3% of the budget, 89.7% of the default cost. Mirror fold +2.9 points, sd 2.0 on 70 questions (clears).
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 77.0 points at 40.0% of the default cost, 20.0% under the budget it was given.
- `avg_gated_lookup` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +6.7 points, sd 4.5, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 91.1% of the budget, 2.2% of the default cost. Mirror fold +2.9 points, sd 5.6 on 70 questions (clears).
- `avg_gated_lookup` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +10.0 points, sd 5.6, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 20.0% of the budget, 40.0% of the default cost. Mirror fold +12.9 points, sd 5.4 on 70 questions (clears).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -3.3 points, sd 7.4, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 10.7% of the budget, 67.0% of the default cost. Mirror fold +0.0 points, sd 0.0 on 70 questions (fails).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -3.3 points, sd 7.4, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 10.3% of the budget, 89.7% of the default cost. Mirror fold +2.9 points, sd 2.0 on 70 questions (clears).
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 77.0 points at 40.0% of the default cost, 20.0% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 77.0 points at 40.0% of the default cost, 46.6% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 77.0 points at 40.0% of the default cost, 60.0% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
