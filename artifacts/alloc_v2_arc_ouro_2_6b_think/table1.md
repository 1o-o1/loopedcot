# Table 1 -- arc (ouro_2_6b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 161239 layer passes over 1072 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 96.5 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 92.0 (91%) | 92.5 | 94.0 |
| lookup | 83.8 | 92.4 | 92.4 | 92.4 |
| equation | 74.3 | 91.9 | 92.4 | 96.3 |
| equation_n30 | 74.3 | 91.8 | 92.4 | 94.0 |
| equation_n100 | 74.3 | 91.9 | 92.4 | 96.3 |
| gated_equation | 74.3 | 91.9 | 92.5 | 96.3 |
| avg_lookup | 87.6 | 92.7 | 93.9 | 95.7 |
| avg_equation | 87.6 | 93.4 | 95.6 | 96.3 |
| avg_gated_lookup | 87.6 | 92.7 | 93.9 | 95.7 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 39959 vs 40310 (-0.9%) | 80394 vs 80620 (-0.3%) | 120410 vs 120930 (-0.4%) | 162082 vs 161239 (+0.5%) |
| avg_equation | 39959 vs 40310 (-0.9%) | 80092 vs 80620 (-0.7%) | 119088 vs 120930 (-1.5%) | 161239 vs 161239 (-0.0%) |
| avg_gated_lookup | 39959 vs 40310 (-0.9%) | 80394 vs 80620 (-0.3%) | 120410 vs 120930 (-0.4%) | 162082 vs 161239 (+0.5%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
