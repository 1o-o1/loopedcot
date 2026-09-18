# Table 1 -- gsm8k (ouro_1_4b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 127112 layer passes over 1219 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 93.1 |
| default_cell | n/a | n/a | n/a | 93.5 (95%) |
| default_at_budget | n/a | 25.7 (28%) | 59.7 | 93.1 |
| lookup | 31.7 | 85.9 | 91.5 | 93.0 |
| equation | 31.7 | 85.9 | 91.8 | 93.0 |
| equation_n30 | 31.7 | 85.9 | 91.8 | 91.8 |
| equation_n100 | 31.7 | 85.9 | 91.8 | 93.0 |
| gated_equation | 31.7 | 85.9 | 91.8 | 93.1 |
| avg_lookup | 37.6 | 86.9 | 91.8 | 93.0 |
| avg_equation | 37.6 | 86.9 | 91.8 | 93.0 |
| avg_gated_lookup | 37.6 | 86.9 | 91.8 | 93.1 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 30863 vs 31778 (-2.9%) | 63695 vs 63556 (+0.2%) | 95648 vs 95334 (+0.3%) | 118650 vs 127112 (-6.7%) |
| avg_equation | 30863 vs 31778 (-2.9%) | 63853 vs 63556 (+0.5%) | 95648 vs 95334 (+0.3%) | 118650 vs 127112 (-6.7%) |
| avg_gated_lookup | 30863 vs 31778 (-2.9%) | 63695 vs 63556 (+0.2%) | 95648 vs 95334 (+0.3%) | 122882 vs 127112 (-3.3%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 93.0 points at 93.3% of the default cost, 6.7% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 93.0 points at 93.3% of the default cost, 6.7% under the budget it was given.
- `avg_gated_lookup` reverted to the default cell for every question at 1.00x: the predicted calibration margin did not clear 0.50 of its own SD.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
