# Table 1 -- bbh (ouro_2_6b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 42462 layer passes over 2137 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 82.5 | +0.0 |
| default_cell | n/a | n/a | n/a | 86.4 (90%) | -3.9 |
| default_at_budget | 56.9 | 56.2 | 78.2 | 81.7 | +0.8 |
| lookup | 56.9 | 73.9 | 80.7 | 81.2 | +1.3 |
| equation | 56.9 | 73.8 | 80.8 | 81.3 | +1.2 |
| equation_n100 | 56.9 | 73.8 | 80.8 | 81.3 | +1.2 |
| equation_n30 | 56.9 | 67.1 | 80.8 | 81.3 | +1.2 |
| equation_resolved | 56.9 | 73.8 | 80.7 | 82.1 | +0.4 |
| gated_equation | 56.9 | 67.0 | 79.9 | 81.7 | +0.8 |
| gated_equation_resolved | 56.9 | 67.0 | 79.9 | 81.7 | +0.8 |
| avg_gated_equation_resolved | 58.0 | 56.6 | 80.1 | 78.4 | +4.1 |
| avg_gated_lookup | 58.0 | 56.6 | 79.2 | 78.4 | +4.1 |
| avg_lookup | 58.0 | 73.9 | 81.2 | 81.2 | +1.3 |
| avg_equation | 57.8 | 73.9 | 80.8 | 81.3 | +1.2 |
| avg_equation_resolved | 58.0 | 73.9 | 81.2 | 82.5 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 2048, 82.5 points over 2137 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F1, F2, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 4405 vs 10616 (-58.5%) | 9302 vs 21231 (-56.2%) | 30129 vs 31847 (-5.4%) | 39616 vs 42462 (-6.7%) |
| avg_gated_lookup | 4405 vs 10616 (-58.5%) | 9302 vs 21231 (-56.2%) | 29746 vs 31847 (-6.6%) | 39616 vs 42462 (-6.7%) |
| avg_lookup | 4405 vs 10616 (-58.5%) | 17599 vs 21231 (-17.1%) | 29015 vs 31847 (-8.9%) | 29015 vs 42462 (-31.7%) |
| avg_equation | 4181 vs 10616 (-60.6%) | 17599 vs 21231 (-17.1%) | 31597 vs 31847 (-0.8%) | 34271 vs 42462 (-19.3%) |
| avg_equation_resolved | 4405 vs 10616 (-58.5%) | 17599 vs 21231 (-17.1%) | 29015 vs 31847 (-8.9%) | 40474 vs 42462 (-4.7%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T32: 2137 | 9302 | 43402 (over) vs 43095 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T32: 2137 | 9302 | 43402 (over) vs 43095 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T32: 2137 | 9302 | 43402 (over) vs 43095 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T32: 220, k4_T4096: 1917 | 39616 | 43402 (over) vs 43095 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T32: 2137 | 9302 | 43402 (over) vs 43095 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T32: 2137 | 9302 | 43402 (over) vs 43095 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T32: 2137 | 9302 | 43402 (over) vs 43095 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T32: 220, k4_T4096: 1917 | 39616 | 43402 (over) vs 43095 (over) |
- `avg_gated_equation_resolved` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F3. Verification margin +2.2 points, sd 3.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 58.5% of the budget, 10.4% of the default cost. Mirror fold +2.4 points, sd 2.0 on 210 questions (clears).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin +1.1 points, sd 4.9, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 56.2% of the budget, 21.9% of the default cost. Mirror fold +2.4 points, sd 2.0 on 210 questions (clears).
- `avg_gated_equation_resolved` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F1. Verification margin +7.8 points, sd 4.2, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 5.4% of the budget, 71.0% of the default cost. Mirror fold +23.3 points, sd 3.5 on 210 questions (clears).
- `avg_gated_equation_resolved` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 6.7% of the budget, 93.3% of the default cost. Mirror fold -3.3 points, sd 1.4 on 210 questions (fails).
- `avg_gated_lookup` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F3. Verification margin +2.2 points, sd 3.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 58.5% of the budget, 10.4% of the default cost. Mirror fold +2.4 points, sd 2.0 on 210 questions (clears).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin +1.1 points, sd 4.9, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 56.2% of the budget, 21.9% of the default cost. Mirror fold +2.4 points, sd 2.0 on 210 questions (clears).
- `avg_gated_lookup` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F1. Verification margin +7.8 points, sd 4.2, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 6.6% of the budget, 70.1% of the default cost. Mirror fold +23.3 points, sd 3.5 on 210 questions (clears).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin +1.1 points, sd 2.9, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 6.7% of the budget, 93.3% of the default cost. Mirror fold -3.8 points, sd 2.3 on 210 questions (fails).
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 81.2 points at 68.3% of the default cost, 8.9% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 81.2 points at 68.3% of the default cost, 31.7% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 81.3 points at 80.7% of the default cost, 19.3% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 82.5 points at 95.3% of the default cost, 4.7% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
