# Table 1 -- csqa (mcleish_llama32_r32), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 2599 layer passes over 977 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 39.0 | +3.9 |
| default_cell | n/a | n/a | n/a | 39.0 | +3.9 |
| default_at_budget | n/a | 42.9 | 42.6 | 39.0 | +3.9 |
| lookup | 42.6 | 42.9 | 42.9 | 42.9 | +0.0 |
| equation | 42.6 | 42.9 | 42.9 | 42.9 | +0.0 |
| equation_n100 | 42.6 | 42.9 | 35.6 | 35.6 | +7.3 |
| equation_n30 | 42.6 | 42.9 | 42.9 | 42.9 | +0.0 |
| equation_resolved | 42.6 | 42.9 | 42.9 | 42.9 | +0.0 |
| gated_equation | 42.6 | 42.9 | 42.6 | 42.9 | +0.0 |
| gated_equation_resolved | 42.6 | 42.9 | 42.6 | 42.9 | +0.0 |
| avg_gated_equation_resolved | 42.6 | 42.9 | 42.6 | 42.9 | +0.0 |
| avg_gated_lookup | 42.6 | 42.9 | 42.6 | 42.9 | +0.0 |
| avg_lookup | 42.6 | 42.9 | 42.9 | 42.9 | +0.0 |
| avg_equation | 42.6 | 42.9 | 42.9 | 42.9 | +0.0 |
| avg_equation_resolved | 42.6 | 42.9 | 42.9 | 42.9 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 8 at cap 0, 42.9 points over 977 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0.

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 416 vs 650 (-36.0%) | 728 vs 1299 (-44.0%) | 1624 vs 1949 (-16.7%) | 728 vs 2599 (-72.0%) |
| avg_gated_lookup | 416 vs 650 (-36.0%) | 728 vs 1299 (-44.0%) | 1624 vs 1949 (-16.7%) | 728 vs 2599 (-72.0%) |
| avg_lookup | 416 vs 650 (-36.0%) | 728 vs 1299 (-44.0%) | 728 vs 1949 (-62.6%) | 728 vs 2599 (-72.0%) |
| avg_equation | 416 vs 650 (-36.0%) | 728 vs 1299 (-44.0%) | 728 vs 1949 (-62.6%) | 728 vs 2599 (-72.0%) |
| avg_equation_resolved | 416 vs 650 (-36.0%) | 728 vs 1299 (-44.0%) | 728 vs 1949 (-62.6%) | 728 vs 2599 (-72.0%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | shallower_depth | 4 | k4_T0: 977 | 416 | 2592 (over) vs 2592 (over) |
| 0.50x | deepest_depth_capped | 8 | k8_T0: 977 | 728 | 2592 (over) vs 2592 (over) |
| 0.75x | deepest_depth_capped | 8 | k8_T16: 977 | 1624 | 2592 (over) vs 2592 (over) |
| 1.00x | default_cell | 8 | k8_T4096: 977 | 2592 | 2592 (fits) vs 2592 (fits) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | shallower_depth | 4 | k4_T0: 977 | 416 | 2592 (over) vs 2592 (over) |
| 0.50x | deepest_depth_capped | 8 | k8_T0: 977 | 728 | 2592 (over) vs 2592 (over) |
| 0.75x | deepest_depth_capped | 8 | k8_T16: 977 | 1624 | 2592 (over) vs 2592 (over) |
| 1.00x | default_cell | 8 | k8_T4096: 977 | 2592 | 2592 (fits) vs 2592 (fits) |
- `avg_gated_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 42.9 points at 28.0% of the default cost, 72.0% under the budget it was given.
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (one depth down, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 36.0% of the budget, 16.0% of the default cost. Mirror fold +0.0 points, sd 0.0 on 171 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin -5.5 points, sd 3.9, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 44.0% of the budget, 28.0% of the default cost. Mirror fold +0.0 points, sd 0.0 on 171 questions (fails).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +1.4 points, sd 5.2, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 16.7% of the budget, 62.5% of the default cost. Mirror fold +0.6 points, sd 2.7 on 171 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: deviated from the default cell on family F0. Verification margin +11.0 points, sd 7.2, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 72.0% of the budget, 28.0% of the default cost. Mirror fold +9.4 points, sd 4.4 on 171 questions (clears).
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 42.9 points at 28.0% of the default cost, 72.0% under the budget it was given.
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (one depth down, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 36.0% of the budget, 16.0% of the default cost. Mirror fold +0.0 points, sd 0.0 on 171 questions (fails).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin -5.5 points, sd 3.9, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 44.0% of the budget, 28.0% of the default cost. Mirror fold +0.0 points, sd 0.0 on 171 questions (fails).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +1.4 points, sd 5.2, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 16.7% of the budget, 62.5% of the default cost. Mirror fold +0.6 points, sd 2.7 on 171 questions (fails).
- `avg_gated_lookup` at 1.00x: deviated from the default cell on family F0. Verification margin +11.0 points, sd 7.2, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 72.0% of the budget, 28.0% of the default cost. Mirror fold +9.4 points, sd 4.4 on 171 questions (clears).
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 42.9 points at 28.0% of the default cost, 44.0% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 42.9 points at 28.0% of the default cost, 62.6% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 42.9 points at 28.0% of the default cost, 72.0% under the budget it was given.
- `avg_equation` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 42.9 points at 28.0% of the default cost, 44.0% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 42.9 points at 28.0% of the default cost, 62.6% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 42.9 points at 28.0% of the default cost, 72.0% under the budget it was given.
- `avg_equation_resolved` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 42.9 points at 28.0% of the default cost, 44.0% under the budget it was given.
- `avg_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 42.9 points at 28.0% of the default cost, 62.6% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 42.9 points at 28.0% of the default cost, 72.0% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
