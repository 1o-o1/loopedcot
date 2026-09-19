# Table 1 -- strategyqa (mcleish_llama32_r32), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 41981 layer passes over 1990 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 49.7 | +1.6 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 50.7 | 50.4 | 50.3 | 50.3 | +1.0 |
| lookup | 50.7 | 50.4 | 50.4 | 50.4 | +0.9 |
| equation | 50.7 | 50.4 | 50.3 | 50.3 | +1.0 |
| equation_n100 | 50.7 | 50.4 | 50.3 | 50.3 | +1.0 |
| equation_n30 | 50.7 | 50.4 | 50.3 | 50.3 | +1.0 |
| equation_resolved | 50.7 | 50.4 | 50.4 | 50.4 | +0.9 |
| gated_equation | 50.7 | 50.4 | 50.3 | 50.3 | +1.0 |
| gated_equation_resolved | 50.7 | 50.4 | 50.3 | 50.3 | +1.0 |
| avg_gated_equation_resolved | 50.7 | 50.4 | 50.3 | 50.3 | +1.0 |
| avg_gated_lookup | 50.7 | 50.4 | 50.3 | 50.3 | +1.0 |
| avg_lookup | 50.4 | 50.4 | 50.4 | 50.4 | +0.9 |
| avg_equation | 50.7 | 50.4 | 50.3 | 50.3 | +1.0 |
| avg_equation_resolved | 50.4 | 50.4 | 50.4 | 50.4 | +0.9 |

The ORACLE GAP is the best single evaluation cell (depth 8 at cap 0, 51.3 points over 1990 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none.

`default_cell` is the default operating point (depth 8 at cap 8192) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 7986 vs 10495 (-23.9%) | 13243 vs 20991 (-36.9%) | 23756 vs 31486 (-24.6%) | 23756 vs 41981 (-43.4%) |
| avg_gated_lookup | 7986 vs 10495 (-23.9%) | 13243 vs 20991 (-36.9%) | 23756 vs 31486 (-24.6%) | 23756 vs 41981 (-43.4%) |
| avg_lookup | 3200 vs 10495 (-69.5%) | 13243 vs 20991 (-36.9%) | 13243 vs 31486 (-57.9%) | 13243 vs 41981 (-68.5%) |
| avg_equation | 3998 vs 10495 (-61.9%) | 13243 vs 20991 (-36.9%) | 23756 vs 31486 (-24.6%) | 23756 vs 41981 (-43.4%) |
| avg_equation_resolved | 3200 vs 10495 (-69.5%) | 13243 vs 20991 (-36.9%) | 13243 vs 31486 (-57.9%) | 13243 vs 41981 (-68.5%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 8 | k8_T512: 1990 | 7986 | 86834 (over) vs 86834 (over) |
| 0.50x | deepest_depth_capped | 8 | k8_T1024: 1990 | 13243 | 86834 (over) vs 86834 (over) |
| 0.75x | deepest_depth_capped | 8 | k8_T2048: 1990 | 23756 | 86834 (over) vs 86834 (over) |
| 1.00x | deepest_depth_capped | 8 | k8_T2048: 1990 | 23756 | 86834 (over) vs 86834 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 8 | k8_T512: 1990 | 7986 | 86834 (over) vs 86834 (over) |
| 0.50x | deepest_depth_capped | 8 | k8_T1024: 1990 | 13243 | 86834 (over) vs 86834 (over) |
| 0.75x | deepest_depth_capped | 8 | k8_T2048: 1990 | 23756 | 86834 (over) vs 86834 (over) |
| 1.00x | deepest_depth_capped | 8 | k8_T2048: 1990 | 23756 | 86834 (over) vs 86834 (over) |
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 3.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 23.9% of the budget, 19.0% of the default cost. Mirror fold -6.7 points, sd 3.9 on 210 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 36.9% of the budget, 31.5% of the default cost. Mirror fold -8.6 points, sd 4.0 on 210 questions (fails).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 24.6% of the budget, 56.6% of the default cost. Mirror fold -8.6 points, sd 4.1 on 210 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 43.4% of the budget, 56.6% of the default cost. Mirror fold -8.6 points, sd 4.1 on 210 questions (fails).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 3.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 23.9% of the budget, 19.0% of the default cost. Mirror fold -6.7 points, sd 3.9 on 210 questions (fails).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 36.9% of the budget, 31.5% of the default cost. Mirror fold -8.6 points, sd 4.0 on 210 questions (fails).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 24.6% of the budget, 56.6% of the default cost. Mirror fold -8.6 points, sd 4.1 on 210 questions (fails).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 43.4% of the budget, 56.6% of the default cost. Mirror fold -8.6 points, sd 4.1 on 210 questions (fails).
- `avg_equation_resolved` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 50.4 points at 31.5% of the default cost, 36.9% under the budget it was given.
- `avg_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 50.4 points at 31.5% of the default cost, 57.9% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 50.4 points at 31.5% of the default cost, 68.5% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
