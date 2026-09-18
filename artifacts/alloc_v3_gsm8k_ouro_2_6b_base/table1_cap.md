# Table 1 -- gsm8k (ouro_2_6b_base), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 151460 layer passes over 1219 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 82.7 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | n/a | 63.7 |
| lookup | 23.4 | 52.7 | 73.5 | 78.4 |
| equation | 23.5 | 52.8 | 73.6 | 78.4 |
| equation_n30 | 23.5 | 52.8 | 73.6 | 78.4 |
| equation_n100 | 23.5 | 52.8 | 73.6 | 78.4 |
| gated_equation | 23.5 | 52.8 | 73.6 | 78.4 |
| avg_lookup | 26.3 | 61.4 | 74.5 | 78.3 |
| avg_equation | 26.3 | 61.3 | 74.5 | 78.3 |
| avg_gated_lookup | 26.3 | 61.4 | 74.4 | 77.8 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 38030 vs 37865 (+0.4%) | 75353 vs 75730 (-0.5%) | 108773 vs 113595 (-4.2%) | 149618 vs 151460 (-1.2%) |
| avg_equation | 38030 vs 37865 (+0.4%) | 74874 vs 75730 (-1.1%) | 108138 vs 113595 (-4.8%) | 149037 vs 151460 (-1.6%) |
| avg_gated_lookup | 38030 vs 37865 (+0.4%) | 75353 vs 75730 (-0.5%) | 105108 vs 113595 (-7.5%) | 145198 vs 151460 (-4.1%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
