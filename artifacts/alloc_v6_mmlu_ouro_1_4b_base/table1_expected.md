# Table 1 -- mmlu (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 12243 layer passes over 1700 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 68.4 | +0.0 |
| default_cell | n/a | n/a | 68.4 | 68.4 | +0.0 |
| default_at_budget | 65.5 | 67.5 | 68.4 | 68.4 | +0.0 |
| lookup | 67.4 | 67.4 | 67.4 | 67.4 | +1.0 |
| equation | 65.5 | 65.5 | 68.4 | 68.4 | +0.0 |
| equation_n100 | 58.9 | 67.5 | 68.4 | 68.4 | +0.0 |
| equation_n30 | 65.5 | 67.5 | 68.4 | 68.4 | +0.0 |
| equation_resolved | 67.4 | 67.4 | 68.4 | 68.4 | +0.0 |
| gated_equation | 67.4 | 67.5 | 68.4 | 68.4 | +0.0 |
| gated_equation_resolved | 67.4 | 67.5 | 68.4 | 68.4 | +0.0 |
| avg_gated_equation_resolved | 67.4 | 67.4 | 68.4 | 68.4 | +0.0 |
| avg_gated_lookup | 67.4 | 67.4 | 68.4 | 68.4 | +0.0 |
| avg_lookup | 67.4 | 67.4 | 67.4 | 67.4 | +1.0 |
| avg_equation | 67.4 | 65.4 | 68.4 | 68.4 | +0.0 |
| avg_equation_resolved | 67.4 | 67.4 | 68.4 | 68.4 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 128, 68.4 points over 1700 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x yes, 1.00x yes.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 1248 vs 3061 (-59.2%) | 1248 vs 6121 (-79.6%) | 8499 vs 9182 (-7.4%) | 8499 vs 12243 (-30.6%) |
| avg_gated_lookup | 1248 vs 3061 (-59.2%) | 1248 vs 6121 (-79.6%) | 8499 vs 9182 (-7.4%) | 8499 vs 12243 (-30.6%) |
| avg_lookup | 1248 vs 3061 (-59.2%) | 1248 vs 6121 (-79.6%) | 1248 vs 9182 (-86.4%) | 1248 vs 12243 (-89.8%) |
| avg_equation | 1248 vs 3061 (-59.2%) | 5691 vs 6121 (-7.0%) | 8499 vs 9182 (-7.4%) | 8499 vs 12243 (-30.6%) |
| avg_equation_resolved | 1248 vs 3061 (-59.2%) | 1248 vs 6121 (-79.6%) | 7516 vs 9182 (-18.1%) | 7516 vs 12243 (-38.6%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T0: 1700 | 1248 | 8499 (over) vs 8499 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T0: 1700 | 1248 | 8499 (over) vs 8499 (over) |
| 0.75x | default_cell | 4 | k4_T4096: 1700 | 8499 | 8499 (fits) vs 8499 (fits) |
| 1.00x | default_cell | 4 | k4_T4096: 1700 | 8499 | 8499 (fits) vs 8499 (fits) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T0: 1700 | 1248 | 8499 (over) vs 8499 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T0: 1700 | 1248 | 8499 (over) vs 8499 (over) |
| 0.75x | default_cell | 4 | k4_T4096: 1700 | 8499 | 8499 (fits) vs 8499 (fits) |
| 1.00x | default_cell | 4 | k4_T4096: 1700 | 8499 | 8499 (fits) vs 8499 (fits) |
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 59.2% of the budget, 10.2% of the default cost. Mirror fold +0.0 points, sd 0.0 on 210 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin -6.7 points, sd 5.4, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 79.6% of the budget, 10.2% of the default cost. Mirror fold +0.0 points, sd 0.0 on 210 questions (fails).
- `avg_gated_equation_resolved` at 0.75x: reverted to the default cell for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 7.4% of the budget, 69.4% of the default cost. Mirror fold -2.4 points, sd 3.1 on 210 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: reverted to the default cell for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 30.6% of the budget, 69.4% of the default cost. Mirror fold -2.4 points, sd 3.1 on 210 questions (fails).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 59.2% of the budget, 10.2% of the default cost. Mirror fold +0.0 points, sd 0.0 on 210 questions (fails).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 79.6% of the budget, 10.2% of the default cost. Mirror fold +0.0 points, sd 0.0 on 210 questions (fails).
- `avg_gated_lookup` at 0.75x: reverted to the default cell for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 7.4% of the budget, 69.4% of the default cost. Mirror fold -2.4 points, sd 3.1 on 210 questions (fails).
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 30.6% of the budget, 69.4% of the default cost. Mirror fold -2.4 points, sd 3.1 on 210 questions (fails).
- `avg_lookup` at 0.25x: the multiplier is 0, so the budget never binds. The row is the same 67.4 points at 10.2% of the default cost, 59.2% under the budget it was given.
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 67.4 points at 10.2% of the default cost, 79.6% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 67.4 points at 10.2% of the default cost, 86.4% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 67.4 points at 10.2% of the default cost, 89.8% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 68.4 points at 69.4% of the default cost, 7.4% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.4 points at 69.4% of the default cost, 30.6% under the budget it was given.
- `avg_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 68.4 points at 61.4% of the default cost, 18.1% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.4 points at 61.4% of the default cost, 38.6% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
