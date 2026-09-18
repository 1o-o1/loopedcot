# Table 1 -- arc (ouro_1_4b_base), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 38812 layer passes over 1072 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 86.5 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | n/a | 86.6 (94%) |
| lookup | 42.9 (94%) | 75.4 | 84.0 | 86.0 |
| equation | 43.4 (94%) | 72.2 | 81.6 | 85.6 |
| equation_n30 | 43.4 (94%) | 72.2 | 84.2 | 84.9 |
| equation_n100 | 43.4 (94%) | 72.2 | 81.6 | 85.6 |
| gated_equation | 43.4 (94%) | 72.3 | 83.7 | 85.7 |
| avg_lookup | 44.8 | 78.0 | 82.6 | 86.1 |
| avg_equation | 41.9 | 74.7 | 83.3 | 86.1 |
| avg_gated_lookup | 44.1 | 77.9 | 83.1 | 86.1 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 9348 vs 9703 (-3.7%) | 18577 vs 19406 (-4.3%) | 29187 vs 29109 (+0.3%) | 38172 vs 38812 (-1.7%) |
| avg_equation | 9583 vs 9703 (-1.2%) | 19235 vs 19406 (-0.9%) | 28950 vs 29109 (-0.5%) | 38501 vs 38812 (-0.8%) |
| avg_gated_lookup | 9168 vs 9703 (-5.5%) | 18487 vs 19406 (-4.7%) | 31014 vs 29109 (+6.5%) | 38172 vs 38812 (-1.7%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 86.1 points at 98.3% of the default cost, 1.7% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 86.1 points at 98.3% of the default cost, 1.7% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
