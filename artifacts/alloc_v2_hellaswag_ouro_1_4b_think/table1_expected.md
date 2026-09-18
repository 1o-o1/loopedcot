# Table 1 -- hellaswag (ouro_1_4b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 145803 layer passes over 1900 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 74.5 |
| default_cell | n/a | n/a | n/a | 74.3 (81%) |
| default_at_budget | n/a | 69.4 (33%) | 72.8 | 74.5 |
| lookup | 38.3 | 76.9 | 76.3 | 76.3 |
| equation | 37.8 | 69.5 | 71.9 | 74.4 |
| equation_n30 | 37.8 | 69.6 | 71.9 | 71.9 |
| equation_n100 | 37.8 | 69.5 | 71.9 | 74.4 |
| gated_equation | 37.8 | 69.5 | 73.5 | 74.5 |
| avg_lookup | 54.5 | 76.7 | 76.3 | 76.3 |
| avg_equation | 56.8 | 73.8 | 73.4 | 74.4 |
| avg_gated_lookup | 54.5 | 76.7 | 76.3 | 76.3 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 36067 vs 36451 (-1.1%) | 73256 vs 72901 (+0.5%) | 76682 vs 109352 (-29.9%) | 76682 vs 145803 (-47.4%) |
| avg_equation | 36136 vs 36451 (-0.9%) | 74236 vs 72901 (+1.8%) | 107352 vs 109352 (-1.8%) | 131879 vs 145803 (-9.5%) |
| avg_gated_lookup | 36067 vs 36451 (-1.1%) | 73256 vs 72901 (+0.5%) | 76682 vs 109352 (-29.9%) | 76682 vs 145803 (-47.4%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 76.3 points at 52.6% of the default cost, 29.9% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 76.3 points at 52.6% of the default cost, 47.4% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 74.4 points at 90.5% of the default cost, 9.5% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 76.3 points at 52.6% of the default cost, 29.9% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 76.3 points at 52.6% of the default cost, 47.4% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
