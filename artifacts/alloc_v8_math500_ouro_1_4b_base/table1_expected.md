# Table 1 -- math500 (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 83459 layer passes over 400 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 63.5 | +2.5 |
| default_cell | n/a | n/a | n/a | 63.5 | +2.5 |
| default_at_budget | 31.8 | 56.5 | 64.0 | 63.5 | +2.5 |
| lookup | 37.0 | 65.5 | 65.5 | 65.5 | +0.5 |
| equation | 37.0 | 64.5 | 66.0 | 66.0 | +0.0 |
| equation_n100 | 37.0 | 64.5 | 66.0 | 66.0 | +0.0 |
| equation_n30 | 37.0 | 65.5 | 66.0 | 66.0 | +0.0 |
| equation_resolved | 37.0 | 65.5 | 64.0 | 63.5 | +2.5 |
| gated_equation | 37.0 | 65.5 | 64.0 | 63.5 | +2.5 |
| gated_equation_resolved | 37.0 | 65.5 | 64.0 | 63.5 | +2.5 |
| avg_gated_equation_resolved | 31.8 | 65.5 | 64.0 | 63.5 | +2.5 |
| avg_gated_lookup | 31.8 | 65.5 | 64.0 | 63.5 | +2.5 |
| avg_lookup | 19.2 | 65.5 | 65.5 | 65.5 | +0.5 |
| avg_equation | 19.2 | 64.5 | 66.0 | 66.0 | +0.0 |
| avg_equation_resolved | 19.2 | 65.5 | 64.0 | 63.5 | +2.5 |

The ORACLE GAP is the best single evaluation cell (depth 3 at cap 4096, 66.0 points over 400 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2. Of the families that CLEAR the bar the one that RUNS is set by `policy.GATE_FAMILY_RULE` = `best`: the cleared family with the largest mean verified margin over the folds, ties to the smaller family. The folds, the bar, the reference and the pricing are the same test under either rule; only which cleared family is taken differs.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 15050 vs 20865 (-27.9%) | 38502 vs 41729 (-7.7%) | 56583 vs 62594 (-9.6%) | 72312 vs 83459 (-13.4%) |
| avg_gated_lookup | 15050 vs 20865 (-27.9%) | 38502 vs 41729 (-7.7%) | 56583 vs 62594 (-9.6%) | 72312 vs 83459 (-13.4%) |
| avg_lookup | 2592 vs 20865 (-87.6%) | 38502 vs 41729 (-7.7%) | 38502 vs 62594 (-38.5%) | 38502 vs 83459 (-53.9%) |
| avg_equation | 2592 vs 20865 (-87.6%) | 35538 vs 41729 (-14.8%) | 61601 vs 62594 (-1.6%) | 61601 vs 83459 (-26.2%) |
| avg_equation_resolved | 2592 vs 20865 (-87.6%) | 38502 vs 41729 (-7.7%) | 56583 vs 62594 (-9.6%) | 72312 vs 83459 (-13.4%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 400 | 15050 | 72312 (over) vs 72312 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T512: 400 | 35293 | 72312 (over) vs 72312 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T2048: 400 | 56583 | 72312 (over) vs 72312 (over) |
| 1.00x | default_cell | 4 | k4_T4096: 400 | 72312 | 72312 (fits) vs 72312 (fits) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 400 | 15050 | 72312 (over) vs 72312 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T512: 400 | 35293 | 72312 (over) vs 72312 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T2048: 400 | 56583 | 72312 (over) vs 72312 (over) |
| 1.00x | default_cell | 4 | k4_T4096: 400 | 72312 | 72312 (fits) vs 72312 (fits) |
- `avg_gated_equation_resolved` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 65.5 points at 46.1% of the default cost, 7.7% under the budget it was given.
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -3.3 points, sd 5.7, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 27.9% of the budget, 18.0% of the default cost. Mirror fold -15.7 points, sd 5.6 on 70 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +6.7 points, sd 8.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 7.7% of the budget, 46.1% of the default cost. Mirror fold +5.7 points, sd 5.3 on 70 questions (clears).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 9.6% of the budget, 67.8% of the default cost. Mirror fold -4.3 points, sd 5.5 on 70 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: reverted to the default cell for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 13.4% of the budget, 86.6% of the default cost. Mirror fold +0.0 points, sd 0.0 on 70 questions (fails).
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 65.5 points at 46.1% of the default cost, 7.7% under the budget it was given.
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -3.3 points, sd 5.7, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 27.9% of the budget, 18.0% of the default cost. Mirror fold -12.9 points, sd 6.0 on 70 questions (fails).
- `avg_gated_lookup` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +6.7 points, sd 8.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 7.7% of the budget, 46.1% of the default cost. Mirror fold +5.7 points, sd 5.3 on 70 questions (clears).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -3.3 points, sd 10.1, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 9.6% of the budget, 67.8% of the default cost. Mirror fold +0.0 points, sd 0.0 on 70 questions (fails).
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin -3.3 points, sd 10.1, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 13.4% of the budget, 86.6% of the default cost. Mirror fold +0.0 points, sd 0.0 on 70 questions (fails).
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 65.5 points at 46.1% of the default cost, 7.7% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 65.5 points at 46.1% of the default cost, 38.5% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 65.5 points at 46.1% of the default cost, 53.9% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 66.0 points at 73.8% of the default cost, 1.6% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 66.0 points at 73.8% of the default cost, 26.2% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 63.5 points at 86.6% of the default cost, 13.4% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
