# Table 1 -- arc (huginn_0125), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 53810 layer passes over 1072 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 41.3 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | n/a | 42.3 (94%) |
| lookup | 25.8 | 39.6 | 42.4 | 41.5 |
| equation | 26.7 | 39.0 | 40.4 | 41.4 |
| equation_n30 | 26.7 | 33.6 | 40.4 | 42.4 |
| equation_n100 | 26.7 | 39.0 | 40.4 | 41.4 |
| gated_equation | 26.7 | 39.0 | 40.4 | 42.4 |
| avg_lookup | 33.7 | 41.9 | 41.4 | 41.3 |
| avg_equation | 33.4 | 40.4 | 40.5 | 41.7 |
| avg_gated_lookup | 33.7 | 41.9 | 41.4 | 41.3 |

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 14008 vs 13452 (+4.1%) | 26038 vs 26905 (-3.2%) | 40445 vs 40357 (+0.2%) | 48464 vs 53810 (-9.9%) |
| avg_equation | 13687 vs 13452 (+1.7%) | 27088 vs 26905 (+0.7%) | 41179 vs 40357 (+2.0%) | 54203 vs 53810 (+0.7%) |
| avg_gated_lookup | 14008 vs 13452 (+4.1%) | 26038 vs 26905 (-3.2%) | 40445 vs 40357 (+0.2%) | 48464 vs 53810 (-9.9%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 41.3 points at 90.1% of the default cost, 9.9% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 41.3 points at 90.1% of the default cost, 9.9% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
