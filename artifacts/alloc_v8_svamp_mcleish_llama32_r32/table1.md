# Table 1 -- svamp (mcleish_llama32_r32), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 3002 layer passes over 200 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 69.0 | +0.0 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 9.0 | 9.0 | 38.5 | 51.5 | +17.5 |
| lookup | 25.0 | 49.5 | 49.5 | 62.0 | +7.0 |
| equation | 25.0 | 49.5 | 49.5 | 62.0 | +7.0 |
| equation_n100 | 25.0 | 49.5 | 49.5 | 62.0 | +7.0 |
| equation_n30 | 25.0 | 49.5 | 49.5 | 62.0 | +7.0 |
| equation_resolved | 25.0 | 49.5 | 49.5 | 51.5 | +17.5 |
| gated_equation | 25.0 | 49.5 | 49.5 | 51.5 | +17.5 |
| gated_equation_resolved | 25.0 | 49.5 | 49.5 | 51.5 | +17.5 |
| avg_gated_equation_resolved | 25.0 | 39.0 | 38.5 | 51.5 | +17.5 |
| avg_gated_lookup | 25.0 | 39.0 | 38.5 | 51.5 | +17.5 |
| avg_lookup | 25.0 | 49.5 | 49.5 | 62.0 | +7.0 |
| avg_equation | 9.0 | 49.5 | 49.5 | 62.0 | +7.0 |
| avg_equation_resolved | 25.0 | 49.5 | 49.5 | 51.5 | +17.5 |

The ORACLE GAP is the best single evaluation cell (depth 8 at cap 128, 69.0 points over 200 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3. Of the families that CLEAR the bar the one that RUNS is set by `policy.GATE_FAMILY_RULE` = `best`: the cleared family with the largest mean verified margin over the folds, ties to the smaller family. The folds, the bar, the reference and the pricing are the same test under either rule; only which cleared family is taken differs.

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 540 vs 751 (-28.1%) | 864 vs 1501 (-42.4%) | 1512 vs 2252 (-32.9%) | 2408 vs 3002 (-19.8%) |
| avg_gated_lookup | 540 vs 751 (-28.1%) | 864 vs 1501 (-42.4%) | 1512 vs 2252 (-32.9%) | 2408 vs 3002 (-19.8%) |
| avg_lookup | 540 vs 751 (-28.1%) | 1376 vs 1501 (-8.3%) | 1376 vs 2252 (-38.9%) | 2400 vs 3002 (-20.1%) |
| avg_equation | 220 vs 751 (-70.7%) | 1376 vs 1501 (-8.3%) | 1376 vs 2252 (-38.9%) | 2400 vs 3002 (-20.1%) |
| avg_equation_resolved | 540 vs 751 (-28.1%) | 1376 vs 1501 (-8.3%) | 1376 vs 2252 (-38.9%) | 2408 vs 3002 (-19.8%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 8 | k8_T0: 200 | 616 | 229992 (over) vs 229992 (over) |
| 0.50x | deepest_depth_capped | 8 | k8_T0: 200 | 616 | 229992 (over) vs 229992 (over) |
| 0.75x | deepest_depth_capped | 8 | k8_T16: 200 | 1512 | 229992 (over) vs 229992 (over) |
| 1.00x | deepest_depth_capped | 8 | k8_T32: 200 | 2408 | 229992 (over) vs 229992 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 8 | k8_T0: 200 | 616 | 229992 (over) vs 229992 (over) |
| 0.50x | deepest_depth_capped | 8 | k8_T0: 200 | 616 | 229992 (over) vs 229992 (over) |
| 0.75x | deepest_depth_capped | 8 | k8_T16: 200 | 1512 | 229992 (over) vs 229992 (over) |
| 1.00x | deepest_depth_capped | 8 | k8_T32: 200 | 2408 | 229992 (over) vs 229992 (over) |
- `avg_gated_equation_resolved` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) on family F3. Verification margin +50.0 points, sd 10.3, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 28.1% of the budget, 18.0% of the default cost. Mirror fold +27.1 points, sd 6.0 on 70 questions (clears).
- `avg_gated_equation_resolved` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) on family F2. Verification margin +33.3 points, sd 11.9, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 42.4% of the budget, 28.8% of the default cost. Mirror fold +45.7 points, sd 6.0 on 70 questions (clears).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin -3.3 points, sd 3.2, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 32.9% of the budget, 50.4% of the default cost. Mirror fold -10.0 points, sd 5.1 on 70 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin -6.7 points, sd 8.1, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 19.8% of the budget, 80.2% of the default cost. Mirror fold -27.1 points, sd 5.9 on 70 questions (fails).
- `avg_gated_lookup` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) on family F3. Verification margin +50.0 points, sd 10.3, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 28.1% of the budget, 18.0% of the default cost. Mirror fold +27.1 points, sd 6.0 on 70 questions (clears).
- `avg_gated_lookup` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) on family F2. Verification margin +33.3 points, sd 11.9, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 42.4% of the budget, 28.8% of the default cost. Mirror fold +45.7 points, sd 6.0 on 70 questions (clears).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin -3.3 points, sd 3.2, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 32.9% of the budget, 50.4% of the default cost. Mirror fold -10.0 points, sd 5.1 on 70 questions (fails).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin -6.7 points, sd 8.1, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 19.8% of the budget, 80.2% of the default cost. Mirror fold -27.1 points, sd 5.9 on 70 questions (fails).

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
