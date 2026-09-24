# Table 1 -- aqua (huginn_0125), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 69861 layer passes over 154 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 24.7 | +3.2 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 23.4 | 23.4 | 23.4 | 23.4 | +4.5 |
| lookup | 23.4 | 24.7 | 24.7 | 24.7 | +3.2 |
| equation | 25.3 | 24.7 | 20.8 | 20.8 | +7.1 |
| equation_n100 | 25.3 | 24.7 | 20.8 | 20.8 | +7.1 |
| equation_n30 | 25.3 | 24.7 | 20.8 | 20.8 | +7.1 |
| equation_resolved | 23.4 | 24.7 | 20.8 | 20.8 | +7.1 |
| gated_equation | 23.4 | 23.4 | 23.4 | 23.4 | +4.5 |
| gated_equation_resolved | 23.4 | 23.4 | 23.4 | 23.4 | +4.5 |
| avg_gated_equation_resolved | 23.4 | 23.4 | 23.4 | 23.4 | +4.5 |
| avg_gated_lookup | 23.4 | 23.4 | 23.4 | 23.4 | +4.5 |
| avg_lookup | 23.4 | 24.7 | 24.7 | 24.7 | +3.2 |
| avg_equation | 25.3 | 25.3 | 20.8 | 20.8 | +7.1 |
| avg_equation_resolved | 23.4 | 24.7 | 24.7 | 24.7 | +3.2 |

The ORACLE GAP is the best single evaluation cell (depth 2 at cap 0, 27.9 points over 154 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none. Of the families that CLEAR the bar the one that RUNS is set by `policy.GATE_FAMILY_RULE` = `best`: the cleared family with the largest mean verified margin over the folds, ties to the smaller family. The folds, the bar, the reference and the pricing are the same test under either rule; only which cleared family is taken differs.

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 15626 vs 17465 (-10.5%) | 32040 vs 34930 (-8.3%) | 32040 vs 52395 (-38.8%) | 53667 vs 69861 (-23.2%) |
| avg_gated_lookup | 15626 vs 17465 (-10.5%) | 32040 vs 34930 (-8.3%) | 32040 vs 52395 (-38.8%) | 53667 vs 69861 (-23.2%) |
| avg_lookup | 849 vs 17465 (-95.1%) | 24332 vs 34930 (-30.3%) | 24332 vs 52395 (-53.6%) | 24332 vs 69861 (-65.2%) |
| avg_equation | 12454 vs 17465 (-28.7%) | 12454 vs 34930 (-64.3%) | 40735 vs 52395 (-22.3%) | 40735 vs 69861 (-41.7%) |
| avg_equation_resolved | 849 vs 17465 (-95.1%) | 24332 vs 34930 (-30.3%) | 24332 vs 52395 (-53.6%) | 24332 vs 69861 (-65.2%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 32 | k32_T256: 154 | 15626 | 83531 (over) vs 83531 (over) |
| 0.50x | deepest_depth_capped | 32 | k32_T1024: 154 | 32040 | 83531 (over) vs 83531 (over) |
| 0.75x | deepest_depth_capped | 32 | k32_T1024: 154 | 32040 | 83531 (over) vs 83531 (over) |
| 1.00x | deepest_depth_capped | 32 | k32_T2048: 154 | 53667 | 83531 (over) vs 83531 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 32 | k32_T256: 154 | 15626 | 83531 (over) vs 83531 (over) |
| 0.50x | deepest_depth_capped | 32 | k32_T1024: 154 | 32040 | 83531 (over) vs 83531 (over) |
| 0.75x | deepest_depth_capped | 32 | k32_T1024: 154 | 32040 | 83531 (over) vs 83531 (over) |
| 1.00x | deepest_depth_capped | 32 | k32_T2048: 154 | 53667 | 83531 (over) vs 83531 (over) |
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) for every question. Verification margin -23.3 points, sd 12.1, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 10.5% of the budget, 22.4% of the default cost. Mirror fold -2.9 points, sd 5.4 on 70 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) for every question. Verification margin -23.3 points, sd 12.1, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 8.3% of the budget, 45.9% of the default cost. Mirror fold -2.9 points, sd 5.4 on 70 questions (fails).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) for every question. Verification margin -23.3 points, sd 12.1, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 38.8% of the budget, 45.9% of the default cost. Mirror fold -2.9 points, sd 5.4 on 70 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) for every question. Verification margin -26.7 points, sd 11.5, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 23.2% of the budget, 76.8% of the default cost. Mirror fold -4.3 points, sd 5.5 on 70 questions (fails).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) for every question. Verification margin -23.3 points, sd 12.1, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 10.5% of the budget, 22.4% of the default cost. Mirror fold +0.0 points, sd 0.0 on 70 questions (fails).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) for every question. Verification margin -23.3 points, sd 12.1, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 8.3% of the budget, 45.9% of the default cost. Mirror fold +0.0 points, sd 0.0 on 70 questions (fails).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) for every question. Verification margin -23.3 points, sd 12.1, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 38.8% of the budget, 45.9% of the default cost. Mirror fold +0.0 points, sd 0.0 on 70 questions (fails).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) for every question. Verification margin -26.7 points, sd 11.5, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 23.2% of the budget, 76.8% of the default cost. Mirror fold +0.0 points, sd 0.0 on 70 questions (fails).
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 24.7 points at 34.8% of the default cost, 30.3% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 24.7 points at 34.8% of the default cost, 53.6% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 24.7 points at 34.8% of the default cost, 65.2% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 20.8 points at 58.3% of the default cost, 22.3% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 20.8 points at 58.3% of the default cost, 41.7% under the budget it was given.
- `avg_equation_resolved` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 24.7 points at 34.8% of the default cost, 30.3% under the budget it was given.
- `avg_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 24.7 points at 34.8% of the default cost, 53.6% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 24.7 points at 34.8% of the default cost, 65.2% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
