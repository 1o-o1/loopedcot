# Table 1 -- bbh (mcleish_llama32_r32), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 49835 layer passes over 2137 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 43.2 | +0.5 |
| default_cell | n/a | n/a | n/a | 47.3 (90%) | -3.6 |
| default_at_budget | 43.5 | 43.5 | 43.5 | 43.2 | +0.5 |
| lookup | 43.6 | 43.6 | 43.6 | 43.6 | +0.1 |
| equation | 43.5 | 43.5 | 43.5 | 43.2 | +0.5 |
| equation_n100 | 43.5 | 43.5 | 43.5 | 43.2 | +0.5 |
| equation_n30 | 34.4 | 34.4 | 34.4 | 42.7 | +1.0 |
| equation_resolved | 43.6 | 43.6 | 43.6 | 43.6 | +0.1 |
| gated_equation | 43.5 | 43.5 | 43.5 | 43.2 | +0.5 |
| gated_equation_resolved | 43.5 | 43.5 | 43.5 | 43.2 | +0.5 |
| avg_gated_equation_resolved | 43.5 | 43.5 | 43.5 | 43.2 | +0.5 |
| avg_gated_lookup | 43.5 | 43.5 | 43.5 | 43.2 | +0.5 |
| avg_lookup | 43.6 | 43.6 | 43.6 | 43.6 | +0.1 |
| avg_equation | 43.7 | 43.5 | 43.5 | 43.2 | +0.5 |
| avg_equation_resolved | 43.6 | 43.6 | 43.6 | 43.6 | +0.1 |

The ORACLE GAP is the best single evaluation cell (depth 8 at cap 512, 43.7 points over 2137 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none. Of the families that CLEAR the bar the one that RUNS is set by `policy.GATE_FAMILY_RULE` = `best`: the cleared family with the largest mean verified margin over the folds, ties to the smaller family. The folds, the bar, the reference and the pricing are the same test under either rule; only which cleared family is taken differs.

`default_cell` is the default operating point (depth 8 at cap 8192) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 12168 vs 12459 (-2.3%) | 17329 vs 24917 (-30.5%) | 27651 vs 37376 (-26.0%) | 48294 vs 49835 (-3.1%) |
| avg_gated_lookup | 12168 vs 12459 (-2.3%) | 17329 vs 24917 (-30.5%) | 27651 vs 37376 (-26.0%) | 48294 vs 49835 (-3.1%) |
| avg_lookup | 8016 vs 12459 (-35.7%) | 8016 vs 24917 (-67.8%) | 8016 vs 37376 (-78.6%) | 8016 vs 49835 (-83.9%) |
| avg_equation | 10381 vs 12459 (-16.7%) | 17329 vs 24917 (-30.5%) | 29776 vs 37376 (-20.3%) | 48294 vs 49835 (-3.1%) |
| avg_equation_resolved | 8016 vs 12459 (-35.7%) | 8016 vs 24917 (-67.8%) | 8016 vs 37376 (-78.6%) | 8016 vs 49835 (-83.9%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 8 | k8_T1024: 2137 | 12168 | 48384 (over) vs 48294 (over) |
| 0.50x | deepest_depth_capped | 8 | k8_T2048: 2137 | 17329 | 48384 (over) vs 48294 (over) |
| 0.75x | deepest_depth_capped | 8 | k8_T4096: 2137 | 27651 | 48384 (over) vs 48294 (over) |
| 1.00x | default_cell | 8 | k8_T8192: 2137 | 48294 | 48384 (fits) vs 48294 (fits) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 8 | k8_T1024: 2137 | 12168 | 48384 (over) vs 48294 (over) |
| 0.50x | deepest_depth_capped | 8 | k8_T2048: 2137 | 17329 | 48384 (over) vs 48294 (over) |
| 0.75x | deepest_depth_capped | 8 | k8_T4096: 2137 | 27651 | 48384 (over) vs 48294 (over) |
| 1.00x | default_cell | 8 | k8_T8192: 2137 | 48294 | 48384 (fits) vs 48294 (fits) |
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 2.3% of the budget, 24.4% of the default cost. Mirror fold -11.0 points, sd 3.5 on 210 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 30.5% of the budget, 34.8% of the default cost. Mirror fold -11.0 points, sd 3.5 on 210 questions (fails).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 26.0% of the budget, 55.5% of the default cost. Mirror fold -11.4 points, sd 3.5 on 210 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: reverted to the default cell for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 3.1% of the budget, 96.9% of the default cost. Mirror fold -11.9 points, sd 3.5 on 210 questions (fails).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 2.3% of the budget, 24.4% of the default cost. Mirror fold -11.0 points, sd 3.5 on 210 questions (fails).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 30.5% of the budget, 34.8% of the default cost. Mirror fold -11.0 points, sd 3.5 on 210 questions (fails).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 26.0% of the budget, 55.5% of the default cost. Mirror fold -11.4 points, sd 3.5 on 210 questions (fails).
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 3.1% of the budget, 96.9% of the default cost. Mirror fold -11.9 points, sd 3.5 on 210 questions (fails).
- `avg_lookup` at 0.25x: the multiplier is 0, so the budget never binds. The row is the same 43.6 points at 16.1% of the default cost, 35.7% under the budget it was given.
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 43.6 points at 16.1% of the default cost, 67.8% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 43.6 points at 16.1% of the default cost, 78.6% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 43.6 points at 16.1% of the default cost, 83.9% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 43.2 points at 96.9% of the default cost, 3.1% under the budget it was given.
- `avg_equation_resolved` at 0.25x: the multiplier is 0, so the budget never binds. The row is the same 43.6 points at 16.1% of the default cost, 35.7% under the budget it was given.
- `avg_equation_resolved` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 43.6 points at 16.1% of the default cost, 67.8% under the budget it was given.
- `avg_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 43.6 points at 16.1% of the default cost, 78.6% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 43.6 points at 16.1% of the default cost, 83.9% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
