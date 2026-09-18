# Table 1 -- bbh (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 100844 layer passes over 2337 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 75.6 |
| default_cell | n/a | 79.6 (10%) | 84.6 (21%) | 81.6 (34%) |
| default_at_budget | 76.7 (10%) | 79.6 (10%) | 80.3 (30%) | 64.9 (86%) |
| lookup | 33.8 (86%) | 49.3 | 63.2 | 72.3 |
| equation | 33.8 (86%) | 48.0 | 65.9 | 72.4 |
| equation_n30 | 33.8 (86%) | 48.0 | 66.0 | 70.3 |
| equation_n100 | 33.8 (86%) | 48.0 | 65.9 | 72.4 |
| gated_equation | 35.1 (86%) | 48.2 | 66.2 | 72.5 |
| avg_lookup | 33.1 | 55.2 | 70.6 | 75.3 |
| avg_equation | 36.5 | 56.7 | 70.0 | 75.6 |
| avg_gated_lookup | 36.3 | 51.5 | 70.2 | 70.2 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 24499 vs 25211 (-2.8%) | 50229 vs 50422 (-0.4%) | 74979 vs 75633 (-0.9%) | 94123 vs 100844 (-6.7%) |
| avg_equation | 25681 vs 25211 (+1.9%) | 49594 vs 50422 (-1.6%) | 75395 vs 75633 (-0.3%) | 100462 vs 100844 (-0.4%) |
| avg_gated_lookup | 25825 vs 25211 (+2.4%) | 54592 vs 50422 (+8.3%) | 70852 vs 75633 (-6.3%) | 70852 vs 100844 (-29.7%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 75.3 points at 93.3% of the default cost, 6.7% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 70.2 points at 70.3% of the default cost, 6.3% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 70.2 points at 70.3% of the default cost, 29.7% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
