# Table 1 -- bbh (ouro_1_4b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 105284 layer passes over 2137 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 84.3 | +0.0 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 54.1 | 78.1 | 79.3 | 83.1 | +1.2 |
| lookup | 59.5 | 78.6 | 80.2 | 83.1 | +1.2 |
| equation | 55.0 | 78.6 | 80.2 | 83.1 | +1.2 |
| equation_n100 | 59.5 | 78.6 | 80.2 | 83.1 | +1.2 |
| equation_n30 | 59.5 | 76.2 | 80.2 | 80.2 | +4.1 |
| equation_resolved | 59.5 | 78.6 | 80.2 | 83.1 | +1.2 |
| gated_equation | 54.1 | 78.6 | 79.3 | 83.1 | +1.2 |
| gated_equation_resolved | 54.1 | 78.6 | 79.3 | 83.1 | +1.2 |
| avg_gated_equation_resolved | 54.1 | 79.3 | 79.3 | 83.1 | +1.2 |
| avg_gated_lookup | 54.1 | 79.3 | 79.3 | 83.1 | +1.2 |
| avg_lookup | 48.5 | 79.3 | 80.2 | 83.1 | +1.2 |
| avg_equation | 48.5 | 76.9 | 80.2 | 83.1 | +1.2 |
| avg_equation_resolved | 48.5 | 76.9 | 80.2 | 83.1 | +1.2 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 4096, 84.3 points over 2137 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 25050 vs 26321 (-4.8%) | 50891 vs 52642 (-3.3%) | 50891 vs 78963 (-35.6%) | 100043 vs 105284 (-5.0%) |
| avg_gated_lookup | 25050 vs 26321 (-4.8%) | 50891 vs 52642 (-3.3%) | 50891 vs 78963 (-35.6%) | 100043 vs 105284 (-5.0%) |
| avg_lookup | 5401 vs 26321 (-79.5%) | 50891 vs 52642 (-3.3%) | 75032 vs 78963 (-5.0%) | 100043 vs 105284 (-5.0%) |
| avg_equation | 5401 vs 26321 (-79.5%) | 41964 vs 52642 (-20.3%) | 75032 vs 78963 (-5.0%) | 100043 vs 105284 (-5.0%) |
| avg_equation_resolved | 5401 vs 26321 (-79.5%) | 41964 vs 52642 (-20.3%) | 75032 vs 78963 (-5.0%) | 100043 vs 105284 (-5.0%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | default_at_budget | 4 | k4_T128: 220, k4_T256: 1917 | 25050 | 395109 (over) vs 394955 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T512: 2137 | 50891 | 395109 (over) vs 394955 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T512: 2137 | 50891 | 395109 (over) vs 394955 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T1024: 2137 | 100043 | 395109 (over) vs 394955 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | default_at_budget | 4 | k4_T128: 220, k4_T256: 1917 | 25050 | 395109 (over) vs 394955 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T512: 2137 | 50891 | 395109 (over) vs 394955 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T512: 2137 | 50891 | 395109 (over) vs 394955 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T1024: 2137 | 100043 | 395109 (over) vs 394955 (over) |
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap each question's own price affords -- the `default_at_budget` row) for every question. Verification margin +1.1 points, sd 3.6, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 4.8% of the budget, 23.8% of the default cost. Mirror fold -11.4 points, sd 3.4 on 210 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -6.7 points, sd 4.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 3.3% of the budget, 48.3% of the default cost. Mirror fold +1.0 points, sd 0.7 on 210 questions (clears).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 4.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 35.6% of the budget, 48.3% of the default cost. Mirror fold +1.0 points, sd 0.7 on 210 questions (clears).
- `avg_gated_equation_resolved` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 5.0% of the budget, 95.0% of the default cost. Mirror fold +0.0 points, sd 0.0 on 210 questions (fails).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap each question's own price affords -- the `default_at_budget` row) for every question. Verification margin +1.1 points, sd 3.6, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 4.8% of the budget, 23.8% of the default cost. Mirror fold -10.0 points, sd 3.2 on 210 questions (fails).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -6.7 points, sd 4.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 3.3% of the budget, 48.3% of the default cost. Mirror fold +1.0 points, sd 0.7 on 210 questions (clears).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 4.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 35.6% of the budget, 48.3% of the default cost. Mirror fold +1.0 points, sd 0.7 on 210 questions (clears).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -3.3 points, sd 4.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 5.0% of the budget, 95.0% of the default cost. Mirror fold +0.0 points, sd 0.0 on 210 questions (fails).

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
