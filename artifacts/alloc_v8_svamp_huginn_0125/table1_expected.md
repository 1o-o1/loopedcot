# Table 1 -- svamp (huginn_0125), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 8195 layer passes over 200 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 44.5 | +0.0 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 2.0 | 20.0 | 28.5 | 41.5 | +3.0 |
| lookup | 14.5 | 39.5 | 39.5 | 39.5 | +5.0 |
| equation | 14.5 | 39.5 | 39.5 | 39.5 | +5.0 |
| equation_n100 | 14.5 | 39.5 | 39.5 | 39.5 | +5.0 |
| equation_n30 | 16.5 | 39.5 | 39.5 | 39.5 | +5.0 |
| equation_resolved | 16.5 | 39.5 | 39.5 | 39.5 | +5.0 |
| gated_equation | 16.5 | 39.5 | 28.5 | 41.5 | +3.0 |
| gated_equation_resolved | 16.5 | 39.5 | 28.5 | 41.5 | +3.0 |
| avg_gated_equation_resolved | 16.5 | 39.5 | 28.5 | 41.5 | +3.0 |
| avg_gated_lookup | 16.5 | 39.5 | 28.5 | 41.5 | +3.0 |
| avg_lookup | 3.5 | 18.5 | 39.5 | 39.5 | +5.0 |
| avg_equation | 3.5 | 20.0 | 39.5 | 39.5 | +5.0 |
| avg_equation_resolved | 2.5 | 18.5 | 39.5 | 39.5 | +5.0 |

The ORACLE GAP is the best single evaluation cell (depth 32 at cap 128, 44.5 points over 200 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2. Of the families that CLEAR the bar the one that RUNS is set by `policy.GATE_FAMILY_RULE` = `best`: the cleared family with the largest mean verified margin over the folds, ties to the smaller family. The folds, the bar, the reference and the pricing are the same test under either rule; only which cleared family is taken differs.

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 1836 vs 2049 (-10.4%) | 3900 vs 4097 (-4.8%) | 5498 vs 6146 (-10.5%) | 7689 vs 8195 (-6.2%) |
| avg_gated_lookup | 1836 vs 2049 (-10.4%) | 3900 vs 4097 (-4.8%) | 5498 vs 6146 (-10.5%) | 7689 vs 8195 (-6.2%) |
| avg_lookup | 396 vs 2049 (-80.7%) | 2134 vs 4097 (-47.9%) | 4289 vs 6146 (-30.2%) | 4289 vs 8195 (-47.7%) |
| avg_equation | 396 vs 2049 (-80.7%) | 2459 vs 4097 (-40.0%) | 4290 vs 6146 (-30.2%) | 4290 vs 8195 (-47.6%) |
| avg_equation_resolved | 194 vs 2049 (-90.5%) | 2134 vs 4097 (-47.9%) | 4290 vs 6146 (-30.2%) | 4290 vs 8195 (-47.6%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 32 | k32_T0: 200 | 1452 | 8717 (over) vs 8717 (over) |
| 0.50x | deepest_depth_capped | 32 | k32_T16: 200 | 3564 | 8717 (over) vs 8717 (over) |
| 0.75x | deepest_depth_capped | 32 | k32_T32: 200 | 5498 | 8717 (over) vs 8717 (over) |
| 1.00x | deepest_depth_capped | 32 | k32_T64: 200 | 7689 | 8717 (over) vs 8717 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 32 | k32_T0: 200 | 1452 | 8717 (over) vs 8717 (over) |
| 0.50x | deepest_depth_capped | 32 | k32_T16: 200 | 3564 | 8717 (over) vs 8717 (over) |
| 0.75x | deepest_depth_capped | 32 | k32_T32: 200 | 5498 | 8717 (over) vs 8717 (over) |
| 1.00x | deepest_depth_capped | 32 | k32_T64: 200 | 7689 | 8717 (over) vs 8717 (over) |
- `avg_gated_equation_resolved` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) on family F2. Verification margin +23.3 points, sd 10.1, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 10.4% of the budget, 22.4% of the default cost. Mirror fold +11.4 points, sd 4.8 on 70 questions (clears).
- `avg_gated_equation_resolved` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) on family F2. Verification margin +6.7 points, sd 7.9, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 4.8% of the budget, 47.6% of the default cost. Mirror fold +4.3 points, sd 5.6 on 70 questions (clears).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) for every question. Verification margin -3.3 points, sd 9.1, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 10.5% of the budget, 67.1% of the default cost. Mirror fold +18.6 points, sd 6.1 on 70 questions (clears).
- `avg_gated_equation_resolved` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) for every question. Verification margin -3.3 points, sd 8.9, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 6.2% of the budget, 93.8% of the default cost. Mirror fold +4.3 points, sd 5.8 on 70 questions (clears).
- `avg_gated_lookup` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) on family F2. Verification margin +23.3 points, sd 10.1, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 10.4% of the budget, 22.4% of the default cost. Mirror fold +11.4 points, sd 4.8 on 70 questions (clears).
- `avg_gated_lookup` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) on family F2. Verification margin +6.7 points, sd 7.9, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 4.8% of the budget, 47.6% of the default cost. Mirror fold +4.3 points, sd 5.6 on 70 questions (clears).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) for every question. Verification margin -3.3 points, sd 9.1, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 10.5% of the budget, 67.1% of the default cost. Mirror fold +0.0 points, sd 0.0 on 70 questions (fails).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) for every question. Verification margin -3.3 points, sd 8.9, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 6.2% of the budget, 93.8% of the default cost. Mirror fold -14.3 points, sd 4.6 on 70 questions (fails).
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 39.5 points at 52.3% of the default cost, 30.2% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 39.5 points at 52.3% of the default cost, 47.7% under the budget it was given.
- `avg_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 39.5 points at 52.4% of the default cost, 30.2% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 39.5 points at 52.4% of the default cost, 47.6% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
