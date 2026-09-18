# Table 1 -- bbh (ouro_1_4b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 182991 layer passes over 2337 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 84.4 |
| default_cell | n/a | n/a | 69.6 (10%) | 83.4 (72%) |
| default_at_budget | 66.2 (10%) | 52.8 (72%) | 66.6 | 84.2 |
| lookup | 35.1 | 66.9 | 81.3 | 82.5 |
| equation | 35.5 | 66.9 | 81.0 | 83.4 |
| equation_n30 | 35.5 | 66.9 | 81.3 | 82.5 |
| equation_n100 | 35.5 | 66.9 | 81.0 | 83.4 |
| gated_equation | 35.5 | 66.7 | 79.5 | 83.3 |
| avg_lookup | 45.5 | 74.1 | 82.5 | 82.5 |
| avg_equation | 43.9 | 75.9 | 81.7 | 84.4 |
| avg_gated_lookup | 35.8 | 77.3 | 80.3 | 84.4 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 47551 vs 45748 (+3.9%) | 91402 vs 91495 (-0.1%) | 136068 vs 137243 (-0.9%) | 155563 vs 182991 (-15.0%) |
| avg_equation | 47332 vs 45748 (+3.5%) | 92646 vs 91495 (+1.3%) | 137464 vs 137243 (+0.2%) | 173767 vs 182991 (-5.0%) |
| avg_gated_lookup | 34781 vs 45748 (-24.0%) | 101632 vs 91495 (+11.1%) | 111504 vs 137243 (-18.8%) | 173767 vs 182991 (-5.0%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 82.5 points at 85.0% of the default cost, 15.0% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 84.4 points at 95.0% of the default cost, 5.0% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 80.3 points at 60.9% of the default cost, 18.8% under the budget it was given.
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin -10.0 points, sd 5.6, bar 0.50 sd (30 verification questions, the ids after the 50 that fit, out of 100 calibration); cost saving 5.0% of the budget, 95.0% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
