# Table 1 -- hellaswag (ouro_2_6b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 170694 layer passes over 1900 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 76.4 |
| default_cell | n/a | n/a | n/a | 74.3 (31%) |
| default_at_budget | n/a | n/a | 76.3 (16%) | 76.3 (100%) |
| lookup | 32.1 (100%) | 66.4 | 81.8 | 81.8 |
| equation | 34.4 (100%) | 58.7 | 75.1 | 76.3 |
| equation_n30 | 34.4 (100%) | 58.7 | 81.7 | 76.3 |
| equation_n100 | 34.4 (100%) | 58.7 | 75.1 | 76.3 |
| gated_equation | 34.4 (100%) | 58.7 | 75.1 | 76.4 |
| avg_lookup | 33.9 | 69.4 | 82.2 | 81.8 |
| avg_equation | 35.6 | 60.8 | 74.9 | 76.3 |
| avg_gated_lookup | 33.9 | 69.4 | 82.2 | 81.8 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 40877 vs 42674 (-4.2%) | 85032 vs 85347 (-0.4%) | 127547 vs 128021 (-0.4%) | 147796 vs 170694 (-13.4%) |
| avg_equation | 40676 vs 42674 (-4.7%) | 84407 vs 85347 (-1.1%) | 127655 vs 128021 (-0.3%) | 159043 vs 170694 (-6.8%) |
| avg_gated_lookup | 40877 vs 42674 (-4.2%) | 85032 vs 85347 (-0.4%) | 127547 vs 128021 (-0.4%) | 147796 vs 170694 (-13.4%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 81.8 points at 86.6% of the default cost, 13.4% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 76.3 points at 93.2% of the default cost, 6.8% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 81.8 points at 86.6% of the default cost, 13.4% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
