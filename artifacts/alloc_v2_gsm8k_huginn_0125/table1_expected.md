# Table 1 -- gsm8k (huginn_0125), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 104580 layer passes over 1219 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 26.3 |
| default_cell | n/a | n/a | n/a | 27.2 (95%) |
| default_at_budget | n/a | n/a | 2.1 (12%) | 26.3 |
| lookup | 7.9 | 21.5 | 21.3 | 26.5 |
| equation | 8.1 | 21.3 | 21.2 | 26.5 |
| equation_n30 | 8.0 | 21.4 | 21.2 | 26.5 |
| equation_n100 | 8.1 | 21.3 | 21.2 | 26.5 |
| gated_equation | 8.1 | 21.3 | 21.2 | 26.4 |
| avg_lookup | 13.8 | 22.4 | 24.6 | 26.4 |
| avg_equation | 13.0 | 21.4 | 24.6 | 26.4 |
| avg_gated_lookup | 13.8 | 22.4 | 24.6 | 26.3 |

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 26271 vs 26145 (+0.5%) | 52055 vs 52290 (-0.4%) | 78041 vs 78435 (-0.5%) | 94504 vs 104580 (-9.6%) |
| avg_equation | 25362 vs 26145 (-3.0%) | 52074 vs 52290 (-0.4%) | 77863 vs 78435 (-0.7%) | 95263 vs 104580 (-8.9%) |
| avg_gated_lookup | 26271 vs 26145 (+0.5%) | 52055 vs 52290 (-0.4%) | 78041 vs 78435 (-0.5%) | 99015 vs 104580 (-5.3%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 26.4 points at 90.4% of the default cost, 9.6% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 26.4 points at 91.1% of the default cost, 8.9% under the budget it was given.
- `avg_gated_lookup` reverted to the default cell for every question at 1.00x: the predicted calibration margin did not clear 0.50 of its own SD.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
