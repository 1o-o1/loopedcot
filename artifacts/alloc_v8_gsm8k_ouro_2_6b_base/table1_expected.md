# Table 1 -- gsm8k (ouro_2_6b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 28142 layer passes over 1056 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 82.8 | +0.0 |
| default_cell | n/a | n/a | n/a | 82.8 | +0.0 |
| default_at_budget | 16.6 | 25.9 | 46.2 | 82.8 | +0.0 |
| lookup | 31.0 | 75.0 | 78.7 | 82.8 | +0.0 |
| equation | 31.0 | 75.0 | 78.7 | 82.8 | +0.0 |
| equation_n100 | 31.0 | 75.0 | 78.7 | 82.8 | +0.0 |
| equation_n30 | 31.0 | 75.0 | 75.0 | 82.8 | +0.0 |
| equation_resolved | 31.0 | 75.0 | 78.7 | 82.8 | +0.0 |
| gated_equation | 31.0 | 41.9 | 78.7 | 82.8 | +0.0 |
| gated_equation_resolved | 21.6 | 41.9 | 78.7 | 82.8 | +0.0 |
| avg_gated_equation_resolved | 21.6 | 75.0 | 78.7 | 82.8 | +0.0 |
| avg_gated_lookup | 21.6 | 74.1 | 78.7 | 82.8 | +0.0 |
| avg_lookup | 21.6 | 75.0 | 78.7 | 82.8 | +0.0 |
| avg_equation | 1.1 | 75.0 | 78.7 | 82.8 | +0.0 |
| avg_equation_resolved | 21.6 | 75.0 | 78.7 | 82.8 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 512, 82.8 points over 1056 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3. Of the families that CLEAR the bar the one that RUNS is set by `policy.GATE_FAMILY_RULE` = `best`: the cleared family with the largest mean verified margin over the folds, ties to the smaller family. The folds, the bar, the reference and the pricing are the same test under either rule; only which cleared family is taken differs.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 2304 vs 7036 (-67.3%) | 12199 vs 14071 (-13.3%) | 18500 vs 21107 (-12.4%) | 27639 vs 28142 (-1.8%) |
| avg_gated_lookup | 2304 vs 7036 (-67.3%) | 12066 vs 14071 (-14.3%) | 18500 vs 21107 (-12.4%) | 27639 vs 28142 (-1.8%) |
| avg_lookup | 2304 vs 7036 (-67.3%) | 12199 vs 14071 (-13.3%) | 18500 vs 21107 (-12.4%) | 25396 vs 28142 (-9.8%) |
| avg_equation | 768 vs 7036 (-89.1%) | 12199 vs 14071 (-13.3%) | 18500 vs 21107 (-12.4%) | 25396 vs 28142 (-9.8%) |
| avg_equation_resolved | 2304 vs 7036 (-67.3%) | 12199 vs 14071 (-13.3%) | 18500 vs 21107 (-12.4%) | 25396 vs 28142 (-9.8%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T16: 1056 | 6144 | 27639 (over) vs 27639 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T32: 1056 | 9215 | 27639 (over) vs 27639 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T64: 1056 | 15058 | 27639 (over) vs 27639 (over) |
| 1.00x | default_cell | 4 | k4_T4096: 1056 | 27639 | 27639 (fits) vs 27639 (fits) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T16: 1056 | 6144 | 27639 (over) vs 27639 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T32: 1056 | 9215 | 27639 (over) vs 27639 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T64: 1056 | 15058 | 27639 (over) vs 27639 (over) |
| 1.00x | default_cell | 4 | k4_T4096: 1056 | 27639 | 27639 (fits) vs 27639 (fits) |
- `avg_gated_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 78.7 points at 65.7% of the default cost, 12.4% under the budget it was given.
- `avg_gated_equation_resolved` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +2.5 points, sd 3.2, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 67.3% of the budget, 8.2% of the default cost. Mirror fold +9.2 points, sd 2.7 on 184 questions (clears).
- `avg_gated_equation_resolved` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F3. Verification margin +45.6 points, sd 5.9, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 13.3% of the budget, 43.3% of the default cost. Mirror fold +47.8 points, sd 4.1 on 184 questions (clears).
- `avg_gated_equation_resolved` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +32.9 points, sd 6.3, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 12.4% of the budget, 65.7% of the default cost. Mirror fold +32.1 points, sd 3.8 on 184 questions (clears).
- `avg_gated_equation_resolved` at 1.00x: reverted to the default cell for every question. Verification margin -1.3 points, sd 1.2, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 1.8% of the budget, 98.2% of the default cost. Mirror fold +0.0 points, sd 0.0 on 184 questions (fails).
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 78.7 points at 65.7% of the default cost, 12.4% under the budget it was given.
- `avg_gated_lookup` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +2.5 points, sd 3.2, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 67.3% of the budget, 8.2% of the default cost. Mirror fold +9.2 points, sd 2.7 on 184 questions (clears).
- `avg_gated_lookup` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F3. Verification margin +44.3 points, sd 6.0, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 14.3% of the budget, 42.9% of the default cost. Mirror fold +47.8 points, sd 4.1 on 184 questions (clears).
- `avg_gated_lookup` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +32.9 points, sd 6.3, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 12.4% of the budget, 65.7% of the default cost. Mirror fold +32.1 points, sd 3.8 on 184 questions (clears).
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin -1.3 points, sd 1.2, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 1.8% of the budget, 98.2% of the default cost. Mirror fold +0.0 points, sd 0.0 on 184 questions (fails).
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 82.8 points at 90.2% of the default cost, 9.8% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 82.8 points at 90.2% of the default cost, 9.8% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 82.8 points at 90.2% of the default cost, 9.8% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
