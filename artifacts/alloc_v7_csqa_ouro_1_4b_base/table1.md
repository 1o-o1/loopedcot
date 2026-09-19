# Table 1 -- csqa (ouro_1_4b_base), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 4576 layer passes over 977 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 72.6 | +0.8 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 73.4 | 72.7 | 72.9 | +0.5 |
| lookup | 72.1 | 73.4 | 73.4 | 73.4 | +0.0 |
| equation | 72.1 | 73.4 | 71.9 | 72.9 | +0.5 |
| equation_n100 | 72.1 | 73.4 | 71.9 | 72.9 | +0.5 |
| equation_n30 | 72.1 | 73.4 | 71.9 | 71.9 | +1.5 |
| equation_resolved | 72.1 | 73.4 | 73.4 | 73.4 | +0.0 |
| gated_equation | 72.1 | 73.4 | 73.4 | 72.9 | +0.5 |
| gated_equation_resolved | 72.1 | 73.4 | 73.4 | 72.9 | +0.5 |
| avg_gated_equation_resolved | 72.1 | 73.4 | 73.4 | 72.9 | +0.5 |
| avg_gated_lookup | 72.1 | 73.4 | 73.4 | 72.9 | +0.5 |
| avg_lookup | 72.1 | 73.4 | 73.4 | 73.4 | +0.0 |
| avg_equation | 72.1 | 73.4 | 71.9 | 72.9 | +0.5 |
| avg_equation_resolved | 72.1 | 73.4 | 73.4 | 73.4 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 0, 73.4 points over 977 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 936 vs 1144 (-18.2%) | 1248 vs 2288 (-45.5%) | 1248 vs 3432 (-63.6%) | 4320 vs 4576 (-5.6%) |
| avg_gated_lookup | 936 vs 1144 (-18.2%) | 1248 vs 2288 (-45.5%) | 1248 vs 3432 (-63.6%) | 4320 vs 4576 (-5.6%) |
| avg_lookup | 936 vs 1144 (-18.2%) | 1248 vs 2288 (-45.5%) | 1248 vs 3432 (-63.6%) | 1248 vs 4576 (-72.7%) |
| avg_equation | 936 vs 1144 (-18.2%) | 1248 vs 2288 (-45.5%) | 3240 vs 3432 (-5.6%) | 4320 vs 4576 (-5.6%) |
| avg_equation_resolved | 936 vs 1144 (-18.2%) | 1248 vs 2288 (-45.5%) | 1248 vs 3432 (-63.6%) | 1248 vs 4576 (-72.7%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | shallower_depth | 3 | k3_T0: 977 | 936 | 394464 (over) vs 394464 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T0: 977 | 1248 | 394464 (over) vs 394464 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T16: 977 | 2784 | 394464 (over) vs 394464 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T32: 977 | 4320 | 394464 (over) vs 394464 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | shallower_depth | 3 | k3_T0: 977 | 936 | 394464 (over) vs 394464 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T0: 977 | 1248 | 394464 (over) vs 394464 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T16: 977 | 2784 | 394464 (over) vs 394464 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T32: 977 | 4320 | 394464 (over) vs 394464 (over) |
- `avg_gated_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 73.4 points at 27.3% of the default cost, 63.6% under the budget it was given.
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (one depth down, depth 3, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 18.2% of the budget, 20.5% of the default cost. Mirror fold +0.0 points, sd 0.0 on 171 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 45.5% of the budget, 27.3% of the default cost. Mirror fold -2.9 points, sd 1.5 on 171 questions (fails).
- `avg_gated_equation_resolved` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F0. Verification margin +5.5 points, sd 3.3, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 63.6% of the budget, 27.3% of the default cost. Mirror fold +4.7 points, sd 1.8 on 171 questions (clears).
- `avg_gated_equation_resolved` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +1.4 points, sd 4.6, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 5.6% of the budget, 94.4% of the default cost. Mirror fold +0.0 points, sd 0.0 on 171 questions (fails).
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 73.4 points at 27.3% of the default cost, 63.6% under the budget it was given.
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (one depth down, depth 3, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 18.2% of the budget, 20.5% of the default cost. Mirror fold +0.0 points, sd 0.0 on 171 questions (fails).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 45.5% of the budget, 27.3% of the default cost. Mirror fold -2.9 points, sd 1.5 on 171 questions (fails).
- `avg_gated_lookup` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F0. Verification margin +5.5 points, sd 3.3, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 63.6% of the budget, 27.3% of the default cost. Mirror fold +4.7 points, sd 1.8 on 171 questions (clears).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +1.4 points, sd 4.6, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 5.6% of the budget, 94.4% of the default cost. Mirror fold +0.6 points, sd 2.9 on 171 questions (fails).
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 73.4 points at 27.3% of the default cost, 45.5% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 73.4 points at 27.3% of the default cost, 63.6% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 73.4 points at 27.3% of the default cost, 72.7% under the budget it was given.
- `avg_equation_resolved` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 73.4 points at 27.3% of the default cost, 45.5% under the budget it was given.
- `avg_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 73.4 points at 27.3% of the default cost, 63.6% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 73.4 points at 27.3% of the default cost, 72.7% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
