# Table 1 -- csqa (ouro_2_6b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 235620 layer passes over 1121 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 80.8 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | 79.2 | 80.5 |
| lookup | 27.4 | 77.4 | 79.2 | 80.6 |
| equation | 19.6 | 76.7 | 77.1 | 80.5 |
| equation_n30 | 27.4 | 76.7 | 78.8 | 80.5 |
| equation_n100 | 19.6 | 76.7 | 77.1 | 80.5 |
| gated_equation | 27.4 | 76.7 | 79.2 | 80.5 |
| avg_lookup | 66.9 | 77.6 | 79.1 | 80.6 |
| avg_equation | 66.9 | 76.7 | 77.2 | 80.5 |
| avg_gated_lookup | 58.3 | 78.3 | 78.1 | 78.1 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 57972 vs 58905 (-1.6%) | 112902 vs 117810 (-4.2%) | 174462 vs 176715 (-1.3%) | 213213 vs 235620 (-9.5%) |
| avg_equation | 57972 vs 58905 (-1.6%) | 117634 vs 117810 (-0.1%) | 166452 vs 176715 (-5.8%) | 235143 vs 235620 (-0.2%) |
| avg_gated_lookup | 56336 vs 58905 (-4.4%) | 112260 vs 117810 (-4.7%) | 127173 vs 176715 (-28.0%) | 127173 vs 235620 (-46.0%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 80.6 points at 90.5% of the default cost, 9.5% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 78.1 points at 54.0% of the default cost, 28.0% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 78.1 points at 54.0% of the default cost, 46.0% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
