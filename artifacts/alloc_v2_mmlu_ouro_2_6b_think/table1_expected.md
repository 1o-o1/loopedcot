# Table 1 -- mmlu (ouro_2_6b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 242015 layer passes over 1900 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 80.1 |
| default_cell | n/a | n/a | n/a | 82.6 (54%) |
| default_at_budget | n/a | 75.2 (90%) | 77.6 | 79.7 |
| lookup | 65.9 | 73.9 | 80.8 | 81.1 |
| equation | 46.3 | 75.3 | 81.8 | 82.0 |
| equation_n30 | 46.3 | 75.1 | 81.8 | 82.0 |
| equation_n100 | 46.3 | 75.3 | 81.8 | 82.0 |
| gated_equation | 46.3 | 75.4 | 81.8 | 82.0 |
| avg_lookup | 70.1 | 78.1 | 81.1 | 81.1 |
| avg_equation | 64.6 | 75.6 | 82.0 | 82.0 |
| avg_gated_lookup | 70.1 | 78.1 | 81.1 | 81.1 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 59953 vs 60504 (-0.9%) | 118045 vs 121007 (-2.4%) | 150903 vs 181511 (-16.9%) | 150903 vs 242015 (-37.6%) |
| avg_equation | 59772 vs 60504 (-1.2%) | 118367 vs 121007 (-2.2%) | 174024 vs 181511 (-4.1%) | 174024 vs 242015 (-28.1%) |
| avg_gated_lookup | 59953 vs 60504 (-0.9%) | 118045 vs 121007 (-2.4%) | 150903 vs 181511 (-16.9%) | 150903 vs 242015 (-37.6%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 81.1 points at 62.4% of the default cost, 16.9% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 81.1 points at 62.4% of the default cost, 37.6% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 82.0 points at 71.9% of the default cost, 4.1% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 82.0 points at 71.9% of the default cost, 28.1% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 81.1 points at 62.4% of the default cost, 16.9% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 81.1 points at 62.4% of the default cost, 37.6% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
