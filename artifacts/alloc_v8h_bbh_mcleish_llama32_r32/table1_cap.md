# Table 1 -- bbh (mcleish_llama32_r32), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 49835 layer passes over 2137 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 43.2 | +0.5 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 39.7 | 43.6 | 43.7 | 43.7 | +0.0 |
| lookup | 39.7 | 43.6 | 43.6 | 43.6 | +0.1 |
| equation | 39.7 | 43.6 | 43.7 | 43.7 | +0.0 |
| equation_n100 | 39.7 | 43.6 | 43.7 | 43.7 | +0.0 |
| equation_n30 | 34.4 | 34.4 | 34.4 | 34.4 | +9.3 |
| equation_resolved | 39.7 | 43.6 | 43.6 | 43.6 | +0.1 |
| gated_equation | 39.7 | 43.6 | 43.7 | 43.7 | +0.0 |
| gated_equation_resolved | 39.7 | 43.6 | 43.7 | 43.7 | +0.0 |
| avg_gated_equation_resolved | 39.7 | 43.6 | 43.7 | 43.7 | +0.0 |
| avg_gated_lookup | 39.7 | 43.6 | 43.7 | 43.7 | +0.0 |
| avg_lookup | 39.7 | 43.6 | 43.6 | 43.6 | +0.1 |
| avg_equation | 39.7 | 43.6 | 43.7 | 43.7 | +0.0 |
| avg_equation_resolved | 39.7 | 43.6 | 43.6 | 43.6 | +0.1 |

The ORACLE GAP is the best single evaluation cell (depth 8 at cap 512, 43.7 points over 2137 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none. Of the families that CLEAR the bar the one that RUNS is set by `policy.GATE_FAMILY_RULE` = `best`: the cleared family with the largest mean verified margin over the folds, ties to the smaller family. The folds, the bar, the reference and the pricing are the same test under either rule; only which cleared family is taken differs.

`default_cell` is the default operating point (depth 8 at cap 8192) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 8127 vs 12459 (-34.8%) | 15295 vs 24917 (-38.6%) | 29631 vs 37376 (-20.7%) | 29631 vs 49835 (-40.5%) |
| avg_gated_lookup | 8127 vs 12459 (-34.8%) | 15295 vs 24917 (-38.6%) | 29631 vs 37376 (-20.7%) | 29631 vs 49835 (-40.5%) |
| avg_lookup | 8865 vs 12459 (-28.8%) | 15295 vs 24917 (-38.6%) | 15295 vs 37376 (-59.1%) | 15295 vs 49835 (-69.3%) |
| avg_equation | 8127 vs 12459 (-34.8%) | 16770 vs 24917 (-32.7%) | 32582 vs 37376 (-12.8%) | 32582 vs 49835 (-34.6%) |
| avg_equation_resolved | 8127 vs 12459 (-34.8%) | 15295 vs 24917 (-38.6%) | 15295 vs 37376 (-59.1%) | 15295 vs 49835 (-69.3%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 8 | k8_T128: 2137 | 8127 | 459800 (over) vs 459711 (over) |
| 0.50x | deepest_depth_capped | 8 | k8_T256: 2137 | 15295 | 459800 (over) vs 459711 (over) |
| 0.75x | deepest_depth_capped | 8 | k8_T512: 2137 | 29631 | 459800 (over) vs 459711 (over) |
| 1.00x | deepest_depth_capped | 8 | k8_T512: 2137 | 29631 | 459800 (over) vs 459711 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 8 | k8_T128: 2137 | 8127 | 459800 (over) vs 459711 (over) |
| 0.50x | deepest_depth_capped | 8 | k8_T256: 2137 | 15295 | 459800 (over) vs 459711 (over) |
| 0.75x | deepest_depth_capped | 8 | k8_T512: 2137 | 29631 | 459800 (over) vs 459711 (over) |
| 1.00x | deepest_depth_capped | 8 | k8_T512: 2137 | 29631 | 459800 (over) vs 459711 (over) |
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 34.8% of the budget, 16.3% of the default cost. Mirror fold -9.5 points, sd 3.4 on 210 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 38.6% of the budget, 30.7% of the default cost. Mirror fold -12.4 points, sd 3.5 on 210 questions (fails).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 20.7% of the budget, 59.5% of the default cost. Mirror fold -11.0 points, sd 3.5 on 210 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 40.5% of the budget, 59.5% of the default cost. Mirror fold -11.0 points, sd 3.5 on 210 questions (fails).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 34.8% of the budget, 16.3% of the default cost. Mirror fold -9.5 points, sd 3.4 on 210 questions (fails).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 38.6% of the budget, 30.7% of the default cost. Mirror fold -12.4 points, sd 3.5 on 210 questions (fails).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 20.7% of the budget, 59.5% of the default cost. Mirror fold -11.0 points, sd 3.5 on 210 questions (fails).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 40.5% of the budget, 59.5% of the default cost. Mirror fold -11.0 points, sd 3.5 on 210 questions (fails).
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 43.6 points at 30.7% of the default cost, 38.6% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 43.6 points at 30.7% of the default cost, 59.1% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 43.6 points at 30.7% of the default cost, 69.3% under the budget it was given.
- `avg_equation_resolved` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 43.6 points at 30.7% of the default cost, 38.6% under the budget it was given.
- `avg_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 43.6 points at 30.7% of the default cost, 59.1% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 43.6 points at 30.7% of the default cost, 69.3% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
