# Table 1 -- mmlu (ouro_1_4b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 134109 layer passes over 1900 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 73.7 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 65.9 (95%) | 70.7 | 73.7 |
| lookup | 58.4 | 70.6 | 72.5 | 73.5 |
| equation | 56.9 | 71.7 | 71.3 | 73.7 |
| equation_n30 | 55.9 | 68.3 | 72.7 | 73.7 |
| equation_n100 | 56.9 | 71.7 | 71.3 | 73.7 |
| gated_equation | 56.6 | 71.4 | 71.3 | 73.7 |
| avg_lookup | 63.8 | 70.3 | 72.8 | 73.5 |
| avg_equation | 63.4 | 71.6 | 73.3 | 73.6 |
| avg_gated_lookup | 62.3 | 70.8 | 72.7 | 73.7 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 33251 vs 33527 (-0.8%) | 67868 vs 67055 (+1.2%) | 98907 vs 100582 (-1.7%) | 135002 vs 134109 (+0.7%) |
| avg_equation | 33052 vs 33527 (-1.4%) | 66523 vs 67055 (-0.8%) | 100635 vs 100582 (+0.1%) | 133389 vs 134109 (-0.5%) |
| avg_gated_lookup | 33541 vs 33527 (+0.0%) | 64992 vs 67055 (-3.1%) | 97206 vs 100582 (-3.4%) | 120342 vs 134109 (-10.3%) |
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 73.7 points at 89.7% of the default cost, 10.3% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
