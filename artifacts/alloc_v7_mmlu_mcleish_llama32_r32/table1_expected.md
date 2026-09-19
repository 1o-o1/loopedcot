# Table 1 -- mmlu (mcleish_llama32_r32), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 16072 layer passes over 1700 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 37.4 | +1.1 |
| default_cell | n/a | n/a | n/a | 37.4 | +1.1 |
| default_at_budget | 37.7 | 37.2 | 37.5 | 37.4 | +1.1 |
| lookup | 36.7 | 36.7 | 36.7 | 36.7 | +1.8 |
| equation | 36.2 | 36.8 | 36.4 | 36.4 | +2.1 |
| equation_n100 | 36.2 | 36.8 | 36.4 | 36.4 | +2.1 |
| equation_n30 | 36.2 | 36.8 | 36.4 | 36.4 | +2.1 |
| equation_resolved | 36.7 | 36.7 | 36.7 | 36.7 | +1.8 |
| gated_equation | 36.2 | 36.8 | 36.4 | 36.4 | +2.1 |
| gated_equation_resolved | 36.7 | 37.2 | 36.7 | 36.7 | +1.8 |
| avg_gated_equation_resolved | 36.7 | 37.2 | 36.7 | 36.7 | +1.8 |
| avg_gated_lookup | 36.7 | 37.2 | 36.7 | 36.7 | +1.8 |
| avg_lookup | 36.7 | 36.7 | 36.7 | 36.7 | +1.8 |
| avg_equation | 36.2 | 36.2 | 36.4 | 36.4 | +2.1 |
| avg_equation_resolved | 36.7 | 36.7 | 36.7 | 36.7 | +1.8 |

