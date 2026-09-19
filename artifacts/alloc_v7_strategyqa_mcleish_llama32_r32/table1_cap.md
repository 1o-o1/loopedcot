# Table 1 -- strategyqa (mcleish_llama32_r32), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 41981 layer passes over 1990 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 49.7 | +2.6 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 50.7 | 50.8 | 50.7 | 50.7 | +1.7 |
| lookup | 51.5 | 51.5 | 51.5 | 49.4 | +2.9 |
| equation | 50.7 | 50.8 | 50.7 | 50.7 | +1.7 |
| equation_n100 | 50.7 | 50.8 | 50.7 | 50.7 | +1.7 |
| equation_n30 | 50.7 | 50.8 | 50.7 | 50.7 | +1.7 |
| equation_resolved | 51.5 | 51.5 | 51.5 | 49.4 | +2.9 |
| gated_equation | 50.7 | 50.8 | 50.7 | 50.7 | +1.7 |
| gated_equation_resolved | 50.7 | 50.8 | 50.7 | 50.7 | +1.7 |
| avg_gated_equation_resolved | 50.7 | 50.8 | 50.7 | 50.7 | +1.7 |
| avg_gated_lookup | 50.7 | 50.8 | 50.7 | 50.7 | +1.7 |
| avg_lookup | 51.5 | 51.5 | 51.5 | 49.4 | +2.9 |
| avg_equation | 50.7 | 50.7 | 50.7 | 50.7 | +1.7 |
| avg_equation_resolved | 51.5 | 51.5 | 51.5 | 49.4 | +2.9 |

The ORACLE GAP is the best single evaluation cell (depth 2 at cap 128, 52.3 points over 1990 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none.

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 7896 vs 10495 (-24.8%) | 15064 vs 20991 (-28.2%) | 29400 vs 31486 (-6.6%) | 29400 vs 41981 (-30.0%) |
| avg_gated_lookup | 7896 vs 10495 (-24.8%) | 15064 vs 20991 (-28.2%) | 29400 vs 31486 (-6.6%) | 29400 vs 41981 (-30.0%) |
| avg_lookup | 5380 vs 10495 (-48.7%) | 5380 vs 20991 (-74.4%) | 5380 vs 31486 (-82.9%) | 33184 vs 41981 (-21.0%) |
| avg_equation | 7896 vs 10495 (-24.8%) | 7896 vs 20991 (-62.4%) | 7896 vs 31486 (-74.9%) | 7896 vs 41981 (-81.2%) |
| avg_equation_resolved | 5380 vs 10495 (-48.7%) | 5380 vs 20991 (-74.4%) | 5380 vs 31486 (-82.9%) | 33184 vs 41981 (-21.0%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 8 | k8_T128: 1990 | 7896 | 230104 (over) vs 230104 (over) |
| 0.50x | deepest_depth_capped | 8 | k8_T256: 1990 | 15064 | 230104 (over) vs 230104 (over) |
| 0.75x | deepest_depth_capped | 8 | k8_T512: 1990 | 29400 | 230104 (over) vs 230104 (over) |
| 1.00x | deepest_depth_capped | 8 | k8_T512: 1990 | 29400 | 230104 (over) vs 230104 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 8 | k8_T128: 1990 | 7896 | 230104 (over) vs 230104 (over) |
| 0.50x | deepest_depth_capped | 8 | k8_T256: 1990 | 15064 | 230104 (over) vs 230104 (over) |
| 0.75x | deepest_depth_capped | 8 | k8_T512: 1990 | 29400 | 230104 (over) vs 230104 (over) |
| 1.00x | deepest_depth_capped | 8 | k8_T512: 1990 | 29400 | 230104 (over) vs 230104 (over) |
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +3.3 points, sd 7.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 24.8% of the budget, 18.8% of the default cost. Mirror fold -5.7 points, sd 3.8 on 210 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +3.3 points, sd 7.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 28.2% of the budget, 35.9% of the default cost. Mirror fold -6.7 points, sd 3.9 on 210 questions (fails).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +2.2 points, sd 7.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 6.6% of the budget, 70.0% of the default cost. Mirror fold -6.7 points, sd 3.9 on 210 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +1.1 points, sd 5.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 30.0% of the budget, 70.0% of the default cost. Mirror fold -6.7 points, sd 3.9 on 210 questions (fails).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +3.3 points, sd 7.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 24.8% of the budget, 18.8% of the default cost. Mirror fold -5.7 points, sd 3.8 on 210 questions (fails).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +3.3 points, sd 7.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 28.2% of the budget, 35.9% of the default cost. Mirror fold -6.7 points, sd 3.9 on 210 questions (fails).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +2.2 points, sd 7.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 6.6% of the budget, 70.0% of the default cost. Mirror fold -6.7 points, sd 3.9 on 210 questions (fails).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +1.1 points, sd 5.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 30.0% of the budget, 70.0% of the default cost. Mirror fold -6.7 points, sd 3.9 on 210 questions (fails).

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
