# Table 1 -- hellaswag (mcleish_llama32_r32), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 45831 layer passes over 1900 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 28.9 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | 40.3 (16%) | 29.0 (99%) |
| lookup | 24.8 (99%) | 30.9 | 31.5 | 28.6 |
| equation | 24.8 (99%) | 26.3 | 27.5 | 28.9 |
| equation_n30 | 25.3 (99%) | 27.6 | 29.0 | 28.9 |
| equation_n100 | 24.8 (99%) | 26.3 | 27.5 | 28.9 |
| gated_equation | 24.8 (99%) | 27.6 | 28.3 | 28.8 |
| avg_lookup | 27.2 | 31.6 | 28.5 | 28.7 |
| avg_equation | 26.2 | 27.0 | 28.1 | 28.9 |
| avg_gated_lookup | 25.3 | 31.6 | 31.7 | 32.3 |

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 11323 vs 11458 (-1.2%) | 23027 vs 22916 (+0.5%) | 33779 vs 34373 (-1.7%) | 41871 vs 45831 (-8.6%) |
| avg_equation | 11283 vs 11458 (-1.5%) | 21540 vs 22916 (-6.0%) | 34079 vs 34373 (-0.9%) | 46668 vs 45831 (+1.8%) |
| avg_gated_lookup | 10591 vs 11458 (-7.6%) | 23013 vs 22916 (+0.4%) | 34493 vs 34373 (+0.3%) | 40079 vs 45831 (-12.6%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 28.7 points at 91.4% of the default cost, 8.6% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 32.3 points at 87.4% of the default cost, 12.6% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
