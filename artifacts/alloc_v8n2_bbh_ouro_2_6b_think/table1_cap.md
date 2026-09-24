# Table 1 -- bbh (ouro_2_6b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 202551 layer passes over 2137 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 88.7 | +0.1 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 57.4 | 82.1 | 83.0 | 85.9 | +2.9 |
| lookup | 77.0 | 81.0 | 85.3 | 86.1 | +2.8 |
| equation | 77.0 | 82.3 | 83.5 | 81.8 | +7.0 |
| equation_n100 | 77.0 | 82.8 | 85.3 | 86.1 | +2.8 |
| equation_n30 | 77.0 | 82.8 | 85.3 | 86.7 | +2.2 |
| equation_resolved | 77.0 | 81.0 | 85.3 | 86.1 | +2.8 |
| gated_equation | 62.6 | 82.8 | 85.3 | 86.1 | +2.8 |
| gated_equation_resolved | 77.0 | 82.8 | 85.3 | 86.1 | +2.8 |
| avg_gated_equation_resolved | 57.4 | 82.1 | 83.0 | 87.7 | +1.1 |
| avg_gated_lookup | 57.4 | 82.1 | 86.1 | 87.7 | +1.1 |
| avg_lookup | 57.0 | 81.2 | 86.1 | 86.1 | +2.8 |
| avg_equation | 57.7 | 80.7 | 86.1 | 85.9 | +2.9 |
| avg_equation_resolved | 57.0 | 81.2 | 86.1 | 86.1 | +2.8 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 2048, 88.8 points over 2137 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3. Of the families that CLEAR the bar the one that RUNS is set by `policy.GATE_FAMILY_RULE` = `best`: the cleared family with the largest mean verified margin over the folds, ties to the smaller family. The folds, the bar, the reference and the pricing are the same test under either rule; only which cleared family is taken differs.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 28055 vs 50638 (-44.6%) | 96723 vs 101275 (-4.5%) | 101783 vs 151913 (-33.0%) | 200087 vs 202551 (-1.2%) |
| avg_gated_lookup | 28055 vs 50638 (-44.6%) | 96723 vs 101275 (-4.5%) | 150065 vs 151913 (-1.2%) | 200087 vs 202551 (-1.2%) |
| avg_lookup | 8005 vs 50638 (-84.2%) | 101249 vs 101275 (-0.0%) | 150065 vs 151913 (-1.2%) | 150065 vs 202551 (-25.9%) |
| avg_equation | 10761 vs 50638 (-78.7%) | 100043 vs 101275 (-1.2%) | 150065 vs 151913 (-1.2%) | 165245 vs 202551 (-18.4%) |
| avg_equation_resolved | 8005 vs 50638 (-84.2%) | 101249 vs 101275 (-0.0%) | 150065 vs 151913 (-1.2%) | 150065 vs 202551 (-25.9%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 2137 | 28055 | 790217 (over) vs 789911 (over) |
| 0.50x | default_at_budget | 4 | k4_T256: 220, k4_T512: 1917 | 96723 | 790217 (over) vs 789911 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T512: 2137 | 101783 | 790217 (over) vs 789911 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T1024: 2137 | 200087 | 790217 (over) vs 789911 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 2137 | 28055 | 790217 (over) vs 789911 (over) |
| 0.50x | default_at_budget | 4 | k4_T256: 220, k4_T512: 1917 | 96723 | 790217 (over) vs 789911 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T512: 2137 | 101783 | 790217 (over) vs 789911 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T1024: 2137 | 200087 | 790217 (over) vs 789911 (over) |
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -3.3 points, sd 1.9, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 44.6% of the budget, 13.9% of the default cost. Mirror fold +25.7 points, sd 3.7 on 210 questions (clears).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap each question's own price affords -- the `default_at_budget` row) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 4.5% of the budget, 47.8% of the default cost. Mirror fold -1.9 points, sd 2.1 on 210 questions (fails).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +4.4 points, sd 3.8, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 33.0% of the budget, 50.3% of the default cost. Mirror fold -1.9 points, sd 2.1 on 210 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +2.2 points, sd 3.9, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 1.2% of the budget, 98.8% of the default cost. Mirror fold -3.3 points, sd 2.1 on 210 questions (fails).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -3.3 points, sd 1.9, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 44.6% of the budget, 13.9% of the default cost. Mirror fold +25.2 points, sd 3.8 on 210 questions (clears).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap each question's own price affords -- the `default_at_budget` row) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 4.5% of the budget, 47.8% of the default cost. Mirror fold -7.1 points, sd 2.4 on 210 questions (fails).
- `avg_gated_lookup` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +4.4 points, sd 3.8, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 1.2% of the budget, 74.1% of the default cost. Mirror fold +1.4 points, sd 2.1 on 210 questions (clears).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +2.2 points, sd 3.9, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 1.2% of the budget, 98.8% of the default cost. Mirror fold -3.3 points, sd 2.1 on 210 questions (fails).

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
