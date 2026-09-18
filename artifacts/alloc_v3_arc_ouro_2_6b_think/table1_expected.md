# Table 1 -- arc (ouro_2_6b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 161239 layer passes over 1072 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 96.5 |
| default_cell | n/a | n/a | n/a | 96.0 (60%) |
| default_at_budget | n/a | 92.0 (91%) | 93.2 | 96.4 |
| lookup | 83.8 | 92.4 | 95.2 | 96.5 |
| equation | 74.3 | 91.9 | 96.4 | 96.5 |
| equation_n30 | 74.3 | 91.8 | 96.1 | 96.2 |
| equation_n100 | 74.3 | 91.9 | 96.4 | 96.5 |
| gated_equation | 74.3 | 91.9 | 96.4 | 96.4 |
| avg_lookup | 87.6 | 93.3 | 96.5 | 96.5 |
| avg_equation | 87.6 | 94.1 | 96.5 | 96.5 |
| avg_gated_lookup | 87.6 | 92.9 | 96.5 | 96.5 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 39959 vs 40310 (-0.9%) | 78887 vs 80620 (-2.1%) | 117565 vs 120930 (-2.8%) | 117565 vs 161239 (-27.1%) |
| avg_equation | 39959 vs 40310 (-0.9%) | 80069 vs 80620 (-0.7%) | 117565 vs 120930 (-2.8%) | 117565 vs 161239 (-27.1%) |
| avg_gated_lookup | 38897 vs 40310 (-3.5%) | 76374 vs 80620 (-5.3%) | 117565 vs 120930 (-2.8%) | 117565 vs 161239 (-27.1%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 96.5 points at 72.9% of the default cost, 2.8% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 96.5 points at 72.9% of the default cost, 27.1% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 96.5 points at 72.9% of the default cost, 2.8% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 96.5 points at 72.9% of the default cost, 27.1% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 96.5 points at 72.9% of the default cost, 2.8% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 96.5 points at 72.9% of the default cost, 27.1% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
