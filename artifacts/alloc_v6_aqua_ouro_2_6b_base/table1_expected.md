# Table 1 -- aqua (ouro_2_6b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 38851 layer passes over 154 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 73.4 | +1.9 |
| default_cell | n/a | n/a | 73.4 | 73.4 | +1.9 |
| default_at_budget | 61.0 | 74.7 | 73.4 | 73.4 | +1.9 |
| lookup | 66.2 | 68.2 | 68.2 | 68.2 | +7.1 |
| equation | 66.2 | 66.2 | 66.2 | 66.2 | +9.1 |
| equation_n100 | 66.2 | 66.2 | 66.2 | 66.2 | +9.1 |
| equation_n30 | 66.2 | 75.3 | 75.3 | 75.3 | +0.0 |
| equation_resolved | 66.2 | 66.2 | 66.2 | 66.2 | +9.1 |
| gated_equation | 66.2 | 74.7 | 73.4 | 73.4 | +1.9 |
| gated_equation_resolved | 61.0 | 74.7 | 73.4 | 73.4 | +1.9 |
| avg_gated_equation_resolved | 59.7 | 72.1 | 73.4 | 73.4 | +1.9 |
| avg_gated_lookup | 59.7 | 72.1 | 73.4 | 73.4 | +1.9 |
| avg_lookup | 59.7 | 68.2 | 68.2 | 68.2 | +7.1 |
| avg_equation | 66.2 | 66.2 | 66.2 | 66.2 | +9.1 |
| avg_equation_resolved | 59.7 | 66.2 | 66.2 | 66.2 | +9.1 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 256, 75.3 points over 154 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F1, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x yes, 1.00x yes.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 2304 vs 9713 (-76.3%) | 17318 vs 19426 (-10.8%) | 26077 vs 29138 (-10.5%) | 26077 vs 38851 (-32.9%) |
| avg_gated_lookup | 2304 vs 9713 (-76.3%) | 17318 vs 19426 (-10.8%) | 26077 vs 29138 (-10.5%) | 26077 vs 38851 (-32.9%) |
| avg_lookup | 2304 vs 9713 (-76.3%) | 10010 vs 19426 (-48.5%) | 10010 vs 29138 (-65.6%) | 10010 vs 38851 (-74.2%) |
| avg_equation | 8916 vs 9713 (-8.2%) | 18616 vs 19426 (-4.2%) | 28447 vs 29138 (-2.4%) | 28447 vs 38851 (-26.8%) |
| avg_equation_resolved | 2304 vs 9713 (-76.3%) | 18616 vs 19426 (-4.2%) | 18616 vs 29138 (-36.1%) | 18616 vs 38851 (-52.1%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T0: 154 | 2304 | 26077 (over) vs 26077 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T0: 154 | 2304 | 26077 (over) vs 26077 (over) |
| 0.75x | default_cell | 4 | k4_T4096: 154 | 26077 | 26077 (fits) vs 26077 (fits) |
| 1.00x | default_cell | 4 | k4_T4096: 154 | 26077 | 26077 (fits) vs 26077 (fits) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T0: 154 | 2304 | 26077 (over) vs 26077 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T0: 154 | 2304 | 26077 (over) vs 26077 (over) |
| 0.75x | default_cell | 4 | k4_T4096: 154 | 26077 | 26077 (fits) vs 26077 (fits) |
| 1.00x | default_cell | 4 | k4_T4096: 154 | 26077 | 26077 (fits) vs 26077 (fits) |
- `avg_gated_equation_resolved` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 72.1 points at 44.6% of the default cost, 10.8% under the budget it was given.
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin -3.3 points, sd 3.2, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 76.3% of the budget, 5.9% of the default cost. Mirror fold -4.3 points, sd 3.7 on 70 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F1. Verification margin +10.0 points, sd 8.7, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 10.8% of the budget, 44.6% of the default cost. Mirror fold +11.4 points, sd 6.5 on 70 questions (clears).
- `avg_gated_equation_resolved` at 0.75x: reverted to the default cell for every question. Verification margin +3.3 points, sd 3.3, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 10.5% of the budget, 67.1% of the default cost. Mirror fold +0.0 points, sd 5.9 on 70 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: reverted to the default cell for every question. Verification margin +3.3 points, sd 3.3, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 32.9% of the budget, 67.1% of the default cost. Mirror fold +0.0 points, sd 5.9 on 70 questions (fails).
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 72.1 points at 44.6% of the default cost, 10.8% under the budget it was given.
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 76.3% of the budget, 5.9% of the default cost. Mirror fold +2.9 points, sd 6.9 on 70 questions (fails).
- `avg_gated_lookup` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F1. Verification margin +10.0 points, sd 8.7, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 10.8% of the budget, 44.6% of the default cost. Mirror fold +11.4 points, sd 6.5 on 70 questions (clears).
- `avg_gated_lookup` at 0.75x: reverted to the default cell for every question. Verification margin +3.3 points, sd 3.3, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 10.5% of the budget, 67.1% of the default cost. Mirror fold -7.1 points, sd 6.3 on 70 questions (fails).
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin +3.3 points, sd 3.3, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 32.9% of the budget, 67.1% of the default cost. Mirror fold -7.1 points, sd 6.3 on 70 questions (fails).
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 68.2 points at 25.8% of the default cost, 48.5% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 68.2 points at 25.8% of the default cost, 65.6% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.2 points at 25.8% of the default cost, 74.2% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 66.2 points at 73.2% of the default cost, 2.4% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 66.2 points at 73.2% of the default cost, 26.8% under the budget it was given.
- `avg_equation_resolved` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 66.2 points at 47.9% of the default cost, 4.2% under the budget it was given.
- `avg_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 66.2 points at 47.9% of the default cost, 36.1% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 66.2 points at 47.9% of the default cost, 52.1% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
