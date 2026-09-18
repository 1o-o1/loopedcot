# Table 1 -- svamp (ouro_2_6b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 249394 layer passes over 200 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 7.0 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 5.6 (45%) | 12.5 | 7.0 |
| lookup | 68.0 | 68.5 | 68.5 | 68.5 |
| equation | 68.0 | 68.5 | 68.5 | 68.5 |
| equation_n30 | 68.0 | 68.5 | 68.5 | 68.5 |
| equation_n100 | 68.0 | 68.5 | 68.5 | 68.5 |
| gated_equation | 68.0 | 68.5 | 68.5 | 68.5 |
| avg_lookup | 68.5 | 68.5 | 68.5 | 68.5 |
| avg_equation | 68.0 | 68.5 | 68.5 | 68.5 |
| avg_gated_lookup | 68.5 | 68.5 | 68.5 | 68.5 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 62766 vs 62348 (+0.7%) | 80460 vs 124697 (-35.5%) | 80460 vs 187045 (-57.0%) | 80460 vs 249394 (-67.7%) |
| avg_equation | 60062 vs 62348 (-3.7%) | 104053 vs 124697 (-16.6%) | 104053 vs 187045 (-44.4%) | 227916 vs 249394 (-8.6%) |
| avg_gated_lookup | 62766 vs 62348 (+0.7%) | 80460 vs 124697 (-35.5%) | 80460 vs 187045 (-57.0%) | 80460 vs 249394 (-67.7%) |
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 32.3% of the default cost, 35.5% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 32.3% of the default cost, 57.0% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 32.3% of the default cost, 67.7% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 91.4% of the default cost, 8.6% under the budget it was given.
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 32.3% of the default cost, 35.5% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 32.3% of the default cost, 57.0% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 32.3% of the default cost, 67.7% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
