# Table 1 -- aqua (ouro_2_6b_base), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 38851 layer passes over 154 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 73.4 | +1.9 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 61.0 | 66.9 | 72.1 | 72.1 | +3.2 |
| lookup | 55.8 | 66.2 | 68.2 | 68.2 | +7.1 |
| equation | 55.8 | 66.2 | 68.2 | 68.2 | +7.1 |
| equation_n100 | 55.8 | 66.2 | 68.2 | 68.2 | +7.1 |
| equation_n30 | 61.0 | 66.2 | 72.1 | 72.1 | +3.2 |
| equation_resolved | 55.8 | 66.2 | 68.2 | 68.2 | +7.1 |
| gated_equation | 61.0 | 66.9 | 72.1 | 72.1 | +3.2 |
| gated_equation_resolved | 61.0 | 66.9 | 72.1 | 72.1 | +3.2 |
| avg_gated_equation_resolved | 61.0 | 66.9 | 72.1 | 72.1 | +3.2 |
| avg_gated_lookup | 61.0 | 66.9 | 72.1 | 72.1 | +3.2 |
| avg_lookup | 55.8 | 55.8 | 68.2 | 68.2 | +7.1 |
| avg_equation | 59.7 | 66.2 | 68.2 | 68.2 | +7.1 |
| avg_equation_resolved | 55.8 | 55.8 | 68.2 | 68.2 | +7.1 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 256, 75.3 points over 154 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none. Of the families that CLEAR the bar the one that RUNS is set by `policy.GATE_FAMILY_RULE` = `best`: the cleared family with the largest mean verified margin over the folds, ties to the smaller family. The folds, the bar, the reference and the pricing are the same test under either rule; only which cleared family is taken differs.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 8448 vs 9713 (-13.0%) | 14592 vs 19426 (-24.9%) | 26880 vs 29138 (-7.8%) | 26880 vs 38851 (-30.8%) |
| avg_gated_lookup | 8448 vs 9713 (-13.0%) | 14592 vs 19426 (-24.9%) | 26880 vs 29138 (-7.8%) | 26880 vs 38851 (-30.8%) |
| avg_lookup | 7296 vs 9713 (-24.9%) | 7296 vs 19426 (-62.4%) | 25728 vs 29138 (-11.7%) | 25728 vs 38851 (-33.8%) |
| avg_equation | 2304 vs 9713 (-76.3%) | 13440 vs 19426 (-30.8%) | 25728 vs 29138 (-11.7%) | 25728 vs 38851 (-33.8%) |
| avg_equation_resolved | 7296 vs 9713 (-24.9%) | 7296 vs 19426 (-62.4%) | 25728 vs 29138 (-11.7%) | 25728 vs 38851 (-33.8%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T32: 154 | 8448 | 788736 (over) vs 788736 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T64: 154 | 14592 | 788736 (over) vs 788736 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T128: 154 | 26880 | 788736 (over) vs 788736 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T128: 154 | 26880 | 788736 (over) vs 788736 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T32: 154 | 8448 | 788736 (over) vs 788736 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T64: 154 | 14592 | 788736 (over) vs 788736 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T128: 154 | 26880 | 788736 (over) vs 788736 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T128: 154 | 26880 | 788736 (over) vs 788736 (over) |
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -6.7 points, sd 6.9, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 13.0% of the budget, 21.7% of the default cost. Mirror fold -1.4 points, sd 5.2 on 70 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 24.9% of the budget, 37.6% of the default cost. Mirror fold -4.3 points, sd 5.5 on 70 questions (fails).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 7.8% of the budget, 69.2% of the default cost. Mirror fold -1.4 points, sd 6.5 on 70 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 30.8% of the budget, 69.2% of the default cost. Mirror fold -1.4 points, sd 6.5 on 70 questions (fails).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -6.7 points, sd 6.9, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 13.0% of the budget, 21.7% of the default cost. Mirror fold -1.4 points, sd 5.2 on 70 questions (fails).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 24.9% of the budget, 37.6% of the default cost. Mirror fold -4.3 points, sd 5.5 on 70 questions (fails).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 7.8% of the budget, 69.2% of the default cost. Mirror fold -8.6 points, sd 5.4 on 70 questions (fails).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 30.8% of the budget, 69.2% of the default cost. Mirror fold -8.6 points, sd 5.4 on 70 questions (fails).
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 68.2 points at 66.2% of the default cost, 11.7% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.2 points at 66.2% of the default cost, 33.8% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
