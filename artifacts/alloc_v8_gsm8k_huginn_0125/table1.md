# Table 1 -- gsm8k (huginn_0125), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 26216 layer passes over 1056 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 25.5 | +0.1 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 4.0 | 10.9 | 22.2 | 22.2 | +3.4 |
| lookup | 8.0 | 19.2 | 22.2 | 22.2 | +3.4 |
| equation | 9.7 | 19.2 | 22.2 | 22.2 | +3.4 |
| equation_n100 | 9.7 | 19.2 | 22.2 | 22.2 | +3.4 |
| equation_n30 | 8.0 | 10.9 | 22.2 | 22.2 | +3.4 |
| equation_resolved | 8.0 | 19.2 | 22.2 | 22.2 | +3.4 |
| gated_equation | 9.7 | 19.2 | 22.2 | 22.2 | +3.4 |
| gated_equation_resolved | 9.7 | 19.2 | 22.2 | 22.2 | +3.4 |
| avg_gated_equation_resolved | 4.0 | 19.2 | 22.2 | 22.2 | +3.4 |
| avg_gated_lookup | 4.0 | 19.2 | 22.2 | 22.2 | +3.4 |
| avg_lookup | 2.5 | 19.2 | 22.2 | 22.2 | +3.4 |
| avg_equation | 2.5 | 19.2 | 22.2 | 22.2 | +3.4 |
| avg_equation_resolved | 2.5 | 19.2 | 22.2 | 22.2 | +3.4 |

The ORACLE GAP is the best single evaluation cell (depth 32 at cap 256, 25.6 points over 1056 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2. Of the families that CLEAR the bar the one that RUNS is set by `policy.GATE_FAMILY_RULE` = `best`: the cleared family with the largest mean verified margin over the folds, ties to the smaller family. The folds, the bar, the reference and the pricing are the same test under either rule; only which cleared family is taken differs.

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 6336 vs 6554 (-3.3%) | 9792 vs 13108 (-25.3%) | 19008 vs 19662 (-3.3%) | 19008 vs 26216 (-27.5%) |
| avg_gated_lookup | 6336 vs 6554 (-3.3%) | 9792 vs 13108 (-25.3%) | 19008 vs 19662 (-3.3%) | 19008 vs 26216 (-27.5%) |
| avg_lookup | 576 vs 6554 (-91.2%) | 9792 vs 13108 (-25.3%) | 19008 vs 19662 (-3.3%) | 19008 vs 26216 (-27.5%) |
| avg_equation | 576 vs 6554 (-91.2%) | 9792 vs 13108 (-25.3%) | 19008 vs 19662 (-3.3%) | 19008 vs 26216 (-27.5%) |
| avg_equation_resolved | 576 vs 6554 (-91.2%) | 9792 vs 13108 (-25.3%) | 19008 vs 19662 (-3.3%) | 19008 vs 26216 (-27.5%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 32 | k32_T32: 1056 | 6336 | 542784 (over) vs 542784 (over) |
| 0.50x | deepest_depth_capped | 32 | k32_T64: 1056 | 10560 | 542784 (over) vs 542784 (over) |
| 0.75x | deepest_depth_capped | 32 | k32_T128: 1056 | 19008 | 542784 (over) vs 542784 (over) |
| 1.00x | deepest_depth_capped | 32 | k32_T128: 1056 | 19008 | 542784 (over) vs 542784 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 32 | k32_T32: 1056 | 6336 | 542784 (over) vs 542784 (over) |
| 0.50x | deepest_depth_capped | 32 | k32_T64: 1056 | 10560 | 542784 (over) vs 542784 (over) |
| 0.75x | deepest_depth_capped | 32 | k32_T128: 1056 | 19008 | 542784 (over) vs 542784 (over) |
| 1.00x | deepest_depth_capped | 32 | k32_T128: 1056 | 19008 | 542784 (over) vs 542784 (over) |
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) for every question. Verification margin -1.3 points, sd 2.2, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 3.3% of the budget, 24.2% of the default cost. Mirror fold +3.3 points, sd 2.5 on 184 questions (clears).
- `avg_gated_equation_resolved` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) on family F2. Verification margin +12.7 points, sd 4.1, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 25.3% of the budget, 37.4% of the default cost. Mirror fold +9.2 points, sd 3.1 on 184 questions (clears).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 3.3% of the budget, 72.5% of the default cost. Mirror fold -4.3 points, sd 3.2 on 184 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 27.5% of the budget, 72.5% of the default cost. Mirror fold -4.3 points, sd 3.2 on 184 questions (fails).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) for every question. Verification margin -1.3 points, sd 2.2, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 3.3% of the budget, 24.2% of the default cost. Mirror fold +3.3 points, sd 2.5 on 184 questions (clears).
- `avg_gated_lookup` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) on family F2. Verification margin +12.7 points, sd 4.1, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 25.3% of the budget, 37.4% of the default cost. Mirror fold +9.2 points, sd 3.1 on 184 questions (clears).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 3.3% of the budget, 72.5% of the default cost. Mirror fold -4.3 points, sd 3.2 on 184 questions (fails).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 27.5% of the budget, 72.5% of the default cost. Mirror fold -4.3 points, sd 3.2 on 184 questions (fails).

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
