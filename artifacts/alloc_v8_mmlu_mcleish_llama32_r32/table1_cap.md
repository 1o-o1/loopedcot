# Table 1 -- mmlu (mcleish_llama32_r32), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 16072 layer passes over 1700 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 37.4 | +1.1 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 35.1 | 37.7 | 37.7 | 37.7 | +0.8 |
| lookup | 36.6 | 36.7 | 36.7 | 36.7 | +1.8 |
| equation | 36.6 | 36.7 | 36.5 | 36.5 | +1.9 |
| equation_n100 | 36.6 | 36.7 | 36.5 | 36.5 | +1.9 |
| equation_n30 | 36.6 | 36.7 | 36.5 | 36.5 | +1.9 |
| equation_resolved | 36.6 | 36.7 | 36.7 | 36.7 | +1.8 |
| gated_equation | 38.5 | 36.7 | 36.5 | 36.5 | +1.9 |
| gated_equation_resolved | 38.5 | 36.7 | 36.7 | 36.7 | +1.8 |
| avg_gated_equation_resolved | 38.5 | 36.7 | 36.7 | 36.7 | +1.8 |
| avg_gated_lookup | 38.5 | 36.7 | 36.7 | 36.7 | +1.8 |
| avg_lookup | 38.5 | 36.7 | 36.7 | 36.7 | +1.8 |
| avg_equation | 36.6 | 36.7 | 36.5 | 36.5 | +1.9 |
| avg_equation_resolved | 38.5 | 36.7 | 36.7 | 36.7 | +1.8 |

The ORACLE GAP is the best single evaluation cell (depth 8 at cap 0, 38.5 points over 1700 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0, F2. Of the families that CLEAR the bar the one that RUNS is set by `policy.GATE_FAMILY_RULE` = `best`: the cleared family with the largest mean verified margin over the folds, ties to the smaller family. The folds, the bar, the reference and the pricing are the same test under either rule; only which cleared family is taken differs.

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 728 vs 4018 (-81.9%) | 4512 vs 8036 (-43.9%) | 4512 vs 12054 (-62.6%) | 4512 vs 16072 (-71.9%) |
| avg_gated_lookup | 728 vs 4018 (-81.9%) | 4512 vs 8036 (-43.9%) | 4512 vs 12054 (-62.6%) | 4512 vs 16072 (-71.9%) |
| avg_lookup | 728 vs 4018 (-81.9%) | 4512 vs 8036 (-43.9%) | 4512 vs 12054 (-62.6%) | 4512 vs 16072 (-71.9%) |
| avg_equation | 2464 vs 4018 (-38.7%) | 4512 vs 8036 (-43.9%) | 8608 vs 12054 (-28.6%) | 8608 vs 16072 (-46.4%) |
| avg_equation_resolved | 728 vs 4018 (-81.9%) | 4512 vs 8036 (-43.9%) | 4512 vs 12054 (-62.6%) | 4512 vs 16072 (-71.9%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 8 | k8_T32: 1700 | 2520 | 230104 (over) vs 230104 (over) |
| 0.50x | deepest_depth_capped | 8 | k8_T128: 1700 | 7896 | 230104 (over) vs 230104 (over) |
| 0.75x | deepest_depth_capped | 8 | k8_T128: 1700 | 7896 | 230104 (over) vs 230104 (over) |
| 1.00x | deepest_depth_capped | 8 | k8_T256: 1700 | 15064 | 230104 (over) vs 230104 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 8 | k8_T32: 1700 | 2520 | 230104 (over) vs 230104 (over) |
| 0.50x | deepest_depth_capped | 8 | k8_T128: 1700 | 7896 | 230104 (over) vs 230104 (over) |
| 0.75x | deepest_depth_capped | 8 | k8_T128: 1700 | 7896 | 230104 (over) vs 230104 (over) |
| 1.00x | deepest_depth_capped | 8 | k8_T256: 1700 | 15064 | 230104 (over) vs 230104 (over) |
- `avg_gated_equation_resolved` at 0.25x: the multiplier is 0, so the budget never binds. The row is the same 38.5 points at 4.5% of the default cost, 81.9% under the budget it was given.
- `avg_gated_equation_resolved` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 28.1% of the default cost, 43.9% under the budget it was given.
- `avg_gated_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 28.1% of the default cost, 62.6% under the budget it was given.
- `avg_gated_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 28.1% of the default cost, 71.9% under the budget it was given.
- `avg_gated_equation_resolved` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) on family F0. Verification margin +4.4 points, sd 5.3, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 81.9% of the budget, 4.5% of the default cost. Mirror fold +6.2 points, sd 3.4 on 210 questions (clears).
- `avg_gated_equation_resolved` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) on family F2. Verification margin +3.3 points, sd 5.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 43.9% of the budget, 28.1% of the default cost. Mirror fold +1.9 points, sd 3.5 on 210 questions (clears).
- `avg_gated_equation_resolved` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) on family F2. Verification margin +3.3 points, sd 5.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 62.6% of the budget, 28.1% of the default cost. Mirror fold +3.8 points, sd 3.5 on 210 questions (clears).
- `avg_gated_equation_resolved` at 1.00x: deviated from normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) on family F2. Verification margin +3.3 points, sd 5.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 71.9% of the budget, 28.1% of the default cost. Mirror fold +4.3 points, sd 3.4 on 210 questions (clears).
- `avg_gated_lookup` at 0.25x: the multiplier is 0, so the budget never binds. The row is the same 38.5 points at 4.5% of the default cost, 81.9% under the budget it was given.
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 28.1% of the default cost, 43.9% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 28.1% of the default cost, 62.6% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 28.1% of the default cost, 71.9% under the budget it was given.
- `avg_gated_lookup` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) on family F0. Verification margin +4.4 points, sd 5.3, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 81.9% of the budget, 4.5% of the default cost. Mirror fold +6.2 points, sd 3.4 on 210 questions (clears).
- `avg_gated_lookup` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) on family F2. Verification margin +3.3 points, sd 5.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 43.9% of the budget, 28.1% of the default cost. Mirror fold +1.9 points, sd 3.5 on 210 questions (clears).
- `avg_gated_lookup` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) on family F2. Verification margin +3.3 points, sd 5.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 62.6% of the budget, 28.1% of the default cost. Mirror fold +3.8 points, sd 3.5 on 210 questions (clears).
- `avg_gated_lookup` at 1.00x: deviated from normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) on family F2. Verification margin +3.3 points, sd 5.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 71.9% of the budget, 28.1% of the default cost. Mirror fold +4.3 points, sd 3.4 on 210 questions (clears).
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 28.1% of the default cost, 43.9% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 28.1% of the default cost, 62.6% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 28.1% of the default cost, 71.9% under the budget it was given.
- `avg_equation_resolved` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 28.1% of the default cost, 43.9% under the budget it was given.
- `avg_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 28.1% of the default cost, 62.6% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 28.1% of the default cost, 71.9% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
