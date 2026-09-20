# Table 1 -- aqua (ouro_2_6b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 431126 layer passes over 154 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 86.4 | +1.3 |
| default_cell | n/a | n/a | n/a | 86.4 | +1.3 |
| default_at_budget | 75.3 | 84.4 | 85.1 | 86.4 | +1.3 |
| lookup | 73.4 | 82.5 | 85.1 | 85.1 | +2.6 |
| equation | 75.3 | 84.4 | 85.1 | 86.4 | +1.3 |
| equation_n100 | 75.3 | 84.4 | 85.1 | 86.4 | +1.3 |
| equation_n30 | 75.3 | 84.4 | 85.1 | 86.4 | +1.3 |
| equation_resolved | 73.4 | 84.4 | 85.1 | 86.4 | +1.3 |
| gated_equation | 75.3 | 84.4 | 85.1 | 86.4 | +1.3 |
| gated_equation_resolved | 75.3 | 84.4 | 85.1 | 86.4 | +1.3 |
| avg_gated_equation_resolved | 75.3 | 84.4 | 85.1 | 86.4 | +1.3 |
| avg_gated_lookup | 75.3 | 84.4 | 85.1 | 86.4 | +1.3 |
| avg_lookup | 73.4 | 82.5 | 85.1 | 85.1 | +2.6 |
| avg_equation | 73.4 | 84.4 | 85.1 | 86.4 | +1.3 |
| avg_equation_resolved | 73.4 | 82.5 | 85.1 | 86.4 | +1.3 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 4096, 87.7 points over 154 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none.

`default_cell` is the default operating point (depth 4 at cap 8192) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 100740 vs 107782 (-6.5%) | 179219 vs 215563 (-16.9%) | 257950 vs 323345 (-20.2%) | 429540 vs 431126 (-0.4%) |
| avg_gated_lookup | 100740 vs 107782 (-6.5%) | 179219 vs 215563 (-16.9%) | 257950 vs 323345 (-20.2%) | 429540 vs 431126 (-0.4%) |
| avg_lookup | 75531 vs 107782 (-29.9%) | 133554 vs 215563 (-38.0%) | 257950 vs 323345 (-20.2%) | 257950 vs 431126 (-40.2%) |
| avg_equation | 75531 vs 107782 (-29.9%) | 179219 vs 215563 (-16.9%) | 257950 vs 323345 (-20.2%) | 429540 vs 431126 (-0.4%) |
| avg_equation_resolved | 75531 vs 107782 (-29.9%) | 133554 vs 215563 (-38.0%) | 257950 vs 323345 (-20.2%) | 429540 vs 431126 (-0.4%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T512: 154 | 100740 | 429540 (over) vs 429540 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T1024: 154 | 179219 | 429540 (over) vs 429540 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T2048: 154 | 257950 | 429540 (over) vs 429540 (over) |
| 1.00x | default_cell | 4 | k4_T8192: 154 | 429540 | 429540 (fits) vs 429540 (fits) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T512: 154 | 100740 | 429540 (over) vs 429540 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T1024: 154 | 179219 | 429540 (over) vs 429540 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T2048: 154 | 257950 | 429540 (over) vs 429540 (over) |
| 1.00x | default_cell | 4 | k4_T8192: 154 | 429540 | 429540 (fits) vs 429540 (fits) |
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +10.0 points, sd 7.3, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 6.5% of the budget, 23.4% of the default cost. Mirror fold +0.0 points, sd 3.6 on 70 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 16.9% of the budget, 41.6% of the default cost. Mirror fold -1.4 points, sd 4.8 on 70 questions (fails).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 20.2% of the budget, 59.8% of the default cost. Mirror fold -4.3 points, sd 4.7 on 70 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: reverted to the default cell for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 0.4% of the budget, 99.6% of the default cost. Mirror fold +0.0 points, sd 0.0 on 70 questions (fails).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +10.0 points, sd 7.3, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 6.5% of the budget, 23.4% of the default cost. Mirror fold +0.0 points, sd 3.6 on 70 questions (fails).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +3.3 points, sd 5.7, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 16.9% of the budget, 41.6% of the default cost. Mirror fold -1.4 points, sd 4.8 on 70 questions (fails).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 20.2% of the budget, 59.8% of the default cost. Mirror fold -4.3 points, sd 4.7 on 70 questions (fails).
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin -3.3 points, sd 3.4, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 0.4% of the budget, 99.6% of the default cost. Mirror fold +0.0 points, sd 0.0 on 70 questions (fails).
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 85.1 points at 59.8% of the default cost, 20.2% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 85.1 points at 59.8% of the default cost, 40.2% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
