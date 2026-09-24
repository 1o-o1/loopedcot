# Table 1 -- mmlu (huginn_0125), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 22796 layer passes over 1700 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 36.3 | +3.1 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 36.2 | 36.8 | 36.8 | 36.5 | +2.9 |
| lookup | 35.5 | 35.5 | 35.5 | 35.5 | +3.9 |
| equation | 36.2 | 35.5 | 35.3 | 35.3 | +4.1 |
| equation_n100 | 36.2 | 35.5 | 35.3 | 35.3 | +4.1 |
| equation_n30 | 36.2 | 35.5 | 35.3 | 35.3 | +4.1 |
| equation_resolved | 35.5 | 35.5 | 35.5 | 35.5 | +3.9 |
| gated_equation | 36.2 | 36.8 | 36.8 | 36.5 | +2.9 |
| gated_equation_resolved | 35.5 | 36.8 | 36.8 | 36.5 | +2.9 |
| avg_gated_equation_resolved | 35.5 | 36.8 | 36.8 | 36.5 | +2.9 |
| avg_gated_lookup | 35.5 | 36.8 | 36.8 | 36.5 | +2.9 |
| avg_lookup | 35.5 | 35.5 | 35.5 | 35.5 | +3.9 |
| avg_equation | 36.2 | 36.2 | 35.3 | 35.3 | +4.1 |
| avg_equation_resolved | 35.5 | 35.5 | 35.5 | 35.5 | +3.9 |

The ORACLE GAP is the best single evaluation cell (depth 16 at cap 0, 39.4 points over 1700 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2. Of the families that CLEAR the bar the one that RUNS is set by `policy.GATE_FAMILY_RULE` = `best`: the cleared family with the largest mean verified margin over the folds, ties to the smaller family. The folds, the bar, the reference and the pricing are the same test under either rule; only which cleared family is taken differs.

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 3720 vs 5699 (-34.7%) | 10912 vs 11398 (-4.3%) | 14292 vs 17097 (-16.4%) | 21050 vs 22796 (-7.7%) |
| avg_gated_lookup | 3720 vs 5699 (-34.7%) | 10912 vs 11398 (-4.3%) | 14292 vs 17097 (-16.4%) | 21050 vs 22796 (-7.7%) |
| avg_lookup | 3720 vs 5699 (-34.7%) | 3720 vs 11398 (-67.4%) | 3720 vs 17097 (-78.2%) | 3720 vs 22796 (-83.7%) |
| avg_equation | 5441 vs 5699 (-4.5%) | 5441 vs 11398 (-52.3%) | 13184 vs 17097 (-22.9%) | 13184 vs 22796 (-42.2%) |
| avg_equation_resolved | 3720 vs 5699 (-34.7%) | 3720 vs 11398 (-67.4%) | 3720 vs 17097 (-78.2%) | 3720 vs 22796 (-83.7%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 32 | k32_T32: 1700 | 5687 | 27016 (over) vs 27016 (over) |
| 0.50x | deepest_depth_capped | 32 | k32_T512: 1700 | 10912 | 27016 (over) vs 27016 (over) |
| 0.75x | deepest_depth_capped | 32 | k32_T1024: 1700 | 14292 | 27016 (over) vs 27016 (over) |
| 1.00x | deepest_depth_capped | 32 | k32_T2048: 1700 | 21050 | 27016 (over) vs 27016 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 32 | k32_T32: 1700 | 5687 | 27016 (over) vs 27016 (over) |
| 0.50x | deepest_depth_capped | 32 | k32_T512: 1700 | 10912 | 27016 (over) vs 27016 (over) |
| 0.75x | deepest_depth_capped | 32 | k32_T1024: 1700 | 14292 | 27016 (over) vs 27016 (over) |
| 1.00x | deepest_depth_capped | 32 | k32_T2048: 1700 | 21050 | 27016 (over) vs 27016 (over) |
- `avg_gated_equation_resolved` at 0.25x: the multiplier is 0, so the budget never binds. The row is the same 35.5 points at 16.3% of the default cost, 34.7% under the budget it was given.
- `avg_gated_equation_resolved` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) on family F2. Verification margin +3.3 points, sd 4.3, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 34.7% of the budget, 16.3% of the default cost. Mirror fold +2.4 points, sd 3.2 on 210 questions (clears).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) for every question. Verification margin -1.1 points, sd 4.2, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 4.3% of the budget, 47.9% of the default cost. Mirror fold +0.5 points, sd 3.7 on 210 questions (fails).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) for every question. Verification margin -1.1 points, sd 4.5, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 16.4% of the budget, 62.7% of the default cost. Mirror fold +1.0 points, sd 3.7 on 210 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) for every question. Verification margin -1.1 points, sd 4.5, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 7.7% of the budget, 92.3% of the default cost. Mirror fold +1.9 points, sd 3.8 on 210 questions (clears).
- `avg_gated_lookup` at 0.25x: the multiplier is 0, so the budget never binds. The row is the same 35.5 points at 16.3% of the default cost, 34.7% under the budget it was given.
- `avg_gated_lookup` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) on family F2. Verification margin +3.3 points, sd 4.3, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 34.7% of the budget, 16.3% of the default cost. Mirror fold +2.4 points, sd 3.2 on 210 questions (clears).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) for every question. Verification margin -1.1 points, sd 4.2, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 4.3% of the budget, 47.9% of the default cost. Mirror fold +0.5 points, sd 3.7 on 210 questions (fails).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) for every question. Verification margin -1.1 points, sd 4.5, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 16.4% of the budget, 62.7% of the default cost. Mirror fold +1.0 points, sd 3.7 on 210 questions (fails).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) for every question. Verification margin -1.1 points, sd 4.5, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 7.7% of the budget, 92.3% of the default cost. Mirror fold +1.9 points, sd 3.8 on 210 questions (clears).
- `avg_lookup` at 0.25x: the multiplier is 0, so the budget never binds. The row is the same 35.5 points at 16.3% of the default cost, 34.7% under the budget it was given.
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 35.5 points at 16.3% of the default cost, 67.4% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 35.5 points at 16.3% of the default cost, 78.2% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 35.5 points at 16.3% of the default cost, 83.7% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 35.3 points at 57.8% of the default cost, 22.9% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 35.3 points at 57.8% of the default cost, 42.2% under the budget it was given.
- `avg_equation_resolved` at 0.25x: the multiplier is 0, so the budget never binds. The row is the same 35.5 points at 16.3% of the default cost, 34.7% under the budget it was given.
- `avg_equation_resolved` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 35.5 points at 16.3% of the default cost, 67.4% under the budget it was given.
- `avg_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 35.5 points at 16.3% of the default cost, 78.2% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 35.5 points at 16.3% of the default cost, 83.7% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
