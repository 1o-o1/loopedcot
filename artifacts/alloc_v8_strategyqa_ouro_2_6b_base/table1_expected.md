# Table 1 -- strategyqa (ouro_2_6b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 29453 layer passes over 1990 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 74.8 | +0.3 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 72.1 | 74.9 | 74.9 | 74.8 | +0.3 |
| lookup | 74.7 | 74.7 | 74.7 | 74.7 | +0.5 |
| equation | 72.1 | 74.9 | 74.9 | 74.9 | +0.3 |
| equation_n100 | 72.1 | 74.9 | 74.9 | 74.9 | +0.3 |
| equation_n30 | 72.1 | 74.9 | 74.9 | 74.9 | +0.3 |
| equation_resolved | 74.7 | 74.7 | 74.7 | 74.7 | +0.5 |
| gated_equation | 72.1 | 74.9 | 74.9 | 74.8 | +0.3 |
| gated_equation_resolved | 72.1 | 74.9 | 75.1 | 75.1 | +0.0 |
| avg_gated_equation_resolved | 72.1 | 74.9 | 74.9 | 74.8 | +0.3 |
| avg_gated_lookup | 72.1 | 74.9 | 74.9 | 74.8 | +0.3 |
| avg_lookup | 74.7 | 74.7 | 74.7 | 74.7 | +0.5 |
| avg_equation | 72.1 | 74.9 | 74.9 | 74.9 | +0.3 |
| avg_equation_resolved | 74.7 | 74.7 | 74.7 | 74.7 | +0.5 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 128, 75.1 points over 1990 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F3. Of the families that CLEAR the bar the one that RUNS is set by `policy.GATE_FAMILY_RULE` = `best`: the cleared family with the largest mean verified margin over the folds, ties to the smaller family. The folds, the bar, the reference and the pricing are the same test under either rule; only which cleared family is taken differs.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 5568 vs 7363 (-24.4%) | 14128 vs 14727 (-4.1%) | 18682 vs 22090 (-15.4%) | 24580 vs 29453 (-16.5%) |
| avg_gated_lookup | 5568 vs 7363 (-24.4%) | 14128 vs 14727 (-4.1%) | 18682 vs 22090 (-15.4%) | 24580 vs 29453 (-16.5%) |
| avg_lookup | 2496 vs 7363 (-66.1%) | 11901 vs 14727 (-19.2%) | 11901 vs 22090 (-46.1%) | 11901 vs 29453 (-59.6%) |
| avg_equation | 5568 vs 7363 (-24.4%) | 14128 vs 14727 (-4.1%) | 18682 vs 22090 (-15.4%) | 18682 vs 29453 (-36.6%) |
| avg_equation_resolved | 2496 vs 7363 (-66.1%) | 11901 vs 14727 (-19.2%) | 11901 vs 22090 (-46.1%) | 11901 vs 29453 (-59.6%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T16: 1990 | 5568 | 36377 (over) vs 36377 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T256: 1990 | 14128 | 36377 (over) vs 36377 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T1024: 1990 | 18682 | 36377 (over) vs 36377 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T2048: 1990 | 24580 | 36377 (over) vs 36377 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T16: 1990 | 5568 | 36377 (over) vs 36377 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T256: 1990 | 14128 | 36377 (over) vs 36377 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T1024: 1990 | 18682 | 36377 (over) vs 36377 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T2048: 1990 | 24580 | 36377 (over) vs 36377 (over) |
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -4.4 points, sd 5.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 24.4% of the budget, 18.9% of the default cost. Mirror fold +0.0 points, sd 0.0 on 210 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 4.1% of the budget, 48.0% of the default cost. Mirror fold +0.0 points, sd 1.0 on 210 questions (fails).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +1.1 points, sd 1.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 15.4% of the budget, 63.4% of the default cost. Mirror fold +0.5 points, sd 1.1 on 210 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +1.1 points, sd 1.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 16.5% of the budget, 83.5% of the default cost. Mirror fold +0.5 points, sd 1.1 on 210 questions (fails).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin -4.4 points, sd 5.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 24.4% of the budget, 18.9% of the default cost. Mirror fold +1.0 points, sd 3.4 on 210 questions (fails).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +2.2 points, sd 2.2, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 4.1% of the budget, 48.0% of the default cost. Mirror fold +0.0 points, sd 1.0 on 210 questions (fails).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +3.3 points, sd 2.5, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 15.4% of the budget, 63.4% of the default cost. Mirror fold +0.5 points, sd 1.1 on 210 questions (fails).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +3.3 points, sd 2.5, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 16.5% of the budget, 83.5% of the default cost. Mirror fold +0.5 points, sd 1.1 on 210 questions (fails).
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 74.7 points at 40.4% of the default cost, 19.2% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 74.7 points at 40.4% of the default cost, 46.1% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 74.7 points at 40.4% of the default cost, 59.6% under the budget it was given.
- `avg_equation_resolved` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 74.7 points at 40.4% of the default cost, 19.2% under the budget it was given.
- `avg_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 74.7 points at 40.4% of the default cost, 46.1% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 74.7 points at 40.4% of the default cost, 59.6% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
