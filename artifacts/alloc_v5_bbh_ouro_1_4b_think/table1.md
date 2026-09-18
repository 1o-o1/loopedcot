# Table 1 -- bbh (ouro_1_4b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 183913 layer passes over 2137 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 84.3 | +0.0 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 65.5 (10%) | 52.9 (72%) | 66.2 | 81.8 | +2.5 |
| lookup | 32.5 | 65.0 | 78.4 | 81.8 | +2.5 |
| equation | 40.1 | 65.0 | 78.4 | 82.2 | +2.1 |
| equation_n30 | 34.3 | 65.0 | 78.8 | 80.3 | +3.9 |
| equation_n100 | 34.3 | 65.0 | 78.4 | 81.8 | +2.5 |
| gated_equation | 35.0 | 49.4 (72%) | 78.8 | 81.8 | +2.5 |
| avg_lookup | 44.9 | 71.1 | 80.0 | 83.1 | +1.2 |
| avg_equation | 40.8 | 71.3 | 80.0 | 82.0 | +2.2 |
| avg_gated_lookup | 42.3 | 76.2 | 80.3 | 81.7 | +2.6 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 4096, 84.3 points over 2137 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0, F2, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 47864 vs 45978 (+4.1%) | 91506 vs 91957 (-0.5%) | 137189 vs 137935 (-0.5%) | 181156 vs 183913 (-1.5%) |
| avg_equation | 46007 vs 45978 (+0.1%) | 91833 vs 91957 (-0.1%) | 137189 vs 137935 (-0.5%) | 185288 vs 183913 (+0.7%) |
| avg_gated_lookup | 44067 vs 45978 (-4.2%) | 98468 vs 91957 (+7.1%) | 137592 vs 137935 (-0.2%) | 185686 vs 183913 (+1.0%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
