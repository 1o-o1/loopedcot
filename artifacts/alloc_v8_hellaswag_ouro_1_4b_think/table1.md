# Table 1 -- hellaswag (ouro_1_4b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 72044 layer passes over 1700 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 74.8 | +2.9 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 71.9 | 70.6 | 75.0 | 75.0 | +2.6 |
| lookup | 77.6 | 77.6 | 77.6 | 77.6 | +0.0 |
| equation | 71.9 | 70.6 | 70.9 | 70.9 | +6.7 |
| equation_n100 | 70.6 | 66.1 | 70.9 | 70.9 | +6.7 |
| equation_n30 | 71.9 | 70.6 | 75.0 | 75.0 | +2.6 |
| equation_resolved | 76.9 | 76.9 | 76.9 | 76.9 | +0.7 |
| gated_equation | 77.6 | 77.6 | 75.0 | 75.0 | +2.6 |
| gated_equation_resolved | 77.6 | 77.6 | 75.0 | 75.0 | +2.6 |
| avg_gated_equation_resolved | 77.6 | 77.6 | 75.0 | 75.0 | +2.6 |
| avg_gated_lookup | 77.6 | 77.6 | 75.0 | 75.0 | +2.6 |
| avg_lookup | 77.6 | 77.6 | 77.6 | 77.6 | +0.0 |
| avg_equation | 77.6 | 77.6 | 70.9 | 70.9 | +6.7 |
| avg_equation_resolved | 76.9 | 76.9 | 76.9 | 76.9 | +0.7 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 0, 77.6 points over 1700 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0. Of the families that CLEAR the bar the one that RUNS is set by `policy.GATE_FAMILY_RULE` = `best`: the cleared family with the largest mean verified margin over the folds, ties to the smaller family. The folds, the bar, the reference and the pricing are the same test under either rule; only which cleared family is taken differs.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 1344 vs 18011 (-92.5%) | 1344 vs 36022 (-96.3%) | 50496 vs 54033 (-6.5%) | 50496 vs 72044 (-29.9%) |
| avg_gated_lookup | 1344 vs 18011 (-92.5%) | 1344 vs 36022 (-96.3%) | 50496 vs 54033 (-6.5%) | 50496 vs 72044 (-29.9%) |
| avg_lookup | 1344 vs 18011 (-92.5%) | 1344 vs 36022 (-96.3%) | 1344 vs 54033 (-97.5%) | 1344 vs 72044 (-98.1%) |
| avg_equation | 1344 vs 18011 (-92.5%) | 1344 vs 36022 (-96.3%) | 37872 vs 54033 (-29.9%) | 37872 vs 72044 (-47.4%) |
| avg_equation_resolved | 4416 vs 18011 (-75.5%) | 4416 vs 36022 (-87.7%) | 4416 vs 54033 (-91.8%) | 4416 vs 72044 (-93.9%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 1700 | 13632 | 394560 (over) vs 394560 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T256: 1700 | 25920 | 394560 (over) vs 394560 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T512: 1700 | 50496 | 394560 (over) vs 394560 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T512: 1700 | 50496 | 394560 (over) vs 394560 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 1700 | 13632 | 394560 (over) vs 394560 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T256: 1700 | 25920 | 394560 (over) vs 394560 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T512: 1700 | 50496 | 394560 (over) vs 394560 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T512: 1700 | 50496 | 394560 (over) vs 394560 (over) |
- `avg_gated_equation_resolved` at 0.25x: the multiplier is 0, so the budget never binds. The row is the same 77.6 points at 1.9% of the default cost, 92.5% under the budget it was given.
- `avg_gated_equation_resolved` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 77.6 points at 1.9% of the default cost, 96.3% under the budget it was given.
- `avg_gated_equation_resolved` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F0. Verification margin +5.6 points, sd 3.7, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 92.5% of the budget, 1.9% of the default cost. Mirror fold +3.8 points, sd 2.4 on 210 questions (clears).
- `avg_gated_equation_resolved` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F0. Verification margin +7.8 points, sd 4.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 96.3% of the budget, 1.9% of the default cost. Mirror fold +6.2 points, sd 2.7 on 210 questions (clears).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -1.1 points, sd 3.8, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 6.5% of the budget, 70.1% of the default cost. Mirror fold +0.0 points, sd 2.8 on 210 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -1.1 points, sd 3.8, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 29.9% of the budget, 70.1% of the default cost. Mirror fold +0.0 points, sd 2.8 on 210 questions (fails).
- `avg_gated_lookup` at 0.25x: the multiplier is 0, so the budget never binds. The row is the same 77.6 points at 1.9% of the default cost, 92.5% under the budget it was given.
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 77.6 points at 1.9% of the default cost, 96.3% under the budget it was given.
- `avg_gated_lookup` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F0. Verification margin +5.6 points, sd 3.7, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 92.5% of the budget, 1.9% of the default cost. Mirror fold +3.8 points, sd 2.4 on 210 questions (clears).
- `avg_gated_lookup` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F0. Verification margin +7.8 points, sd 4.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 96.3% of the budget, 1.9% of the default cost. Mirror fold +6.2 points, sd 2.7 on 210 questions (clears).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +2.2 points, sd 3.5, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 6.5% of the budget, 70.1% of the default cost. Mirror fold +0.0 points, sd 2.8 on 210 questions (fails).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +2.2 points, sd 3.5, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 29.9% of the budget, 70.1% of the default cost. Mirror fold +0.0 points, sd 2.8 on 210 questions (fails).
- `avg_lookup` at 0.25x: the multiplier is 0, so the budget never binds. The row is the same 77.6 points at 1.9% of the default cost, 92.5% under the budget it was given.
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 77.6 points at 1.9% of the default cost, 96.3% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 77.6 points at 1.9% of the default cost, 97.5% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 77.6 points at 1.9% of the default cost, 98.1% under the budget it was given.
- `avg_equation_resolved` at 0.25x: the multiplier is 0, so the budget never binds. The row is the same 76.9 points at 6.1% of the default cost, 75.5% under the budget it was given.
- `avg_equation_resolved` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 76.9 points at 6.1% of the default cost, 87.7% under the budget it was given.
- `avg_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 76.9 points at 6.1% of the default cost, 91.8% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 76.9 points at 6.1% of the default cost, 93.9% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
