# Table 1 -- strategyqa (ouro_2_6b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 144213 layer passes over 1990 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 77.6 | +1.5 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 76.6 | 78.0 | 78.2 | 77.7 | +1.4 |
| lookup | 76.6 | 79.1 | 78.8 | 78.8 | +0.3 |
| equation | 76.6 | 79.1 | 78.8 | 77.7 | +1.4 |
| equation_n100 | 76.6 | 78.0 | 78.2 | 77.7 | +1.4 |
| equation_n30 | 76.6 | 78.0 | 78.2 | 77.7 | +1.4 |
| equation_resolved | 76.6 | 79.1 | 78.8 | 78.8 | +0.3 |
| gated_equation | 76.6 | 78.0 | 78.2 | 77.7 | +1.4 |
| gated_equation_resolved | 76.6 | 78.0 | 78.4 | 77.7 | +1.4 |
| avg_gated_equation_resolved | 76.6 | 78.0 | 78.2 | 77.7 | +1.4 |
| avg_gated_lookup | 76.6 | 78.0 | 78.2 | 77.7 | +1.4 |
| avg_lookup | 74.6 | 79.1 | 78.8 | 78.8 | +0.3 |
| avg_equation | 75.0 | 79.1 | 78.8 | 77.7 | +1.4 |
| avg_equation_resolved | 74.6 | 79.1 | 78.8 | 78.8 | +0.3 |

The ORACLE GAP is the best single evaluation cell (depth 3 at cap 512, 79.1 points over 1990 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F3. Of the families that CLEAR the bar the one that RUNS is set by `policy.GATE_FAMILY_RULE` = `best`: the cleared family with the largest mean verified margin over the folds, ties to the smaller family. The folds, the bar, the reference and the pricing are the same test under either rule; only which cleared family is taken differs.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 27264 vs 36053 (-24.4%) | 51840 vs 72106 (-28.1%) | 95579 vs 108159 (-11.6%) | 139969 vs 144213 (-2.9%) |
| avg_gated_lookup | 27264 vs 36053 (-24.4%) | 51840 vs 72106 (-28.1%) | 95579 vs 108159 (-11.6%) | 139969 vs 144213 (-2.9%) |
| avg_lookup | 14976 vs 36053 (-58.5%) | 71531 vs 72106 (-0.8%) | 102481 vs 108159 (-5.2%) | 102481 vs 144213 (-28.9%) |
| avg_equation | 8832 vs 36053 (-75.5%) | 71531 vs 72106 (-0.8%) | 102481 vs 108159 (-5.2%) | 139969 vs 144213 (-2.9%) |
| avg_equation_resolved | 14976 vs 36053 (-58.5%) | 71531 vs 72106 (-0.8%) | 102481 vs 108159 (-5.2%) | 102481 vs 144213 (-28.9%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 1990 | 27264 | 150468 (over) vs 150468 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T256: 1990 | 51840 | 150468 (over) vs 150468 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T512: 1990 | 95579 | 150468 (over) vs 150468 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T2048: 1990 | 139969 | 150468 (over) vs 150468 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 1990 | 27264 | 150468 (over) vs 150468 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T256: 1990 | 51840 | 150468 (over) vs 150468 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T512: 1990 | 95579 | 150468 (over) vs 150468 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T2048: 1990 | 139969 | 150468 (over) vs 150468 (over) |
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -3.3 points, sd 3.7, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 24.4% of the budget, 18.9% of the default cost. Mirror fold +0.0 points, sd 0.0 on 210 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -1.1 points, sd 2.5, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 28.1% of the budget, 35.9% of the default cost. Mirror fold +0.5 points, sd 2.4 on 210 questions (fails).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +2.2 points, sd 3.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 11.6% of the budget, 66.3% of the default cost. Mirror fold +1.0 points, sd 2.6 on 210 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +1.1 points, sd 3.3, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 2.9% of the budget, 97.1% of the default cost. Mirror fold +1.0 points, sd 2.6 on 210 questions (fails).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -4.4 points, sd 4.9, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 24.4% of the budget, 18.9% of the default cost. Mirror fold +0.0 points, sd 0.0 on 210 questions (fails).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -1.1 points, sd 2.5, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 28.1% of the budget, 35.9% of the default cost. Mirror fold +0.0 points, sd 2.2 on 210 questions (fails).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -1.1 points, sd 2.4, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 11.6% of the budget, 66.3% of the default cost. Mirror fold +1.0 points, sd 2.6 on 210 questions (fails).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -2.2 points, sd 3.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 2.9% of the budget, 97.1% of the default cost. Mirror fold +1.0 points, sd 2.6 on 210 questions (fails).
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 78.8 points at 71.1% of the default cost, 5.2% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 78.8 points at 71.1% of the default cost, 28.9% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 77.7 points at 97.1% of the default cost, 2.9% under the budget it was given.
- `avg_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 78.8 points at 71.1% of the default cost, 5.2% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 78.8 points at 71.1% of the default cost, 28.9% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
