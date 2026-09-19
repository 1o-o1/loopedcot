# Table 1 -- bbh (ouro_1_4b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 105284 layer passes over 2137 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 84.3 | +0.0 |
| default_cell | n/a | n/a | n/a | 84.3 | +0.0 |
| default_at_budget | 54.1 | 79.3 | 83.1 | 84.3 | +0.0 |
| lookup | 58.4 | 80.2 | 83.1 | 84.1 | +0.1 |
| equation | 53.9 | 80.2 | 82.2 | 84.3 | +0.0 |
| equation_n100 | 58.4 | 80.2 | 83.1 | 84.3 | +0.0 |
| equation_n30 | 58.4 | 79.5 | 82.2 | 82.3 | +2.0 |
| equation_resolved | 58.4 | 80.2 | 83.1 | 84.3 | +0.0 |
| gated_equation | 54.1 | 79.3 | 83.1 | 84.3 | +0.0 |
| gated_equation_resolved | 54.1 | 79.3 | 83.1 | 84.3 | +0.0 |
| avg_gated_equation_resolved | 54.1 | 79.3 | 83.1 | 84.3 | +0.0 |
| avg_gated_lookup | 54.1 | 79.3 | 83.1 | 84.3 | +0.0 |
| avg_lookup | 48.5 | 80.2 | 80.2 | 84.1 | +0.1 |
| avg_equation | 48.5 | 80.2 | 80.2 | 84.3 | +0.0 |
| avg_equation_resolved | 48.5 | 80.2 | 80.2 | 84.3 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 4096, 84.3 points over 2137 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 25004 vs 26321 (-5.0%) | 47063 vs 52642 (-10.6%) | 67998 vs 78963 (-13.9%) | 94530 vs 105284 (-10.2%) |
| avg_gated_lookup | 25004 vs 26321 (-5.0%) | 47063 vs 52642 (-10.6%) | 67998 vs 78963 (-13.9%) | 94530 vs 105284 (-10.2%) |
| avg_lookup | 5106 vs 26321 (-80.6%) | 52551 vs 52642 (-0.2%) | 52551 vs 78963 (-33.4%) | 82820 vs 105284 (-21.3%) |
| avg_equation | 5106 vs 26321 (-80.6%) | 52551 vs 52642 (-0.2%) | 52551 vs 78963 (-33.4%) | 94530 vs 105284 (-10.2%) |
| avg_equation_resolved | 5106 vs 26321 (-80.6%) | 52551 vs 52642 (-0.2%) | 52551 vs 78963 (-33.4%) | 94530 vs 105284 (-10.2%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | default_at_budget | 4 | k4_T128: 220, k4_T256: 1917 | 25004 | 94683 (over) vs 94530 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T512: 2137 | 47063 | 94683 (over) vs 94530 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T1024: 2137 | 67998 | 94683 (over) vs 94530 (over) |
| 1.00x | default_cell | 4 | k4_T4096: 2137 | 94530 | 94683 (fits) vs 94530 (fits) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | default_at_budget | 4 | k4_T128: 220, k4_T256: 1917 | 25004 | 94683 (over) vs 94530 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T512: 2137 | 47063 | 94683 (over) vs 94530 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T1024: 2137 | 67998 | 94683 (over) vs 94530 (over) |
| 1.00x | default_cell | 4 | k4_T4096: 2137 | 94530 | 94683 (fits) vs 94530 (fits) |
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap each question's own price affords -- the `default_at_budget` row) for every question. Verification margin +1.1 points, sd 3.6, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 5.0% of the budget, 23.7% of the default cost. Mirror fold -11.4 points, sd 3.4 on 210 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 4.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 10.6% of the budget, 44.7% of the default cost. Mirror fold +0.0 points, sd 0.0 on 210 questions (fails).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -4.4 points, sd 3.9, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 13.9% of the budget, 64.6% of the default cost. Mirror fold +0.0 points, sd 0.0 on 210 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: reverted to the default cell for every question. Verification margin -2.2 points, sd 3.2, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 10.2% of the budget, 89.8% of the default cost. Mirror fold +0.5 points, sd 0.8 on 210 questions (clears).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap each question's own price affords -- the `default_at_budget` row) for every question. Verification margin +1.1 points, sd 3.6, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 5.0% of the budget, 23.7% of the default cost. Mirror fold -10.0 points, sd 3.2 on 210 questions (fails).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -6.7 points, sd 4.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 10.6% of the budget, 44.7% of the default cost. Mirror fold +1.0 points, sd 0.7 on 210 questions (clears).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -4.4 points, sd 3.9, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 13.9% of the budget, 64.6% of the default cost. Mirror fold +0.0 points, sd 0.0 on 210 questions (fails).
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin -2.2 points, sd 3.2, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 10.2% of the budget, 89.8% of the default cost. Mirror fold -1.4 points, sd 1.5 on 210 questions (fails).
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 84.1 points at 78.7% of the default cost, 21.3% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 84.3 points at 89.8% of the default cost, 10.2% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 84.3 points at 89.8% of the default cost, 10.2% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
