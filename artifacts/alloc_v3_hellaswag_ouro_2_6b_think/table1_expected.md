# Table 1 -- hellaswag (ouro_2_6b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 280144 layer passes over 1900 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 81.2 |
| default_cell | n/a | n/a | n/a | 77.5 (32%) |
| default_at_budget | n/a | 74.9 (31%) | 81.3 | 81.4 |
| lookup | 40.5 | 80.7 | 79.8 | 79.8 |
| equation | 39.9 | 74.6 | 79.1 | 79.1 |
| equation_n30 | 39.9 | 74.6 | 74.2 | 74.2 |
| equation_n100 | 39.9 | 74.6 | 79.1 | 79.1 |
| gated_equation | 39.9 | 74.8 | 81.3 | 81.4 |
| avg_lookup | 64.4 | 79.5 | 79.8 | 79.8 |
| avg_equation | 64.6 | 74.2 | 79.1 | 79.1 |
| avg_gated_lookup | 63.9 | 79.8 | 79.8 | 79.8 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 69498 vs 70036 (-0.8%) | 143386 vs 140072 (+2.4%) | 149520 vs 210108 (-28.8%) | 149520 vs 280144 (-46.6%) |
| avg_equation | 69391 vs 70036 (-0.9%) | 137646 vs 140072 (-1.7%) | 200449 vs 210108 (-4.6%) | 200449 vs 280144 (-28.4%) |
| avg_gated_lookup | 69118 vs 70036 (-1.3%) | 141230 vs 140072 (+0.8%) | 149520 vs 210108 (-28.8%) | 149520 vs 280144 (-46.6%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 79.8 points at 53.4% of the default cost, 28.8% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 79.8 points at 53.4% of the default cost, 46.6% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 79.1 points at 71.6% of the default cost, 4.6% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 79.1 points at 71.6% of the default cost, 28.4% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 79.8 points at 53.4% of the default cost, 28.8% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 79.8 points at 53.4% of the default cost, 46.6% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
