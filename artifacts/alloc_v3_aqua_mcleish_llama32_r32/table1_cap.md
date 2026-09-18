# Table 1 -- aqua (mcleish_llama32_r32), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 41537 layer passes over 154 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 53.2 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | 37.0 (35%) | 53.9 |
| lookup | 23.4 | 43.5 | 55.2 | 53.2 |
| equation | 24.0 | 42.9 | 55.2 | 55.8 |
| equation_n30 | 24.0 | 42.9 | 55.2 | 55.8 |
| equation_n100 | 24.0 | 42.9 | 55.2 | 55.8 |
| gated_equation | 29.9 | 42.9 | 55.2 | 53.2 |
| avg_lookup | 40.3 | 49.4 | 54.5 | 53.9 |
| avg_equation | 41.6 | 51.9 | 55.2 | 55.8 |
| avg_gated_lookup | 43.5 | 46.1 | 46.1 | 46.1 |

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 10813 vs 10384 (+4.1%) | 20553 vs 20768 (-1.0%) | 32055 vs 31153 (+2.9%) | 38846 vs 41537 (-6.5%) |
| avg_equation | 10300 vs 10384 (-0.8%) | 20340 vs 20768 (-2.1%) | 30709 vs 31153 (-1.4%) | 42678 vs 41537 (+2.7%) |
| avg_gated_lookup | 10523 vs 10384 (+1.3%) | 20150 vs 20768 (-3.0%) | 44447 vs 31153 (+42.7%) | 44447 vs 41537 (+7.0%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 53.9 points at 93.5% of the default cost, 6.5% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
