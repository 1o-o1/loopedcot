# Table 1 -- arc (ouro_2_6b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 9835 layer passes over 938 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 93.1 | +0.0 |
| default_cell | n/a | n/a | n/a | 93.1 | +0.0 |
| default_at_budget | n/a | 92.2 | 92.4 | 93.1 | +0.0 |
| lookup | 91.3 | 92.2 | 92.2 | 92.2 | +0.9 |
| equation | 91.3 | 92.2 | 91.7 | 91.7 | +1.4 |
| equation_n100 | 91.3 | 92.2 | 91.7 | 91.7 | +1.4 |
| equation_n30 | 91.3 | 92.2 | 91.7 | 92.3 | +0.7 |
| equation_resolved | 91.3 | 92.2 | 92.4 | 92.3 | +0.7 |
| gated_equation | 91.3 | 92.2 | 92.4 | 92.2 | +0.9 |
| gated_equation_resolved | 91.3 | 92.2 | 92.4 | 92.2 | +0.9 |
| avg_gated_equation_resolved | 91.3 | 92.2 | 92.4 | 92.2 | +0.9 |
| avg_gated_lookup | 91.3 | 92.2 | 92.4 | 92.2 | +0.9 |
| avg_lookup | 91.3 | 92.2 | 92.2 | 92.2 | +0.9 |
| avg_equation | 91.3 | 92.2 | 91.7 | 91.7 | +1.4 |
| avg_equation_resolved | 91.3 | 92.2 | 92.4 | 92.3 | +0.7 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 128, 93.1 points over 938 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 1872 vs 2459 (-23.9%) | 2496 vs 4917 (-49.2%) | 5568 vs 7376 (-24.5%) | 2496 vs 9835 (-74.6%) |
| avg_gated_lookup | 1872 vs 2459 (-23.9%) | 2496 vs 4917 (-49.2%) | 5568 vs 7376 (-24.5%) | 2496 vs 9835 (-74.6%) |
| avg_lookup | 1872 vs 2459 (-23.9%) | 2496 vs 4917 (-49.2%) | 2496 vs 7376 (-66.2%) | 2496 vs 9835 (-74.6%) |
| avg_equation | 1872 vs 2459 (-23.9%) | 2496 vs 4917 (-49.2%) | 7305 vs 7376 (-1.0%) | 7305 vs 9835 (-25.7%) |
| avg_equation_resolved | 1872 vs 2459 (-23.9%) | 2496 vs 4917 (-49.2%) | 5568 vs 7376 (-24.5%) | 8558 vs 9835 (-13.0%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | shallower_depth | 3 | k3_T0: 938 | 1872 | 9611 (over) vs 9611 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T0: 938 | 2496 | 9611 (over) vs 9611 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T16: 938 | 5568 | 9611 (over) vs 9611 (over) |
| 1.00x | default_cell | 4 | k4_T4096: 938 | 9611 | 9611 (fits) vs 9611 (fits) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | shallower_depth | 3 | k3_T0: 938 | 1872 | 9611 (over) vs 9611 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T0: 938 | 2496 | 9611 (over) vs 9611 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T16: 938 | 5568 | 9611 (over) vs 9611 (over) |
| 1.00x | default_cell | 4 | k4_T4096: 938 | 9611 | 9611 (fits) vs 9611 (fits) |
- `avg_gated_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 92.2 points at 25.4% of the default cost, 74.6% under the budget it was given.
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (one depth down, depth 3, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (70 verification questions, the ids after the 164 that fit, out of 234 calibration); cost saving 23.9% of the budget, 19.0% of the default cost. Mirror fold +0.0 points, sd 0.0 on 164 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (70 verification questions, the ids after the 164 that fit, out of 234 calibration); cost saving 49.2% of the budget, 25.4% of the default cost. Mirror fold +0.0 points, sd 0.0 on 164 questions (fails).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -4.3 points, sd 2.5, bar 0.50 sd (70 verification questions, the ids after the 164 that fit, out of 234 calibration); cost saving 24.5% of the budget, 56.6% of the default cost. Mirror fold -0.6 points, sd 1.1 on 164 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: deviated from the default cell on family F0. Verification margin +2.9 points, sd 2.9, bar 0.50 sd (70 verification questions, the ids after the 164 that fit, out of 234 calibration); cost saving 74.6% of the budget, 25.4% of the default cost. Mirror fold +0.6 points, sd 0.6 on 164 questions (clears).
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 92.2 points at 25.4% of the default cost, 74.6% under the budget it was given.
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (one depth down, depth 3, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (70 verification questions, the ids after the 164 that fit, out of 234 calibration); cost saving 23.9% of the budget, 19.0% of the default cost. Mirror fold +0.0 points, sd 0.0 on 164 questions (fails).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (70 verification questions, the ids after the 164 that fit, out of 234 calibration); cost saving 49.2% of the budget, 25.4% of the default cost. Mirror fold +0.0 points, sd 0.0 on 164 questions (fails).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -4.3 points, sd 2.5, bar 0.50 sd (70 verification questions, the ids after the 164 that fit, out of 234 calibration); cost saving 24.5% of the budget, 56.6% of the default cost. Mirror fold +0.0 points, sd 0.0 on 164 questions (fails).
- `avg_gated_lookup` at 1.00x: deviated from the default cell on family F0. Verification margin +2.9 points, sd 2.9, bar 0.50 sd (70 verification questions, the ids after the 164 that fit, out of 234 calibration); cost saving 74.6% of the budget, 25.4% of the default cost. Mirror fold +0.6 points, sd 0.6 on 164 questions (clears).
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 92.2 points at 25.4% of the default cost, 49.2% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 92.2 points at 25.4% of the default cost, 66.2% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 92.2 points at 25.4% of the default cost, 74.6% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 91.7 points at 74.3% of the default cost, 25.7% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 92.3 points at 87.0% of the default cost, 13.0% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
