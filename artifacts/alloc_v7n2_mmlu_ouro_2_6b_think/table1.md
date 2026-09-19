# Table 1 -- mmlu (ouro_2_6b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 175146 layer passes over 1700 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 79.7 | +1.8 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 73.9 | 75.8 | 78.2 | 78.2 | +3.2 |
| lookup | 73.6 | 78.1 | 78.1 | 80.8 | +0.7 |
| equation | 74.9 | 78.1 | 78.1 | 80.8 | +0.7 |
| equation_n100 | 74.9 | 78.1 | 78.1 | 80.8 | +0.7 |
| equation_n30 | 74.9 | 78.1 | 78.2 | 80.8 | +0.7 |
| equation_resolved | 74.9 | 78.1 | 78.1 | 80.8 | +0.7 |
| gated_equation | 73.9 | 78.1 | 78.2 | 80.8 | +0.7 |
| gated_equation_resolved | 73.9 | 78.1 | 78.2 | 80.8 | +0.7 |
| avg_gated_equation_resolved | 73.9 | 75.8 | 78.2 | 80.8 | +0.7 |
| avg_gated_lookup | 73.9 | 75.8 | 78.2 | 80.8 | +0.7 |
| avg_lookup | 73.6 | 78.1 | 78.1 | 80.8 | +0.7 |
| avg_equation | 74.9 | 78.1 | 78.1 | 80.8 | +0.7 |
| avg_equation_resolved | 73.6 | 78.1 | 78.1 | 80.8 | +0.7 |

The ORACLE GAP is the best single evaluation cell (depth 3 at cap 4096, 81.5 points over 1700 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 27264 vs 43786 (-37.7%) | 51840 vs 87573 (-40.8%) | 100992 vs 131359 (-23.1%) | 149472 vs 175146 (-14.7%) |
| avg_gated_lookup | 27264 vs 43786 (-37.7%) | 51840 vs 87573 (-40.8%) | 100992 vs 131359 (-23.1%) | 149472 vs 175146 (-14.7%) |
| avg_lookup | 5760 vs 43786 (-86.8%) | 75744 vs 87573 (-13.5%) | 75744 vs 131359 (-42.3%) | 149472 vs 175146 (-14.7%) |
| avg_equation | 38880 vs 43786 (-11.2%) | 75744 vs 87573 (-13.5%) | 75744 vs 131359 (-42.3%) | 149472 vs 175146 (-14.7%) |
| avg_equation_resolved | 5760 vs 43786 (-86.8%) | 75744 vs 87573 (-13.5%) | 75744 vs 131359 (-42.3%) | 149472 vs 175146 (-14.7%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 1700 | 27264 | 789120 (over) vs 789120 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T256: 1700 | 51840 | 789120 (over) vs 789120 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T512: 1700 | 100992 | 789120 (over) vs 789120 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T512: 1700 | 100992 | 789120 (over) vs 789120 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 1700 | 27264 | 789120 (over) vs 789120 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T256: 1700 | 51840 | 789120 (over) vs 789120 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T512: 1700 | 100992 | 789120 (over) vs 789120 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T512: 1700 | 100992 | 789120 (over) vs 789120 (over) |
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -2.2 points, sd 2.3, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 37.7% of the budget, 15.6% of the default cost. Mirror fold -1.0 points, sd 1.6 on 210 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +2.2 points, sd 4.3, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 40.8% of the budget, 29.6% of the default cost. Mirror fold -1.4 points, sd 1.9 on 210 questions (fails).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -1.1 points, sd 3.3, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 23.1% of the budget, 57.7% of the default cost. Mirror fold -7.1 points, sd 2.7 on 210 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +2.2 points, sd 3.8, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 14.7% of the budget, 85.3% of the default cost. Mirror fold +5.2 points, sd 1.8 on 210 questions (clears).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -2.2 points, sd 2.3, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 37.7% of the budget, 15.6% of the default cost. Mirror fold +0.0 points, sd 0.0 on 210 questions (fails).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +2.2 points, sd 4.3, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 40.8% of the budget, 29.6% of the default cost. Mirror fold -0.5 points, sd 2.0 on 210 questions (fails).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -1.1 points, sd 3.3, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 23.1% of the budget, 57.7% of the default cost. Mirror fold -6.2 points, sd 2.7 on 210 questions (fails).
- `avg_gated_lookup` at 1.00x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +2.2 points, sd 3.8, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 14.7% of the budget, 85.3% of the default cost. Mirror fold +5.2 points, sd 1.8 on 210 questions (clears).

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
