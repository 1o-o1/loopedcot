# Table 1 -- mmlu (ouro_2_6b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 242015 layer passes over 1900 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 80.1 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 75.2 (90%) | 75.5 | 78.7 |
| lookup | 65.9 | 73.9 | 77.9 | 80.6 |
| equation | 45.8 | 75.3 | 78.1 | 80.6 |
| equation_n30 | 45.8 | 75.3 | 78.1 | 80.6 |
| equation_n100 | 45.8 | 75.3 | 78.1 | 80.6 |
| gated_equation | 46.4 | 75.1 | 78.1 | 80.6 |
| avg_lookup | 70.1 | 76.3 | 79.4 | 81.1 |
| avg_equation | 64.6 | 75.7 | 79.7 | 81.4 |
| avg_gated_lookup | 69.8 | 74.4 | 79.9 | 81.1 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 59953 vs 60504 (-0.9%) | 120408 vs 121007 (-0.5%) | 188180 vs 181511 (+3.7%) | 221086 vs 242015 (-8.6%) |
| avg_equation | 59772 vs 60504 (-1.2%) | 120932 vs 121007 (-0.1%) | 177586 vs 181511 (-2.2%) | 236841 vs 242015 (-2.1%) |
| avg_gated_lookup | 59208 vs 60504 (-2.1%) | 122128 vs 121007 (+0.9%) | 178137 vs 181511 (-1.9%) | 221086 vs 242015 (-8.6%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 81.1 points at 91.4% of the default cost, 8.6% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 81.1 points at 91.4% of the default cost, 8.6% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
