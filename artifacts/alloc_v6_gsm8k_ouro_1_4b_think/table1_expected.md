# Table 1 -- gsm8k (ouro_1_4b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 64301 layer passes over 1056 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 93.0 | +0.0 |
| default_cell | n/a | n/a | n/a | 93.0 | +0.0 |
| default_at_budget | 27.2 | 59.8 | 88.5 | 93.0 | +0.0 |
| lookup | 55.5 | 86.8 | 91.4 | 91.4 | +1.6 |
| equation | 55.5 | 86.8 | 91.4 | 93.0 | +0.0 |
| equation_n100 | 55.5 | 86.8 | 91.4 | 93.0 | +0.0 |
| equation_n30 | 55.5 | 86.8 | 91.4 | 93.0 | +0.0 |
| equation_resolved | 55.5 | 86.8 | 91.4 | 93.0 | +0.0 |
| gated_equation | 55.5 | 86.8 | 91.4 | 93.0 | +0.0 |
| gated_equation_resolved | 55.5 | 86.8 | 91.4 | 93.0 | +0.0 |
| avg_gated_equation_resolved | 27.2 | 86.8 | 88.5 | 93.0 | +0.0 |
| avg_gated_lookup | 27.2 | 59.8 | 88.5 | 93.0 | +0.0 |
| avg_lookup | 55.5 | 86.8 | 91.4 | 91.4 | +1.6 |
| avg_equation | 55.5 | 86.8 | 91.4 | 93.0 | +0.0 |
| avg_equation_resolved | 55.5 | 86.8 | 91.4 | 93.0 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 4096, 93.0 points over 1056 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F1, F2, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 14016 vs 16075 (-12.8%) | 30478 vs 32150 (-5.2%) | 40869 vs 48226 (-15.3%) | 60194 vs 64301 (-6.4%) |
| avg_gated_lookup | 14016 vs 16075 (-12.8%) | 26092 vs 32150 (-18.8%) | 40869 vs 48226 (-15.3%) | 60194 vs 64301 (-6.4%) |
| avg_lookup | 12940 vs 16075 (-19.5%) | 30478 vs 32150 (-5.2%) | 47115 vs 48226 (-2.3%) | 47115 vs 64301 (-26.7%) |
| avg_equation | 12940 vs 16075 (-19.5%) | 30478 vs 32150 (-5.2%) | 47115 vs 48226 (-2.3%) | 60194 vs 64301 (-6.4%) |
| avg_equation_resolved | 12940 vs 16075 (-19.5%) | 30478 vs 32150 (-5.2%) | 47115 vs 48226 (-2.3%) | 60194 vs 64301 (-6.4%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 1056 | 14016 | 60194 (over) vs 60194 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T128: 1056 | 14016 | 60194 (over) vs 60194 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T128: 1056 | 14016 | 60194 (over) vs 60194 (over) |
| 1.00x | default_cell | 4 | k4_T4096: 1056 | 60194 | 60194 (fits) vs 60194 (fits) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 1056 | 14016 | 60194 (over) vs 60194 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T128: 1056 | 14016 | 60194 (over) vs 60194 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T128: 1056 | 14016 | 60194 (over) vs 60194 (over) |
| 1.00x | default_cell | 4 | k4_T4096: 1056 | 60194 | 60194 (fits) vs 60194 (fits) |
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin +27.8 points, sd 6.2, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 12.8% of the budget, 21.8% of the default cost. Mirror fold -15.2 points, sd 3.1 on 184 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F2. Verification margin +68.4 points, sd 5.6, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 5.2% of the budget, 47.4% of the default cost. Mirror fold +65.8 points, sd 3.6 on 184 questions (clears).
- `avg_gated_equation_resolved` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F1. Verification margin +63.3 points, sd 5.6, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 15.3% of the budget, 63.6% of the default cost. Mirror fold +64.1 points, sd 3.6 on 184 questions (clears).
- `avg_gated_equation_resolved` at 1.00x: reverted to the default cell for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 6.4% of the budget, 93.6% of the default cost. Mirror fold -0.5 points, sd 1.2 on 184 questions (fails).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin +27.8 points, sd 6.2, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 12.8% of the budget, 21.8% of the default cost. Mirror fold -15.2 points, sd 3.1 on 184 questions (fails).
- `avg_gated_lookup` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F1. Verification margin +35.4 points, sd 6.2, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 18.8% of the budget, 40.6% of the default cost. Mirror fold +39.1 points, sd 3.8 on 184 questions (clears).
- `avg_gated_lookup` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) on family F1. Verification margin +63.3 points, sd 5.6, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 15.3% of the budget, 63.6% of the default cost. Mirror fold +64.1 points, sd 3.6 on 184 questions (clears).
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 6.4% of the budget, 93.6% of the default cost. Mirror fold -1.6 points, sd 1.4 on 184 questions (fails).
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 91.4 points at 73.3% of the default cost, 2.3% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 91.4 points at 73.3% of the default cost, 26.7% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 93.0 points at 93.6% of the default cost, 6.4% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 93.0 points at 93.6% of the default cost, 6.4% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
