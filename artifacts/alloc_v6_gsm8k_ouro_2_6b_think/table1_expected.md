# Table 1 -- gsm8k (ouro_2_6b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 112957 layer passes over 1056 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 21.5 | +43.5 |
| default_cell | n/a | n/a | n/a | 21.5 | +43.5 |
| default_at_budget | 14.2 | 23.4 | 25.5 | 21.5 | +43.5 |
| lookup | 57.4 | 65.0 | 65.0 | 65.0 | +0.0 |
| equation | 57.4 | 65.0 | 64.6 | 64.6 | +0.4 |
| equation_n100 | 57.4 | 65.0 | 64.6 | 64.6 | +0.4 |
| equation_n30 | 57.4 | 65.0 | 64.6 | 64.6 | +0.4 |
| equation_resolved | 57.4 | 65.0 | 65.0 | 65.0 | +0.0 |
| gated_equation | 57.4 | 65.0 | 64.6 | 64.6 | +0.4 |
| gated_equation_resolved | 57.4 | 65.0 | 64.6 | 25.5 | +39.5 |
| avg_gated_equation_resolved | 57.4 | 23.4 | 25.5 | 25.5 | +39.5 |
| avg_gated_lookup | 57.4 | 23.4 | 25.5 | 25.5 | +39.5 |
| avg_lookup | 57.4 | 65.0 | 65.0 | 65.0 | +0.0 |
| avg_equation | 57.4 | 65.0 | 64.6 | 64.6 | +0.4 |
| avg_equation_resolved | 57.4 | 65.0 | 65.0 | 65.0 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 1 at cap 2048, 65.0 points over 1056 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F1, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 21451 vs 28239 (-24.0%) | 52258 vs 56478 (-7.5%) | 79574 vs 84718 (-6.1%) | 79574 vs 112957 (-29.6%) |
| avg_gated_lookup | 21451 vs 28239 (-24.0%) | 52258 vs 56478 (-7.5%) | 79574 vs 84718 (-6.1%) | 79574 vs 112957 (-29.6%) |
| avg_lookup | 21451 vs 28239 (-24.0%) | 39186 vs 56478 (-30.6%) | 39186 vs 84718 (-53.7%) | 39186 vs 112957 (-65.3%) |
| avg_equation | 21451 vs 28239 (-24.0%) | 39186 vs 56478 (-30.6%) | 57501 vs 84718 (-32.1%) | 57501 vs 112957 (-49.1%) |
| avg_equation_resolved | 21451 vs 28239 (-24.0%) | 39186 vs 56478 (-30.6%) | 39186 vs 84718 (-53.7%) | 39186 vs 112957 (-65.3%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 1056 | 28032 | 100047 (over) vs 100047 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T128: 1056 | 28032 | 100047 (over) vs 100047 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T128: 1056 | 28032 | 100047 (over) vs 100047 (over) |
| 1.00x | default_cell | 4 | k4_T4096: 1056 | 100047 | 100047 (fits) vs 100047 (fits) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 1056 | 28032 | 100047 (over) vs 100047 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T128: 1056 | 28032 | 100047 (over) vs 100047 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T128: 1056 | 28032 | 100047 (over) vs 100047 (over) |
| 1.00x | default_cell | 4 | k4_T4096: 1056 | 100047 | 100047 (fits) vs 100047 (fits) |
- `avg_gated_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 25.5 points at 70.4% of the default cost, 6.1% under the budget it was given.
- `avg_gated_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 25.5 points at 70.4% of the default cost, 29.6% under the budget it was given.
- `avg_gated_equation_resolved` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F3. Verification margin +38.0 points, sd 6.1, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 24.0% of the budget, 19.0% of the default cost. Mirror fold +48.9 points, sd 4.3 on 184 questions (clears).
- `avg_gated_equation_resolved` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F1. Verification margin +7.6 points, sd 5.8, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 7.5% of the budget, 46.3% of the default cost. Mirror fold +4.9 points, sd 2.8 on 184 questions (clears).
- `avg_gated_equation_resolved` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F1. Verification margin +10.1 points, sd 6.2, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 6.1% of the budget, 70.4% of the default cost. Mirror fold +9.8 points, sd 3.6 on 184 questions (clears).
- `avg_gated_equation_resolved` at 1.00x: deviated from the default cell on family F1. Verification margin +5.1 points, sd 3.0, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 29.6% of the budget, 70.4% of the default cost. Mirror fold +5.4 points, sd 2.5 on 184 questions (clears).
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 25.5 points at 70.4% of the default cost, 6.1% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 25.5 points at 70.4% of the default cost, 29.6% under the budget it was given.
- `avg_gated_lookup` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F3. Verification margin +38.0 points, sd 6.1, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 24.0% of the budget, 19.0% of the default cost. Mirror fold +48.9 points, sd 4.3 on 184 questions (clears).
- `avg_gated_lookup` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F1. Verification margin +7.6 points, sd 5.8, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 7.5% of the budget, 46.3% of the default cost. Mirror fold +4.9 points, sd 2.8 on 184 questions (clears).
- `avg_gated_lookup` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F1. Verification margin +10.1 points, sd 6.2, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 6.1% of the budget, 70.4% of the default cost. Mirror fold +9.8 points, sd 3.6 on 184 questions (clears).
- `avg_gated_lookup` at 1.00x: deviated from the default cell on family F1. Verification margin +5.1 points, sd 3.0, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 29.6% of the budget, 70.4% of the default cost. Mirror fold +5.4 points, sd 2.5 on 184 questions (clears).
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 65.0 points at 34.7% of the default cost, 30.6% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 65.0 points at 34.7% of the default cost, 53.7% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 65.0 points at 34.7% of the default cost, 65.3% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 64.6 points at 50.9% of the default cost, 32.1% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 64.6 points at 50.9% of the default cost, 49.1% under the budget it was given.
- `avg_equation_resolved` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 65.0 points at 34.7% of the default cost, 30.6% under the budget it was given.
- `avg_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 65.0 points at 34.7% of the default cost, 53.7% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 65.0 points at 34.7% of the default cost, 65.3% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
