# Table 1 -- strategyqa (huginn_0125), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 119422 layer passes over 2190 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 55.5 |
| default_cell | n/a | n/a | n/a | 55.5 |
| default_at_budget | n/a | 56.3 | 56.4 | 55.5 |
| lookup | 56.4 | 56.0 | 56.0 | 56.0 |
| equation | 56.3 | 56.3 | 56.3 | 55.5 |
| equation_n30 | 56.3 | 56.4 | 56.3 | 56.3 |
| equation_n100 | 56.3 | 56.3 | 56.3 | 55.5 |
| gated_equation | 56.3 | 56.3 | 56.4 | 55.5 |
| avg_lookup | 53.3 | 56.0 | 56.0 | 56.0 |
| avg_equation | 56.5 | 55.9 | 56.0 | 55.5 |
| avg_gated_lookup | 53.3 | 56.0 | 56.0 | 56.0 |

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 23210 vs 29855 (-22.3%) | 53070 vs 59711 (-11.1%) | 53070 vs 89566 (-40.7%) | 53070 vs 119422 (-55.6%) |
| avg_equation | 29384 vs 29855 (-1.6%) | 59822 vs 59711 (+0.2%) | 79169 vs 89566 (-11.6%) | 116097 vs 119422 (-2.8%) |
| avg_gated_lookup | 23210 vs 29855 (-22.3%) | 53070 vs 59711 (-11.1%) | 53070 vs 89566 (-40.7%) | 53070 vs 119422 (-55.6%) |
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 56.0 points at 44.4% of the default cost, 11.1% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 56.0 points at 44.4% of the default cost, 40.7% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 56.0 points at 44.4% of the default cost, 55.6% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 55.5 points at 97.2% of the default cost, 2.8% under the budget it was given.
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 56.0 points at 44.4% of the default cost, 11.1% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 56.0 points at 44.4% of the default cost, 40.7% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 56.0 points at 44.4% of the default cost, 55.6% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
