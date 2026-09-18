# Table 1 -- csqa (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 61952 layer passes over 1121 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 72.3 |
| default_cell | n/a | n/a | n/a | 73.6 (55%) |
| default_at_budget | n/a | n/a | n/a | 72.1 |
| lookup | 33.6 | 65.6 | 71.8 | 73.1 |
| equation | 33.0 | 61.6 | 71.1 | 72.0 |
| equation_n30 | 32.3 | 61.6 | 71.3 | 73.1 |
| equation_n100 | 33.0 | 61.6 | 71.1 | 72.0 |
| gated_equation | 33.0 | 61.6 | 71.3 | 72.0 |
| avg_lookup | 31.0 | 65.7 | 71.3 | 73.1 |
| avg_equation | 33.6 | 61.8 | 71.4 | 72.3 |
| avg_gated_lookup | 33.2 | 64.3 | 71.6 | 72.3 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 15240 vs 15488 (-1.6%) | 30124 vs 30976 (-2.8%) | 46214 vs 46464 (-0.5%) | 58626 vs 61952 (-5.4%) |
| avg_equation | 15475 vs 15488 (-0.1%) | 31071 vs 30976 (+0.3%) | 46531 vs 46464 (+0.1%) | 61970 vs 61952 (+0.0%) |
| avg_gated_lookup | 15434 vs 15488 (-0.3%) | 30482 vs 30976 (-1.6%) | 45464 vs 46464 (-2.2%) | 61970 vs 61952 (+0.0%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 73.1 points at 94.6% of the default cost, 5.4% under the budget it was given.
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin -6.7 points, sd 6.6, bar 0.50 sd (30 verification questions, the ids after the 50 that fit, out of 100 calibration); cost saving -0.0% of the budget, 100.0% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
