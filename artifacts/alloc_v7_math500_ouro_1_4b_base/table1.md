# Table 1 -- math500 (ouro_1_4b_base), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 83459 layer passes over 400 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 63.5 | +2.5 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 31.8 | 44.8 | 56.5 | 56.5 | +9.5 |
| lookup | 31.8 | 54.5 | 64.0 | 65.5 | +0.5 |
| equation | 31.8 | 54.5 | 64.0 | 65.5 | +0.5 |
| equation_n100 | 31.8 | 54.5 | 64.0 | 65.5 | +0.5 |
| equation_n30 | 31.8 | 54.5 | 54.5 | 65.5 | +0.5 |
| equation_resolved | 31.8 | 54.5 | 56.5 | 65.5 | +0.5 |
| gated_equation | 31.8 | 54.5 | 56.5 | 65.5 | +0.5 |
| gated_equation_resolved | 31.8 | 54.5 | 56.5 | 65.5 | +0.5 |
| avg_gated_equation_resolved | 31.8 | 54.5 | 56.5 | 65.5 | +0.5 |
| avg_gated_lookup | 31.8 | 54.5 | 56.5 | 65.5 | +0.5 |
| avg_lookup | 19.2 | 54.5 | 54.5 | 65.5 | +0.5 |
| avg_equation | 19.2 | 54.5 | 64.0 | 65.5 | +0.5 |
| avg_equation_resolved | 19.2 | 54.5 | 56.5 | 65.5 | +0.5 |

The ORACLE GAP is the best single evaluation cell (depth 3 at cap 4096, 66.0 points over 400 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 15744 vs 20865 (-24.5%) | 39456 vs 41729 (-5.4%) | 52608 vs 62594 (-16.0%) | 76320 vs 83459 (-8.6%) |
| avg_gated_lookup | 15744 vs 20865 (-24.5%) | 39456 vs 41729 (-5.4%) | 52608 vs 62594 (-16.0%) | 76320 vs 83459 (-8.6%) |
| avg_lookup | 2592 vs 20865 (-87.6%) | 39456 vs 41729 (-5.4%) | 39456 vs 62594 (-37.0%) | 76320 vs 83459 (-8.6%) |
| avg_equation | 2592 vs 20865 (-87.6%) | 39456 vs 41729 (-5.4%) | 50880 vs 62594 (-18.7%) | 76320 vs 83459 (-8.6%) |
| avg_equation_resolved | 2592 vs 20865 (-87.6%) | 39456 vs 41729 (-5.4%) | 52608 vs 62594 (-16.0%) | 76320 vs 83459 (-8.6%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 400 | 15744 | 396672 (over) vs 396672 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T256: 400 | 28032 | 396672 (over) vs 396672 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T512: 400 | 52608 | 396672 (over) vs 396672 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T512: 400 | 52608 | 396672 (over) vs 396672 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 400 | 15744 | 396672 (over) vs 396672 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T256: 400 | 28032 | 396672 (over) vs 396672 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T512: 400 | 52608 | 396672 (over) vs 396672 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T512: 400 | 52608 | 396672 (over) vs 396672 (over) |
- `avg_gated_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 65.5 points at 91.4% of the default cost, 8.6% under the budget it was given.
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -3.3 points, sd 5.7, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 24.5% of the budget, 18.9% of the default cost. Mirror fold -15.7 points, sd 5.6 on 70 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +16.7 points, sd 9.5, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 5.4% of the budget, 47.3% of the default cost. Mirror fold +14.3 points, sd 6.2 on 70 questions (clears).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 16.0% of the budget, 63.0% of the default cost. Mirror fold -2.9 points, sd 5.2 on 70 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +6.7 points, sd 8.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 8.6% of the budget, 91.4% of the default cost. Mirror fold +5.7 points, sd 5.3 on 70 questions (clears).
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 65.5 points at 91.4% of the default cost, 8.6% under the budget it was given.
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -3.3 points, sd 5.7, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 24.5% of the budget, 18.9% of the default cost. Mirror fold -12.9 points, sd 6.0 on 70 questions (fails).
- `avg_gated_lookup` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +16.7 points, sd 9.5, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 5.4% of the budget, 47.3% of the default cost. Mirror fold +14.3 points, sd 6.2 on 70 questions (clears).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 8.1, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 16.0% of the budget, 63.0% of the default cost. Mirror fold -2.9 points, sd 5.2 on 70 questions (fails).
- `avg_gated_lookup` at 1.00x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +6.7 points, sd 8.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 8.6% of the budget, 91.4% of the default cost. Mirror fold +5.7 points, sd 5.3 on 70 questions (clears).
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 65.5 points at 91.4% of the default cost, 8.6% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
