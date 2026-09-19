# Table 1 -- aqua (huginn_0125), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 69861 layer passes over 154 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 24.7 | +3.2 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 20.8 | 21.4 | 23.4 | 22.7 | +5.2 |
| lookup | 23.4 | 23.4 | 24.7 | 24.7 | +3.2 |
| equation | 24.0 | 25.3 | 24.7 | 24.7 | +3.2 |
| equation_n100 | 24.0 | 25.3 | 24.7 | 24.7 | +3.2 |
| equation_n30 | 24.0 | 25.3 | 24.7 | 24.7 | +3.2 |
| equation_resolved | 25.3 | 25.3 | 24.7 | 24.7 | +3.2 |
| gated_equation | 20.8 | 21.4 | 23.4 | 22.7 | +5.2 |
| gated_equation_resolved | 20.8 | 21.4 | 23.4 | 22.7 | +5.2 |
| avg_gated_equation_resolved | 20.8 | 21.4 | 23.4 | 22.7 | +5.2 |
| avg_gated_lookup | 20.8 | 21.4 | 23.4 | 22.7 | +5.2 |
| avg_lookup | 23.4 | 23.4 | 24.7 | 24.7 | +3.2 |
| avg_equation | 26.0 | 25.3 | 24.7 | 24.7 | +3.2 |
| avg_equation_resolved | 25.3 | 25.3 | 24.7 | 24.7 | +3.2 |

The ORACLE GAP is the best single evaluation cell (depth 2 at cap 0, 27.9 points over 154 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none.

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 10032 vs 17465 (-42.6%) | 18480 vs 34930 (-47.1%) | 35376 vs 52395 (-32.5%) | 69168 vs 69861 (-1.0%) |
| avg_gated_lookup | 10032 vs 17465 (-42.6%) | 18480 vs 34930 (-47.1%) | 35376 vs 52395 (-32.5%) | 69168 vs 69861 (-1.0%) |
| avg_lookup | 912 vs 17465 (-94.8%) | 912 vs 34930 (-97.4%) | 41200 vs 52395 (-21.4%) | 41200 vs 69861 (-41.0%) |
| avg_equation | 5360 vs 17465 (-69.3%) | 20720 vs 34930 (-40.7%) | 41200 vs 52395 (-21.4%) | 41200 vs 69861 (-41.0%) |
| avg_equation_resolved | 3216 vs 17465 (-81.6%) | 3216 vs 34930 (-90.8%) | 41200 vs 52395 (-21.4%) | 41200 vs 69861 (-41.0%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 32 | k32_T64: 154 | 10032 | 542256 (over) vs 542256 (over) |
| 0.50x | deepest_depth_capped | 32 | k32_T128: 154 | 18480 | 542256 (over) vs 542256 (over) |
| 0.75x | deepest_depth_capped | 32 | k32_T256: 154 | 35376 | 542256 (over) vs 542256 (over) |
| 1.00x | deepest_depth_capped | 32 | k32_T512: 154 | 69168 | 542256 (over) vs 542256 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 32 | k32_T64: 154 | 10032 | 542256 (over) vs 542256 (over) |
| 0.50x | deepest_depth_capped | 32 | k32_T128: 154 | 18480 | 542256 (over) vs 542256 (over) |
| 0.75x | deepest_depth_capped | 32 | k32_T256: 154 | 35376 | 542256 (over) vs 542256 (over) |
| 1.00x | deepest_depth_capped | 32 | k32_T512: 154 | 69168 | 542256 (over) vs 542256 (over) |
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) for every question. Verification margin -16.7 points, sd 11.4, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 42.6% of the budget, 14.4% of the default cost. Mirror fold -4.3 points, sd 4.7 on 70 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) for every question. Verification margin -13.3 points, sd 11.1, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 47.1% of the budget, 26.5% of the default cost. Mirror fold -5.7 points, sd 5.4 on 70 questions (fails).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) for every question. Verification margin -23.3 points, sd 12.1, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 32.5% of the budget, 50.6% of the default cost. Mirror fold -4.3 points, sd 5.2 on 70 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) for every question. Verification margin -23.3 points, sd 12.1, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 1.0% of the budget, 99.0% of the default cost. Mirror fold -4.3 points, sd 5.2 on 70 questions (fails).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) for every question. Verification margin -16.7 points, sd 11.4, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 42.6% of the budget, 14.4% of the default cost. Mirror fold +0.0 points, sd 0.0 on 70 questions (fails).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) for every question. Verification margin -13.3 points, sd 11.1, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 47.1% of the budget, 26.5% of the default cost. Mirror fold -1.4 points, sd 3.6 on 70 questions (fails).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) for every question. Verification margin -23.3 points, sd 12.1, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 32.5% of the budget, 50.6% of the default cost. Mirror fold +0.0 points, sd 0.0 on 70 questions (fails).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) for every question. Verification margin -23.3 points, sd 12.1, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 1.0% of the budget, 99.0% of the default cost. Mirror fold +0.0 points, sd 0.0 on 70 questions (fails).
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 24.7 points at 59.0% of the default cost, 21.4% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 24.7 points at 59.0% of the default cost, 41.0% under the budget it was given.
- `avg_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 24.7 points at 59.0% of the default cost, 21.4% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 24.7 points at 59.0% of the default cost, 41.0% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
