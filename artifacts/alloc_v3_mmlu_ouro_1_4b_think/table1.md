# Table 1 -- mmlu (ouro_1_4b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 134109 layer passes over 1900 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 73.7 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 65.3 (95%) | 69.5 | 70.7 |
| lookup | 58.4 | 64.7 | 71.7 | 72.5 |
| equation | 56.9 | 65.4 | 70.8 | 70.7 |
| equation_n30 | 56.3 | 65.4 | 70.8 | 72.6 |
| equation_n100 | 56.9 | 65.4 | 70.8 | 70.7 |
| gated_equation | 56.5 | 64.8 | 70.9 | 70.7 |
| avg_lookup | 63.8 | 68.7 | 72.2 | 72.2 |
| avg_equation | 63.4 | 68.9 | 71.0 | 72.5 |
| avg_gated_lookup | 62.3 | 65.3 | 71.8 | 72.6 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 33251 vs 33527 (-0.8%) | 66262 vs 67055 (-1.2%) | 97020 vs 100582 (-3.5%) | 130323 vs 134109 (-2.8%) |
| avg_equation | 33052 vs 33527 (-1.4%) | 66093 vs 67055 (-1.4%) | 100360 vs 100582 (-0.2%) | 134404 vs 134109 (+0.2%) |
| avg_gated_lookup | 33541 vs 33527 (+0.0%) | 67273 vs 67055 (+0.3%) | 99359 vs 100582 (-1.2%) | 137351 vs 134109 (+2.4%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
