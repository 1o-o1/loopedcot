# Table 1 -- bbh (ouro_2_6b_base), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 42462 layer passes over 2137 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 82.5 | +0.0 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 56.9 | 56.2 | 67.5 | 68.1 | +14.4 |
| lookup | 57.4 | 67.0 | 67.4 | 76.6 | +5.8 |
| equation | 56.9 | 67.0 | 69.9 | 76.1 | +6.4 |
| equation_n100 | 56.9 | 67.0 | 67.4 | 76.6 | +5.8 |
| equation_n30 | 56.9 | 66.2 | 67.8 | 76.9 | +5.6 |
| equation_resolved | 56.9 | 67.0 | 67.4 | 76.6 | +5.8 |
| gated_equation | 56.9 | 67.0 | 67.5 | 76.6 | +5.8 |
| gated_equation_resolved | 56.9 | 67.0 | 67.5 | 76.6 | +5.8 |
| avg_gated_equation_resolved | 57.9 | 67.4 | 69.1 | 77.4 | +5.1 |
| avg_gated_lookup | 57.4 | 57.4 | 69.1 | 77.4 | +5.1 |
| avg_lookup | 57.9 | 67.4 | 67.4 | 77.4 | +5.1 |
| avg_equation | 57.9 | 67.4 | 68.2 | 77.4 | +5.1 |
| avg_equation_resolved | 57.9 | 67.4 | 67.4 | 77.4 | +5.1 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 2048, 82.5 points over 2137 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F1, F2, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 4028 vs 10616 (-62.1%) | 20897 vs 21231 (-1.6%) | 30393 vs 31847 (-4.6%) | 39329 vs 42462 (-7.4%) |
| avg_gated_lookup | 3287 vs 10616 (-69.0%) | 3287 vs 21231 (-84.5%) | 30393 vs 31847 (-4.6%) | 39329 vs 42462 (-7.4%) |
| avg_lookup | 4028 vs 10616 (-62.1%) | 20897 vs 21231 (-1.6%) | 20897 vs 31847 (-34.4%) | 39329 vs 42462 (-7.4%) |
| avg_equation | 4028 vs 10616 (-62.1%) | 20897 vs 21231 (-1.6%) | 22795 vs 31847 (-28.4%) | 39329 vs 42462 (-7.4%) |
| avg_equation_resolved | 4028 vs 10616 (-62.1%) | 20897 vs 21231 (-1.6%) | 20897 vs 31847 (-34.4%) | 39329 vs 42462 (-7.4%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T32: 1917, k4_T64: 220 | 10063 | 790025 (over) vs 789719 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T128: 220, k4_T64: 1917 | 16840 | 790025 (over) vs 789719 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T128: 1917, k4_T256: 220 | 30393 | 790025 (over) vs 789719 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T128: 1917, k4_T256: 220 | 30393 | 790025 (over) vs 789719 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T32: 1917, k4_T64: 220 | 10063 | 790025 (over) vs 789719 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T128: 220, k4_T64: 1917 | 16840 | 790025 (over) vs 789719 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T128: 1917, k4_T256: 220 | 30393 | 790025 (over) vs 789719 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T128: 1917, k4_T256: 220 | 30393 | 790025 (over) vs 789719 (over) |
- `avg_gated_equation_resolved` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F3. Verification margin +2.2 points, sd 3.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 62.1% of the budget, 9.5% of the default cost. Mirror fold +1.4 points, sd 1.9 on 210 questions (clears).
- `avg_gated_equation_resolved` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F2. Verification margin +4.4 points, sd 3.8, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 1.6% of the budget, 49.2% of the default cost. Mirror fold +14.3 points, sd 2.9 on 210 questions (clears).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin +2.2 points, sd 2.7, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 4.6% of the budget, 71.6% of the default cost. Mirror fold -11.4 points, sd 2.7 on 210 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F2. Verification margin +6.7 points, sd 3.4, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 7.4% of the budget, 92.6% of the default cost. Mirror fold +9.0 points, sd 2.7 on 210 questions (clears).
- `avg_gated_lookup` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F1. Verification margin +2.2 points, sd 3.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 69.0% of the budget, 7.7% of the default cost. Mirror fold +1.4 points, sd 1.9 on 210 questions (clears).
- `avg_gated_lookup` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F1. Verification margin +2.2 points, sd 3.2, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 84.5% of the budget, 7.7% of the default cost. Mirror fold +2.9 points, sd 2.4 on 210 questions (clears).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin +2.2 points, sd 2.7, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 4.6% of the budget, 71.6% of the default cost. Mirror fold -11.4 points, sd 2.7 on 210 questions (fails).
- `avg_gated_lookup` at 1.00x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F2. Verification margin +6.7 points, sd 3.4, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 7.4% of the budget, 92.6% of the default cost. Mirror fold +9.0 points, sd 2.7 on 210 questions (clears).

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
