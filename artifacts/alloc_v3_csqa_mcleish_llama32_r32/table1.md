# Table 1 -- csqa (mcleish_llama32_r32), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 35104 layer passes over 1121 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 38.1 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | n/a | 39.9 (100%) |
| lookup | 21.4 (100%) | 30.0 | 42.2 | 42.2 |
| equation | 21.4 (100%) | 32.7 | 42.2 | 42.2 |
| equation_n30 | 21.4 (100%) | 28.0 | 42.2 | 42.2 |
| equation_n100 | 21.4 (100%) | 32.7 | 42.2 | 42.2 |
| gated_equation | 21.4 (100%) | 32.7 | 42.2 | 39.8 |
| avg_lookup | 22.1 | 39.9 | 42.4 | 42.2 |
| avg_equation | 22.2 | 39.9 | 42.4 | 42.2 |
| avg_gated_lookup | 22.1 | 39.9 | 42.2 | 42.2 |

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 8701 vs 8776 (-0.9%) | 17229 vs 17552 (-1.8%) | 25337 vs 26328 (-3.8%) | 33234 vs 35104 (-5.3%) |
| avg_equation | 8669 vs 8776 (-1.2%) | 17147 vs 17552 (-2.3%) | 25337 vs 26328 (-3.8%) | 33234 vs 35104 (-5.3%) |
| avg_gated_lookup | 8701 vs 8776 (-0.9%) | 17229 vs 17552 (-1.8%) | 18991 vs 26328 (-27.9%) | 18991 vs 35104 (-45.9%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 42.2 points at 94.7% of the default cost, 5.3% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 42.2 points at 94.7% of the default cost, 5.3% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 42.2 points at 54.1% of the default cost, 27.9% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 42.2 points at 54.1% of the default cost, 45.9% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
