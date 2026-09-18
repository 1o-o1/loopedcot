# Table 1 -- bbh (ouro_1_4b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 182991 layer passes over 2337 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 84.4 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | 66.2 (10%) | 52.8 (72%) | 66.5 | 81.3 |
| lookup | 35.1 | 64.4 | 78.6 | 81.3 |
| equation | 35.5 | 62.0 | 78.9 | 80.5 |
| equation_n30 | 35.5 | 62.0 | 78.9 | 80.5 |
| equation_n100 | 35.5 | 62.0 | 78.9 | 80.5 |
| gated_equation | 35.5 | 62.0 | 78.6 | 81.7 |
| avg_lookup | 45.2 | 72.1 | 80.1 | 83.0 |
| avg_equation | 43.6 | 71.5 | 80.1 | 82.0 |
| avg_gated_lookup | 45.2 | 72.1 | 80.1 | 83.0 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 47910 vs 45748 (+4.7%) | 89010 vs 91495 (-2.7%) | 137121 vs 137243 (-0.1%) | 180778 vs 182991 (-1.2%) |
| avg_equation | 47686 vs 45748 (+4.2%) | 88978 vs 91495 (-2.8%) | 136101 vs 137243 (-0.8%) | 180363 vs 182991 (-1.4%) |
| avg_gated_lookup | 47910 vs 45748 (+4.7%) | 89010 vs 91495 (-2.7%) | 137121 vs 137243 (-0.1%) | 180778 vs 182991 (-1.2%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
