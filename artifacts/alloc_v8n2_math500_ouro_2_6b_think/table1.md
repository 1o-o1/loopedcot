# Table 1 -- math500 (ouro_2_6b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 423560 layer passes over 400 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 91.2 | +0.0 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 60.5 | 76.2 | 76.2 | 84.0 | +7.2 |
| lookup | 73.0 | 79.2 | 84.0 | 84.0 | +7.2 |
| equation | 73.0 | 79.2 | 84.0 | 82.2 | +9.0 |
| equation_n100 | 73.0 | 79.2 | 84.0 | 82.2 | +9.0 |
| equation_n30 | 60.5 | 76.2 | 76.2 | 84.0 | +7.2 |
| equation_resolved | 73.0 | 79.2 | 84.0 | 84.0 | +7.2 |
| gated_equation | 73.0 | 76.2 | 84.0 | 84.0 | +7.2 |
| gated_equation_resolved | 73.0 | 76.2 | 84.0 | 84.0 | +7.2 |
| avg_gated_equation_resolved | 60.5 | 76.2 | 84.0 | 84.0 | +7.2 |
| avg_gated_lookup | 60.5 | 76.2 | 84.0 | 84.0 | +7.2 |
| avg_lookup | 73.0 | 79.2 | 84.0 | 84.0 | +7.2 |
| avg_equation | 73.0 | 79.2 | 79.2 | 82.2 | +9.0 |
| avg_equation_resolved | 73.0 | 79.2 | 84.0 | 84.0 | +7.2 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 4096, 91.2 points over 400 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3. Of the families that CLEAR the bar the one that RUNS is set by `policy.GATE_FAMILY_RULE` = `best`: the cleared family with the largest mean verified margin over the folds, ties to the smaller family. The folds, the bar, the reference and the pricing are the same test under either rule; only which cleared family is taken differs.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 105600 vs 105890 (-0.3%) | 203904 vs 211780 (-3.7%) | 300384 vs 317670 (-5.4%) | 400512 vs 423560 (-5.4%) |
| avg_gated_lookup | 105600 vs 105890 (-0.3%) | 203904 vs 211780 (-3.7%) | 300384 vs 317670 (-5.4%) | 400512 vs 423560 (-5.4%) |
| avg_lookup | 101952 vs 105890 (-3.7%) | 200256 vs 211780 (-5.4%) | 300384 vs 317670 (-5.4%) | 400512 vs 423560 (-5.4%) |
| avg_equation | 101952 vs 105890 (-3.7%) | 200256 vs 211780 (-5.4%) | 200256 vs 317670 (-37.0%) | 396864 vs 423560 (-6.3%) |
| avg_equation_resolved | 101952 vs 105890 (-3.7%) | 200256 vs 211780 (-5.4%) | 300384 vs 317670 (-5.4%) | 400512 vs 423560 (-5.4%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T512: 400 | 105600 | 793728 (over) vs 793728 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T1024: 400 | 203904 | 793728 (over) vs 793728 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T1024: 400 | 203904 | 793728 (over) vs 793728 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T2048: 400 | 400512 | 793728 (over) vs 793728 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T512: 400 | 105600 | 793728 (over) vs 793728 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T1024: 400 | 203904 | 793728 (over) vs 793728 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T1024: 400 | 203904 | 793728 (over) vs 793728 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T2048: 400 | 400512 | 793728 (over) vs 793728 (over) |
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +10.0 points, sd 7.2, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 0.3% of the budget, 24.9% of the default cost. Mirror fold -10.0 points, sd 4.6 on 70 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 3.7% of the budget, 48.1% of the default cost. Mirror fold -1.4 points, sd 3.8 on 70 questions (fails).
- `avg_gated_equation_resolved` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +10.0 points, sd 5.3, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 5.4% of the budget, 70.9% of the default cost. Mirror fold +2.9 points, sd 3.5 on 70 questions (clears).
- `avg_gated_equation_resolved` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 5.4% of the budget, 94.6% of the default cost. Mirror fold -1.4 points, sd 1.4 on 70 questions (fails).
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 84.0 points at 70.9% of the default cost, 5.4% under the budget it was given.
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +10.0 points, sd 7.2, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 0.3% of the budget, 24.9% of the default cost. Mirror fold -10.0 points, sd 4.6 on 70 questions (fails).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 3.7% of the budget, 48.1% of the default cost. Mirror fold -1.4 points, sd 3.8 on 70 questions (fails).
- `avg_gated_lookup` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) on family F2. Verification margin +10.0 points, sd 5.3, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 5.4% of the budget, 70.9% of the default cost. Mirror fold +2.9 points, sd 3.5 on 70 questions (clears).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -6.7 points, sd 4.6, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 5.4% of the budget, 94.6% of the default cost. Mirror fold +0.0 points, sd 0.0 on 70 questions (fails).

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
