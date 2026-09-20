# Table 1 -- math500 (ouro_1_4b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 270990 layer passes over 400 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 90.0 | +0.0 |
| default_cell | n/a | n/a | n/a | 90.0 | +0.0 |
| default_at_budget | 59.0 | 75.5 | 89.5 | 90.0 | +0.0 |
| lookup | 59.0 | 84.5 | 89.2 | 90.0 | +0.0 |
| equation | 59.0 | 84.5 | 89.2 | 90.0 | +0.0 |
| equation_n100 | 59.0 | 84.5 | 89.2 | 90.0 | +0.0 |
| equation_n30 | 59.0 | 84.5 | 89.2 | 90.0 | +0.0 |
| equation_resolved | 59.0 | 84.5 | 89.2 | 90.0 | +0.0 |
| gated_equation | 59.0 | 84.5 | 89.5 | 90.0 | +0.0 |
| gated_equation_resolved | 59.0 | 84.5 | 89.5 | 90.0 | +0.0 |
| avg_gated_equation_resolved | 59.0 | 84.5 | 89.5 | 90.0 | +0.0 |
| avg_gated_lookup | 59.0 | 84.5 | 89.5 | 90.0 | +0.0 |
| avg_lookup | 59.5 | 84.5 | 89.2 | 90.0 | +0.0 |
| avg_equation | 59.5 | 84.5 | 89.2 | 90.0 | +0.0 |
| avg_equation_resolved | 59.5 | 84.5 | 89.2 | 90.0 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 8192, 90.0 points over 400 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2.

`default_cell` is the default operating point (depth 4 at cap 8192) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 52542 vs 67748 (-22.4%) | 104067 vs 135495 (-23.2%) | 197228 vs 203242 (-3.0%) | 266586 vs 270990 (-1.6%) |
| avg_gated_lookup | 52542 vs 67748 (-22.4%) | 104067 vs 135495 (-23.2%) | 197228 vs 203242 (-3.0%) | 266586 vs 270990 (-1.6%) |
| avg_lookup | 39177 vs 67748 (-42.2%) | 104067 vs 135495 (-23.2%) | 194948 vs 203242 (-4.1%) | 266586 vs 270990 (-1.6%) |
| avg_equation | 39177 vs 67748 (-42.2%) | 104067 vs 135495 (-23.2%) | 194948 vs 203242 (-4.1%) | 266586 vs 270990 (-1.6%) |
| avg_equation_resolved | 39177 vs 67748 (-42.2%) | 104067 vs 135495 (-23.2%) | 194948 vs 203242 (-4.1%) | 266586 vs 270990 (-1.6%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T512: 400 | 52542 | 266586 (over) vs 266586 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T1024: 400 | 92331 | 266586 (over) vs 266586 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T4096: 400 | 197228 | 266586 (over) vs 266586 (over) |
| 1.00x | default_cell | 4 | k4_T8192: 400 | 266586 | 266586 (fits) vs 266586 (fits) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T512: 400 | 52542 | 266586 (over) vs 266586 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T1024: 400 | 92331 | 266586 (over) vs 266586 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T4096: 400 | 197228 | 266586 (over) vs 266586 (over) |
| 1.00x | default_cell | 4 | k4_T8192: 400 | 266586 | 266586 (fits) vs 266586 (fits) |
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 22.4% of the budget, 19.4% of the default cost. Mirror fold -40.0 points, sd 6.1 on 70 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +6.7 points, sd 8.1, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 23.2% of the budget, 38.4% of the default cost. Mirror fold +8.6 points, sd 3.3 on 70 questions (clears).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -3.3 points, sd 3.2, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 3.0% of the budget, 72.8% of the default cost. Mirror fold -5.7 points, sd 3.4 on 70 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: reverted to the default cell for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 1.6% of the budget, 98.4% of the default cost. Mirror fold +0.0 points, sd 0.0 on 70 questions (fails).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 22.4% of the budget, 19.4% of the default cost. Mirror fold -40.0 points, sd 6.1 on 70 questions (fails).
- `avg_gated_lookup` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +6.7 points, sd 8.1, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 23.2% of the budget, 38.4% of the default cost. Mirror fold +8.6 points, sd 3.3 on 70 questions (clears).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -3.3 points, sd 3.2, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 3.0% of the budget, 72.8% of the default cost. Mirror fold -5.7 points, sd 3.4 on 70 questions (fails).
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin -3.3 points, sd 3.2, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 1.6% of the budget, 98.4% of the default cost. Mirror fold -8.6 points, sd 3.3 on 70 questions (fails).
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 90.0 points at 98.4% of the default cost, 1.6% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 90.0 points at 98.4% of the default cost, 1.6% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 90.0 points at 98.4% of the default cost, 1.6% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
