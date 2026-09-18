# Table 1 -- strategyqa (mcleish_llama32_r32), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 59637 layer passes over 2190 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 50.3 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 51.0 | 50.8 | 50.8 |
| lookup | 52.3 | 52.3 | 52.3 | 52.3 |
| equation | 50.0 | 49.9 | 49.5 | 49.5 |
| equation_n30 | 50.0 | 49.9 | 50.8 | 50.8 |
| equation_n100 | 50.0 | 49.9 | 49.5 | 49.5 |
| gated_equation | 50.0 | 49.9 | 49.5 | 49.5 |
| avg_lookup | 52.3 | 52.3 | 52.3 | 52.3 |
| avg_equation | 50.3 | 49.5 | 49.5 | 49.5 |
| avg_gated_lookup | 52.3 | 52.3 | 52.3 | 52.3 |

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 7768 vs 14909 (-47.9%) | 7768 vs 29819 (-73.9%) | 7768 vs 44728 (-82.6%) | 7768 vs 59637 (-87.0%) |
| avg_equation | 14714 vs 14909 (-1.3%) | 28062 vs 29819 (-5.9%) | 36404 vs 44728 (-18.6%) | 36404 vs 59637 (-39.0%) |
| avg_gated_lookup | 7768 vs 14909 (-47.9%) | 7768 vs 29819 (-73.9%) | 7768 vs 44728 (-82.6%) | 7768 vs 59637 (-87.0%) |
- `avg_lookup` at 0.25x: the multiplier is 0, so the budget never binds. The row is the same 52.3 points at 13.0% of the default cost, 47.9% under the budget it was given.
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 52.3 points at 13.0% of the default cost, 73.9% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 52.3 points at 13.0% of the default cost, 82.6% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 52.3 points at 13.0% of the default cost, 87.0% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 49.5 points at 61.0% of the default cost, 18.6% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 49.5 points at 61.0% of the default cost, 39.0% under the budget it was given.
- `avg_gated_lookup` at 0.25x: the multiplier is 0, so the budget never binds. The row is the same 52.3 points at 13.0% of the default cost, 47.9% under the budget it was given.
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 52.3 points at 13.0% of the default cost, 73.9% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 52.3 points at 13.0% of the default cost, 82.6% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 52.3 points at 13.0% of the default cost, 87.0% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
