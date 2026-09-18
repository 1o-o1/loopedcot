# Table 1 -- strategyqa (ouro_2_6b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 98679 layer passes over 1990 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 74.8 | +0.3 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | 74.3 (100%) | 74.8 | +0.3 |
| lookup | 59.8 | 69.7 | 73.7 | 74.7 | +0.5 |
| equation | 59.7 | 69.9 | 73.8 | 74.9 | +0.3 |
| equation_n30 | 59.8 | 69.9 | 73.7 | 74.9 | +0.3 |
| equation_n100 | 59.7 | 69.9 | 73.8 | 74.9 | +0.3 |
| gated_equation | 59.7 | 69.9 | 73.8 | 74.8 | +0.3 |
| avg_lookup | 62.5 | 71.4 | 74.0 | 74.7 | +0.5 |
| avg_equation | 61.8 | 70.7 | 74.4 | 74.9 | +0.3 |
| avg_gated_lookup | 61.7 | 71.5 | 74.0 | 74.7 | +0.5 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 128, 75.1 points over 1990 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 23860 vs 24670 (-3.3%) | 49417 vs 49339 (+0.2%) | 73814 vs 74009 (-0.3%) | 81127 vs 98679 (-17.8%) |
| avg_equation | 22777 vs 24670 (-7.7%) | 47986 vs 49339 (-2.7%) | 73169 vs 74009 (-1.1%) | 96621 vs 98679 (-2.1%) |
| avg_gated_lookup | 22594 vs 24670 (-8.4%) | 49097 vs 49339 (-0.5%) | 73814 vs 74009 (-0.3%) | 81127 vs 98679 (-17.8%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 74.7 points at 82.2% of the default cost, 17.8% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 74.7 points at 82.2% of the default cost, 17.8% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
