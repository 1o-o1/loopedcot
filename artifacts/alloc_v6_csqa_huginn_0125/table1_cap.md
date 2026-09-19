# Table 1 -- csqa (huginn_0125), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 6894 layer passes over 977 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 42.8 | +0.0 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 39.9 | 39.9 | 36.5 | 42.0 | +0.8 |
| lookup | 39.9 | 39.1 | 39.1 | 42.0 | +0.8 |
| equation | 39.9 | 39.1 | 39.1 | 41.7 | +1.1 |
| equation_n100 | 39.9 | 39.1 | 39.1 | 41.7 | +1.1 |
| equation_n30 | 39.9 | 39.1 | 39.1 | 41.7 | +1.1 |
| equation_resolved | 39.9 | 39.1 | 39.1 | 42.0 | +0.8 |
| gated_equation | 39.9 | 39.9 | 36.5 | 42.0 | +0.8 |
| gated_equation_resolved | 39.9 | 39.9 | 36.5 | 42.0 | +0.8 |
| avg_gated_equation_resolved | 39.9 | 39.9 | 36.5 | 42.0 | +0.8 |
| avg_gated_lookup | 39.9 | 39.9 | 36.5 | 42.0 | +0.8 |
| avg_lookup | 39.9 | 39.1 | 39.1 | 42.0 | +0.8 |
| avg_equation | 36.7 | 39.1 | 39.1 | 41.7 | +1.1 |
| avg_equation_resolved | 39.9 | 39.1 | 39.1 | 42.0 | +0.8 |

The ORACLE GAP is the best single evaluation cell (depth 32 at cap 64, 42.8 points over 977 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none.

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 1716 vs 1723 (-0.4%) | 1716 vs 3447 (-50.2%) | 3828 vs 5170 (-26.0%) | 5940 vs 6894 (-13.8%) |
| avg_gated_lookup | 1716 vs 1723 (-0.4%) | 1716 vs 3447 (-50.2%) | 3828 vs 5170 (-26.0%) | 5940 vs 6894 (-13.8%) |
| avg_lookup | 1716 vs 1723 (-0.4%) | 3060 vs 3447 (-11.2%) | 3060 vs 5170 (-40.8%) | 5940 vs 6894 (-13.8%) |
| avg_equation | 884 vs 1723 (-48.7%) | 3060 vs 3447 (-11.2%) | 3060 vs 5170 (-40.8%) | 5236 vs 6894 (-24.0%) |
| avg_equation_resolved | 1716 vs 1723 (-0.4%) | 3060 vs 3447 (-11.2%) | 3060 vs 5170 (-40.8%) | 5940 vs 6894 (-13.8%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 32 | k32_T0: 977 | 1716 | 542388 (over) vs 542388 (over) |
| 0.50x | deepest_depth_capped | 32 | k32_T0: 977 | 1716 | 542388 (over) vs 542388 (over) |
| 0.75x | deepest_depth_capped | 32 | k32_T16: 977 | 3828 | 542388 (over) vs 542388 (over) |
| 1.00x | deepest_depth_capped | 32 | k32_T32: 977 | 5940 | 542388 (over) vs 542388 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 32 | k32_T0: 977 | 1716 | 542388 (over) vs 542388 (over) |
| 0.50x | deepest_depth_capped | 32 | k32_T0: 977 | 1716 | 542388 (over) vs 542388 (over) |
| 0.75x | deepest_depth_capped | 32 | k32_T16: 977 | 3828 | 542388 (over) vs 542388 (over) |
| 1.00x | deepest_depth_capped | 32 | k32_T32: 977 | 5940 | 542388 (over) vs 542388 (over) |
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 0.4% of the budget, 24.9% of the default cost. Mirror fold +0.0 points, sd 0.0 on 171 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 6.5, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 50.2% of the budget, 24.9% of the default cost. Mirror fold +0.0 points, sd 0.0 on 171 questions (fails).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap it affords) for every question. Verification margin +2.7 points, sd 6.5, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 26.0% of the budget, 55.5% of the default cost. Mirror fold +8.2 points, sd 3.4 on 171 questions (clears).
- `avg_gated_equation_resolved` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 13.8% of the budget, 86.2% of the default cost. Mirror fold +0.0 points, sd 0.0 on 171 questions (fails).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 0.4% of the budget, 24.9% of the default cost. Mirror fold +0.0 points, sd 0.0 on 171 questions (fails).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 6.5, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 50.2% of the budget, 24.9% of the default cost. Mirror fold +0.0 points, sd 0.0 on 171 questions (fails).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap it affords) for every question. Verification margin +2.7 points, sd 6.5, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 26.0% of the budget, 55.5% of the default cost. Mirror fold +8.2 points, sd 3.4 on 171 questions (clears).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 13.8% of the budget, 86.2% of the default cost. Mirror fold +0.0 points, sd 0.0 on 171 questions (fails).
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 42.0 points at 86.2% of the default cost, 13.8% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 42.0 points at 86.2% of the default cost, 13.8% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
