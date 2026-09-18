# Table 1 -- math500 (mcleish_llama32_r32), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 96379 layer passes over 400 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 30.2 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | 30.6 (99%) | 30.0 |
| lookup | 23.2 | 32.0 | 28.7 | 28.7 |
| equation | 26.2 | 30.8 | 30.8 | 30.8 |
| equation_n30 | 26.2 | 30.8 | 29.8 | 30.0 |
| equation_n100 | 26.2 | 30.8 | 30.8 | 30.8 |
| gated_equation | 26.2 | 30.8 | 30.8 | 30.8 |
| avg_lookup | 26.5 | 30.8 | 28.7 | 28.7 |
| avg_equation | 24.8 | 30.8 | 30.2 | 31.0 |
| avg_gated_lookup | 26.5 | 30.8 | 28.7 | 28.7 |

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 24717 vs 24095 (+2.6%) | 49327 vs 48189 (+2.4%) | 62558 vs 72284 (-13.5%) | 62558 vs 96379 (-35.1%) |
| avg_equation | 24581 vs 24095 (+2.0%) | 47988 vs 48189 (-0.4%) | 69440 vs 72284 (-3.9%) | 95287 vs 96379 (-1.1%) |
| avg_gated_lookup | 24717 vs 24095 (+2.6%) | 49327 vs 48189 (+2.4%) | 62558 vs 72284 (-13.5%) | 62558 vs 96379 (-35.1%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 28.7 points at 64.9% of the default cost, 13.5% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 28.7 points at 64.9% of the default cost, 35.1% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 28.7 points at 64.9% of the default cost, 13.5% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 28.7 points at 64.9% of the default cost, 35.1% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
