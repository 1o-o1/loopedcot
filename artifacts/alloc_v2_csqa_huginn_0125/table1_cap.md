# Table 1 -- csqa (huginn_0125), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 87279 layer passes over 1121 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 43.6 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | n/a | 42.2 |
| lookup | 19.1 | 30.9 | 42.6 | 43.1 |
| equation | 19.1 | 31.4 | 42.6 | 42.6 |
| equation_n30 | 19.1 | 31.4 | 42.6 | 42.6 |
| equation_n100 | 19.1 | 31.4 | 42.6 | 42.6 |
| gated_equation | 19.1 | 31.4 | 42.6 | 43.1 |
| avg_lookup | 25.9 | 40.1 | 42.3 | 43.1 |
| avg_equation | 26.6 | 40.8 | 42.6 | 42.6 |
| avg_gated_lookup | 25.9 | 40.1 | 42.3 | 43.1 |

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 21645 vs 21820 (-0.8%) | 43234 vs 43639 (-0.9%) | 62855 vs 65459 (-4.0%) | 86330 vs 87279 (-1.1%) |
| avg_equation | 21671 vs 21820 (-0.7%) | 43401 vs 43639 (-0.5%) | 46649 vs 65459 (-28.7%) | 46649 vs 87279 (-46.6%) |
| avg_gated_lookup | 21645 vs 21820 (-0.8%) | 43234 vs 43639 (-0.9%) | 62855 vs 65459 (-4.0%) | 86330 vs 87279 (-1.1%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 43.1 points at 98.9% of the default cost, 1.1% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 42.6 points at 53.4% of the default cost, 28.7% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 42.6 points at 53.4% of the default cost, 46.6% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 43.1 points at 98.9% of the default cost, 1.1% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
