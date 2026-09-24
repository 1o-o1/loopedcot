# Table 1 -- math500 (mcleish_llama32_r32), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 44956 layer passes over 400 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 30.2 | +1.8 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 27.0 | 28.7 | 30.0 | 30.0 | +2.0 |
| lookup | 32.0 | 28.7 | 28.7 | 28.7 | +3.3 |
| equation | 32.0 | 30.8 | 30.8 | 30.8 | +1.2 |
| equation_n100 | 32.0 | 30.8 | 30.8 | 30.8 | +1.2 |
| equation_n30 | 27.0 | 28.7 | 30.0 | 30.0 | +2.0 |
| equation_resolved | 32.0 | 32.0 | 32.0 | 32.0 | +0.0 |
| gated_equation | 27.0 | 28.7 | 30.0 | 30.0 | +2.0 |
| gated_equation_resolved | 27.0 | 28.7 | 30.0 | 30.0 | +2.0 |
| avg_gated_equation_resolved | 27.0 | 28.7 | 30.0 | 30.0 | +2.0 |
| avg_gated_lookup | 27.0 | 28.7 | 30.0 | 30.0 | +2.0 |
| avg_lookup | 32.0 | 28.7 | 28.7 | 28.7 | +3.3 |
| avg_equation | 32.0 | 30.8 | 30.8 | 30.8 | +1.2 |
| avg_equation_resolved | 32.0 | 32.0 | 32.0 | 32.0 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 256, 32.0 points over 400 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none. Of the families that CLEAR the bar the one that RUNS is set by `policy.GATE_FAMILY_RULE` = `best`: the cleared family with the largest mean verified margin over the folds, ties to the smaller family. The folds, the bar, the reference and the pricing are the same test under either rule; only which cleared family is taken differs.

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 9184 vs 11239 (-18.3%) | 16352 vs 22478 (-27.3%) | 30688 vs 33717 (-9.0%) | 30688 vs 44956 (-31.7%) |
| avg_gated_lookup | 9184 vs 11239 (-18.3%) | 16352 vs 22478 (-27.3%) | 30688 vs 33717 (-9.0%) | 30688 vs 44956 (-31.7%) |
| avg_lookup | 9344 vs 11239 (-16.9%) | 16352 vs 22478 (-27.3%) | 16352 vs 33717 (-51.5%) | 16352 vs 44956 (-63.6%) |
| avg_equation | 9344 vs 11239 (-16.9%) | 17536 vs 22478 (-22.0%) | 17536 vs 33717 (-48.0%) | 33920 vs 44956 (-24.5%) |
| avg_equation_resolved | 9344 vs 11239 (-16.9%) | 9344 vs 22478 (-58.4%) | 9344 vs 33717 (-72.3%) | 9344 vs 44956 (-79.2%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 8 | k8_T128: 400 | 9184 | 231392 (over) vs 231392 (over) |
| 0.50x | deepest_depth_capped | 8 | k8_T256: 400 | 16352 | 231392 (over) vs 231392 (over) |
| 0.75x | deepest_depth_capped | 8 | k8_T512: 400 | 30688 | 231392 (over) vs 231392 (over) |
| 1.00x | deepest_depth_capped | 8 | k8_T512: 400 | 30688 | 231392 (over) vs 231392 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 8 | k8_T128: 400 | 9184 | 231392 (over) vs 231392 (over) |
| 0.50x | deepest_depth_capped | 8 | k8_T256: 400 | 16352 | 231392 (over) vs 231392 (over) |
| 0.75x | deepest_depth_capped | 8 | k8_T512: 400 | 30688 | 231392 (over) vs 231392 (over) |
| 1.00x | deepest_depth_capped | 8 | k8_T512: 400 | 30688 | 231392 (over) vs 231392 (over) |
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 9.4, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 18.3% of the budget, 20.4% of the default cost. Mirror fold +12.9 points, sd 5.4 on 70 questions (clears).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 8.2, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 27.3% of the budget, 36.4% of the default cost. Mirror fold -2.9 points, sd 5.6 on 70 questions (fails).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 8.2, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 9.0% of the budget, 68.3% of the default cost. Mirror fold +2.9 points, sd 4.9 on 70 questions (clears).
- `avg_gated_equation_resolved` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 8.2, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 31.7% of the budget, 68.3% of the default cost. Mirror fold +2.9 points, sd 4.9 on 70 questions (clears).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 9.4, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 18.3% of the budget, 20.4% of the default cost. Mirror fold +0.0 points, sd 0.0 on 70 questions (fails).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 27.3% of the budget, 36.4% of the default cost. Mirror fold -14.3 points, sd 5.0 on 70 questions (fails).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 9.0% of the budget, 68.3% of the default cost. Mirror fold -8.6 points, sd 4.4 on 70 questions (fails).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 31.7% of the budget, 68.3% of the default cost. Mirror fold -8.6 points, sd 4.4 on 70 questions (fails).
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 28.7 points at 36.4% of the default cost, 27.3% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 28.7 points at 36.4% of the default cost, 51.5% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 28.7 points at 36.4% of the default cost, 63.6% under the budget it was given.
- `avg_equation_resolved` at 0.25x: the multiplier is 0, so the budget never binds. The row is the same 32.0 points at 20.8% of the default cost, 16.9% under the budget it was given.
- `avg_equation_resolved` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 32.0 points at 20.8% of the default cost, 58.4% under the budget it was given.
- `avg_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 32.0 points at 20.8% of the default cost, 72.3% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 32.0 points at 20.8% of the default cost, 79.2% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
