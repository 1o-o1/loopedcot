# Table 1 -- csqa (huginn_0125), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 87279 layer passes over 1121 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 43.6 |
| default_cell | n/a | n/a | n/a | 43.8 (60%) |
| default_at_budget | n/a | n/a | n/a | 42.8 |
| lookup | 19.0 | 30.9 | 42.6 | 43.1 |
| equation | 19.0 | 31.4 | 42.6 | 42.6 |
| equation_n30 | 19.0 | 31.4 | 42.6 | 42.6 |
| equation_n100 | 19.0 | 31.4 | 42.6 | 42.6 |
| gated_equation | 19.0 | 31.4 | 42.6 | 43.6 |
| avg_lookup | 25.9 | 41.9 | 42.3 | 43.1 |
| avg_equation | 27.2 | 42.2 | 42.6 | 42.6 |
| avg_gated_lookup | 25.9 | 41.9 | 42.3 | 43.1 |

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 21618 vs 21820 (-0.9%) | 42949 vs 43639 (-1.6%) | 61841 vs 65459 (-5.5%) | 86310 vs 87279 (-1.1%) |
| avg_equation | 21773 vs 21820 (-0.2%) | 42966 vs 43639 (-1.5%) | 44939 vs 65459 (-31.3%) | 44939 vs 87279 (-48.5%) |
| avg_gated_lookup | 21618 vs 21820 (-0.9%) | 42949 vs 43639 (-1.6%) | 61841 vs 65459 (-5.5%) | 86310 vs 87279 (-1.1%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 43.1 points at 98.9% of the default cost, 1.1% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 42.6 points at 51.5% of the default cost, 31.3% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 42.6 points at 51.5% of the default cost, 48.5% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 43.1 points at 98.9% of the default cost, 1.1% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
