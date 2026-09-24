# Table 1 -- strategyqa (ouro_1_4b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 103179 layer passes over 1990 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 71.8 | +0.3 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 69.7 | 72.1 | 72.1 | 71.9 | +0.2 |
| lookup | 69.7 | 71.0 | 71.0 | 71.0 | +1.1 |
| equation | 69.7 | 72.1 | 71.0 | 71.9 | +0.2 |
| equation_n100 | 69.7 | 72.1 | 72.1 | 71.9 | +0.2 |
| equation_n30 | 69.7 | 72.1 | 72.1 | 71.9 | +0.2 |
| equation_resolved | 69.7 | 71.0 | 71.0 | 71.0 | +1.1 |
| gated_equation | 69.7 | 72.1 | 72.1 | 71.9 | +0.2 |
| gated_equation_resolved | 69.7 | 72.1 | 72.1 | 71.9 | +0.2 |
| avg_gated_equation_resolved | 69.7 | 72.1 | 72.1 | 71.9 | +0.2 |
| avg_gated_lookup | 69.7 | 72.1 | 72.1 | 71.9 | +0.2 |
| avg_lookup | 69.7 | 71.0 | 71.0 | 71.0 | +1.1 |
| avg_equation | 69.7 | 72.1 | 71.0 | 71.9 | +0.2 |
| avg_equation_resolved | 69.7 | 71.0 | 71.0 | 71.0 | +1.1 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 512, 72.1 points over 1990 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none. Of the families that CLEAR the bar the one that RUNS is set by `policy.GATE_FAMILY_RULE` = `best`: the cleared family with the largest mean verified margin over the folds, ties to the smaller family. The folds, the bar, the reference and the pricing are the same test under either rule; only which cleared family is taken differs.

`default_cell` is the default operating point (depth 4 at cap 8192) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 13632 vs 25795 (-47.2%) | 50496 vs 51589 (-2.1%) | 50496 vs 77384 (-34.7%) | 99648 vs 103179 (-3.4%) |
| avg_gated_lookup | 13632 vs 25795 (-47.2%) | 50496 vs 51589 (-2.1%) | 50496 vs 77384 (-34.7%) | 99648 vs 103179 (-3.4%) |
| avg_lookup | 13632 vs 25795 (-47.2%) | 25920 vs 51589 (-49.8%) | 74736 vs 77384 (-3.4%) | 74736 vs 103179 (-27.6%) |
| avg_equation | 13632 vs 25795 (-47.2%) | 50496 vs 51589 (-2.1%) | 74736 vs 77384 (-3.4%) | 99648 vs 103179 (-3.4%) |
| avg_equation_resolved | 13632 vs 25795 (-47.2%) | 25920 vs 51589 (-49.8%) | 74736 vs 77384 (-3.4%) | 74736 vs 103179 (-27.6%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 1990 | 13632 | 787776 (over) vs 787776 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T512: 1990 | 50496 | 787776 (over) vs 787776 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T512: 1990 | 50496 | 787776 (over) vs 787776 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T1024: 1990 | 99648 | 787776 (over) vs 787776 (over) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 4 | k4_T128: 1990 | 13632 | 787776 (over) vs 787776 (over) |
| 0.50x | deepest_depth_capped | 4 | k4_T512: 1990 | 50496 | 787776 (over) vs 787776 (over) |
| 0.75x | deepest_depth_capped | 4 | k4_T512: 1990 | 50496 | 787776 (over) vs 787776 (over) |
| 1.00x | deepest_depth_capped | 4 | k4_T1024: 1990 | 99648 | 787776 (over) vs 787776 (over) |
- `avg_gated_equation_resolved` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 47.2% of the budget, 13.2% of the default cost. Mirror fold -2.4 points, sd 3.0 on 210 questions (fails).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 3.2, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 2.1% of the budget, 48.9% of the default cost. Mirror fold -5.7 points, sd 3.4 on 210 questions (fails).
- `avg_gated_equation_resolved` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 3.2, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 34.7% of the budget, 48.9% of the default cost. Mirror fold -0.5 points, sd 3.1 on 210 questions (fails).
- `avg_gated_equation_resolved` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 3.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 3.4% of the budget, 96.6% of the default cost. Mirror fold -0.5 points, sd 3.0 on 210 questions (fails).
- `avg_gated_lookup` at 0.25x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 47.2% of the budget, 13.2% of the default cost. Mirror fold -2.4 points, sd 3.0 on 210 questions (fails).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 3.2, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 2.1% of the budget, 48.9% of the default cost. Mirror fold -5.7 points, sd 3.4 on 210 questions (fails).
- `avg_gated_lookup` at 0.75x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 3.2, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 34.7% of the budget, 48.9% of the default cost. Mirror fold -0.5 points, sd 3.1 on 210 questions (fails).
- `avg_gated_lookup` at 1.00x: reverted to normal operation at this budget (the deepest depth, depth 4, at the largest cap whose mean price fits it) for every question. Verification margin +0.0 points, sd 3.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 3.4% of the budget, 96.6% of the default cost. Mirror fold -0.5 points, sd 3.0 on 210 questions (fails).

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
