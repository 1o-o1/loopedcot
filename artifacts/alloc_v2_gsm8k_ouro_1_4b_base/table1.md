# Table 1 -- gsm8k (ouro_1_4b_base), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 77130 layer passes over 1219 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 76.9 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | n/a | 61.6 |
| lookup | 20.3 | 50.8 | 64.5 | 73.3 |
| equation | 20.3 | 50.8 | 64.5 | 73.3 |
| equation_n30 | 20.3 | 49.9 | 64.4 | 73.3 |
| equation_n100 | 20.3 | 50.8 | 64.5 | 73.3 |
| gated_equation | 20.3 | 50.8 | 64.5 | 73.3 |
| avg_lookup | 21.7 | 55.2 | 66.1 | 74.2 |
| avg_equation | 21.7 | 55.2 | 69.1 | 73.7 |
| avg_gated_lookup | 21.7 | 55.2 | 66.1 | 74.2 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 19385 vs 19283 (+0.5%) | 38407 vs 38565 (-0.4%) | 57543 vs 57848 (-0.5%) | 77526 vs 77130 (+0.5%) |
| avg_equation | 19385 vs 19283 (+0.5%) | 38301 vs 38565 (-0.7%) | 57054 vs 57848 (-1.4%) | 76134 vs 77130 (-1.3%) |
| avg_gated_lookup | 19385 vs 19283 (+0.5%) | 38407 vs 38565 (-0.4%) | 57543 vs 57848 (-0.5%) | 77526 vs 77130 (+0.5%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
