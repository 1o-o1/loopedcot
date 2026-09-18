# Table 1 -- mmlu (mcleish_llama32_r32), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 40492 layer passes over 1900 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 37.3 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | 38.8 (86%) | 38.1 (98%) |
| lookup | 26.8 (98%) | 36.6 | 36.7 | 36.7 |
| equation | 28.2 (98%) | 36.9 | 37.1 | 37.1 |
| equation_n30 | 31.8 (98%) | 36.4 | 37.1 | 37.1 |
| equation_n100 | 28.2 (98%) | 36.9 | 37.1 | 37.1 |
| gated_equation | 28.2 (98%) | 36.9 | 37.1 | 37.1 |
| avg_lookup | 32.3 | 37.0 | 36.7 | 36.7 |
| avg_equation | 32.3 | 37.1 | 37.0 | 36.8 |
| avg_gated_lookup | 32.3 | 37.0 | 36.7 | 36.7 |

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 10058 vs 10123 (-0.6%) | 19998 vs 20246 (-1.2%) | 22665 vs 30369 (-25.4%) | 22665 vs 40492 (-44.0%) |
| avg_equation | 10058 vs 10123 (-0.6%) | 23581 vs 20246 (+16.5%) | 32670 vs 30369 (+7.6%) | 41959 vs 40492 (+3.6%) |
| avg_gated_lookup | 10058 vs 10123 (-0.6%) | 19998 vs 20246 (-1.2%) | 22665 vs 30369 (-25.4%) | 22665 vs 40492 (-44.0%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 56.0% of the default cost, 25.4% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 56.0% of the default cost, 44.0% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 56.0% of the default cost, 25.4% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 56.0% of the default cost, 44.0% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
