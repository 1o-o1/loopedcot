# Table 1 -- bbh (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 23044 layer passes over 2137 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 75.8 | +0.0 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 45.4 | 60.9 | 74.0 | 75.8 | +0.0 |
| lookup | 45.4 | 66.3 | 75.0 | 75.4 | +0.4 |
| equation | 46.0 | 66.3 | 75.0 | 75.8 | +0.0 |
| equation_n100 | 45.8 | 67.3 | 75.0 | 75.8 | +0.0 |
| equation_n30 | 46.0 | 56.0 | 73.0 | 75.8 | +0.0 |
| equation_resolved | 45.4 | 66.3 | 75.0 | 75.4 | +0.4 |
| gated_equation | 45.4 | 60.9 | 74.0 | 75.8 | +0.0 |
| gated_equation_resolved | 45.4 | 60.9 | 74.0 | 75.8 | +0.0 |
| avg_gated_equation_resolved | 45.8 | 60.9 | 75.4 | 75.8 | +0.0 |
| avg_gated_lookup | 45.8 | 60.9 | 75.4 | 75.8 | +0.0 |
| avg_lookup | 49.6 | 49.6 | 75.4 | 75.4 | +0.4 |
| avg_equation | 47.6 | 68.1 | 73.7 | 75.8 | +0.0 |
| avg_equation_resolved | 49.6 | 49.6 | 75.4 | 75.4 | +0.4 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 2048, 75.8 points over 2137 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none. Of the families that CLEAR the bar the one that RUNS is set by `policy.GATE_FAMILY_RULE` = `best`: the cleared family with the largest mean verified margin over the folds, ties to the smaller family. The folds, the bar, the reference and the pricing are the same test under either rule; only which cleared family is taken differs.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 4647 vs 5761 (-19.3%) | 11222 vs 11522 (-2.6%) | 16936 vs 17283 (-2.0%) | 21561 vs 23044 (-6.4%) |
| avg_gated_lookup | 4647 vs 5761 (-19.3%) | 11222 vs 11522 (-2.6%) | 16936 vs 17283 (-2.0%) | 21561 vs 23044 (-6.4%) |
| avg_lookup | 2716 vs 5761 (-52.9%) | 2716 vs 11522 (-76.4%) | 16936 vs 17283 (-2.0%) | 16936 vs 23044 (-26.5%) |
| avg_equation | 2087 vs 5761 (-63.8%) | 11381 vs 11522 (-1.2%) | 15475 vs 17283 (-10.5%) | 21966 vs 23044 (-4.7%) |
| avg_equation_resolved | 2716 vs 5761 (-52.9%) | 2716 vs 11522 (-76.4%) | 16936 vs 17283 (-2.0%) | 16936 vs 23044 (-26.5%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T32: 2137 | 4647 | 25646 (over) vs 25493 (over) |
| 0.50x | default_at_budget | 4 | k4_T128: 1917, k4_T64: 220 | 11222 | 25646 (over) vs 25493 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T512: 2137 | 16936 | 25646 (over) vs 25493 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T2048: 2137 | 21561 | 25646 (over) vs 25493 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T32: 2137 | 4647 | 25646 (over) vs 25493 (over) |
| 0.50x | default_at_budget | 4 | k4_T128: 1917, k4_T64: 220 | 11222 | 25646 (over) vs 25493 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T512: 2137 | 16936 | 25646 (over) vs 25493 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T2048: 2137 | 21561 | 25646 (over) vs 25493 (over) |
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -1.1 points, sd 3.7, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 19.3% of the budget, 20.2% of the default cost. Mirror fold -0.5 points, sd 3.0 on 210 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap each question's own price affords -- the `default_at_budget` row) for every question. Verification margin -14.4 points, sd 4.6, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 2.6% of the budget, 48.7% of the default cost. Mirror fold +0.0 points, sd 0.0 on 210 questions (fails).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 2.0% of the budget, 73.5% of the default cost. Mirror fold -2.4 points, sd 1.0 on 210 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 6.4% of the budget, 93.6% of the default cost. Mirror fold -2.4 points, sd 1.0 on 210 questions (fails).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -1.1 points, sd 3.7, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 19.3% of the budget, 20.2% of the default cost. Mirror fold -0.5 points, sd 3.0 on 210 questions (fails).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap each question's own price affords -- the `default_at_budget` row) for every question. Verification margin -14.4 points, sd 4.6, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 2.6% of the budget, 48.7% of the default cost. Mirror fold +0.0 points, sd 0.0 on 210 questions (fails).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 2.0% of the budget, 73.5% of the default cost. Mirror fold -2.4 points, sd 1.0 on 210 questions (fails).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 6.4% of the budget, 93.6% of the default cost. Mirror fold -2.4 points, sd 1.0 on 210 questions (fails).
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 75.4 points at 73.5% of the default cost, 2.0% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 75.4 points at 73.5% of the default cost, 26.5% under the budget it was given.
- `avg_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 75.4 points at 73.5% of the default cost, 2.0% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 75.4 points at 73.5% of the default cost, 26.5% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
