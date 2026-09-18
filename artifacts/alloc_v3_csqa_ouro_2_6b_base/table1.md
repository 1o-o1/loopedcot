# Table 1 -- csqa (ouro_2_6b_base), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 124178 layer passes over 1121 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 80.0 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | n/a | 81.0 |
| lookup | 33.7 | 75.2 | 80.6 | 80.6 |
| equation | 33.7 | 74.2 | 74.0 | 74.0 |
| equation_n30 | 33.7 | 74.2 | 74.0 | 74.0 |
| equation_n100 | 33.7 | 74.2 | 74.0 | 74.0 |
| gated_equation | 33.7 | 74.2 | 74.0 | 78.6 |
| avg_lookup | 34.3 | 75.2 | 80.6 | 80.6 |
| avg_equation | 34.3 | 74.0 | 74.0 | 74.0 |
| avg_gated_lookup | 34.7 | 75.2 | 78.4 | 82.0 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 31008 vs 31044 (-0.1%) | 60965 vs 62089 (-1.8%) | 87939 vs 93133 (-5.6%) | 87939 vs 124178 (-29.2%) |
| avg_equation | 31008 vs 31044 (-0.1%) | 61698 vs 62089 (-0.6%) | 61698 vs 93133 (-33.8%) | 61698 vs 124178 (-50.3%) |
| avg_gated_lookup | 30845 vs 31044 (-0.6%) | 61813 vs 62089 (-0.4%) | 88390 vs 93133 (-5.1%) | 117252 vs 124178 (-5.6%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 80.6 points at 70.8% of the default cost, 5.6% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 80.6 points at 70.8% of the default cost, 29.2% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 74.0 points at 49.7% of the default cost, 33.8% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 74.0 points at 49.7% of the default cost, 50.3% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 82.0 points at 94.4% of the default cost, 5.6% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
