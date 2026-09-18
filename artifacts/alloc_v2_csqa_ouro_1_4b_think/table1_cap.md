# Table 1 -- csqa (ouro_1_4b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 131275 layer passes over 1121 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 77.4 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 70.9 | 75.6 | 76.1 |
| lookup | 55.8 | 70.2 | 74.2 | 74.2 |
| equation | 55.6 | 74.0 | 75.6 | 76.3 |
| equation_n30 | 55.6 | 74.0 | 75.6 | 76.1 |
| equation_n100 | 55.6 | 74.0 | 75.6 | 76.3 |
| gated_equation | 55.6 | 74.0 | 75.6 | 76.1 |
| avg_lookup | 56.0 | 73.1 | 74.2 | 74.2 |
| avg_equation | 60.1 | 74.1 | 76.0 | 76.4 |
| avg_gated_lookup | 56.0 | 73.1 | 74.2 | 74.2 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 32413 vs 32819 (-1.2%) | 64893 vs 65638 (-1.1%) | 66690 vs 98456 (-32.3%) | 66690 vs 131275 (-49.2%) |
| avg_equation | 32562 vs 32819 (-0.8%) | 64170 vs 65638 (-2.2%) | 100354 vs 98456 (+1.9%) | 131436 vs 131275 (+0.1%) |
| avg_gated_lookup | 32413 vs 32819 (-1.2%) | 64893 vs 65638 (-1.1%) | 66690 vs 98456 (-32.3%) | 66690 vs 131275 (-49.2%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 74.2 points at 50.8% of the default cost, 32.3% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 74.2 points at 50.8% of the default cost, 49.2% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 74.2 points at 50.8% of the default cost, 32.3% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 74.2 points at 50.8% of the default cost, 49.2% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
