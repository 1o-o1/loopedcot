# Table 1 -- strategyqa (ouro_2_6b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 99332 layer passes over 2190 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 74.7 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | 73.1 (100%) | 74.7 |
| lookup | 59.5 | 66.9 | 73.6 | 75.0 |
| equation | 59.1 | 69.7 | 73.7 | 74.7 |
| equation_n30 | 59.1 | 66.4 | 73.3 | 74.7 |
| equation_n100 | 59.1 | 69.7 | 73.7 | 74.7 |
| gated_equation | 59.4 | 69.8 | 73.1 | 74.7 |
| avg_lookup | 61.1 | 68.1 | 73.4 | 75.0 |
| avg_equation | 61.1 | 70.9 | 74.1 | 74.7 |
| avg_gated_lookup | 61.1 | 67.9 | 73.2 | 74.7 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 21870 vs 24833 (-11.9%) | 46509 vs 49666 (-6.4%) | 73453 vs 74499 (-1.4%) | 82364 vs 99332 (-17.1%) |
| avg_equation | 23649 vs 24833 (-4.8%) | 48020 vs 49666 (-3.3%) | 72569 vs 74499 (-2.6%) | 98880 vs 99332 (-0.5%) |
| avg_gated_lookup | 21870 vs 24833 (-11.9%) | 46248 vs 49666 (-6.9%) | 72429 vs 74499 (-2.8%) | 81091 vs 99332 (-18.4%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 75.0 points at 82.9% of the default cost, 17.1% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 74.7 points at 81.6% of the default cost, 18.4% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
