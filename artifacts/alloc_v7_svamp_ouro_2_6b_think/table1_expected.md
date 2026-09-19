# Table 1 -- svamp (ouro_2_6b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 126848 layer passes over 200 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 7.0 | +61.5 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 14.0 | 12.5 | 8.0 | 6.5 | +62.0 |
| lookup | 68.5 | 68.5 | 68.5 | 68.5 | +0.0 |
| equation | 68.5 | 68.5 | 68.5 | 68.5 | +0.0 |
| equation_n100 | 68.5 | 68.5 | 68.5 | 68.5 | +0.0 |
| equation_n30 | 68.5 | 68.5 | 68.5 | 68.5 | +0.0 |
| equation_resolved | 68.5 | 68.5 | 68.5 | 68.5 | +0.0 |
| gated_equation | 68.5 | 68.5 | 68.5 | 68.5 | +0.0 |
| gated_equation_resolved | 21.0 | 68.5 | 68.5 | 68.5 | +0.0 |
| avg_gated_equation_resolved | 21.0 | 68.5 | 68.5 | 68.5 | +0.0 |
| avg_gated_lookup | 21.0 | 68.5 | 68.5 | 68.5 | +0.0 |
| avg_lookup | 68.5 | 68.5 | 68.5 | 68.5 | +0.0 |
| avg_equation | 68.5 | 68.5 | 68.5 | 68.5 | +0.0 |
| avg_equation_resolved | 68.5 | 68.5 | 68.5 | 68.5 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 1 at cap 1024, 68.5 points over 200 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 20444 vs 31712 (-35.5%) | 39592 vs 63424 (-37.6%) | 39592 vs 95136 (-58.4%) | 39592 vs 126848 (-68.8%) |
| avg_gated_lookup | 20444 vs 31712 (-35.5%) | 25524 vs 63424 (-59.8%) | 25524 vs 95136 (-73.2%) | 25524 vs 126848 (-79.9%) |
| avg_lookup | 25524 vs 31712 (-19.5%) | 25524 vs 63424 (-59.8%) | 25524 vs 95136 (-73.2%) | 25524 vs 126848 (-79.9%) |
| avg_equation | 25524 vs 31712 (-19.5%) | 25524 vs 63424 (-59.8%) | 67117 vs 95136 (-29.5%) | 67117 vs 126848 (-47.1%) |
| avg_equation_resolved | 25524 vs 31712 (-19.5%) | 39592 vs 63424 (-37.6%) | 39592 vs 95136 (-58.4%) | 39592 vs 126848 (-68.8%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 200 | 27260 | 155808 (over) vs 155808 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T256: 200 | 49258 | 155808 (over) vs 155808 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T1024: 200 | 87815 | 155808 (over) vs 155808 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T2048: 200 | 113313 | 155808 (over) vs 155808 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 200 | 27260 | 155808 (over) vs 155808 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T256: 200 | 49258 | 155808 (over) vs 155808 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T1024: 200 | 87815 | 155808 (over) vs 155808 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T2048: 200 | 113313 | 155808 (over) vs 155808 (over) |
- `avg_gated_equation_resolved` at 0.25x: the multiplier is 0, so the budget never binds. The row is the same 21.0 points at 16.1% of the default cost, 35.5% under the budget it was given.
- `avg_gated_equation_resolved` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 31.2% of the default cost, 37.6% under the budget it was given.
- `avg_gated_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 31.2% of the default cost, 58.4% under the budget it was given.
- `avg_gated_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 31.2% of the default cost, 68.8% under the budget it was given.
- `avg_gated_equation_resolved` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +13.3 points, sd 7.8, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 35.5% of the budget, 16.1% of the default cost. Mirror fold +7.1 points, sd 4.2 on 70 questions (clears).
- `avg_gated_equation_resolved` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F3. Verification margin +36.7 points, sd 11.9, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 37.6% of the budget, 31.2% of the default cost. Mirror fold +50.0 points, sd 6.9 on 70 questions (clears).
- `avg_gated_equation_resolved` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F3. Verification margin +40.0 points, sd 10.9, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 58.4% of the budget, 31.2% of the default cost. Mirror fold +48.6 points, sd 7.3 on 70 questions (clears).
- `avg_gated_equation_resolved` at 1.00x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F3. Verification margin +40.0 points, sd 10.9, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 68.8% of the budget, 31.2% of the default cost. Mirror fold +47.1 points, sd 7.3 on 70 questions (clears).
- `avg_gated_lookup` at 0.25x: the multiplier is 0, so the budget never binds. The row is the same 21.0 points at 16.1% of the default cost, 35.5% under the budget it was given.
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 20.1% of the default cost, 59.8% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 20.1% of the default cost, 73.2% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 20.1% of the default cost, 79.9% under the budget it was given.
- `avg_gated_lookup` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +13.3 points, sd 7.8, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 35.5% of the budget, 16.1% of the default cost. Mirror fold +7.1 points, sd 4.2 on 70 questions (clears).
- `avg_gated_lookup` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F3. Verification margin +36.7 points, sd 11.9, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 59.8% of the budget, 20.1% of the default cost. Mirror fold +47.1 points, sd 7.2 on 70 questions (clears).
- `avg_gated_lookup` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F3. Verification margin +40.0 points, sd 10.9, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 73.2% of the budget, 20.1% of the default cost. Mirror fold +48.6 points, sd 7.2 on 70 questions (clears).
- `avg_gated_lookup` at 1.00x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F3. Verification margin +40.0 points, sd 10.9, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 79.9% of the budget, 20.1% of the default cost. Mirror fold +47.1 points, sd 7.3 on 70 questions (clears).
- `avg_lookup` at 0.25x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 20.1% of the default cost, 19.5% under the budget it was given.
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 20.1% of the default cost, 59.8% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 20.1% of the default cost, 73.2% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 20.1% of the default cost, 79.9% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 52.9% of the default cost, 29.5% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 52.9% of the default cost, 47.1% under the budget it was given.
- `avg_equation_resolved` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 31.2% of the default cost, 37.6% under the budget it was given.
- `avg_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 31.2% of the default cost, 58.4% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 31.2% of the default cost, 68.8% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
