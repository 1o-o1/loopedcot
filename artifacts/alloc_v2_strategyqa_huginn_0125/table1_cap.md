# Table 1 -- strategyqa (huginn_0125), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 119422 layer passes over 2190 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 55.5 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 56.0 | 56.3 | 55.9 |
| lookup | 56.4 | 56.0 | 56.0 | 56.0 |
| equation | 56.4 | 56.0 | 56.3 | 55.9 |
| equation_n30 | 56.4 | 56.7 | 56.7 | 56.3 |
| equation_n100 | 56.4 | 56.0 | 56.3 | 55.9 |
| gated_equation | 56.4 | 56.0 | 56.3 | 55.9 |
| avg_lookup | 53.3 | 56.0 | 56.0 | 56.0 |
| avg_equation | 56.5 | 56.1 | 56.2 | 56.3 |
| avg_gated_lookup | 53.3 | 56.0 | 56.0 | 56.0 |

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 23756 vs 29855 (-20.4%) | 55195 vs 59711 (-7.6%) | 55195 vs 89566 (-38.4%) | 55195 vs 119422 (-53.8%) |
| avg_equation | 29568 vs 29855 (-1.0%) | 59862 vs 59711 (+0.3%) | 93083 vs 89566 (+3.9%) | 120122 vs 119422 (+0.6%) |
| avg_gated_lookup | 23756 vs 29855 (-20.4%) | 55195 vs 59711 (-7.6%) | 55195 vs 89566 (-38.4%) | 55195 vs 119422 (-53.8%) |
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 56.0 points at 46.2% of the default cost, 7.6% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 56.0 points at 46.2% of the default cost, 38.4% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 56.0 points at 46.2% of the default cost, 53.8% under the budget it was given.
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 56.0 points at 46.2% of the default cost, 7.6% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 56.0 points at 46.2% of the default cost, 38.4% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 56.0 points at 46.2% of the default cost, 53.8% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
