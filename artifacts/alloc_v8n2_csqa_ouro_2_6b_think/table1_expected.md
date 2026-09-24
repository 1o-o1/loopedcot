# Table 1 -- csqa (ouro_2_6b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 134261 layer passes over 977 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 80.7 | +0.0 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 80.5 | 79.2 | 80.1 | 80.5 | +0.2 |
| lookup | 80.0 | 80.0 | 80.0 | 80.5 | +0.2 |
| equation | 80.5 | 76.4 | 79.8 | 80.5 | +0.2 |
| equation_n100 | 80.3 | 78.1 | 80.1 | 80.5 | +0.2 |
| equation_n30 | 75.0 | 76.4 | 76.6 | 76.6 | +4.1 |
| equation_resolved | 80.0 | 80.0 | 80.0 | 80.5 | +0.2 |
| gated_equation | 80.5 | 79.2 | 80.1 | 80.5 | +0.2 |
| gated_equation_resolved | 80.5 | 79.2 | 80.1 | 80.5 | +0.2 |
| avg_gated_equation_resolved | 80.5 | 79.2 | 80.1 | 80.5 | +0.2 |
| avg_gated_lookup | 80.5 | 79.2 | 80.1 | 80.5 | +0.2 |
| avg_lookup | 80.0 | 80.0 | 80.0 | 80.5 | +0.2 |
| avg_equation | 78.9 | 78.3 | 76.6 | 80.5 | +0.2 |
| avg_equation_resolved | 80.0 | 80.0 | 80.0 | 80.5 | +0.2 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 1024, 80.7 points over 977 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none. Of the families that CLEAR the bar the one that RUNS is set by `policy.GATE_FAMILY_RULE` = `best`: the cleared family with the largest mean verified margin over the folds, ties to the smaller family. The folds, the bar, the reference and the pricing are the same test under either rule; only which cleared family is taken differs.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 27264 vs 33565 (-18.8%) | 51794 vs 67130 (-22.8%) | 89334 vs 100696 (-11.3%) | 130285 vs 134261 (-3.0%) |
| avg_gated_lookup | 27264 vs 33565 (-18.8%) | 51794 vs 67130 (-22.8%) | 89334 vs 100696 (-11.3%) | 130285 vs 134261 (-3.0%) |
| avg_lookup | 14976 vs 33565 (-55.4%) | 14976 vs 67130 (-77.7%) | 14976 vs 100696 (-85.1%) | 130285 vs 134261 (-3.0%) |
| avg_equation | 2688 vs 33565 (-92.0%) | 38769 vs 67130 (-42.2%) | 80638 vs 100696 (-19.9%) | 130285 vs 134261 (-3.0%) |
| avg_equation_resolved | 14976 vs 33565 (-55.4%) | 14976 vs 67130 (-77.7%) | 14976 vs 100696 (-85.1%) | 130285 vs 134261 (-3.0%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 977 | 27264 | 149397 (over) vs 149397 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T256: 977 | 51794 | 149397 (over) vs 149397 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T512: 977 | 89334 | 149397 (over) vs 149397 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T2048: 977 | 130285 | 149397 (over) vs 149397 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 977 | 27264 | 149397 (over) vs 149397 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T256: 977 | 51794 | 149397 (over) vs 149397 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T512: 977 | 89334 | 149397 (over) vs 149397 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T2048: 977 | 130285 | 149397 (over) vs 149397 (over) |
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -2.7 points, sd 2.7, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 18.8% of the budget, 20.3% of the default cost. Mirror fold +1.8 points, sd 1.5 on 171 questions (clears).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 22.8% of the budget, 38.6% of the default cost. Mirror fold -1.2 points, sd 2.3 on 171 questions (fails).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -1.4 points, sd 3.0, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 11.3% of the budget, 66.5% of the default cost. Mirror fold +1.2 points, sd 2.2 on 171 questions (clears).
- `avg_gated_equation_resolved` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 3.0% of the budget, 97.0% of the default cost. Mirror fold -1.8 points, sd 2.4 on 171 questions (fails).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -2.7 points, sd 2.7, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 18.8% of the budget, 20.3% of the default cost. Mirror fold +0.0 points, sd 0.0 on 171 questions (fails).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +1.4 points, sd 3.6, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 22.8% of the budget, 38.6% of the default cost. Mirror fold -2.9 points, sd 2.3 on 171 questions (fails).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 3.9, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 11.3% of the budget, 66.5% of the default cost. Mirror fold -1.2 points, sd 2.5 on 171 questions (fails).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 3.0% of the budget, 97.0% of the default cost. Mirror fold -4.1 points, sd 2.6 on 171 questions (fails).
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 80.5 points at 97.0% of the default cost, 3.0% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 80.5 points at 97.0% of the default cost, 3.0% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
