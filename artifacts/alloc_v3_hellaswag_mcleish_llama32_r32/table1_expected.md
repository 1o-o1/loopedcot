# Table 1 -- hellaswag (mcleish_llama32_r32), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 45831 layer passes over 1900 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 28.9 |
| default_cell | n/a | n/a | n/a | 32.4 (41%) |
| default_at_budget | n/a | n/a | 40.7 (16%) | 29.2 (99%) |
| lookup | 24.8 (99%) | 30.9 | 31.5 | 28.6 |
| equation | 24.8 (99%) | 26.4 | 26.5 | 29.1 |
| equation_n30 | 26.0 (99%) | 27.9 | 28.1 | 29.1 |
| equation_n100 | 24.8 (99%) | 26.4 | 26.5 | 29.1 |
| gated_equation | 24.8 (99%) | 27.7 | 28.1 | 29.1 |
| avg_lookup | 27.2 | 31.6 | 28.5 | 28.7 |
| avg_equation | 26.1 | 27.2 | 28.2 | 28.9 |
| avg_gated_lookup | 25.3 | 31.6 | 31.7 | 28.9 |

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 11323 vs 11458 (-1.2%) | 23027 vs 22916 (+0.5%) | 33768 vs 34373 (-1.8%) | 41852 vs 45831 (-8.7%) |
| avg_equation | 11251 vs 11458 (-1.8%) | 21453 vs 22916 (-6.4%) | 33876 vs 34373 (-1.4%) | 42685 vs 45831 (-6.9%) |
| avg_gated_lookup | 10591 vs 11458 (-7.6%) | 23013 vs 22916 (+0.4%) | 34493 vs 34373 (+0.3%) | 44835 vs 45831 (-2.2%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 28.7 points at 91.3% of the default cost, 8.7% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 28.9 points at 93.1% of the default cost, 6.9% under the budget it was given.
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin -6.7 points, sd 6.6, bar 0.50 sd (30 verification questions, the ids after the 50 that fit, out of 100 calibration); cost saving 2.2% of the budget, 97.8% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
