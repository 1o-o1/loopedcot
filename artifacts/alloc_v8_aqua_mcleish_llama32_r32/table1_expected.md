# Table 1 -- aqua (mcleish_llama32_r32), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 10531 layer passes over 154 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 53.2 | +3.9 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 41.6 | 53.9 | 53.9 | 52.6 | +4.5 |
| lookup | 43.5 | 53.9 | 53.9 | 53.9 | +3.2 |
| equation | 46.1 | 55.8 | 54.5 | 54.5 | +2.6 |
| equation_n100 | 46.1 | 55.8 | 54.5 | 54.5 | +2.6 |
| equation_n30 | 46.1 | 55.8 | 54.5 | 54.5 | +2.6 |
| equation_resolved | 42.9 | 53.9 | 53.9 | 53.9 | +3.2 |
| gated_equation | 46.1 | 53.9 | 53.9 | 52.6 | +4.5 |
| gated_equation_resolved | 46.1 | 53.9 | 53.9 | 52.6 | +4.5 |
| avg_gated_equation_resolved | 42.2 | 53.9 | 53.9 | 52.6 | +4.5 |
| avg_gated_lookup | 42.2 | 53.9 | 53.9 | 52.6 | +4.5 |
| avg_lookup | 43.5 | 53.9 | 53.9 | 53.9 | +3.2 |
| avg_equation | 25.3 | 55.8 | 54.5 | 54.5 | +2.6 |
| avg_equation_resolved | 43.5 | 55.2 | 53.9 | 53.9 | +3.2 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 1024, 57.1 points over 154 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3. Of the families that CLEAR the bar the one that RUNS is set by `policy.GATE_FAMILY_RULE` = `best`: the cleared family with the largest mean verified margin over the folds, ties to the smaller family. The folds, the bar, the reference and the pricing are the same test under either rule; only which cleared family is taken differs.

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 1328 vs 2633 (-49.6%) | 4785 vs 5265 (-9.1%) | 6597 vs 7898 (-16.5%) | 8317 vs 10531 (-21.0%) |
| avg_gated_lookup | 1328 vs 2633 (-49.6%) | 4785 vs 5265 (-9.1%) | 6597 vs 7898 (-16.5%) | 8317 vs 10531 (-21.0%) |
| avg_lookup | 1735 vs 2633 (-34.1%) | 4785 vs 5265 (-9.1%) | 4785 vs 7898 (-39.4%) | 4785 vs 10531 (-54.6%) |
| avg_equation | 240 vs 2633 (-90.9%) | 3551 vs 5265 (-32.6%) | 6992 vs 7898 (-11.5%) | 6992 vs 10531 (-33.6%) |
| avg_equation_resolved | 1735 vs 2633 (-34.1%) | 3240 vs 5265 (-38.5%) | 6597 vs 7898 (-16.5%) | 6597 vs 10531 (-37.4%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 8 | k8_T32: 154 | 2423 | 11758 (over) vs 11758 (over) |
| 0.50x | deepest_depth_capped | 8 | k8_T128: 154 | 4785 | 11758 (over) vs 11758 (over) |
| 0.75x | deepest_depth_capped | 8 | k8_T1024: 154 | 6597 | 11758 (over) vs 11758 (over) |
| 1.00x | deepest_depth_capped | 8 | k8_T2048: 154 | 8317 | 11758 (over) vs 11758 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 8 | k8_T32: 154 | 2423 | 11758 (over) vs 11758 (over) |
| 0.50x | deepest_depth_capped | 8 | k8_T128: 154 | 4785 | 11758 (over) vs 11758 (over) |
| 0.75x | deepest_depth_capped | 8 | k8_T1024: 154 | 6597 | 11758 (over) vs 11758 (over) |
| 1.00x | deepest_depth_capped | 8 | k8_T2048: 154 | 8317 | 11758 (over) vs 11758 (over) |
- `avg_gated_equation_resolved` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) on family F3. Verification margin +10.0 points, sd 10.9, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 49.6% of the budget, 12.6% of the default cost. Mirror fold +7.1 points, sd 6.6 on 70 questions (clears).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin -10.0 points, sd 9.7, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 9.1% of the budget, 45.4% of the default cost. Mirror fold +1.4 points, sd 6.3 on 70 questions (fails).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin -10.0 points, sd 9.7, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 16.5% of the budget, 62.6% of the default cost. Mirror fold +2.9 points, sd 2.0 on 70 questions (clears).
- `avg_gated_equation_resolved` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin -10.0 points, sd 9.7, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 21.0% of the budget, 79.0% of the default cost. Mirror fold +2.9 points, sd 2.0 on 70 questions (clears).
- `avg_gated_lookup` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) on family F3. Verification margin +10.0 points, sd 10.9, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 49.6% of the budget, 12.6% of the default cost. Mirror fold +7.1 points, sd 6.6 on 70 questions (clears).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin -10.0 points, sd 9.7, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 9.1% of the budget, 45.4% of the default cost. Mirror fold +0.0 points, sd 0.0 on 70 questions (fails).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin -10.0 points, sd 9.7, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 16.5% of the budget, 62.6% of the default cost. Mirror fold +2.9 points, sd 2.8 on 70 questions (clears).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin -10.0 points, sd 9.7, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 21.0% of the budget, 79.0% of the default cost. Mirror fold +2.9 points, sd 2.8 on 70 questions (clears).
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 53.9 points at 45.4% of the default cost, 9.1% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 53.9 points at 45.4% of the default cost, 39.4% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 53.9 points at 45.4% of the default cost, 54.6% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 54.5 points at 66.4% of the default cost, 11.5% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 54.5 points at 66.4% of the default cost, 33.6% under the budget it was given.
- `avg_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 53.9 points at 62.6% of the default cost, 16.5% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 53.9 points at 62.6% of the default cost, 37.4% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
