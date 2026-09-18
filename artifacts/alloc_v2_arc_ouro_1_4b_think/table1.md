# Table 1 -- arc (ouro_1_4b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 85662 layer passes over 1072 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 93.4 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 87.2 (98%) | 89.0 | 90.6 |
| lookup | 74.4 | 86.3 | 89.6 | 89.6 |
| equation | 74.6 | 84.2 | 90.6 | 93.1 |
| equation_n30 | 74.6 | 84.1 | 90.2 | 93.1 |
| equation_n100 | 74.6 | 84.2 | 90.6 | 93.1 |
| gated_equation | 74.6 | 84.2 | 90.6 | 93.1 |
| avg_lookup | 74.5 | 88.2 | 89.6 | 89.6 |
| avg_equation | 76.5 | 88.9 | 92.8 | 93.5 |
| avg_gated_lookup | 74.5 | 88.2 | 89.6 | 89.6 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 21166 vs 21415 (-1.2%) | 42199 vs 42831 (-1.5%) | 46197 vs 64246 (-28.1%) | 46197 vs 85662 (-46.1%) |
| avg_equation | 21252 vs 21415 (-0.8%) | 41838 vs 42831 (-2.3%) | 62996 vs 64246 (-1.9%) | 84161 vs 85662 (-1.8%) |
| avg_gated_lookup | 21166 vs 21415 (-1.2%) | 42199 vs 42831 (-1.5%) | 46197 vs 64246 (-28.1%) | 46197 vs 85662 (-46.1%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 89.6 points at 53.9% of the default cost, 28.1% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 89.6 points at 53.9% of the default cost, 46.1% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 89.6 points at 53.9% of the default cost, 28.1% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 89.6 points at 53.9% of the default cost, 46.1% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
