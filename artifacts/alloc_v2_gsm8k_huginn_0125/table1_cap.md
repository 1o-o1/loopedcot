# Table 1 -- gsm8k (huginn_0125), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 104580 layer passes over 1219 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 26.3 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | 2.1 (12%) | 22.8 |
| lookup | 5.2 | 18.9 | 21.3 | 22.9 |
| equation | 5.3 | 18.8 | 21.3 | 21.3 |
| equation_n30 | 5.1 | 18.9 | 21.3 | 22.9 |
| equation_n100 | 5.3 | 18.8 | 21.3 | 21.3 |
| gated_equation | 5.3 | 18.8 | 21.3 | 22.9 |
| avg_lookup | 8.4 | 18.7 | 23.0 | 24.9 |
| avg_equation | 11.9 | 19.4 | 23.0 | 24.9 |
| avg_gated_lookup | 8.4 | 18.7 | 23.0 | 24.9 |

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 25142 vs 26145 (-3.8%) | 49686 vs 52290 (-5.0%) | 75289 vs 78435 (-4.0%) | 101097 vs 104580 (-3.3%) |
| avg_equation | 25719 vs 26145 (-1.6%) | 51953 vs 52290 (-0.6%) | 75289 vs 78435 (-4.0%) | 101097 vs 104580 (-3.3%) |
| avg_gated_lookup | 25142 vs 26145 (-3.8%) | 49686 vs 52290 (-5.0%) | 75289 vs 78435 (-4.0%) | 101097 vs 104580 (-3.3%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
