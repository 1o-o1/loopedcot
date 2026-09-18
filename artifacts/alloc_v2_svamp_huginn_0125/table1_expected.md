# Table 1 -- svamp (huginn_0125), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 84875 layer passes over 200 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 44.5 |
| default_cell | n/a | n/a | n/a | 58.8 (40%) |
| default_at_budget | n/a | n/a | n/a | 40.0 |
| lookup | 4.5 | 27.5 | 39.5 | 39.5 |
| equation | 3.5 | 28.0 | 39.5 | 41.0 |
| equation_n30 | 3.5 | 20.0 | 20.0 | 20.0 |
| equation_n100 | 3.5 | 28.0 | 39.5 | 41.0 |
| gated_equation | 3.5 | 28.0 | 39.5 | 41.0 |
| avg_lookup | 18.0 | 38.0 | 39.5 | 39.5 |
| avg_equation | 19.5 | 38.0 | 41.5 | 45.0 |
| avg_gated_lookup | 18.0 | 38.0 | 39.5 | 39.5 |

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 21280 vs 21219 (+0.3%) | 42712 vs 42438 (+0.6%) | 43791 vs 63657 (-31.2%) | 43791 vs 84875 (-48.4%) |
| avg_equation | 21562 vs 21219 (+1.6%) | 42728 vs 42438 (+0.7%) | 67841 vs 63657 (+6.6%) | 83838 vs 84875 (-1.2%) |
| avg_gated_lookup | 21280 vs 21219 (+0.3%) | 42712 vs 42438 (+0.6%) | 43791 vs 63657 (-31.2%) | 43791 vs 84875 (-48.4%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 39.5 points at 51.6% of the default cost, 31.2% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 39.5 points at 51.6% of the default cost, 48.4% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 39.5 points at 51.6% of the default cost, 31.2% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 39.5 points at 51.6% of the default cost, 48.4% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
