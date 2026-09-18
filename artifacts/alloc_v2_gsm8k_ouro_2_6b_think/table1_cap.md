# Table 1 -- gsm8k (ouro_2_6b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 237574 layer passes over 1219 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 21.7 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | 16.5 | 24.6 |
| lookup | 57.3 | 63.1 | 65.1 | 65.1 |
| equation | 57.3 | 63.1 | 65.1 | 64.8 |
| equation_n30 | 57.3 | 63.1 | 65.1 | 64.8 |
| equation_n100 | 57.3 | 63.1 | 65.1 | 64.8 |
| gated_equation | 57.3 | 63.1 | 65.1 | 64.8 |
| avg_lookup | 58.4 | 64.5 | 65.1 | 65.1 |
| avg_equation | 57.9 | 64.6 | 65.1 | 64.8 |
| avg_gated_lookup | 58.4 | 64.5 | 65.1 | 65.1 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 59818 vs 59394 (+0.7%) | 117458 vs 118787 (-1.1%) | 130844 vs 178181 (-26.6%) | 130844 vs 237574 (-44.9%) |
| avg_equation | 57116 vs 59394 (-3.8%) | 122337 vs 118787 (+3.0%) | 176166 vs 178181 (-1.1%) | 229148 vs 237574 (-3.5%) |
| avg_gated_lookup | 59818 vs 59394 (+0.7%) | 117458 vs 118787 (-1.1%) | 130844 vs 178181 (-26.6%) | 130844 vs 237574 (-44.9%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 65.1 points at 55.1% of the default cost, 26.6% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 65.1 points at 55.1% of the default cost, 44.9% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 64.8 points at 96.5% of the default cost, 3.5% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 65.1 points at 55.1% of the default cost, 26.6% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 65.1 points at 55.1% of the default cost, 44.9% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
