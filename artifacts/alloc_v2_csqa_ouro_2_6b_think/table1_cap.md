# Table 1 -- csqa (ouro_2_6b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 235620 layer passes over 1121 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 80.8 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | 79.2 | 79.9 |
| lookup | 27.4 | 77.4 | 79.2 | 79.2 |
| equation | 19.6 | 76.6 | 78.2 | 79.9 |
| equation_n30 | 27.4 | 80.3 | 78.2 | 78.2 |
| equation_n100 | 19.6 | 76.6 | 78.2 | 79.9 |
| gated_equation | 19.6 | 76.6 | 78.2 | 79.9 |
| avg_lookup | 66.9 | 77.6 | 79.6 | 79.9 |
| avg_equation | 66.9 | 77.4 | 77.9 | 80.1 |
| avg_gated_lookup | 66.9 | 77.6 | 79.6 | 79.9 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 57972 vs 58905 (-1.6%) | 113046 vs 117810 (-4.0%) | 176952 vs 176715 (+0.1%) | 242854 vs 235620 (+3.1%) |
| avg_equation | 57972 vs 58905 (-1.6%) | 116329 vs 117810 (-1.3%) | 167329 vs 176715 (-5.3%) | 229218 vs 235620 (-2.7%) |
| avg_gated_lookup | 57972 vs 58905 (-1.6%) | 113046 vs 117810 (-4.0%) | 176952 vs 176715 (+0.1%) | 242854 vs 235620 (+3.1%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
