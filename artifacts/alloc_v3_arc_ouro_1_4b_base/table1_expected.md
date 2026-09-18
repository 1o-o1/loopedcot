# Table 1 -- arc (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 38812 layer passes over 1072 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 86.5 |
| default_cell | n/a | n/a | n/a | 86.3 (55%) |
| default_at_budget | n/a | n/a | n/a | 86.6 (94%) |
| lookup | 42.9 (94%) | 75.4 | 84.0 | 86.0 |
| equation | 44.0 (94%) | 72.8 | 81.8 | 85.6 |
| equation_n30 | 44.0 (94%) | 72.8 | 84.4 | 85.7 |
| equation_n100 | 44.0 (94%) | 72.8 | 81.8 | 85.6 |
| gated_equation | 44.1 (94%) | 72.9 | 83.9 | 85.7 |
| avg_lookup | 44.8 | 78.0 | 82.6 | 86.1 |
| avg_equation | 42.6 | 75.4 | 84.6 | 86.4 |
| avg_gated_lookup | 44.1 | 77.9 | 83.1 | 86.1 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 9348 vs 9703 (-3.7%) | 18574 vs 19406 (-4.3%) | 29163 vs 29109 (+0.2%) | 38131 vs 38812 (-1.8%) |
| avg_equation | 9621 vs 9703 (-0.9%) | 19406 vs 19406 (-0.0%) | 29073 vs 29109 (-0.1%) | 38747 vs 38812 (-0.2%) |
| avg_gated_lookup | 9168 vs 9703 (-5.5%) | 18485 vs 19406 (-4.7%) | 30986 vs 29109 (+6.4%) | 38131 vs 38812 (-1.8%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 86.1 points at 98.2% of the default cost, 1.8% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 86.1 points at 98.2% of the default cost, 1.8% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
