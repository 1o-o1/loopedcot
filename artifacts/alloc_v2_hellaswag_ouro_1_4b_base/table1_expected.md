# Table 1 -- hellaswag (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 94300 layer passes over 1900 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 57.4 |
| default_cell | n/a | n/a | n/a | 70.6 (4%) |
| default_at_budget | n/a | n/a | 63.6 (32%) | 57.6 |
| lookup | 34.7 | 56.9 | 65.4 | 65.4 |
| equation | 31.5 | 46.8 | 56.1 | 57.5 |
| equation_n30 | 31.5 | 46.8 | 56.4 | 56.3 |
| equation_n100 | 31.5 | 46.8 | 56.1 | 57.5 |
| gated_equation | 31.5 | 46.8 | 56.1 | 57.6 |
| avg_lookup | 39.8 | 61.5 | 65.4 | 65.4 |
| avg_equation | 35.5 | 49.7 | 56.8 | 57.4 |
| avg_gated_lookup | 39.8 | 61.5 | 65.4 | 65.4 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 22538 vs 23575 (-4.4%) | 47077 vs 47150 (-0.2%) | 55423 vs 70725 (-21.6%) | 55423 vs 94300 (-41.2%) |
| avg_equation | 22659 vs 23575 (-3.9%) | 46585 vs 47150 (-1.2%) | 70414 vs 70725 (-0.4%) | 94499 vs 94300 (+0.2%) |
| avg_gated_lookup | 22538 vs 23575 (-4.4%) | 47077 vs 47150 (-0.2%) | 55423 vs 70725 (-21.6%) | 55423 vs 94300 (-41.2%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 65.4 points at 58.8% of the default cost, 21.6% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 65.4 points at 58.8% of the default cost, 41.2% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 65.4 points at 58.8% of the default cost, 21.6% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 65.4 points at 58.8% of the default cost, 41.2% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
