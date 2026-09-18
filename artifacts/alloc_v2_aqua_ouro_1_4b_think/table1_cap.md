# Table 1 -- aqua (ouro_1_4b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 223283 layer passes over 154 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 82.5 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 50.0 | 78.6 | 78.6 |
| lookup | 49.4 | 74.0 | 81.2 | 84.4 |
| equation | 49.4 | 74.0 | 81.2 | 84.4 |
| equation_n30 | 49.4 | 74.0 | 81.2 | 84.4 |
| equation_n100 | 49.4 | 74.0 | 81.2 | 84.4 |
| gated_equation | 49.4 | 74.0 | 78.6 | 84.4 |
| avg_lookup | 57.1 | 76.6 | 81.2 | 84.4 |
| avg_equation | 57.1 | 76.6 | 85.1 | 85.7 |
| avg_gated_lookup | 57.1 | 76.6 | 81.2 | 84.4 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 56073 vs 55821 (+0.5%) | 107433 vs 111641 (-3.8%) | 170304 vs 167462 (+1.7%) | 210801 vs 223283 (-5.6%) |
| avg_equation | 56073 vs 55821 (+0.5%) | 107433 vs 111641 (-3.8%) | 172678 vs 167462 (+3.1%) | 224850 vs 223283 (+0.7%) |
| avg_gated_lookup | 56073 vs 55821 (+0.5%) | 107433 vs 111641 (-3.8%) | 170304 vs 167462 (+1.7%) | 210801 vs 223283 (-5.6%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
