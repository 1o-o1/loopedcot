# Table 1 -- arc (mcleish_llama32_r32), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 22554 layer passes over 1072 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 44.5 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | n/a | 43.7 (95%) |
| lookup | 24.1 (95%) | 38.0 | 42.8 | 42.8 |
| equation | 24.7 (95%) | 38.1 | 42.8 | 42.4 |
| equation_n30 | 22.5 (95%) | 38.0 | 42.8 | 42.4 |
| equation_n100 | 24.7 (95%) | 38.1 | 42.8 | 42.4 |
| gated_equation | 24.7 (95%) | 38.1 | 42.8 | 42.4 |
| avg_lookup | 26.8 | 43.1 | 42.8 | 42.8 |
| avg_equation | 26.8 | 43.1 | 41.7 | 43.9 |
| avg_gated_lookup | 26.8 | 43.1 | 42.8 | 42.8 |

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 5725 vs 5638 (+1.5%) | 11334 vs 11277 (+0.5%) | 11570 vs 16915 (-31.6%) | 11570 vs 22554 (-48.7%) |
| avg_equation | 5725 vs 5638 (+1.5%) | 11334 vs 11277 (+0.5%) | 16880 vs 16915 (-0.2%) | 22040 vs 22554 (-2.3%) |
| avg_gated_lookup | 5725 vs 5638 (+1.5%) | 11334 vs 11277 (+0.5%) | 11570 vs 16915 (-31.6%) | 11570 vs 22554 (-48.7%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 42.8 points at 51.3% of the default cost, 31.6% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 42.8 points at 51.3% of the default cost, 48.7% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 43.9 points at 97.7% of the default cost, 2.3% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 42.8 points at 51.3% of the default cost, 31.6% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 42.8 points at 51.3% of the default cost, 48.7% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
