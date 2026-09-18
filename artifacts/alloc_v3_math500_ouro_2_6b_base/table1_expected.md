# Table 1 -- math500 (ouro_2_6b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 338737 layer passes over 400 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 56.0 |
| default_cell | n/a | n/a | n/a | 56.6 (98%) |
| default_at_budget | n/a | n/a | 55.1 (98%) | 56.1 (100%) |
| lookup | 31.3 (100%) | 53.0 | 53.8 | 53.5 |
| equation | 34.8 (100%) | 53.0 | 52.5 | 55.8 |
| equation_n30 | 34.8 (100%) | 53.0 | 52.5 | 52.5 |
| equation_n100 | 34.8 (100%) | 53.0 | 52.5 | 55.8 |
| gated_equation | 34.8 (100%) | 53.0 | 54.5 | 56.2 |
| avg_lookup | 35.2 | 53.8 | 53.5 | 53.5 |
| avg_equation | 36.8 | 52.5 | 54.5 | 56.0 |
| avg_gated_lookup | 35.2 | 53.2 | 53.2 | 56.0 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 83347 vs 84684 (-1.6%) | 170761 vs 169369 (+0.8%) | 181071 vs 254053 (-28.7%) | 181071 vs 338737 (-46.5%) |
| avg_equation | 85709 vs 84684 (+1.2%) | 167582 vs 169369 (-1.1%) | 258292 vs 254053 (+1.7%) | 290726 vs 338737 (-14.2%) |
| avg_gated_lookup | 82995 vs 84684 (-2.0%) | 161462 vs 169369 (-4.7%) | 161462 vs 254053 (-36.4%) | 290726 vs 338737 (-14.2%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 53.5 points at 53.5% of the default cost, 28.7% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 53.5 points at 53.5% of the default cost, 46.5% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 56.0 points at 85.8% of the default cost, 14.2% under the budget it was given.
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 53.2 points at 47.7% of the default cost, 4.7% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 53.2 points at 47.7% of the default cost, 36.4% under the budget it was given.
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin -3.3 points, sd 5.7, bar 0.50 sd (30 verification questions, the ids after the 50 that fit, out of 100 calibration); cost saving 14.2% of the budget, 85.8% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
