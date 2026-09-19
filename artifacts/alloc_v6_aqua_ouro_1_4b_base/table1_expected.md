# Table 1 -- aqua (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 18914 layer passes over 154 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 67.5 | +1.3 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 57.1 | 68.8 | 67.5 | 67.5 | +1.3 |
| lookup | 53.2 | 68.8 | 68.8 | 68.8 | +0.0 |
| equation | 53.2 | 68.8 | 68.8 | 68.2 | +0.6 |
| equation_n100 | 53.2 | 68.8 | 68.8 | 68.2 | +0.6 |
| equation_n30 | 53.2 | 68.8 | 68.8 | 68.2 | +0.6 |
| equation_resolved | 53.2 | 68.8 | 68.8 | 68.2 | +0.6 |
| gated_equation | 53.2 | 68.8 | 68.8 | 68.2 | +0.6 |
| gated_equation_resolved | 53.2 | 68.8 | 68.8 | 68.2 | +0.6 |
| avg_gated_equation_resolved | 57.1 | 68.8 | 68.8 | 68.2 | +0.6 |
| avg_gated_lookup | 57.1 | 68.8 | 68.8 | 68.8 | +0.0 |
| avg_lookup | 53.9 | 68.8 | 68.8 | 68.8 | +0.0 |
| avg_equation | 53.9 | 68.8 | 68.8 | 68.2 | +0.6 |
| avg_equation_resolved | 53.9 | 68.8 | 68.8 | 68.2 | +0.6 |

The ORACLE GAP is the best single evaluation cell (depth 3 at cap 256, 68.8 points over 154 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F1, F2, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 4153 vs 4728 (-12.2%) | 8454 vs 9457 (-10.6%) | 7304 vs 14185 (-48.5%) | 15765 vs 18914 (-16.6%) |
| avg_gated_lookup | 4153 vs 4728 (-12.2%) | 8454 vs 9457 (-10.6%) | 7304 vs 14185 (-48.5%) | 7304 vs 18914 (-61.4%) |
| avg_lookup | 864 vs 4728 (-81.7%) | 7304 vs 9457 (-22.8%) | 7304 vs 14185 (-48.5%) | 7304 vs 18914 (-61.4%) |
| avg_equation | 864 vs 4728 (-81.7%) | 7304 vs 9457 (-22.8%) | 7304 vs 14185 (-48.5%) | 15765 vs 18914 (-16.6%) |
| avg_equation_resolved | 864 vs 4728 (-81.7%) | 7304 vs 9457 (-22.8%) | 7304 vs 14185 (-48.5%) | 15765 vs 18914 (-16.6%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T32: 154 | 4153 | 24264 (over) vs 24264 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T32: 154 | 4153 | 24264 (over) vs 24264 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T1024: 154 | 12468 | 24264 (over) vs 24264 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T2048: 154 | 16400 | 24264 (over) vs 24264 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T32: 154 | 4153 | 24264 (over) vs 24264 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T32: 154 | 4153 | 24264 (over) vs 24264 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T1024: 154 | 12468 | 24264 (over) vs 24264 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T2048: 154 | 16400 | 24264 (over) vs 24264 (over) |
- `avg_gated_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.2 points at 83.4% of the default cost, 16.6% under the budget it was given.
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin -10.0 points, sd 5.3, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 12.2% of the budget, 22.0% of the default cost. Mirror fold -2.9 points, sd 4.0 on 70 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F1. Verification margin +26.7 points, sd 9.6, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 10.6% of the budget, 44.7% of the default cost. Mirror fold +12.9 points, sd 5.7 on 70 questions (clears).
- `avg_gated_equation_resolved` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F2. Verification margin +6.7 points, sd 4.6, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 48.5% of the budget, 38.6% of the default cost. Mirror fold +2.9 points, sd 4.1 on 70 questions (clears).
- `avg_gated_equation_resolved` at 1.00x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F2. Verification margin +6.7 points, sd 4.6, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 16.6% of the budget, 83.4% of the default cost. Mirror fold +2.9 points, sd 4.1 on 70 questions (clears).
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 68.8 points at 44.7% of the default cost, 10.6% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 68.8 points at 38.6% of the default cost, 48.5% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.8 points at 38.6% of the default cost, 61.4% under the budget it was given.
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin -10.0 points, sd 5.3, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 12.2% of the budget, 22.0% of the default cost. Mirror fold -2.9 points, sd 4.0 on 70 questions (fails).
- `avg_gated_lookup` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F1. Verification margin +26.7 points, sd 9.6, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 10.6% of the budget, 44.7% of the default cost. Mirror fold +12.9 points, sd 5.7 on 70 questions (clears).
- `avg_gated_lookup` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F2. Verification margin +6.7 points, sd 4.6, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 48.5% of the budget, 38.6% of the default cost. Mirror fold +2.9 points, sd 4.1 on 70 questions (clears).
- `avg_gated_lookup` at 1.00x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F2. Verification margin +6.7 points, sd 4.6, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 61.4% of the budget, 38.6% of the default cost. Mirror fold +2.9 points, sd 4.1 on 70 questions (clears).
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 68.8 points at 38.6% of the default cost, 22.8% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 68.8 points at 38.6% of the default cost, 48.5% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.8 points at 38.6% of the default cost, 61.4% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.2 points at 83.4% of the default cost, 16.6% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.2 points at 83.4% of the default cost, 16.6% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