The ORACLE GAP is the best single evaluation cell (depth 8 at cap 0, 38.5 points over 1700 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2.

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

The average-budget arms (`avg_gated_equation_resolved`, `avg_gated_lookup`, `avg_lookup`, `avg_equation`, `avg_equation_resolved`) hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_gated_equation_resolved | 1896 vs 4018 (-52.8%) | 5663 vs 8036 (-29.5%) | 1896 vs 12054 (-84.3%) | 1896 vs 16072 (-88.2%) |
| avg_gated_lookup | 1896 vs 4018 (-52.8%) | 5663 vs 8036 (-29.5%) | 1896 vs 12054 (-84.3%) | 1896 vs 16072 (-88.2%) |
| avg_lookup | 1896 vs 4018 (-52.8%) | 1896 vs 8036 (-76.4%) | 1896 vs 12054 (-84.3%) | 1896 vs 16072 (-88.2%) |
| avg_equation | 2648 vs 4018 (-34.1%) | 2648 vs 8036 (-67.1%) | 8786 vs 12054 (-27.1%) | 8786 vs 16072 (-45.3%) |
| avg_equation_resolved | 1896 vs 4018 (-52.8%) | 1896 vs 8036 (-76.4%) | 1896 vs 12054 (-84.3%) | 1896 vs 16072 (-88.2%) |

`avg_gated_lookup`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 8 | k8_T256: 1700 | 3656 | 13692 (over) vs 13692 (over) |
| 0.50x | deepest_depth_capped | 8 | k8_T1024: 1700 | 5663 | 13692 (over) vs 13692 (over) |
| 0.75x | deepest_depth_capped | 8 | k8_T2048: 1700 | 8340 | 13692 (over) vs 13692 (over) |
| 1.00x | default_cell | 8 | k8_T4096: 1700 | 13692 | 13692 (fits) vs 13692 (fits) |

`avg_gated_equation_resolved`'s gate measures its margin against NORMAL OPERATION AT THE BUDGET and returns to it when the margin fails: the deepest depth at the largest cap per question the budget affords ON AVERAGE. That is the default cell itself wherever the default cell is affordable on average, a stepped-down cap where it is not, and one depth shallower where not even the cheapest cap at the deepest depth fits. The affordability test reads the CALIBRATION mean price, so the two price columns below say when the evaluation half is the cheaper one and the default cell would have fitted there; the gate runs against the reference either way, and never leaves the row an ungated pick. What the gate ruled against, per budget:

| budget | rule | depth | reference cells over the evaluation questions | mean price | default cell cal vs eval |
|---|---|---|---|---|---|
| 0.25x | deepest_depth_capped | 8 | k8_T256: 1700 | 3656 | 13692 (over) vs 13692 (over) |
| 0.50x | deepest_depth_capped | 8 | k8_T1024: 1700 | 5663 | 13692 (over) vs 13692 (over) |
| 0.75x | deepest_depth_capped | 8 | k8_T2048: 1700 | 8340 | 13692 (over) vs 13692 (over) |
| 1.00x | default_cell | 8 | k8_T4096: 1700 | 13692 | 13692 (fits) vs 13692 (fits) |
- `avg_gated_equation_resolved` at 0.25x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 11.8% of the default cost, 52.8% under the budget it was given.
- `avg_gated_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 11.8% of the default cost, 84.3% under the budget it was given.
- `avg_gated_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 11.8% of the default cost, 88.2% under the budget it was given.
- `avg_gated_equation_resolved` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) on family F2. Verification margin +3.3 points, sd 5.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 52.8% of the budget, 11.8% of the default cost. Mirror fold +3.8 points, sd 3.5 on 210 questions (clears).
- `avg_gated_equation_resolved` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +2.2 points, sd 5.3, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 29.5% of the budget, 35.2% of the default cost. Mirror fold +3.3 points, sd 3.2 on 210 questions (clears).
- `avg_gated_equation_resolved` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) on family F2. Verification margin +3.3 points, sd 5.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 84.3% of the budget, 11.8% of the default cost. Mirror fold +2.9 points, sd 3.3 on 210 questions (clears).
- `avg_gated_equation_resolved` at 1.00x: deviated from the default cell on family F2. Verification margin +3.3 points, sd 5.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 88.2% of the budget, 11.8% of the default cost. Mirror fold +2.9 points, sd 3.3 on 210 questions (clears).
- `avg_gated_lookup` at 0.25x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 11.8% of the default cost, 52.8% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 11.8% of the default cost, 84.3% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 11.8% of the default cost, 88.2% under the budget it was given.
- `avg_gated_lookup` at 0.25x: deviated from normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) on family F2. Verification margin +3.3 points, sd 5.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 52.8% of the budget, 11.8% of the default cost. Mirror fold +3.8 points, sd 3.5 on 210 questions (clears).
- `avg_gated_lookup` at 0.50x: reverted to normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) for every question. Verification margin +2.2 points, sd 5.3, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 29.5% of the budget, 35.2% of the default cost. Mirror fold +4.8 points, sd 3.3 on 210 questions (clears).
- `avg_gated_lookup` at 0.75x: deviated from normal operation at this budget (the deepest depth, depth 8, at the largest cap whose mean price fits it) on family F2. Verification margin +3.3 points, sd 5.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 84.3% of the budget, 11.8% of the default cost. Mirror fold +4.3 points, sd 3.4 on 210 questions (clears).
- `avg_gated_lookup` at 1.00x: deviated from the default cell on family F2. Verification margin +3.3 points, sd 5.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 88.2% of the budget, 11.8% of the default cost. Mirror fold +4.3 points, sd 3.4 on 210 questions (clears).
- `avg_lookup` at 0.25x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 11.8% of the default cost, 52.8% under the budget it was given.
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 11.8% of the default cost, 76.4% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 11.8% of the default cost, 84.3% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 11.8% of the default cost, 88.2% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 36.4 points at 54.7% of the default cost, 27.1% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 36.4 points at 54.7% of the default cost, 45.3% under the budget it was given.
- `avg_equation_resolved` at 0.25x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 11.8% of the default cost, 52.8% under the budget it was given.
- `avg_equation_resolved` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 11.8% of the default cost, 76.4% under the budget it was given.
- `avg_equation_resolved` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 11.8% of the default cost, 84.3% under the budget it was given.
- `avg_equation_resolved` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 11.8% of the default cost, 88.2% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
