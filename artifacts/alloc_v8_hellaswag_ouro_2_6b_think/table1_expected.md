# Table 1 -- hellaswag (ouro_2_6b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 132866 layer passes over 1700 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 81.2 | +0.9 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 80.2 | 81.2 | 81.5 | 81.2 | +0.9 |
| lookup | 80.4 | 81.2 | 81.2 | 81.2 | +0.8 |
| equation | 80.2 | 79.5 | 78.9 | 78.9 | +3.1 |
| equation_n100 | 80.2 | 73.9 | 73.9 | 81.2 | +0.9 |
| equation_n30 | 79.6 | 73.9 | 73.9 | 81.2 | +0.9 |
| equation_resolved | 80.4 | 81.2 | 81.2 | 81.2 | +0.8 |
| gated_equation | 80.2 | 81.2 | 81.5 | 81.2 | +0.9 |
| gated_equation_resolved | 80.2 | 81.2 | 81.2 | 81.2 | +0.8 |
| avg_gated_equation_resolved | 80.2 | 81.2 | 81.2 | 81.2 | +0.8 |
| avg_gated_lookup | 80.2 | 81.2 | 81.5 | 81.2 | +0.9 |
| avg_lookup | 80.4 | 81.2 | 81.2 | 81.2 | +0.8 |
| avg_equation | 81.8 | 81.8 | 78.9 | 78.9 | +3.1 |
| avg_equation_resolved | 80.4 | 81.2 | 81.2 | 81.2 | +0.8 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 64, 82.1 points over 1700 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F1. Of the families that CLEAR the bar the one that RUNS is set by `policy.GATE_FAMILY_RULE` = `best`: the cleared family with the largest mean verified margin over the folds, ties to the smaller family. The folds, the bar, the reference and the pricing are the same test under either rule; only which cleared family is taken differs.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 27264 vs 33216 (-17.9%) | 51804 vs 66433 (-22.0%) | 51804 vs 99649 (-48.0%) | 51804 vs 132866 (-61.0%) |
| avg_gated_lookup | 27264 vs 33216 (-17.9%) | 51804 vs 66433 (-22.0%) | 85094 vs 99649 (-14.6%) | 114913 vs 132866 (-13.5%) |
| avg_lookup | 6624 vs 33216 (-80.1%) | 51804 vs 66433 (-22.0%) | 51804 vs 99649 (-48.0%) | 51804 vs 132866 (-61.0%) |
| avg_equation | 5760 vs 33216 (-82.7%) | 5760 vs 66433 (-91.3%) | 85196 vs 99649 (-14.5%) | 85196 vs 132866 (-35.9%) |
| avg_equation_resolved | 6624 vs 33216 (-80.1%) | 51804 vs 66433 (-22.0%) | 51804 vs 99649 (-48.0%) | 51804 vs 132866 (-61.0%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 1700 | 27264 | 133776 (over) vs 133776 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T256: 1700 | 51804 | 133776 (over) vs 133776 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T512: 1700 | 85094 | 133776 (over) vs 133776 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T2048: 1700 | 114913 | 133776 (over) vs 133776 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 1700 | 27264 | 133776 (over) vs 133776 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T256: 1700 | 51804 | 133776 (over) vs 133776 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T512: 1700 | 85094 | 133776 (over) vs 133776 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T2048: 1700 | 114913 | 133776 (over) vs 133776 (over) |
- `avg_gated_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 81.2 points at 39.0% of the default cost, 48.0% under the budget it was given.
- `avg_gated_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 81.2 points at 39.0% of the default cost, 61.0% under the budget it was given.
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -2.2 points, sd 2.2, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 17.9% of the budget, 20.5% of the default cost. Mirror fold +2.4 points, sd 1.4 on 210 questions (clears).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 22.0% of the budget, 39.0% of the default cost. Mirror fold +0.0 points, sd 1.6 on 210 questions (fails).
- `avg_gated_equation_resolved` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F1. Verification margin +4.4 points, sd 2.7, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 48.0% of the budget, 39.0% of the default cost. Mirror fold +1.0 points, sd 1.7 on 210 questions (clears).
- `avg_gated_equation_resolved` at 1.00x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F1. Verification margin +2.2 points, sd 2.8, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 61.0% of the budget, 39.0% of the default cost. Mirror fold +1.4 points, sd 1.6 on 210 questions (clears).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -2.2 points, sd 2.2, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 17.9% of the budget, 20.5% of the default cost. Mirror fold +1.9 points, sd 1.3 on 210 questions (clears).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -5.6 points, sd 3.2, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 22.0% of the budget, 39.0% of the default cost. Mirror fold +0.0 points, sd 0.0 on 210 questions (fails).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -1.1 points, sd 3.4, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 14.6% of the budget, 64.0% of the default cost. Mirror fold +1.0 points, sd 1.7 on 210 questions (clears).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -3.3 points, sd 3.7, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 13.5% of the budget, 86.5% of the default cost. Mirror fold +1.4 points, sd 1.6 on 210 questions (clears).
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 81.2 points at 39.0% of the default cost, 22.0% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 81.2 points at 39.0% of the default cost, 48.0% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 81.2 points at 39.0% of the default cost, 61.0% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 78.9 points at 64.1% of the default cost, 14.5% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 78.9 points at 64.1% of the default cost, 35.9% under the budget it was given.
- `avg_equation_resolved` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 81.2 points at 39.0% of the default cost, 22.0% under the budget it was given.
- `avg_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 81.2 points at 39.0% of the default cost, 48.0% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 81.2 points at 39.0% of the default cost, 61.0% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
