# Table 1 -- arc (ouro_1_4b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 62974 layer passes over 938 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 93.7 | +0.4 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 86.2 | 89.8 | 89.8 | 91.3 | +2.9 |
| lookup | 86.2 | 89.7 | 93.0 | 93.0 | +1.2 |
| equation | 86.2 | 89.7 | 93.0 | 93.0 | +1.2 |
| equation_n100 | 84.5 | 89.7 | 93.0 | 93.0 | +1.2 |
| equation_n30 | 82.2 | 88.0 | 93.0 | 89.4 | +4.7 |
| equation_resolved | 86.2 | 89.7 | 93.0 | 93.0 | +1.2 |
| gated_equation | 86.2 | 89.8 | 93.0 | 93.0 | +1.2 |
| gated_equation_resolved | 86.2 | 89.8 | 93.0 | 93.0 | +1.2 |
| avg_gated_equation_resolved | 86.2 | 89.8 | 93.0 | 93.0 | +1.2 |
| avg_gated_lookup | 86.2 | 89.8 | 93.0 | 93.0 | +1.2 |
| avg_lookup | 87.0 | 89.7 | 93.0 | 93.0 | +1.2 |
| avg_equation | 87.0 | 89.7 | 93.0 | 93.0 | +1.2 |
| avg_equation_resolved | 87.0 | 89.7 | 93.0 | 93.0 | +1.2 |

The ORACLE GAP is the best single evaluation cell (depth 3 at cap 1024, 94.1 points over 938 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 13632 vs 15743 (-13.4%) | 25920 vs 31487 (-17.7%) | 37872 vs 47230 (-19.8%) | 37872 vs 62974 (-39.9%) |
| avg_gated_lookup | 13632 vs 15743 (-13.4%) | 25920 vs 31487 (-17.7%) | 37872 vs 47230 (-19.8%) | 37872 vs 62974 (-39.9%) |
| avg_lookup | 1344 vs 15743 (-91.5%) | 19440 vs 31487 (-38.3%) | 37872 vs 47230 (-19.8%) | 37872 vs 62974 (-39.9%) |
| avg_equation | 1344 vs 15743 (-91.5%) | 19440 vs 31487 (-38.3%) | 37872 vs 47230 (-19.8%) | 37872 vs 62974 (-39.9%) |
| avg_equation_resolved | 1344 vs 15743 (-91.5%) | 19440 vs 31487 (-38.3%) | 37872 vs 47230 (-19.8%) | 37872 vs 62974 (-39.9%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 938 | 13632 | 394560 (over) vs 394560 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T256: 938 | 25920 | 394560 (over) vs 394560 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T256: 938 | 25920 | 394560 (over) vs 394560 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T512: 938 | 50496 | 394560 (over) vs 394560 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 938 | 13632 | 394560 (over) vs 394560 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T256: 938 | 25920 | 394560 (over) vs 394560 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T256: 938 | 25920 | 394560 (over) vs 394560 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T512: 938 | 50496 | 394560 (over) vs 394560 (over) |
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -2.9 points, sd 4.2, bar 0.50 sd (70 verification questions, the ids after the 164 that fit, out of 234 calibration); cost saving 13.4% of the budget, 21.6% of the default cost. Mirror fold -3.0 points, sd 2.4 on 164 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +1.4 points, sd 3.1, bar 0.50 sd (70 verification questions, the ids after the 164 that fit, out of 234 calibration); cost saving 17.7% of the budget, 41.2% of the default cost. Mirror fold -1.8 points, sd 2.5 on 164 questions (fails).
- `avg_gated_equation_resolved` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +5.7 points, sd 4.0, bar 0.50 sd (70 verification questions, the ids after the 164 that fit, out of 234 calibration); cost saving 19.8% of the budget, 60.1% of the default cost. Mirror fold +4.3 points, sd 1.8 on 164 questions (clears).
- `avg_gated_equation_resolved` at 1.00x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +2.9 points, sd 4.0, bar 0.50 sd (70 verification questions, the ids after the 164 that fit, out of 234 calibration); cost saving 39.9% of the budget, 60.1% of the default cost. Mirror fold +1.2 points, sd 1.2 on 164 questions (clears).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +1.4 points, sd 3.1, bar 0.50 sd (70 verification questions, the ids after the 164 that fit, out of 234 calibration); cost saving 13.4% of the budget, 21.6% of the default cost. Mirror fold -3.0 points, sd 2.4 on 164 questions (fails).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +1.4 points, sd 3.1, bar 0.50 sd (70 verification questions, the ids after the 164 that fit, out of 234 calibration); cost saving 17.7% of the budget, 41.2% of the default cost. Mirror fold -1.8 points, sd 2.5 on 164 questions (fails).
- `avg_gated_lookup` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +5.7 points, sd 4.0, bar 0.50 sd (70 verification questions, the ids after the 164 that fit, out of 234 calibration); cost saving 19.8% of the budget, 60.1% of the default cost. Mirror fold +4.3 points, sd 1.8 on 164 questions (clears).
- `avg_gated_lookup` at 1.00x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +2.9 points, sd 4.0, bar 0.50 sd (70 verification questions, the ids after the 164 that fit, out of 234 calibration); cost saving 39.9% of the budget, 60.1% of the default cost. Mirror fold +1.2 points, sd 1.2 on 164 questions (clears).
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 93.0 points at 60.1% of the default cost, 19.8% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 93.0 points at 60.1% of the default cost, 39.9% under the budget it was given.
- `avg_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 93.0 points at 60.1% of the default cost, 19.8% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 93.0 points at 60.1% of the default cost, 39.9% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
