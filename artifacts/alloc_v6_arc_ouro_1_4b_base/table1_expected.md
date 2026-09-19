# Table 1 -- arc (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 4970 layer passes over 938 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 86.4 | +0.0 |
| default_cell | n/a | n/a | n/a | 86.4 | +0.0 |
| default_at_budget | n/a | 86.0 | 85.8 | 86.4 | +0.0 |
| lookup | 83.9 | 86.0 | 85.8 | 85.9 | +0.4 |
| equation | 83.9 | 86.0 | 84.4 | 86.2 | +0.1 |
| equation_n100 | 83.9 | 86.0 | 84.4 | 84.4 | +1.9 |
| equation_n30 | 83.9 | 86.0 | 84.4 | 84.4 | +1.9 |
| equation_resolved | 83.9 | 86.0 | 84.4 | 86.2 | +0.1 |
| gated_equation | 83.9 | 86.0 | 85.8 | 86.4 | +0.0 |
| gated_equation_resolved | 83.9 | 86.0 | 85.8 | 86.4 | +0.0 |
| avg_gated_equation_resolved | 83.9 | 86.0 | 86.0 | 86.4 | +0.0 |
| avg_gated_lookup | 83.9 | 86.0 | 86.0 | 86.4 | +0.0 |
| avg_lookup | 83.9 | 86.0 | 86.0 | 85.9 | +0.4 |
| avg_equation | 83.9 | 86.0 | 86.0 | 86.2 | +0.1 |
| avg_equation_resolved | 83.9 | 86.0 | 86.0 | 86.2 | +0.1 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 128, 86.4 points over 938 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 936 vs 1243 (-24.7%) | 1248 vs 2485 (-49.8%) | 1248 vs 3728 (-66.5%) | 4908 vs 4970 (-1.2%) |
| avg_gated_lookup | 936 vs 1243 (-24.7%) | 1248 vs 2485 (-49.8%) | 1248 vs 3728 (-66.5%) | 4908 vs 4970 (-1.2%) |
| avg_lookup | 936 vs 1243 (-24.7%) | 1248 vs 2485 (-49.8%) | 1248 vs 3728 (-66.5%) | 4278 vs 4970 (-13.9%) |
| avg_equation | 936 vs 1243 (-24.7%) | 1248 vs 2485 (-49.8%) | 1248 vs 3728 (-66.5%) | 4903 vs 4970 (-1.4%) |
| avg_equation_resolved | 936 vs 1243 (-24.7%) | 1248 vs 2485 (-49.8%) | 1248 vs 3728 (-66.5%) | 4903 vs 4970 (-1.4%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | shallower_depth | 3 | k3_T0: 938 | 936 | 4908 (over) vs 4908 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T0: 938 | 1248 | 4908 (over) vs 4908 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T0: 938 | 1248 | 4908 (over) vs 4908 (over) |
| 1.00x | default_cell | 4 | k4_T4096: 938 | 4908 | 4908 (fits) vs 4908 (fits) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | shallower_depth | 3 | k3_T0: 938 | 936 | 4908 (over) vs 4908 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T0: 938 | 1248 | 4908 (over) vs 4908 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T0: 938 | 1248 | 4908 (over) vs 4908 (over) |
| 1.00x | default_cell | 4 | k4_T4096: 938 | 4908 | 4908 (fits) vs 4908 (fits) |
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (one depth down, depth 3, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (70 verification questions, the ids after the 164 that fit, out of 234 calibration); cost saving 24.7% of the budget, 18.8% of the default cost. Mirror fold +0.0 points, sd 0.0 on 164 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (70 verification questions, the ids after the 164 that fit, out of 234 calibration); cost saving 49.8% of the budget, 25.1% of the default cost. Mirror fold +0.0 points, sd 0.0 on 164 questions (fails).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin -4.3 points, sd 2.5, bar 0.50 sd (70 verification questions, the ids after the 164 that fit, out of 234 calibration); cost saving 66.5% of the budget, 25.1% of the default cost. Mirror fold +0.0 points, sd 0.0 on 164 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: reverted to the default cell for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (70 verification questions, the ids after the 164 that fit, out of 234 calibration); cost saving 1.2% of the budget, 98.8% of the default cost. Mirror fold +0.0 points, sd 0.0 on 164 questions (fails).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (one depth down, depth 3, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (70 verification questions, the ids after the 164 that fit, out of 234 calibration); cost saving 24.7% of the budget, 18.8% of the default cost. Mirror fold +0.0 points, sd 0.0 on 164 questions (fails).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (70 verification questions, the ids after the 164 that fit, out of 234 calibration); cost saving 49.8% of the budget, 25.1% of the default cost. Mirror fold +0.0 points, sd 0.0 on 164 questions (fails).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (70 verification questions, the ids after the 164 that fit, out of 234 calibration); cost saving 66.5% of the budget, 25.1% of the default cost. Mirror fold +0.0 points, sd 0.0 on 164 questions (fails).
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (70 verification questions, the ids after the 164 that fit, out of 234 calibration); cost saving 1.2% of the budget, 98.8% of the default cost. Mirror fold -3.0 points, sd 2.0 on 164 questions (fails).
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 85.9 points at 86.1% of the default cost, 13.9% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 86.2 points at 98.6% of the default cost, 1.4% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 86.2 points at 98.6% of the default cost, 1.4% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
