# Table 1 -- bbh (huginn_0125), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 142666 layer passes over 2337 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 35.7 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | 55.8 (10%) | 61.0 (21%) | 52.5 (42%) | 35.9 (88%) |
| lookup | 30.6 | 31.4 | 33.6 | 35.4 |
| equation | 28.3 | 24.7 | 28.4 | 35.4 |
| equation_n30 | 31.8 | 34.4 | 34.6 | 34.5 |
| equation_n100 | 28.3 | 24.7 | 28.4 | 35.4 |
| gated_equation | 28.3 | 24.7 | 30.3 | 35.6 |
| avg_lookup | 32.1 | 35.3 | 36.4 | 35.3 |
| avg_equation | 29.0 | 30.0 | 35.8 | 36.5 |
| avg_gated_lookup | 32.1 | 35.3 | 36.4 | 35.3 |

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 34973 vs 35667 (-1.9%) | 69991 vs 71333 (-1.9%) | 106954 vs 107000 (-0.0%) | 142007 vs 142666 (-0.5%) |
| avg_equation | 36113 vs 35667 (+1.3%) | 70898 vs 71333 (-0.6%) | 108657 vs 107000 (+1.5%) | 138693 vs 142666 (-2.8%) |
| avg_gated_lookup | 34973 vs 35667 (-1.9%) | 69991 vs 71333 (-1.9%) | 106954 vs 107000 (-0.0%) | 142007 vs 142666 (-0.5%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
