# Table 1 -- arc (ouro_2_6b_base), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 77503 layer passes over 1072 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 93.3 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | n/a | 93.0 (93%) |
| lookup | 63.0 (93%) | 86.6 | 88.1 | 88.1 |
| equation | 52.7 (93%) | 85.5 | 90.4 | 91.9 |
| equation_n30 | 52.7 (93%) | 85.9 | 91.0 | 92.4 |
| equation_n100 | 52.7 (93%) | 85.5 | 90.4 | 91.9 |
| gated_equation | 52.7 (93%) | 85.5 | 90.4 | 91.9 |
| avg_lookup | 64.8 | 88.1 | 88.1 | 88.1 |
| avg_equation | 48.3 | 87.2 | 91.1 | 91.9 |
| avg_gated_lookup | 64.8 | 88.1 | 88.1 | 88.1 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 18696 vs 19376 (-3.5%) | 35100 vs 38752 (-9.4%) | 35100 vs 58127 (-39.6%) | 35100 vs 77503 (-54.7%) |
| avg_equation | 19152 vs 19376 (-1.2%) | 38453 vs 38752 (-0.8%) | 57760 vs 58127 (-0.6%) | 61866 vs 77503 (-20.2%) |
| avg_gated_lookup | 18696 vs 19376 (-3.5%) | 35100 vs 38752 (-9.4%) | 35100 vs 58127 (-39.6%) | 35100 vs 77503 (-54.7%) |
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 88.1 points at 45.3% of the default cost, 9.4% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 88.1 points at 45.3% of the default cost, 39.6% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 88.1 points at 45.3% of the default cost, 54.7% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 91.9 points at 79.8% of the default cost, 20.2% under the budget it was given.
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 88.1 points at 45.3% of the default cost, 9.4% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 88.1 points at 45.3% of the default cost, 39.6% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 88.1 points at 45.3% of the default cost, 54.7% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
