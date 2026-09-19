# Table 1 -- math500 (huginn_0125), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 96956 layer passes over 400 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 15.0 | +0.8 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 15.2 | 15.8 | 15.2 | 15.2 | +0.5 |
| lookup | 15.2 | 15.8 | 15.8 | 15.8 | +0.0 |
| equation | 15.2 | 15.8 | 15.2 | 15.2 | +0.5 |
| equation_n100 | 15.2 | 15.8 | 15.2 | 15.2 | +0.5 |
| equation_n30 | 15.2 | 15.8 | 15.2 | 15.2 | +0.5 |
| equation_resolved | 15.2 | 15.8 | 15.8 | 15.8 | +0.0 |
| gated_equation | 15.2 | 15.8 | 15.2 | 15.2 | +0.5 |
| gated_equation_resolved | 15.2 | 15.8 | 15.2 | 15.2 | +0.5 |
| avg_gated_equation_resolved | 15.2 | 15.8 | 15.2 | 15.2 | +0.5 |
| avg_gated_lookup | 15.2 | 15.8 | 15.2 | 15.2 | +0.5 |
| avg_lookup | 15.2 | 15.8 | 15.8 | 15.8 | +0.0 |
| avg_equation | 15.2 | 15.8 | 15.2 | 15.2 | +0.5 |
| avg_equation_resolved | 15.2 | 15.8 | 15.8 | 15.8 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 16 at cap 256, 15.8 points over 400 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none.

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 21648 vs 24239 (-10.7%) | 38544 vs 48478 (-20.5%) | 72336 vs 72717 (-0.5%) | 72336 vs 96956 (-25.4%) |
| avg_gated_lookup | 21648 vs 24239 (-10.7%) | 38544 vs 48478 (-20.5%) | 72336 vs 72717 (-0.5%) | 72336 vs 96956 (-25.4%) |
| avg_lookup | 21648 vs 24239 (-10.7%) | 38544 vs 48478 (-20.5%) | 38544 vs 72717 (-47.0%) | 38544 vs 96956 (-60.2%) |
| avg_equation | 21648 vs 24239 (-10.7%) | 38544 vs 48478 (-20.5%) | 72336 vs 72717 (-0.5%) | 72336 vs 96956 (-25.4%) |
| avg_equation_resolved | 21648 vs 24239 (-10.7%) | 38544 vs 48478 (-20.5%) | 38544 vs 72717 (-47.0%) | 38544 vs 96956 (-60.2%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 32 | k32_T128: 400 | 21648 | 545424 (over) vs 545424 (over) |
| 0.50x | deepest_depth_capped | 32 | k32_T256: 400 | 38544 | 545424 (over) vs 545424 (over) |
| 0.75x | deepest_depth_capped | 32 | k32_T512: 400 | 72336 | 545424 (over) vs 545424 (over) |
| 1.00x | deepest_depth_capped | 32 | k32_T512: 400 | 72336 | 545424 (over) vs 545424 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 32 | k32_T128: 400 | 21648 | 545424 (over) vs 545424 (over) |
| 0.50x | deepest_depth_capped | 32 | k32_T256: 400 | 38544 | 545424 (over) vs 545424 (over) |
| 0.75x | deepest_depth_capped | 32 | k32_T512: 400 | 72336 | 545424 (over) vs 545424 (over) |
| 1.00x | deepest_depth_capped | 32 | k32_T512: 400 | 72336 | 545424 (over) vs 545424 (over) |
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 10.7% of the budget, 22.3% of the default cost. Mirror fold -8.6 points, sd 3.4 on 70 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap it affords) for every question. Verification margin -3.3 points, sd 3.4, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 20.5% of the budget, 39.8% of the default cost. Mirror fold -8.6 points, sd 3.3 on 70 questions (fails).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap it affords) for every question. Verification margin -3.3 points, sd 3.4, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 0.5% of the budget, 74.6% of the default cost. Mirror fold -7.1 points, sd 3.1 on 70 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap it affords) for every question. Verification margin -3.3 points, sd 3.4, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 25.4% of the budget, 74.6% of the default cost. Mirror fold -7.1 points, sd 3.1 on 70 questions (fails).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 10.7% of the budget, 22.3% of the default cost. Mirror fold -8.6 points, sd 3.4 on 70 questions (fails).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap it affords) for every question. Verification margin -3.3 points, sd 3.4, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 20.5% of the budget, 39.8% of the default cost. Mirror fold -8.6 points, sd 3.3 on 70 questions (fails).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap it affords) for every question. Verification margin -3.3 points, sd 3.4, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 0.5% of the budget, 74.6% of the default cost. Mirror fold -7.1 points, sd 3.1 on 70 questions (fails).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap it affords) for every question. Verification margin -3.3 points, sd 3.4, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 25.4% of the budget, 74.6% of the default cost. Mirror fold -7.1 points, sd 3.1 on 70 questions (fails).
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 15.8 points at 39.8% of the default cost, 20.5% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 15.8 points at 39.8% of the default cost, 47.0% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 15.8 points at 39.8% of the default cost, 60.2% under the budget it was given.
- `avg_equation_resolved` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 15.8 points at 39.8% of the default cost, 20.5% under the budget it was given.
- `avg_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 15.8 points at 39.8% of the default cost, 47.0% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 15.8 points at 39.8% of the default cost, 60.2% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
