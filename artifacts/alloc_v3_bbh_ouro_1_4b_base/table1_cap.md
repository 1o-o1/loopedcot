# Table 1 -- bbh (ouro_1_4b_base), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 100844 layer passes over 2337 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 75.6 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | 76.7 (10%) | 79.6 (10%) | 79.1 (30%) | 59.8 (86%) |
| lookup | 33.8 (86%) | 46.8 | 56.1 | 65.4 |
| equation | 34.3 (86%) | 46.5 | 62.7 | 68.4 |
| equation_n30 | 35.6 (86%) | 46.5 | 63.3 | 68.1 |
| equation_n100 | 34.3 (86%) | 46.5 | 62.7 | 68.4 |
| gated_equation | 35.6 (86%) | 46.6 | 60.8 | 68.5 |
| avg_lookup | 32.0 | 47.8 | 56.6 | 70.7 |
| avg_equation | 36.2 | 52.8 | 63.5 | 70.9 |
| avg_gated_lookup | 36.5 | 48.7 | 68.0 | 70.2 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 23804 vs 25211 (-5.6%) | 48870 vs 50422 (-3.1%) | 74825 vs 75633 (-1.1%) | 98740 vs 100844 (-2.1%) |
| avg_equation | 25243 vs 25211 (+0.1%) | 49675 vs 50422 (-1.5%) | 74082 vs 75633 (-2.1%) | 100053 vs 100844 (-0.8%) |
| avg_gated_lookup | 25856 vs 25211 (+2.6%) | 51936 vs 50422 (+3.0%) | 85066 vs 75633 (+12.5%) | 96250 vs 100844 (-4.6%) |
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 70.2 points at 95.4% of the default cost, 4.6% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
