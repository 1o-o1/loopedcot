# Table 1 -- csqa (ouro_1_4b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 83226 layer passes over 977 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 76.7 | +0.0 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 72.8 | 75.2 | 75.2 | 75.2 | +1.4 |
| lookup | 73.9 | 73.9 | 75.2 | 75.2 | +1.4 |
| equation | 73.9 | 75.5 | 75.2 | 75.2 | +1.4 |
| equation_n100 | 73.9 | 75.5 | 75.2 | 75.2 | +1.4 |
| equation_n30 | 73.9 | 75.5 | 75.5 | 75.9 | +0.7 |
| equation_resolved | 73.9 | 73.9 | 75.2 | 75.2 | +1.4 |
| gated_equation | 72.8 | 75.2 | 75.2 | 75.2 | +1.4 |
| gated_equation_resolved | 72.8 | 75.2 | 75.2 | 75.2 | +1.4 |
| avg_gated_equation_resolved | 72.8 | 75.2 | 75.2 | 75.2 | +1.4 |
| avg_gated_lookup | 72.8 | 75.2 | 75.2 | 75.2 | +1.4 |
| avg_lookup | 73.9 | 73.9 | 75.2 | 75.2 | +1.4 |
| avg_equation | 73.9 | 75.2 | 75.2 | 75.2 | +1.4 |
| avg_equation_resolved | 73.9 | 73.9 | 75.2 | 75.2 | +1.4 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 2048, 76.7 points over 977 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 13632 vs 20807 (-34.5%) | 25920 vs 41613 (-37.7%) | 50496 vs 62420 (-19.1%) | 50496 vs 83226 (-39.3%) |
| avg_gated_lookup | 13632 vs 20807 (-34.5%) | 25920 vs 41613 (-37.7%) | 50496 vs 62420 (-19.1%) | 50496 vs 83226 (-39.3%) |
| avg_lookup | 7488 vs 20807 (-64.0%) | 7488 vs 41613 (-82.0%) | 50496 vs 62420 (-19.1%) | 50496 vs 83226 (-39.3%) |
| avg_equation | 7488 vs 20807 (-64.0%) | 25920 vs 41613 (-37.7%) | 50496 vs 62420 (-19.1%) | 50496 vs 83226 (-39.3%) |
| avg_equation_resolved | 7488 vs 20807 (-64.0%) | 7488 vs 41613 (-82.0%) | 50496 vs 62420 (-19.1%) | 50496 vs 83226 (-39.3%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 977 | 13632 | 394560 (over) vs 394560 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T256: 977 | 25920 | 394560 (over) vs 394560 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T512: 977 | 50496 | 394560 (over) vs 394560 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T512: 977 | 50496 | 394560 (over) vs 394560 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 977 | 13632 | 394560 (over) vs 394560 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T256: 977 | 25920 | 394560 (over) vs 394560 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T512: 977 | 50496 | 394560 (over) vs 394560 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T512: 977 | 50496 | 394560 (over) vs 394560 (over) |
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 34.5% of the budget, 16.4% of the default cost. Mirror fold -1.8 points, sd 2.1 on 171 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 37.7% of the budget, 31.1% of the default cost. Mirror fold -2.3 points, sd 2.5 on 171 questions (fails).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 19.1% of the budget, 60.7% of the default cost. Mirror fold -4.1 points, sd 2.7 on 171 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 39.3% of the budget, 60.7% of the default cost. Mirror fold -4.1 points, sd 2.7 on 171 questions (fails).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 34.5% of the budget, 16.4% of the default cost. Mirror fold -1.8 points, sd 2.1 on 171 questions (fails).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +5.5 points, sd 4.6, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 37.7% of the budget, 31.1% of the default cost. Mirror fold -2.3 points, sd 2.5 on 171 questions (fails).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 19.1% of the budget, 60.7% of the default cost. Mirror fold -4.1 points, sd 2.7 on 171 questions (fails).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 39.3% of the budget, 60.7% of the default cost. Mirror fold -4.1 points, sd 2.7 on 171 questions (fails).

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
