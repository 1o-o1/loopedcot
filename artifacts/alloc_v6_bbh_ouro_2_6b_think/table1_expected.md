# Table 1 -- bbh (ouro_2_6b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 163110 layer passes over 2137 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 91.2 | +0.0 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 57.4 | 63.5 | 83.2 | 90.7 | +0.5 |
| lookup | 61.5 | 81.9 | 88.3 | 89.8 | +1.4 |
| equation | 61.5 | 81.9 | 83.4 | 89.8 | +1.4 |
| equation_n100 | 61.5 | 81.9 | 86.4 | 89.8 | +1.4 |
| equation_n30 | 61.5 | 82.9 | 88.3 | 89.8 | +1.4 |
| equation_resolved | 61.5 | 81.9 | 88.3 | 90.7 | +0.5 |
| gated_equation | 61.5 | 82.9 | 88.3 | 90.7 | +0.5 |
| gated_equation_resolved | 61.5 | 81.9 | 88.3 | 90.7 | +0.5 |
| avg_gated_equation_resolved | 58.9 | 68.0 | 87.1 | 90.7 | +0.5 |
| avg_gated_lookup | 58.9 | 68.0 | 89.6 | 90.7 | +0.5 |
| avg_lookup | 55.6 | 81.9 | 88.4 | 89.8 | +1.4 |
| avg_equation | 57.1 | 81.9 | 83.4 | 89.8 | +1.4 |
| avg_equation_resolved | 55.6 | 81.9 | 87.1 | 89.8 | +1.4 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 4096, 91.2 points over 2137 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F1, F2, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 30573 vs 40777 (-25.0%) | 65177 vs 81555 (-20.1%) | 95925 vs 122332 (-21.6%) | 150302 vs 163110 (-7.9%) |
| avg_gated_lookup | 30573 vs 40777 (-25.0%) | 65177 vs 81555 (-20.1%) | 120961 vs 122332 (-1.1%) | 150302 vs 163110 (-7.9%) |
| avg_lookup | 7029 vs 40777 (-82.8%) | 66887 vs 81555 (-18.0%) | 100403 vs 122332 (-17.9%) | 139422 vs 163110 (-14.5%) |
| avg_equation | 7632 vs 40777 (-81.3%) | 66887 vs 81555 (-18.0%) | 112831 vs 122332 (-7.8%) | 139422 vs 163110 (-14.5%) |
| avg_equation_resolved | 7029 vs 40777 (-82.8%) | 66887 vs 81555 (-18.0%) | 95925 vs 122332 (-21.6%) | 139422 vs 163110 (-14.5%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 1917, k4_T256: 220 | 30573 | 175826 (over) vs 175520 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T256: 1917, k4_T4096: 220 | 65177 | 175826 (over) vs 175520 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T256: 1917, k4_T4096: 220 | 65177 | 175826 (over) vs 175520 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T256: 1917, k4_T4096: 220 | 65177 | 175826 (over) vs 175520 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 1917, k4_T256: 220 | 30573 | 175826 (over) vs 175520 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T256: 1917, k4_T4096: 220 | 65177 | 175826 (over) vs 175520 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T256: 1917, k4_T4096: 220 | 65177 | 175826 (over) vs 175520 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T256: 1917, k4_T4096: 220 | 65177 | 175826 (over) vs 175520 (over) |
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin -3.3 points, sd 1.9, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 25.0% of the budget, 18.7% of the default cost. Mirror fold -0.5 points, sd 2.5 on 210 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin +11.1 points, sd 5.4, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 20.1% of the budget, 40.0% of the default cost. Mirror fold -7.1 points, sd 2.7 on 210 questions (fails).
- `avg_gated_equation_resolved` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F2. Verification margin +11.1 points, sd 4.8, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 21.6% of the budget, 58.8% of the default cost. Mirror fold +29.0 points, sd 3.4 on 210 questions (clears).
- `avg_gated_equation_resolved` at 1.00x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F1. Verification margin +15.6 points, sd 3.8, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 7.9% of the budget, 92.1% of the default cost. Mirror fold +29.5 points, sd 3.2 on 210 questions (clears).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin -3.3 points, sd 1.9, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 25.0% of the budget, 18.7% of the default cost. Mirror fold -0.5 points, sd 2.5 on 210 questions (fails).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin +11.1 points, sd 5.4, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 20.1% of the budget, 40.0% of the default cost. Mirror fold -7.1 points, sd 2.7 on 210 questions (fails).
- `avg_gated_lookup` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F2. Verification margin +8.9 points, sd 4.6, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 1.1% of the budget, 74.2% of the default cost. Mirror fold +27.1 points, sd 3.5 on 210 questions (clears).
- `avg_gated_lookup` at 1.00x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F1. Verification margin +15.6 points, sd 3.8, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 7.9% of the budget, 92.1% of the default cost. Mirror fold +29.5 points, sd 3.2 on 210 questions (clears).

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
