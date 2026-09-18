# Table 1 -- aqua (ouro_2_6b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 401640 layer passes over 154 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 89.0 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 55.8 | 75.3 | 85.1 |
| lookup | 50.0 | 79.2 | 83.1 | 85.1 |
| equation | 48.1 | 79.2 | 83.1 | 85.1 |
| equation_n30 | 50.6 | 73.4 | 83.1 | 85.1 |
| equation_n100 | 48.1 | 79.2 | 83.1 | 85.1 |
| gated_equation | 51.3 | 79.2 | 83.1 | 85.1 |
| avg_lookup | 63.6 | 81.8 | 83.8 | 87.7 |
| avg_equation | 63.0 | 81.8 | 83.8 | 85.1 |
| avg_gated_lookup | 64.9 | 83.1 | 84.4 | 85.1 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 94558 vs 100410 (-5.8%) | 203324 vs 200820 (+1.2%) | 293935 vs 301230 (-2.4%) | 426006 vs 401640 (+6.1%) |
| avg_equation | 94722 vs 100410 (-5.7%) | 203324 vs 200820 (+1.2%) | 293935 vs 301230 (-2.4%) | 387705 vs 401640 (-3.5%) |
| avg_gated_lookup | 101445 vs 100410 (+1.0%) | 214019 vs 200820 (+6.6%) | 301193 vs 301230 (-0.0%) | 322595 vs 401640 (-19.7%) |
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 85.1 points at 80.3% of the default cost, 19.7% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
