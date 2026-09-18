# Table 1 -- gsm8k (ouro_2_6b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 151460 layer passes over 1219 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 82.7 |
| default_cell | n/a | n/a | n/a | 84.3 (87%) |
| default_at_budget | n/a | n/a | n/a | 77.9 |
| lookup | 29.8 | 68.7 | 76.9 | 82.0 |
| equation | 29.9 | 68.9 | 77.4 | 82.0 |
| equation_n30 | 29.9 | 68.9 | 77.4 | 82.0 |
| equation_n100 | 29.9 | 68.9 | 77.4 | 82.0 |
| gated_equation | 29.9 | 68.9 | 77.4 | 82.1 |
| avg_lookup | 31.7 | 73.6 | 78.9 | 82.3 |
| avg_equation | 31.7 | 74.5 | 78.1 | 82.3 |
| avg_gated_lookup | 31.7 | 73.6 | 78.9 | 82.7 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 37683 vs 37865 (-0.5%) | 75590 vs 75730 (-0.2%) | 113426 vs 113595 (-0.1%) | 146701 vs 151460 (-3.1%) |
| avg_equation | 37686 vs 37865 (-0.5%) | 75807 vs 75730 (+0.1%) | 110285 vs 113595 (-2.9%) | 146701 vs 151460 (-3.1%) |
| avg_gated_lookup | 37683 vs 37865 (-0.5%) | 75590 vs 75730 (-0.2%) | 113426 vs 113595 (-0.1%) | 146701 vs 151460 (-3.1%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 82.3 points at 96.9% of the default cost, 3.1% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 82.3 points at 96.9% of the default cost, 3.1% under the budget it was given.
- `avg_gated_lookup` reverted to the default cell for every question at 1.00x: the predicted calibration margin did not clear 0.50 of its own SD.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
