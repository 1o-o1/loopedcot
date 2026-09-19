# Table 1 -- strategyqa (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 24413 layer passes over 1990 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 66.5 | +1.9 |
| default_cell | n/a | n/a | n/a | 66.5 | +1.9 |
| default_at_budget | 66.5 | 66.7 | 66.6 | 66.5 | +1.9 |
| lookup | 68.1 | 68.1 | 68.1 | 68.1 | +0.3 |
| equation | 68.2 | 67.8 | 68.1 | 67.7 | +0.7 |
| equation_n100 | 66.5 | 66.8 | 66.6 | 66.6 | +1.8 |
| equation_n30 | 53.8 | 53.1 | 52.7 | 52.7 | +15.7 |
| equation_resolved | 68.1 | 68.1 | 68.1 | 68.1 | +0.3 |
| gated_equation | 68.2 | 66.7 | 66.6 | 66.5 | +1.9 |
| gated_equation_resolved | 68.1 | 68.1 | 68.1 | 68.1 | +0.3 |
| avg_gated_equation_resolved | 66.5 | 66.7 | 66.6 | 66.5 | +1.9 |
| avg_gated_lookup | 66.5 | 66.7 | 66.6 | 66.5 | +1.9 |
| avg_lookup | 68.1 | 68.1 | 68.1 | 68.1 | +0.3 |
| avg_equation | 68.2 | 68.2 | 68.1 | 67.7 | +0.7 |
| avg_equation_resolved | 68.1 | 68.1 | 68.1 | 68.1 | +0.3 |

The ORACLE GAP is the best single evaluation cell (depth 3 at cap 128, 68.4 points over 1990 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 5979 vs 6103 (-2.0%) | 10537 vs 12206 (-13.7%) | 14797 vs 18310 (-19.2%) | 23316 vs 24413 (-4.5%) |
| avg_gated_lookup | 5979 vs 6103 (-2.0%) | 10537 vs 12206 (-13.7%) | 14797 vs 18310 (-19.2%) | 23316 vs 24413 (-4.5%) |
| avg_lookup | 4464 vs 6103 (-26.9%) | 4464 vs 12206 (-63.4%) | 4464 vs 18310 (-75.6%) | 4464 vs 24413 (-81.7%) |
| avg_equation | 5783 vs 6103 (-5.2%) | 5783 vs 12206 (-52.6%) | 13524 vs 18310 (-26.1%) | 22372 vs 24413 (-8.4%) |
| avg_equation_resolved | 4464 vs 6103 (-26.9%) | 4464 vs 12206 (-63.4%) | 4464 vs 18310 (-75.6%) | 4464 vs 24413 (-81.7%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T64: 1990 | 5979 | 23316 (over) vs 23316 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T1024: 1990 | 10537 | 23316 (over) vs 23316 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T2048: 1990 | 14797 | 23316 (over) vs 23316 (over) |
| 1.00x | default_cell | 4 | k4_T4096: 1990 | 23316 | 23316 (fits) vs 23316 (fits) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T64: 1990 | 5979 | 23316 (over) vs 23316 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T1024: 1990 | 10537 | 23316 (over) vs 23316 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T2048: 1990 | 14797 | 23316 (over) vs 23316 (over) |
| 1.00x | default_cell | 4 | k4_T4096: 1990 | 23316 | 23316 (fits) vs 23316 (fits) |
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +6.7 points, sd 4.8, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 2.0% of the budget, 24.5% of the default cost. Mirror fold -1.0 points, sd 4.3 on 210 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +11.1 points, sd 4.6, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 13.7% of the budget, 43.2% of the default cost. Mirror fold -1.0 points, sd 4.4 on 210 questions (fails).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +11.1 points, sd 4.7, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 19.2% of the budget, 60.6% of the default cost. Mirror fold -1.4 points, sd 4.4 on 210 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: reverted to the default cell for every question. Verification margin +11.1 points, sd 4.7, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 4.5% of the budget, 95.5% of the default cost. Mirror fold -1.4 points, sd 4.4 on 210 questions (fails).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +6.7 points, sd 4.8, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 2.0% of the budget, 24.5% of the default cost. Mirror fold -1.0 points, sd 4.3 on 210 questions (fails).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +11.1 points, sd 4.6, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 13.7% of the budget, 43.2% of the default cost. Mirror fold -1.0 points, sd 4.4 on 210 questions (fails).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +11.1 points, sd 4.7, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 19.2% of the budget, 60.6% of the default cost. Mirror fold -1.4 points, sd 4.4 on 210 questions (fails).
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin +11.1 points, sd 4.7, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 4.5% of the budget, 95.5% of the default cost. Mirror fold -1.4 points, sd 4.4 on 210 questions (fails).
- `avg_lookup` at 0.25x: the multiplier is 0, so the budget never binds. The row is the same 68.1 points at 18.3% of the default cost, 26.9% under the budget it was given.
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 68.1 points at 18.3% of the default cost, 63.4% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 68.1 points at 18.3% of the default cost, 75.6% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.1 points at 18.3% of the default cost, 81.7% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 67.7 points at 91.6% of the default cost, 8.4% under the budget it was given.
- `avg_equation_resolved` at 0.25x: the multiplier is 0, so the budget never binds. The row is the same 68.1 points at 18.3% of the default cost, 26.9% under the budget it was given.
- `avg_equation_resolved` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 68.1 points at 18.3% of the default cost, 63.4% under the budget it was given.
- `avg_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 68.1 points at 18.3% of the default cost, 75.6% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.1 points at 18.3% of the default cost, 81.7% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
