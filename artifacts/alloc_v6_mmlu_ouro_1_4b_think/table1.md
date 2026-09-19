# Table 1 -- mmlu (ouro_1_4b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 86519 layer passes over 1700 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 73.6 | +0.4 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 64.6 | 67.1 | 70.7 | 70.7 | +3.3 |
| lookup | 64.4 | 71.5 | 71.5 | 72.5 | +1.5 |
| equation | 64.6 | 71.5 | 70.7 | 72.5 | +1.5 |
| equation_n100 | 64.6 | 71.5 | 70.7 | 72.5 | +1.5 |
| equation_n30 | 64.6 | 71.5 | 71.5 | 72.5 | +1.5 |
| equation_resolved | 64.4 | 71.5 | 71.5 | 72.5 | +1.5 |
| gated_equation | 64.6 | 71.5 | 70.7 | 70.7 | +3.3 |
| gated_equation_resolved | 64.4 | 71.5 | 70.7 | 70.7 | +3.3 |
| avg_gated_equation_resolved | 64.4 | 71.5 | 70.7 | 70.7 | +3.3 |
| avg_gated_lookup | 64.4 | 71.5 | 70.7 | 70.7 | +3.3 |
| avg_lookup | 64.4 | 71.5 | 71.5 | 71.5 | +2.5 |
| avg_equation | 64.6 | 71.5 | 71.5 | 72.5 | +1.5 |
| avg_equation_resolved | 64.4 | 71.5 | 71.5 | 71.5 | +2.5 |

The ORACLE GAP is the best single evaluation cell (depth 3 at cap 4096, 74.0 points over 1700 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 1008 vs 21630 (-95.3%) | 37872 vs 43260 (-12.5%) | 50496 vs 64889 (-22.2%) | 50496 vs 86519 (-41.6%) |
| avg_gated_lookup | 1008 vs 21630 (-95.3%) | 37872 vs 43260 (-12.5%) | 50496 vs 64889 (-22.2%) | 50496 vs 86519 (-41.6%) |
| avg_lookup | 1008 vs 21630 (-95.3%) | 37872 vs 43260 (-12.5%) | 37872 vs 64889 (-41.6%) | 37872 vs 86519 (-56.2%) |
| avg_equation | 19440 vs 21630 (-10.1%) | 37872 vs 43260 (-12.5%) | 37872 vs 64889 (-41.6%) | 74736 vs 86519 (-13.6%) |
| avg_equation_resolved | 1008 vs 21630 (-95.3%) | 37872 vs 43260 (-12.5%) | 37872 vs 64889 (-41.6%) | 37872 vs 86519 (-56.2%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 1700 | 13632 | 394560 (over) vs 394560 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T256: 1700 | 25920 | 394560 (over) vs 394560 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T512: 1700 | 50496 | 394560 (over) vs 394560 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T512: 1700 | 50496 | 394560 (over) vs 394560 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 1700 | 13632 | 394560 (over) vs 394560 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T256: 1700 | 25920 | 394560 (over) vs 394560 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T512: 1700 | 50496 | 394560 (over) vs 394560 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T512: 1700 | 50496 | 394560 (over) vs 394560 (over) |
- `avg_gated_equation_resolved` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F2. Verification margin +2.2 points, sd 4.2, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 95.3% of the budget, 1.2% of the default cost. Mirror fold +5.7 points, sd 2.7 on 210 questions (clears).
- `avg_gated_equation_resolved` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F2. Verification margin +2.2 points, sd 3.9, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 12.5% of the budget, 43.8% of the default cost. Mirror fold +6.7 points, sd 2.7 on 210 questions (clears).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin -4.4 points, sd 3.2, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 22.2% of the budget, 58.4% of the default cost. Mirror fold +0.0 points, sd 0.0 on 210 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin -2.2 points, sd 3.6, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 41.6% of the budget, 58.4% of the default cost. Mirror fold +0.0 points, sd 0.0 on 210 questions (fails).
- `avg_gated_lookup` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F2. Verification margin +2.2 points, sd 4.2, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 95.3% of the budget, 1.2% of the default cost. Mirror fold +5.7 points, sd 2.7 on 210 questions (clears).
- `avg_gated_lookup` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F2. Verification margin +2.2 points, sd 3.9, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 12.5% of the budget, 43.8% of the default cost. Mirror fold +1.9 points, sd 3.0 on 210 questions (clears).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin -4.4 points, sd 3.2, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 22.2% of the budget, 58.4% of the default cost. Mirror fold +0.0 points, sd 0.0 on 210 questions (fails).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin -2.2 points, sd 3.6, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 41.6% of the budget, 58.4% of the default cost. Mirror fold +0.0 points, sd 0.0 on 210 questions (fails).

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
