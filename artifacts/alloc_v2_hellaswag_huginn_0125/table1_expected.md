# Table 1 -- hellaswag (huginn_0125), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 116966 layer passes over 1900 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 34.4 |
| default_cell | n/a | n/a | n/a | 41.2 (51%) |
| default_at_budget | n/a | n/a | 57.1 (12%) | 34.9 (100%) |
| lookup | 27.8 | 39.1 | 39.4 | 40.3 |
| equation | 28.1 | 33.6 | 33.0 | 33.0 |
| equation_n30 | 28.1 | 33.6 | 33.0 | 33.0 |
| equation_n100 | 28.1 | 33.6 | 33.0 | 33.0 |
| gated_equation | 28.1 | 33.6 | 33.3 | 34.6 |
| avg_lookup | 33.8 | 39.4 | 39.9 | 40.3 |
| avg_equation | 31.3 | 33.0 | 33.0 | 33.0 |
| avg_gated_lookup | 33.8 | 39.4 | 39.9 | 40.3 |

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 26834 vs 29241 (-8.2%) | 56146 vs 58483 (-4.0%) | 87098 vs 87724 (-0.7%) | 102349 vs 116966 (-12.5%) |
| avg_equation | 25664 vs 29241 (-12.2%) | 59588 vs 58483 (+1.9%) | 62244 vs 87724 (-29.0%) | 62244 vs 116966 (-46.8%) |
| avg_gated_lookup | 26834 vs 29241 (-8.2%) | 56146 vs 58483 (-4.0%) | 87098 vs 87724 (-0.7%) | 102349 vs 116966 (-12.5%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 40.3 points at 87.5% of the default cost, 12.5% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 33.0 points at 53.2% of the default cost, 29.0% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 33.0 points at 53.2% of the default cost, 46.8% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 40.3 points at 87.5% of the default cost, 12.5% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
