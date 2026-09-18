# Table 1 -- mmlu (huginn_0125), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 85934 layer passes over 1900 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 36.4 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | 39.0 (71%) | 37.6 (92%) |
| lookup | 24.8 | 35.5 | 35.8 | 35.8 |
| equation | 24.2 | 35.8 | 36.2 | 36.2 |
| equation_n30 | 24.2 | 35.8 | 36.2 | 36.2 |
| equation_n100 | 24.2 | 35.8 | 36.2 | 36.2 |
| gated_equation | 24.2 | 35.8 | 36.2 | 36.2 |
| avg_lookup | 33.8 | 35.8 | 35.8 | 35.8 |
| avg_equation | 32.9 | 36.5 | 36.0 | 36.1 |
| avg_gated_lookup | 33.8 | 35.8 | 35.8 | 35.8 |

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 21976 vs 21483 (+2.3%) | 37646 vs 42967 (-12.4%) | 37646 vs 64450 (-41.6%) | 37646 vs 85934 (-56.2%) |
| avg_equation | 21587 vs 21483 (+0.5%) | 42470 vs 42967 (-1.2%) | 60900 vs 64450 (-5.5%) | 88349 vs 85934 (+2.8%) |
| avg_gated_lookup | 21976 vs 21483 (+2.3%) | 37646 vs 42967 (-12.4%) | 37646 vs 64450 (-41.6%) | 37646 vs 85934 (-56.2%) |
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 35.8 points at 43.8% of the default cost, 12.4% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 35.8 points at 43.8% of the default cost, 41.6% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 35.8 points at 43.8% of the default cost, 56.2% under the budget it was given.
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 35.8 points at 43.8% of the default cost, 12.4% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 35.8 points at 43.8% of the default cost, 41.6% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 35.8 points at 43.8% of the default cost, 56.2% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
