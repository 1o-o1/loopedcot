# Table 1 -- bbh (mcleish_llama32_r32), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 28561 layer passes over 2137 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 43.5 | +0.2 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 34.5 | 39.7 | 43.6 | 43.6 | +0.1 |
| lookup | 33.8 | 39.7 | 43.6 | 43.6 | +0.1 |
| equation | 39.4 | 39.7 | 43.6 | 43.6 | +0.1 |
| equation_n100 | 34.5 | 39.7 | 43.6 | 43.6 | +0.1 |
| equation_n30 | 34.4 | 34.4 | 34.4 | 34.4 | +9.3 |
| equation_resolved | 33.8 | 39.7 | 43.6 | 43.6 | +0.1 |
| gated_equation | 34.5 | 39.7 | 43.6 | 43.6 | +0.1 |
| gated_equation_resolved | 34.5 | 39.7 | 43.6 | 43.6 | +0.1 |
| avg_gated_equation_resolved | 34.5 | 39.7 | 43.6 | 43.6 | +0.1 |
| avg_gated_lookup | 34.5 | 39.7 | 43.6 | 43.6 | +0.1 |
| avg_lookup | 33.8 | 39.7 | 43.6 | 43.6 | +0.1 |
| avg_equation | 39.4 | 39.7 | 43.6 | 43.7 | +0.0 |
| avg_equation_resolved | 33.8 | 39.7 | 43.6 | 43.6 | +0.1 |

The ORACLE GAP is the best single evaluation cell (depth 8 at cap 512, 43.7 points over 2137 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none.

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 4912 vs 7140 (-31.2%) | 8865 vs 14280 (-37.9%) | 16770 vs 21421 (-21.7%) | 16770 vs 28561 (-41.3%) |
| avg_gated_lookup | 4912 vs 7140 (-31.2%) | 8865 vs 14280 (-37.9%) | 16770 vs 21421 (-21.7%) | 16770 vs 28561 (-41.3%) |
| avg_lookup | 959 vs 7140 (-86.6%) | 8865 vs 14280 (-37.9%) | 15295 vs 21421 (-28.6%) | 15295 vs 28561 (-46.4%) |
| avg_equation | 4644 vs 7140 (-35.0%) | 8127 vs 14280 (-43.1%) | 15295 vs 21421 (-28.6%) | 28155 vs 28561 (-1.4%) |
| avg_equation_resolved | 959 vs 7140 (-86.6%) | 8127 vs 14280 (-43.1%) | 15295 vs 21421 (-28.6%) | 15295 vs 28561 (-46.4%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 8 | k8_T128: 220, k8_T64: 1917 | 4912 | 230424 (over) vs 230335 (over) |
| 0.50x | deepest_depth_capped | 8 | k8_T128: 1917, k8_T256: 220 | 8865 | 230424 (over) vs 230335 (over) |
| 0.75x | deepest_depth_capped | 8 | k8_T256: 1917, k8_T512: 220 | 16770 | 230424 (over) vs 230335 (over) |
| 1.00x | deepest_depth_capped | 8 | k8_T256: 1917, k8_T512: 220 | 16770 | 230424 (over) vs 230335 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 8 | k8_T128: 220, k8_T64: 1917 | 4912 | 230424 (over) vs 230335 (over) |
| 0.50x | deepest_depth_capped | 8 | k8_T128: 1917, k8_T256: 220 | 8865 | 230424 (over) vs 230335 (over) |
| 0.75x | deepest_depth_capped | 8 | k8_T256: 1917, k8_T512: 220 | 16770 | 230424 (over) vs 230335 (over) |
| 1.00x | deepest_depth_capped | 8 | k8_T256: 1917, k8_T512: 220 | 16770 | 230424 (over) vs 230335 (over) |
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap it affords) for every question. Verification margin -6.7 points, sd 5.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 31.2% of the budget, 17.2% of the default cost. Mirror fold -12.9 points, sd 4.2 on 210 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 37.9% of the budget, 31.0% of the default cost. Mirror fold -20.5 points, sd 4.3 on 210 questions (fails).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 21.7% of the budget, 58.7% of the default cost. Mirror fold -23.3 points, sd 4.5 on 210 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 41.3% of the budget, 58.7% of the default cost. Mirror fold -23.3 points, sd 4.5 on 210 questions (fails).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap it affords) for every question. Verification margin -6.7 points, sd 5.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 31.2% of the budget, 17.2% of the default cost. Mirror fold -12.9 points, sd 4.2 on 210 questions (fails).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 37.9% of the budget, 31.0% of the default cost. Mirror fold -20.5 points, sd 4.3 on 210 questions (fails).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 21.7% of the budget, 58.7% of the default cost. Mirror fold -23.3 points, sd 4.5 on 210 questions (fails).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 41.3% of the budget, 58.7% of the default cost. Mirror fold -23.3 points, sd 4.5 on 210 questions (fails).
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 43.6 points at 53.6% of the default cost, 28.6% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 43.6 points at 53.6% of the default cost, 46.4% under the budget it was given.
- `avg_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 43.6 points at 53.6% of the default cost, 28.6% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 43.6 points at 53.6% of the default cost, 46.4% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
