# Table 1 -- gsm8k (ouro_1_4b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 127112 layer passes over 1219 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 93.1 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 25.7 (28%) | 59.6 | 88.7 |
| lookup | 31.7 | 80.6 | 87.4 | 91.1 |
| equation | 31.7 | 80.6 | 87.4 | 91.1 |
| equation_n30 | 31.7 | 80.6 | 87.4 | 91.1 |
| equation_n100 | 31.7 | 80.6 | 87.4 | 91.1 |
| gated_equation | 31.7 | 80.6 | 87.4 | 91.1 |
| avg_lookup | 35.9 | 80.9 | 88.0 | 91.1 |
| avg_equation | 35.9 | 81.2 | 88.6 | 91.1 |
| avg_gated_lookup | 35.9 | 80.9 | 88.0 | 91.1 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 31139 vs 31778 (-2.0%) | 61580 vs 63556 (-3.1%) | 90846 vs 95334 (-4.7%) | 126258 vs 127112 (-0.7%) |
| avg_equation | 31139 vs 31778 (-2.0%) | 60180 vs 63556 (-5.3%) | 93810 vs 95334 (-1.6%) | 126258 vs 127112 (-0.7%) |
| avg_gated_lookup | 31139 vs 31778 (-2.0%) | 61580 vs 63556 (-3.1%) | 90846 vs 95334 (-4.7%) | 126258 vs 127112 (-0.7%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
