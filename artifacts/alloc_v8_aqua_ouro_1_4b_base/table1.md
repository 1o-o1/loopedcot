# Table 1 -- aqua (ouro_1_4b_base), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 18914 layer passes over 154 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 67.5 | +1.3 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 57.1 | 60.4 | 68.8 | 68.8 | +0.0 |
| lookup | 57.1 | 55.2 | 66.2 | 66.2 | +2.6 |
| equation | 49.4 | 55.2 | 66.2 | 66.2 | +2.6 |
| equation_n100 | 49.4 | 55.2 | 66.2 | 66.2 | +2.6 |
| equation_n30 | 49.4 | 55.2 | 66.2 | 66.2 | +2.6 |
| equation_resolved | 57.1 | 53.2 | 66.2 | 66.2 | +2.6 |
| gated_equation | 57.1 | 60.4 | 68.8 | 68.8 | +0.0 |
| gated_equation_resolved | 57.1 | 60.4 | 68.8 | 68.8 | +0.0 |
| avg_gated_equation_resolved | 57.1 | 60.4 | 68.8 | 68.8 | +0.0 |
| avg_gated_lookup | 57.1 | 60.4 | 68.8 | 68.8 | +0.0 |
| avg_lookup | 53.9 | 53.9 | 66.2 | 66.2 | +2.6 |
| avg_equation | 49.4 | 55.2 | 66.2 | 66.2 | +2.6 |
| avg_equation_resolved | 53.9 | 53.9 | 66.2 | 66.2 | +2.6 |

The ORACLE GAP is the best single evaluation cell (depth 3 at cap 256, 68.8 points over 154 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none. Of the families that CLEAR the bar the one that RUNS is set by `policy.GATE_FAMILY_RULE` = `best`: the cleared family with the largest mean verified margin over the folds, ties to the smaller family. The folds, the bar, the reference and the pricing are the same test under either rule; only which cleared family is taken differs.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 4224 vs 4728 (-10.7%) | 7296 vs 9457 (-22.9%) | 13440 vs 14185 (-5.3%) | 13440 vs 18914 (-28.9%) |
| avg_gated_lookup | 4224 vs 4728 (-10.7%) | 7296 vs 9457 (-22.9%) | 13440 vs 14185 (-5.3%) | 13440 vs 18914 (-28.9%) |
| avg_lookup | 864 vs 4728 (-81.7%) | 864 vs 9457 (-90.9%) | 10080 vs 14185 (-28.9%) | 10080 vs 18914 (-46.7%) |
| avg_equation | 3168 vs 4728 (-33.0%) | 5472 vs 9457 (-42.1%) | 10080 vs 14185 (-28.9%) | 10080 vs 18914 (-46.7%) |
| avg_equation_resolved | 864 vs 4728 (-81.7%) | 864 vs 9457 (-90.9%) | 10080 vs 14185 (-28.9%) | 10080 vs 18914 (-46.7%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T32: 154 | 4224 | 394368 (over) vs 394368 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T64: 154 | 7296 | 394368 (over) vs 394368 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T128: 154 | 13440 | 394368 (over) vs 394368 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T128: 154 | 13440 | 394368 (over) vs 394368 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T32: 154 | 4224 | 394368 (over) vs 394368 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T64: 154 | 7296 | 394368 (over) vs 394368 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T128: 154 | 13440 | 394368 (over) vs 394368 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T128: 154 | 13440 | 394368 (over) vs 394368 (over) |
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -10.0 points, sd 5.3, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 10.7% of the budget, 22.3% of the default cost. Mirror fold -2.9 points, sd 4.0 on 70 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -10.0 points, sd 10.1, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 22.9% of the budget, 38.6% of the default cost. Mirror fold +0.0 points, sd 5.4 on 70 questions (fails).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +6.7 points, sd 4.6, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 5.3% of the budget, 71.1% of the default cost. Mirror fold +1.4 points, sd 4.3 on 70 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +6.7 points, sd 4.6, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 28.9% of the budget, 71.1% of the default cost. Mirror fold +1.4 points, sd 4.3 on 70 questions (fails).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -10.0 points, sd 5.3, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 10.7% of the budget, 22.3% of the default cost. Mirror fold -2.9 points, sd 4.0 on 70 questions (fails).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -26.7 points, sd 9.5, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 22.9% of the budget, 38.6% of the default cost. Mirror fold +0.0 points, sd 5.4 on 70 questions (fails).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +6.7 points, sd 4.6, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 5.3% of the budget, 71.1% of the default cost. Mirror fold +1.4 points, sd 4.3 on 70 questions (fails).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +6.7 points, sd 4.6, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 28.9% of the budget, 71.1% of the default cost. Mirror fold +1.4 points, sd 4.3 on 70 questions (fails).

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
