# Table 1 -- math500 (ouro_2_6b_base), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 148998 layer passes over 400 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 56.0 | +0.0 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 47.2 | 53.0 | 55.5 | 55.5 | +0.5 |
| lookup | 47.2 | 53.0 | 53.5 | 53.5 | +2.5 |
| equation | 47.2 | 53.0 | 55.5 | 55.5 | +0.5 |
| equation_n100 | 47.2 | 53.0 | 55.5 | 55.5 | +0.5 |
| equation_n30 | 35.5 | 49.0 | 53.2 | 53.2 | +2.8 |
| equation_resolved | 47.2 | 53.0 | 53.5 | 53.5 | +2.5 |
| gated_equation | 47.2 | 53.0 | 55.5 | 55.5 | +0.5 |
| gated_equation_resolved | 47.2 | 53.0 | 55.5 | 55.5 | +0.5 |
| avg_gated_equation_resolved | 47.2 | 53.0 | 55.5 | 55.5 | +0.5 |
| avg_gated_lookup | 47.2 | 53.0 | 55.5 | 55.5 | +0.5 |
| avg_lookup | 47.2 | 53.0 | 53.5 | 53.5 | +2.5 |
| avg_equation | 40.8 | 53.0 | 53.5 | 53.5 | +2.5 |
| avg_equation_resolved | 47.2 | 48.5 | 53.5 | 53.5 | +2.5 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 4096, 56.0 points over 400 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 31488 vs 37249 (-15.5%) | 56064 vs 74499 (-24.7%) | 105216 vs 111748 (-5.8%) | 105216 vs 148998 (-29.4%) |
| avg_gated_lookup | 31488 vs 37249 (-15.5%) | 56064 vs 74499 (-24.7%) | 105216 vs 111748 (-5.8%) | 105216 vs 148998 (-29.4%) |
| avg_lookup | 31488 vs 37249 (-15.5%) | 56064 vs 74499 (-24.7%) | 78912 vs 111748 (-29.4%) | 78912 vs 148998 (-47.0%) |
| avg_equation | 23616 vs 37249 (-36.6%) | 56064 vs 74499 (-24.7%) | 78912 vs 111748 (-29.4%) | 78912 vs 148998 (-47.0%) |
| avg_equation_resolved | 31488 vs 37249 (-15.5%) | 42048 vs 74499 (-43.6%) | 78912 vs 111748 (-29.4%) | 78912 vs 148998 (-47.0%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 400 | 31488 | 793344 (over) vs 793344 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T256: 400 | 56064 | 793344 (over) vs 793344 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T512: 400 | 105216 | 793344 (over) vs 793344 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T512: 400 | 105216 | 793344 (over) vs 793344 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 400 | 31488 | 793344 (over) vs 793344 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T256: 400 | 56064 | 793344 (over) vs 793344 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T512: 400 | 105216 | 793344 (over) vs 793344 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T512: 400 | 105216 | 793344 (over) vs 793344 (over) |
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin -6.7 points, sd 4.6, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 15.5% of the budget, 21.1% of the default cost. Mirror fold +0.0 points, sd 0.0 on 70 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 24.7% of the budget, 37.6% of the default cost. Mirror fold -4.3 points, sd 4.6 on 70 questions (fails).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin +10.0 points, sd 5.4, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 5.8% of the budget, 70.6% of the default cost. Mirror fold -1.4 points, sd 5.1 on 70 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin +10.0 points, sd 5.4, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 29.4% of the budget, 70.6% of the default cost. Mirror fold -1.4 points, sd 5.1 on 70 questions (fails).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 15.5% of the budget, 21.1% of the default cost. Mirror fold -17.1 points, sd 5.4 on 70 questions (fails).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 24.7% of the budget, 37.6% of the default cost. Mirror fold -4.3 points, sd 4.6 on 70 questions (fails).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 5.8% of the budget, 70.6% of the default cost. Mirror fold -1.4 points, sd 5.1 on 70 questions (fails).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap it affords) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 29.4% of the budget, 70.6% of the default cost. Mirror fold -1.4 points, sd 5.1 on 70 questions (fails).
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 53.5 points at 53.0% of the default cost, 29.4% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 53.5 points at 53.0% of the default cost, 47.0% under the budget it was given.
- `avg_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 53.5 points at 53.0% of the default cost, 29.4% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 53.5 points at 53.0% of the default cost, 47.0% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
