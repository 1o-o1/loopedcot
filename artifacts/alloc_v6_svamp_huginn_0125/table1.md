# Table 1 -- svamp (huginn_0125), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 8195 layer passes over 200 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 44.5 | +0.0 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 2.0 | 20.0 | 28.5 | 28.5 | +16.0 |
| lookup | 14.5 | 28.5 | 39.5 | 39.5 | +5.0 |
| equation | 16.5 | 28.5 | 39.5 | 39.5 | +5.0 |
| equation_n100 | 16.5 | 28.5 | 39.5 | 39.5 | +5.0 |
| equation_n30 | 16.5 | 28.5 | 20.0 | 20.0 | +24.5 |
| equation_resolved | 16.5 | 28.5 | 39.5 | 39.5 | +5.0 |
| gated_equation | 16.5 | 28.5 | 28.5 | 28.5 | +16.0 |
| gated_equation_resolved | 16.5 | 28.5 | 28.5 | 28.5 | +16.0 |
| avg_gated_equation_resolved | 16.5 | 28.5 | 28.5 | 28.5 | +16.0 |
| avg_gated_lookup | 16.5 | 28.5 | 28.5 | 28.5 | +16.0 |
| avg_lookup | 14.5 | 28.5 | 39.5 | 39.5 | +5.0 |
| avg_equation | 16.5 | 16.5 | 39.5 | 39.5 | +5.0 |
| avg_equation_resolved | 14.5 | 28.5 | 39.5 | 39.5 | +5.0 |

The ORACLE GAP is the best single evaluation cell (depth 32 at cap 128, 44.5 points over 200 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3.

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 1836 vs 2049 (-10.4%) | 2924 vs 4097 (-28.6%) | 5676 vs 6146 (-7.6%) | 5676 vs 8195 (-30.7%) |
| avg_gated_lookup | 1836 vs 2049 (-10.4%) | 2924 vs 4097 (-28.6%) | 5676 vs 6146 (-7.6%) | 5676 vs 8195 (-30.7%) |
| avg_lookup | 1548 vs 2049 (-24.4%) | 2924 vs 4097 (-28.6%) | 5100 vs 6146 (-17.0%) | 5100 vs 8195 (-37.8%) |
| avg_equation | 1836 vs 2049 (-10.4%) | 1836 vs 4097 (-55.2%) | 5100 vs 6146 (-17.0%) | 5100 vs 8195 (-37.8%) |
| avg_equation_resolved | 1548 vs 2049 (-24.4%) | 2924 vs 4097 (-28.6%) | 5100 vs 6146 (-17.0%) | 5100 vs 8195 (-37.8%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 32 | k32_T0: 200 | 1452 | 542124 (over) vs 542124 (over) |
| 0.50x | deepest_depth_capped | 32 | k32_T16: 200 | 3564 | 542124 (over) vs 542124 (over) |
| 0.75x | deepest_depth_capped | 32 | k32_T32: 200 | 5676 | 542124 (over) vs 542124 (over) |
| 1.00x | deepest_depth_capped | 32 | k32_T32: 200 | 5676 | 542124 (over) vs 542124 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 32 | k32_T0: 200 | 1452 | 542124 (over) vs 542124 (over) |
| 0.50x | deepest_depth_capped | 32 | k32_T16: 200 | 3564 | 542124 (over) vs 542124 (over) |
| 0.75x | deepest_depth_capped | 32 | k32_T32: 200 | 5676 | 542124 (over) vs 542124 (over) |
| 1.00x | deepest_depth_capped | 32 | k32_T32: 200 | 5676 | 542124 (over) vs 542124 (over) |
- `avg_gated_equation_resolved` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 32, at the largest cap it affords) on family F2. Verification margin +23.3 points, sd 10.1, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 10.4% of the budget, 22.4% of the default cost. Mirror fold +11.4 points, sd 4.8 on 70 questions (clears).
- `avg_gated_equation_resolved` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 32, at the largest cap it affords) on family F2. Verification margin +6.7 points, sd 6.4, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 28.6% of the budget, 35.7% of the default cost. Mirror fold +4.3 points, sd 5.6 on 70 questions (clears).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap it affords) for every question. Verification margin -6.7 points, sd 8.2, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 7.6% of the budget, 69.3% of the default cost. Mirror fold +0.0 points, sd 0.0 on 70 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap it affords) for every question. Verification margin -6.7 points, sd 8.2, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 30.7% of the budget, 69.3% of the default cost. Mirror fold +0.0 points, sd 0.0 on 70 questions (fails).
- `avg_gated_lookup` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 32, at the largest cap it affords) on family F2. Verification margin +23.3 points, sd 10.1, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 10.4% of the budget, 22.4% of the default cost. Mirror fold +11.4 points, sd 4.8 on 70 questions (clears).
- `avg_gated_lookup` at 0.50x: deviated from normal operation at this budget (the deepest depth, depth 32, at the largest cap it affords) on family F2. Verification margin +6.7 points, sd 6.4, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 28.6% of the budget, 35.7% of the default cost. Mirror fold +4.3 points, sd 5.6 on 70 questions (clears).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap it affords) for every question. Verification margin -6.7 points, sd 8.2, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 7.6% of the budget, 69.3% of the default cost. Mirror fold +0.0 points, sd 0.0 on 70 questions (fails).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap it affords) for every question. Verification margin -6.7 points, sd 8.2, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 30.7% of the budget, 69.3% of the default cost. Mirror fold +0.0 points, sd 0.0 on 70 questions (fails).

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
