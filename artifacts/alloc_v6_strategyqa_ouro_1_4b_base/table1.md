# Table 1 -- strategyqa (ouro_1_4b_base), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 24413 layer passes over 1990 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 66.5 | +1.9 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 66.9 | 66.5 | 66.6 | 66.6 | +1.8 |
| lookup | 68.1 | 68.1 | 68.1 | 68.1 | +0.3 |
| equation | 68.1 | 68.4 | 68.4 | 68.2 | +0.2 |
| equation_n100 | 66.9 | 66.5 | 66.6 | 66.6 | +1.8 |
| equation_n30 | 53.5 | 53.7 | 53.8 | 53.8 | +14.6 |
| equation_resolved | 68.1 | 68.1 | 68.1 | 68.1 | +0.3 |
| gated_equation | 66.9 | 68.4 | 68.4 | 68.2 | +0.2 |
| gated_equation_resolved | 66.9 | 68.1 | 68.1 | 68.1 | +0.3 |
| avg_gated_equation_resolved | 66.9 | 66.5 | 66.6 | 66.6 | +1.8 |
| avg_gated_lookup | 66.9 | 66.5 | 66.6 | 66.6 | +1.8 |
| avg_lookup | 68.1 | 68.1 | 68.1 | 68.1 | +0.3 |
| avg_equation | 68.1 | 68.4 | 68.4 | 68.2 | +0.2 |
| avg_equation_resolved | 68.1 | 68.1 | 68.1 | 68.1 | +0.3 |

The ORACLE GAP is the best single evaluation cell (depth 3 at cap 128, 68.4 points over 1990 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 4320 vs 6103 (-29.2%) | 7392 vs 12206 (-39.4%) | 13536 vs 18310 (-26.1%) | 13536 vs 24413 (-44.6%) |
| avg_gated_lookup | 4320 vs 6103 (-29.2%) | 7392 vs 12206 (-39.4%) | 13536 vs 18310 (-26.1%) | 13536 vs 24413 (-44.6%) |
| avg_lookup | 5544 vs 6103 (-9.2%) | 5544 vs 12206 (-54.6%) | 5544 vs 18310 (-69.7%) | 5544 vs 24413 (-77.3%) |
| avg_equation | 5544 vs 6103 (-9.2%) | 10152 vs 12206 (-16.8%) | 10152 vs 18310 (-44.6%) | 19368 vs 24413 (-20.7%) |
| avg_equation_resolved | 5544 vs 6103 (-9.2%) | 5544 vs 12206 (-54.6%) | 5544 vs 18310 (-69.7%) | 5544 vs 24413 (-77.3%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T32: 1990 | 4320 | 394464 (over) vs 394464 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T64: 1990 | 7392 | 394464 (over) vs 394464 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T128: 1990 | 13536 | 394464 (over) vs 394464 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T128: 1990 | 13536 | 394464 (over) vs 394464 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T32: 1990 | 4320 | 394464 (over) vs 394464 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T64: 1990 | 7392 | 394464 (over) vs 394464 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T128: 1990 | 13536 | 394464 (over) vs 394464 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T128: 1990 | 13536 | 394464 (over) vs 394464 (over) |
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin +1.1 points, sd 5.2, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 29.2% of the budget, 17.7% of the default cost. Mirror fold -0.5 points, sd 4.0 on 210 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin +6.7 points, sd 4.8, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 39.4% of the budget, 30.3% of the default cost. Mirror fold -1.0 points, sd 4.3 on 210 questions (fails).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin +10.0 points, sd 4.5, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 26.1% of the budget, 55.4% of the default cost. Mirror fold -1.0 points, sd 4.4 on 210 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin +10.0 points, sd 4.5, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 44.6% of the budget, 55.4% of the default cost. Mirror fold -1.0 points, sd 4.4 on 210 questions (fails).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin +1.1 points, sd 5.2, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 29.2% of the budget, 17.7% of the default cost. Mirror fold -0.5 points, sd 4.0 on 210 questions (fails).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin +6.7 points, sd 4.8, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 39.4% of the budget, 30.3% of the default cost. Mirror fold -1.0 points, sd 4.3 on 210 questions (fails).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin +10.0 points, sd 4.5, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 26.1% of the budget, 55.4% of the default cost. Mirror fold -1.0 points, sd 4.4 on 210 questions (fails).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin +10.0 points, sd 4.5, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 44.6% of the budget, 55.4% of the default cost. Mirror fold -1.0 points, sd 4.4 on 210 questions (fails).
- `avg_lookup` at 0.25x: the multiplier is 0, so the budget never binds. The row is the same 68.1 points at 22.7% of the default cost, 9.2% under the budget it was given.
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 68.1 points at 22.7% of the default cost, 54.6% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 68.1 points at 22.7% of the default cost, 69.7% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.1 points at 22.7% of the default cost, 77.3% under the budget it was given.
- `avg_equation_resolved` at 0.25x: the multiplier is 0, so the budget never binds. The row is the same 68.1 points at 22.7% of the default cost, 9.2% under the budget it was given.
- `avg_equation_resolved` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 68.1 points at 22.7% of the default cost, 54.6% under the budget it was given.
- `avg_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 68.1 points at 22.7% of the default cost, 69.7% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.1 points at 22.7% of the default cost, 77.3% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
