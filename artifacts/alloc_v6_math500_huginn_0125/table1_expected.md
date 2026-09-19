# Table 1 -- math500 (huginn_0125), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 96956 layer passes over 400 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 15.0 | +0.8 |
| default_cell | n/a | n/a | n/a | 15.0 | +0.8 |
| default_at_budget | 15.2 | 15.2 | 15.2 | 15.0 | +0.8 |
| lookup | 15.2 | 15.8 | 15.8 | 15.8 | +0.0 |
| equation | 15.2 | 15.2 | 15.2 | 15.0 | +0.8 |
| equation_n100 | 15.2 | 15.2 | 15.2 | 15.0 | +0.8 |
| equation_n30 | 15.2 | 15.2 | 15.2 | 15.0 | +0.8 |
| equation_resolved | 15.2 | 15.8 | 15.8 | 15.8 | +0.0 |
| gated_equation | 15.2 | 15.2 | 15.2 | 15.0 | +0.8 |
| gated_equation_resolved | 15.2 | 15.2 | 15.2 | 15.0 | +0.8 |
| avg_gated_equation_resolved | 15.2 | 15.2 | 15.2 | 15.0 | +0.8 |
| avg_gated_lookup | 15.2 | 15.2 | 15.2 | 15.0 | +0.8 |
| avg_lookup | 15.2 | 15.8 | 15.8 | 15.8 | +0.0 |
| avg_equation | 15.2 | 15.2 | 15.2 | 15.0 | +0.8 |
| avg_equation_resolved | 15.2 | 15.8 | 15.8 | 15.8 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 16 at cap 256, 15.8 points over 400 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none.

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 19692 vs 24239 (-18.8%) | 39213 vs 48478 (-19.1%) | 56210 vs 72717 (-22.7%) | 94259 vs 96956 (-2.8%) |
| avg_gated_lookup | 19692 vs 24239 (-18.8%) | 39213 vs 48478 (-19.1%) | 56210 vs 72717 (-22.7%) | 94259 vs 96956 (-2.8%) |
| avg_lookup | 19692 vs 24239 (-18.8%) | 28292 vs 48478 (-41.6%) | 28292 vs 72717 (-61.1%) | 28292 vs 96956 (-70.8%) |
| avg_equation | 9947 vs 24239 (-59.0%) | 39213 vs 48478 (-19.1%) | 39213 vs 72717 (-46.1%) | 94259 vs 96956 (-2.8%) |
| avg_equation_resolved | 19692 vs 24239 (-18.8%) | 28292 vs 48478 (-41.6%) | 28292 vs 72717 (-61.1%) | 28292 vs 96956 (-70.8%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 32 | k32_T128: 400 | 19692 | 94259 (over) vs 94259 (over) |
| 0.50x | deepest_depth_capped | 32 | k32_T512: 400 | 39213 | 94259 (over) vs 94259 (over) |
| 0.75x | deepest_depth_capped | 32 | k32_T1024: 400 | 56210 | 94259 (over) vs 94259 (over) |
| 1.00x | default_cell | 32 | k32_T4096: 400 | 94259 | 94259 (fits) vs 94259 (fits) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 32 | k32_T128: 400 | 19692 | 94259 (over) vs 94259 (over) |
| 0.50x | deepest_depth_capped | 32 | k32_T512: 400 | 39213 | 94259 (over) vs 94259 (over) |
| 0.75x | deepest_depth_capped | 32 | k32_T1024: 400 | 56210 | 94259 (over) vs 94259 (over) |
| 1.00x | default_cell | 32 | k32_T4096: 400 | 94259 | 94259 (fits) vs 94259 (fits) |
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 18.8% of the budget, 20.3% of the default cost. Mirror fold -8.6 points, sd 3.4 on 70 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap it affords) for every question. Verification margin -3.3 points, sd 3.4, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 19.1% of the budget, 40.4% of the default cost. Mirror fold -7.1 points, sd 3.1 on 70 questions (fails).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap it affords) for every question. Verification margin -3.3 points, sd 3.4, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 22.7% of the budget, 58.0% of the default cost. Mirror fold -7.1 points, sd 3.1 on 70 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: reverted to the default cell for every question. Verification margin -3.3 points, sd 3.4, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 2.8% of the budget, 97.2% of the default cost. Mirror fold -7.1 points, sd 3.1 on 70 questions (fails).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 18.8% of the budget, 20.3% of the default cost. Mirror fold -8.6 points, sd 3.4 on 70 questions (fails).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap it affords) for every question. Verification margin -3.3 points, sd 3.4, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 19.1% of the budget, 40.4% of the default cost. Mirror fold -7.1 points, sd 3.1 on 70 questions (fails).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap it affords) for every question. Verification margin -3.3 points, sd 3.4, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 22.7% of the budget, 58.0% of the default cost. Mirror fold -7.1 points, sd 3.1 on 70 questions (fails).
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin -3.3 points, sd 3.4, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 2.8% of the budget, 97.2% of the default cost. Mirror fold -7.1 points, sd 3.1 on 70 questions (fails).
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 15.8 points at 29.2% of the default cost, 41.6% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 15.8 points at 29.2% of the default cost, 61.1% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 15.8 points at 29.2% of the default cost, 70.8% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 15.0 points at 97.2% of the default cost, 2.8% under the budget it was given.
- `avg_equation_resolved` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 15.8 points at 29.2% of the default cost, 41.6% under the budget it was given.
- `avg_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 15.8 points at 29.2% of the default cost, 61.1% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 15.8 points at 29.2% of the default cost, 70.8% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
