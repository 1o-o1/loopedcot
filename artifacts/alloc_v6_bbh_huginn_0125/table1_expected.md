# Table 1 -- bbh (huginn_0125), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 37633 layer passes over 2137 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 35.6 | +0.1 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 30.7 | 33.5 | 35.6 | 35.5 | +0.1 |
| lookup | 31.8 | 31.8 | 35.0 | 35.0 | +0.6 |
| equation | 33.1 | 33.5 | 35.6 | 35.5 | +0.1 |
| equation_n100 | 30.7 | 33.5 | 35.6 | 35.5 | +0.1 |
| equation_n30 | 31.8 | 31.8 | 31.8 | 31.8 | +3.8 |
| equation_resolved | 31.8 | 31.8 | 35.7 | 35.7 | +0.0 |
| gated_equation | 30.7 | 33.5 | 35.6 | 35.5 | +0.1 |
| gated_equation_resolved | 30.7 | 33.5 | 35.6 | 35.5 | +0.1 |
| avg_gated_equation_resolved | 30.7 | 31.6 | 35.6 | 35.6 | +0.1 |
| avg_gated_lookup | 30.7 | 31.6 | 35.6 | 35.6 | +0.1 |
| avg_lookup | 31.8 | 31.8 | 35.0 | 35.0 | +0.6 |
| avg_equation | 29.1 | 35.3 | 35.6 | 35.6 | +0.1 |
| avg_equation_resolved | 31.8 | 31.8 | 35.0 | 35.0 | +0.6 |

The ORACLE GAP is the best single evaluation cell (depth 32 at cap 512, 35.7 points over 2137 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none.

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 6783 vs 9408 (-27.9%) | 11985 vs 18817 (-36.3%) | 27943 vs 28225 (-1.0%) | 29045 vs 37633 (-22.8%) |
| avg_gated_lookup | 6783 vs 9408 (-27.9%) | 11985 vs 18817 (-36.3%) | 27943 vs 28225 (-1.0%) | 29045 vs 37633 (-22.8%) |
| avg_lookup | 4192 vs 9408 (-55.4%) | 4192 vs 18817 (-77.7%) | 21031 vs 28225 (-25.5%) | 21031 vs 37633 (-44.1%) |
| avg_equation | 534 vs 9408 (-94.3%) | 12541 vs 18817 (-33.4%) | 27943 vs 28225 (-1.0%) | 37546 vs 37633 (-0.2%) |
| avg_equation_resolved | 4192 vs 9408 (-55.4%) | 4192 vs 18817 (-77.7%) | 21031 vs 28225 (-25.5%) | 21031 vs 37633 (-44.1%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 32 | k32_T32: 1917, k32_T64: 220 | 6783 | 38859 (over) vs 38648 (over) |
| 0.50x | deepest_depth_capped | 32 | k32_T1024: 220, k32_T64: 1917 | 11985 | 38859 (over) vs 38648 (over) |
| 0.75x | deepest_depth_capped | 32 | k32_T1024: 2137 | 27943 | 38859 (over) vs 38648 (over) |
| 1.00x | deepest_depth_capped | 32 | k32_T1024: 1917, k32_T4096: 220 | 29045 | 38859 (over) vs 38648 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 32 | k32_T32: 1917, k32_T64: 220 | 6783 | 38859 (over) vs 38648 (over) |
| 0.50x | deepest_depth_capped | 32 | k32_T1024: 220, k32_T64: 1917 | 11985 | 38859 (over) vs 38648 (over) |
| 0.75x | deepest_depth_capped | 32 | k32_T1024: 2137 | 27943 | 38859 (over) vs 38648 (over) |
| 1.00x | deepest_depth_capped | 32 | k32_T1024: 1917, k32_T4096: 220 | 29045 | 38859 (over) vs 38648 (over) |
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap it affords) for every question. Verification margin -5.6 points, sd 5.2, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 27.9% of the budget, 18.0% of the default cost. Mirror fold -1.0 points, sd 0.7 on 210 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap it affords) for every question. Verification margin -1.1 points, sd 4.4, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 36.3% of the budget, 31.8% of the default cost. Mirror fold +4.8 points, sd 2.5 on 210 questions (clears).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap it affords) for every question. Verification margin -2.2 points, sd 5.8, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 1.0% of the budget, 74.3% of the default cost. Mirror fold -3.8 points, sd 1.9 on 210 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap it affords) for every question. Verification margin -2.2 points, sd 5.8, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 22.8% of the budget, 77.2% of the default cost. Mirror fold -3.8 points, sd 1.9 on 210 questions (fails).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap it affords) for every question. Verification margin -5.6 points, sd 5.2, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 27.9% of the budget, 18.0% of the default cost. Mirror fold -8.1 points, sd 3.1 on 210 questions (fails).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap it affords) for every question. Verification margin -1.1 points, sd 4.4, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 36.3% of the budget, 31.8% of the default cost. Mirror fold +4.8 points, sd 2.5 on 210 questions (clears).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap it affords) for every question. Verification margin -2.2 points, sd 5.8, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 1.0% of the budget, 74.3% of the default cost. Mirror fold -3.8 points, sd 1.9 on 210 questions (fails).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 32, at the largest cap it affords) for every question. Verification margin -2.2 points, sd 5.8, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 22.8% of the budget, 77.2% of the default cost. Mirror fold -3.8 points, sd 1.9 on 210 questions (fails).
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 35.0 points at 55.9% of the default cost, 25.5% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 35.0 points at 55.9% of the default cost, 44.1% under the budget it was given.
- `avg_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 35.0 points at 55.9% of the default cost, 25.5% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 35.0 points at 55.9% of the default cost, 44.1% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
