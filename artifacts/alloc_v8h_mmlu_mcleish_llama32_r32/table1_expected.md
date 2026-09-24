# Table 1 -- mmlu (mcleish_llama32_r32), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 29160 layer passes over 1700 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 37.2 | +1.2 |
| default_cell | n/a | n/a | n/a | 37.2 | +1.2 |
| default_at_budget | 37.2 | 37.4 | 37.4 | 37.2 | +1.2 |
| lookup | 36.7 | 36.7 | 36.7 | 36.7 | +1.8 |
| equation | 36.8 | 36.4 | 35.8 | 35.8 | +2.6 |
| equation_n100 | 36.8 | 36.4 | 35.8 | 35.8 | +2.6 |
| equation_n30 | 36.8 | 36.4 | 35.8 | 35.8 | +2.6 |
| equation_resolved | 36.7 | 36.7 | 36.7 | 36.7 | +1.8 |
| gated_equation | 36.8 | 36.4 | 35.8 | 35.8 | +2.6 |
| gated_equation_resolved | 37.2 | 36.7 | 36.7 | 36.7 | +1.8 |
| avg_gated_equation_resolved | 37.2 | 36.7 | 36.7 | 36.7 | +1.8 |
| avg_gated_lookup | 37.2 | 36.7 | 36.7 | 36.7 | +1.8 |
| avg_lookup | 36.7 | 36.7 | 36.7 | 36.7 | +1.8 |
| avg_equation | 36.2 | 36.4 | 35.8 | 35.8 | +2.6 |
| avg_equation_resolved | 36.7 | 36.7 | 36.7 | 36.7 | +1.8 |

The ORACLE GAP is the best single evaluation cell (depth 8 at cap 0, 38.5 points over 1700 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2. Of the families that CLEAR the bar the one that RUNS is set by `policy.GATE_FAMILY_RULE` = `best`: the cleared family with the largest mean verified margin over the folds, ties to the smaller family. The folds, the bar, the reference and the pricing are the same test under either rule; only which cleared family is taken differs.

`default_cell` is the default operating point (depth 8 at cap 8192) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 5663 vs 7290 (-22.3%) | 1896 vs 14580 (-87.0%) | 1896 vs 21870 (-91.3%) | 1896 vs 29160 (-93.5%) |
| avg_gated_lookup | 5663 vs 7290 (-22.3%) | 1896 vs 14580 (-87.0%) | 1896 vs 21870 (-91.3%) | 1896 vs 29160 (-93.5%) |
| avg_lookup | 1896 vs 7290 (-74.0%) | 1896 vs 14580 (-87.0%) | 1896 vs 21870 (-91.3%) | 1896 vs 29160 (-93.5%) |
| avg_equation | 2648 vs 7290 (-63.7%) | 8786 vs 14580 (-39.7%) | 15777 vs 21870 (-27.9%) | 15777 vs 29160 (-45.9%) |
| avg_equation_resolved | 1896 vs 7290 (-74.0%) | 1896 vs 14580 (-87.0%) | 1896 vs 21870 (-91.3%) | 1896 vs 29160 (-93.5%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 8 | k8_T1024: 1700 | 5663 | 24396 (over) vs 24396 (over) |
| 0.50x | deepest_depth_capped | 8 | k8_T4096: 1700 | 13692 | 24396 (over) vs 24396 (over) |
| 0.75x | deepest_depth_capped | 8 | k8_T4096: 1700 | 13692 | 24396 (over) vs 24396 (over) |
| 1.00x | default_cell | 8 | k8_T8192: 1700 | 24396 | 24396 (fits) vs 24396 (fits) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 8 | k8_T1024: 1700 | 5663 | 24396 (over) vs 24396 (over) |
| 0.50x | deepest_depth_capped | 8 | k8_T4096: 1700 | 13692 | 24396 (over) vs 24396 (over) |
| 0.75x | deepest_depth_capped | 8 | k8_T4096: 1700 | 13692 | 24396 (over) vs 24396 (over) |
| 1.00x | default_cell | 8 | k8_T8192: 1700 | 24396 | 24396 (fits) vs 24396 (fits) |
- `avg_gated_equation_resolved` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 6.5% of the default cost, 87.0% under the budget it was given.
- `avg_gated_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 6.5% of the default cost, 91.3% under the budget it was given.
- `avg_gated_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 6.5% of the default cost, 93.5% under the budget it was given.
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +2.2 points, sd 5.3, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 22.3% of the budget, 19.4% of the default cost. Mirror fold +3.3 points, sd 3.2 on 210 questions (clears).
- `avg_gated_equation_resolved` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) on family F2. Verification margin +3.3 points, sd 5.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 87.0% of the budget, 6.5% of the default cost. Mirror fold +2.9 points, sd 3.3 on 210 questions (clears).
- `avg_gated_equation_resolved` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) on family F2. Verification margin +3.3 points, sd 5.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 91.3% of the budget, 6.5% of the default cost. Mirror fold +2.9 points, sd 3.3 on 210 questions (clears).
- `avg_gated_equation_resolved` at 1.00x: deviated from the default cell on family F2. Verification margin +3.3 points, sd 5.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 93.5% of the budget, 6.5% of the default cost. Mirror fold +1.9 points, sd 3.3 on 210 questions (clears).
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 6.5% of the default cost, 87.0% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 6.5% of the default cost, 91.3% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 6.5% of the default cost, 93.5% under the budget it was given.
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +2.2 points, sd 5.3, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 22.3% of the budget, 19.4% of the default cost. Mirror fold +4.8 points, sd 3.3 on 210 questions (clears).
- `avg_gated_lookup` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) on family F2. Verification margin +3.3 points, sd 5.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 87.0% of the budget, 6.5% of the default cost. Mirror fold +4.3 points, sd 3.4 on 210 questions (clears).
- `avg_gated_lookup` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) on family F2. Verification margin +3.3 points, sd 5.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 91.3% of the budget, 6.5% of the default cost. Mirror fold +4.3 points, sd 3.4 on 210 questions (clears).
- `avg_gated_lookup` at 1.00x: deviated from the default cell on family F2. Verification margin +3.3 points, sd 5.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 93.5% of the budget, 6.5% of the default cost. Mirror fold +3.3 points, sd 3.4 on 210 questions (clears).
- `avg_lookup` at 0.25x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 6.5% of the default cost, 74.0% under the budget it was given.
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 6.5% of the default cost, 87.0% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 6.5% of the default cost, 91.3% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 6.5% of the default cost, 93.5% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 35.8 points at 54.1% of the default cost, 27.9% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 35.8 points at 54.1% of the default cost, 45.9% under the budget it was given.
- `avg_equation_resolved` at 0.25x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 6.5% of the default cost, 74.0% under the budget it was given.
- `avg_equation_resolved` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 6.5% of the default cost, 87.0% under the budget it was given.
- `avg_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 6.5% of the default cost, 91.3% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 6.5% of the default cost, 93.5% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
