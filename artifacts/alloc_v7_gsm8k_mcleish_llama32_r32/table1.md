# Table 1 -- gsm8k (mcleish_llama32_r32), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 33171 layer passes over 1056 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 48.9 | +0.6 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 4.8 | 31.9 | 31.9 | 47.6 | +1.8 |
| lookup | 48.0 | 49.4 | 49.4 | 49.4 | +0.0 |
| equation | 48.0 | 49.4 | 49.4 | 49.4 | +0.0 |
| equation_n100 | 48.0 | 47.9 | 47.9 | 48.9 | +0.6 |
| equation_n30 | 48.0 | 47.9 | 47.9 | 48.9 | +0.6 |
| equation_resolved | 48.0 | 49.4 | 49.4 | 49.4 | +0.0 |
| gated_equation | 5.4 | 47.9 | 47.9 | 49.4 | +0.0 |
| gated_equation_resolved | 5.4 | 47.9 | 47.9 | 49.4 | +0.0 |
| avg_gated_equation_resolved | 5.4 | 47.9 | 47.9 | 47.6 | +1.8 |
| avg_gated_lookup | 5.4 | 47.9 | 47.9 | 47.6 | +1.8 |
| avg_lookup | 48.0 | 49.4 | 49.4 | 49.4 | +0.0 |
| avg_equation | 48.0 | 49.4 | 49.4 | 49.4 | +0.0 |
| avg_equation_resolved | 48.0 | 49.4 | 49.4 | 49.4 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 8 at cap 256, 49.4 points over 1056 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0, F2, F3.

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 3200 vs 8293 (-61.4%) | 14976 vs 16585 (-9.7%) | 14976 vs 24878 (-39.8%) | 28800 vs 33171 (-13.2%) |
| avg_gated_lookup | 3200 vs 8293 (-61.4%) | 14976 vs 16585 (-9.7%) | 14976 vs 24878 (-39.8%) | 28800 vs 33171 (-13.2%) |
| avg_lookup | 8064 vs 8293 (-2.8%) | 15232 vs 16585 (-8.2%) | 15232 vs 24878 (-38.8%) | 15232 vs 33171 (-54.1%) |
| avg_equation | 8064 vs 8293 (-2.8%) | 15232 vs 16585 (-8.2%) | 15232 vs 24878 (-38.8%) | 15232 vs 33171 (-54.1%) |
| avg_equation_resolved | 8064 vs 8293 (-2.8%) | 15232 vs 16585 (-8.2%) | 15232 vs 24878 (-38.8%) | 15232 vs 33171 (-54.1%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 32 | k32_T16: 1056 | 6400 | 822400 (over) vs 822400 (over) |
| 0.50x | deepest_depth_capped | 32 | k32_T64: 1056 | 16000 | 822400 (over) vs 822400 (over) |
| 0.75x | deepest_depth_capped | 32 | k32_T64: 1056 | 16000 | 822400 (over) vs 822400 (over) |
| 1.00x | deepest_depth_capped | 32 | k32_T128: 1056 | 28800 | 822400 (over) vs 822400 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 32 | k32_T16: 1056 | 6400 | 822400 (over) vs 822400 (over) |
| 0.50x | deepest_depth_capped | 32 | k32_T64: 1056 | 16000 | 822400 (over) vs 822400 (over) |
| 0.75x | deepest_depth_capped | 32 | k32_T64: 1056 | 16000 | 822400 (over) vs 822400 (over) |
| 1.00x | deepest_depth_capped | 32 | k32_T128: 1056 | 28800 | 822400 (over) vs 822400 (over) |
- `avg_gated_equation_resolved` at 0.25x: the multiplier is 0, so the budget never binds. The row is the same 5.4 points at 9.6% of the default cost, 61.4% under the budget it was given.
- `avg_gated_equation_resolved` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) on family F0. Verification margin +1.3 points, sd 2.2, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 61.4% of the budget, 9.6% of the default cost. Mirror fold +3.8 points, sd 2.2 on 184 questions (clears).
- `avg_gated_equation_resolved` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) on family F2. Verification margin +16.5 points, sd 4.6, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 9.7% of the budget, 45.1% of the default cost. Mirror fold +16.3 points, sd 3.1 on 184 questions (clears).
- `avg_gated_equation_resolved` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) on family F2. Verification margin +16.5 points, sd 4.6, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 39.8% of the budget, 45.1% of the default cost. Mirror fold +16.3 points, sd 3.1 on 184 questions (clears).
- `avg_gated_equation_resolved` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) for every question. Verification margin +3.8 points, sd 3.8, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 13.2% of the budget, 86.8% of the default cost. Mirror fold +0.5 points, sd 1.7 on 184 questions (fails).
- `avg_gated_lookup` at 0.25x: the multiplier is 0, so the budget never binds. The row is the same 5.4 points at 9.6% of the default cost, 61.4% under the budget it was given.
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 47.9 points at 45.1% of the default cost, 9.7% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 47.9 points at 45.1% of the default cost, 39.8% under the budget it was given.
- `avg_gated_lookup` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) on family F0. Verification margin +1.3 points, sd 2.2, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 61.4% of the budget, 9.6% of the default cost. Mirror fold +3.8 points, sd 2.2 on 184 questions (clears).
- `avg_gated_lookup` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) on family F2. Verification margin +16.5 points, sd 4.6, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 9.7% of the budget, 45.1% of the default cost. Mirror fold +16.3 points, sd 3.1 on 184 questions (clears).
- `avg_gated_lookup` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) on family F2. Verification margin +16.5 points, sd 4.6, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 39.8% of the budget, 45.1% of the default cost. Mirror fold +16.3 points, sd 3.1 on 184 questions (clears).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap whose mean price fits it) for every question. Verification margin +3.8 points, sd 3.8, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 13.2% of the budget, 86.8% of the default cost. Mirror fold +0.5 points, sd 1.7 on 184 questions (fails).

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
