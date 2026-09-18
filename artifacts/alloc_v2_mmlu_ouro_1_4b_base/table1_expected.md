# Table 1 -- mmlu (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 58295 layer passes over 1900 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 68.7 |
| default_cell | n/a | n/a | n/a | 72.9 (70%) |
| default_at_budget | n/a | n/a | 74.4 (38%) | 70.3 (88%) |
| lookup | 41.2 (88%) | 56.2 | 66.0 | 67.2 |
| equation | 41.4 (88%) | 58.3 | 64.5 | 65.9 |
| equation_n30 | 41.4 (88%) | 58.3 | 64.6 | 66.1 |
| equation_n100 | 41.4 (88%) | 58.3 | 64.5 | 65.9 |
| gated_equation | 41.4 (88%) | 58.3 | 64.5 | 68.2 |
| avg_lookup | 43.2 | 61.4 | 65.7 | 67.7 |
| avg_equation | 43.9 | 61.5 | 66.0 | 65.8 |
| avg_gated_lookup | 43.2 | 61.4 | 65.7 | 67.7 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 13986 vs 14574 (-4.0%) | 28834 vs 29148 (-1.1%) | 43006 vs 43721 (-1.6%) | 47839 vs 58295 (-17.9%) |
| avg_equation | 14186 vs 14574 (-2.7%) | 28899 vs 29148 (-0.9%) | 43315 vs 43721 (-0.9%) | 48721 vs 58295 (-16.4%) |
| avg_gated_lookup | 13986 vs 14574 (-4.0%) | 28834 vs 29148 (-1.1%) | 43006 vs 43721 (-1.6%) | 47839 vs 58295 (-17.9%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 67.7 points at 82.1% of the default cost, 17.9% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 65.8 points at 83.6% of the default cost, 16.4% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 67.7 points at 82.1% of the default cost, 17.9% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
