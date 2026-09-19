# Table 1 -- math500 (mcleish_llama32_r32), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 44956 layer passes over 400 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 30.2 | +1.8 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 28.7 | 29.8 | 30.0 | 30.0 | +2.0 |
| lookup | 28.7 | 28.7 | 28.7 | 28.7 | +3.3 |
| equation | 30.8 | 30.8 | 30.8 | 30.8 | +1.2 |
| equation_n100 | 30.8 | 30.8 | 30.8 | 30.8 | +1.2 |
| equation_n30 | 28.7 | 29.8 | 30.0 | 30.0 | +2.0 |
| equation_resolved | 32.0 | 32.0 | 32.0 | 32.0 | +0.0 |
| gated_equation | 28.7 | 29.8 | 30.0 | 30.0 | +2.0 |
| gated_equation_resolved | 28.7 | 29.8 | 30.0 | 30.0 | +2.0 |
| avg_gated_equation_resolved | 28.7 | 29.8 | 30.0 | 30.0 | +2.0 |
| avg_gated_lookup | 28.7 | 29.8 | 30.0 | 30.0 | +2.0 |
| avg_lookup | 28.7 | 28.7 | 28.7 | 28.7 | +3.3 |
| avg_equation | 30.8 | 30.8 | 30.8 | 30.8 | +1.2 |
| avg_equation_resolved | 32.0 | 32.0 | 32.0 | 32.0 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 256, 32.0 points over 400 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none.

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 11135 vs 11239 (-0.9%) | 19984 vs 22478 (-11.1%) | 30306 vs 33717 (-10.1%) | 30306 vs 44956 (-32.6%) |
| avg_gated_lookup | 11135 vs 11239 (-0.9%) | 19984 vs 22478 (-11.1%) | 30306 vs 33717 (-10.1%) | 30306 vs 44956 (-32.6%) |
| avg_lookup | 11135 vs 11239 (-0.9%) | 11135 vs 22478 (-50.5%) | 11135 vs 33717 (-67.0%) | 11135 vs 44956 (-75.2%) |
| avg_equation | 10242 vs 11239 (-8.9%) | 10242 vs 22478 (-54.4%) | 24005 vs 33717 (-28.8%) | 24005 vs 44956 (-46.6%) |
| avg_equation_resolved | 6188 vs 11239 (-44.9%) | 6188 vs 22478 (-72.5%) | 6188 vs 33717 (-81.6%) | 6188 vs 44956 (-86.2%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 8 | k8_T256: 400 | 11135 | 50949 (over) vs 50949 (over) |
| 0.50x | deepest_depth_capped | 8 | k8_T1024: 400 | 19984 | 50949 (over) vs 50949 (over) |
| 0.75x | deepest_depth_capped | 8 | k8_T2048: 400 | 30306 | 50949 (over) vs 50949 (over) |
| 1.00x | deepest_depth_capped | 8 | k8_T2048: 400 | 30306 | 50949 (over) vs 50949 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 8 | k8_T256: 400 | 11135 | 50949 (over) vs 50949 (over) |
| 0.50x | deepest_depth_capped | 8 | k8_T1024: 400 | 19984 | 50949 (over) vs 50949 (over) |
| 0.75x | deepest_depth_capped | 8 | k8_T2048: 400 | 30306 | 50949 (over) vs 50949 (over) |
| 1.00x | deepest_depth_capped | 8 | k8_T2048: 400 | 30306 | 50949 (over) vs 50949 (over) |
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 0.9% of the budget, 24.8% of the default cost. Mirror fold -2.9 points, sd 5.6 on 70 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 11.1% of the budget, 44.5% of the default cost. Mirror fold +5.7 points, sd 5.3 on 70 questions (clears).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 10.1% of the budget, 67.4% of the default cost. Mirror fold +2.9 points, sd 5.3 on 70 questions (clears).
- `avg_gated_equation_resolved` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 32.6% of the budget, 67.4% of the default cost. Mirror fold +2.9 points, sd 5.3 on 70 questions (clears).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 0.9% of the budget, 24.8% of the default cost. Mirror fold -1.4 points, sd 5.8 on 70 questions (fails).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 11.1% of the budget, 44.5% of the default cost. Mirror fold +7.1 points, sd 5.4 on 70 questions (clears).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 10.1% of the budget, 67.4% of the default cost. Mirror fold +2.9 points, sd 5.3 on 70 questions (clears).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 32.6% of the budget, 67.4% of the default cost. Mirror fold +2.9 points, sd 5.3 on 70 questions (clears).
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 28.7 points at 24.8% of the default cost, 50.5% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 28.7 points at 24.8% of the default cost, 67.0% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 28.7 points at 24.8% of the default cost, 75.2% under the budget it was given.
- `avg_equation_resolved` at 0.25x: the multiplier is 0, so the budget never binds. The row is the same 32.0 points at 13.8% of the default cost, 44.9% under the budget it was given.
- `avg_equation_resolved` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 32.0 points at 13.8% of the default cost, 72.5% under the budget it was given.
- `avg_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 32.0 points at 13.8% of the default cost, 81.6% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 32.0 points at 13.8% of the default cost, 86.2% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
