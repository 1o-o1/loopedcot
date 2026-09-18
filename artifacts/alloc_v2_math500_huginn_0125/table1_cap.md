# Table 1 -- math500 (huginn_0125), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 224131 layer passes over 400 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 15.0 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | 16.5 (98%) | 15.4 (99%) |
| lookup | 8.2 | 15.2 | 16.2 | 15.8 |
| equation | 7.5 | 14.5 | 16.0 | 15.2 |
| equation_n30 | 7.5 | 6.8 | 15.5 | 15.2 |
| equation_n100 | 7.5 | 14.5 | 16.0 | 15.2 |
| gated_equation | 7.5 | 14.5 | 16.0 | 15.2 |
| avg_lookup | 13.2 | 16.2 | 15.8 | 15.8 |
| avg_equation | 13.8 | 16.2 | 15.8 | 15.2 |
| avg_gated_lookup | 13.2 | 16.2 | 15.8 | 15.8 |

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 57395 vs 56033 (+2.4%) | 110285 vs 112065 (-1.6%) | 165718 vs 168098 (-1.4%) | 165718 vs 224131 (-26.1%) |
| avg_equation | 57046 vs 56033 (+1.8%) | 111428 vs 112065 (-0.6%) | 166184 vs 168098 (-1.1%) | 202045 vs 224131 (-9.9%) |
| avg_gated_lookup | 57395 vs 56033 (+2.4%) | 110285 vs 112065 (-1.6%) | 165718 vs 168098 (-1.4%) | 165718 vs 224131 (-26.1%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 15.8 points at 73.9% of the default cost, 1.4% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 15.8 points at 73.9% of the default cost, 26.1% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 15.8 points at 73.9% of the default cost, 1.4% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 15.8 points at 73.9% of the default cost, 26.1% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
