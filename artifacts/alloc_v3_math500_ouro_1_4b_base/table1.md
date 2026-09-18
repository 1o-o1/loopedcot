# Table 1 -- math500 (ouro_1_4b_base), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 178329 layer passes over 400 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 63.5 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | 45.2 (99%) | 56.9 (100%) |
| lookup | 24.1 (100%) | 53.0 | 64.0 | 65.5 |
| equation | 24.1 (100%) | 53.0 | 64.0 | 64.8 |
| equation_n30 | 24.1 (100%) | 53.0 | 54.8 | 65.5 |
| equation_n100 | 24.1 (100%) | 53.0 | 64.0 | 64.8 |
| gated_equation | 24.1 (100%) | 53.0 | 64.0 | 65.5 |
| avg_lookup | 28.0 | 60.8 | 67.2 | 65.5 |
| avg_equation | 28.0 | 57.8 | 64.2 | 65.2 |
| avg_gated_lookup | 28.0 | 54.5 | 64.2 | 65.5 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 44421 vs 44582 (-0.4%) | 89898 vs 89164 (+0.8%) | 135047 vs 133746 (+1.0%) | 147472 vs 178329 (-17.3%) |
| avg_equation | 44421 vs 44582 (-0.4%) | 87397 vs 89164 (-2.0%) | 132721 vs 133746 (-0.8%) | 175945 vs 178329 (-1.3%) |
| avg_gated_lookup | 44421 vs 44582 (-0.4%) | 91813 vs 89164 (+3.0%) | 132105 vs 133746 (-1.2%) | 147472 vs 178329 (-17.3%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 65.5 points at 82.7% of the default cost, 17.3% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 65.5 points at 82.7% of the default cost, 17.3% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
