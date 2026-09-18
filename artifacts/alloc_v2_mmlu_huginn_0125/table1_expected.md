# Table 1 -- mmlu (huginn_0125), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 85934 layer passes over 1900 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 36.4 |
| default_cell | n/a | n/a | n/a | 45.3 (21%) |
| default_at_budget | n/a | n/a | 39.8 (71%) | 37.4 (92%) |
| lookup | 24.8 | 35.5 | 35.8 | 35.8 |
| equation | 24.3 | 35.2 | 35.4 | 35.5 |
| equation_n30 | 24.3 | 35.2 | 35.4 | 35.5 |
| equation_n100 | 24.3 | 35.2 | 35.4 | 35.5 |
| gated_equation | 24.3 | 35.2 | 35.4 | 35.5 |
| avg_lookup | 33.3 | 35.8 | 35.8 | 35.8 |
| avg_equation | 33.3 | 35.9 | 35.5 | 35.5 |
| avg_gated_lookup | 33.3 | 35.8 | 35.8 | 35.8 |

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 22314 vs 21483 (+3.9%) | 36262 vs 42967 (-15.6%) | 36262 vs 64450 (-43.7%) | 36262 vs 85934 (-57.8%) |
| avg_equation | 22314 vs 21483 (+3.9%) | 42165 vs 42967 (-1.9%) | 48397 vs 64450 (-24.9%) | 48397 vs 85934 (-43.7%) |
| avg_gated_lookup | 22314 vs 21483 (+3.9%) | 36262 vs 42967 (-15.6%) | 36262 vs 64450 (-43.7%) | 36262 vs 85934 (-57.8%) |
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 35.8 points at 42.2% of the default cost, 15.6% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 35.8 points at 42.2% of the default cost, 43.7% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 35.8 points at 42.2% of the default cost, 57.8% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 35.5 points at 56.3% of the default cost, 24.9% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 35.5 points at 56.3% of the default cost, 43.7% under the budget it was given.
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 35.8 points at 42.2% of the default cost, 15.6% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 35.8 points at 42.2% of the default cost, 43.7% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 35.8 points at 42.2% of the default cost, 57.8% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
