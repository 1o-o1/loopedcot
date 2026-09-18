# Table 1 -- bbh (ouro_2_6b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 320368 layer passes over 2137 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 91.2 | +0.0 |
| default_cell | n/a | n/a | 84.1 (10%) | 91.9 (21%) | -0.6 |
| default_at_budget | 85.9 (10%) | 79.3 (38%) | 62.8 (95%) | 90.4 | +0.9 |
| lookup | 48.1 | 79.7 | 87.1 | 89.9 | +1.3 |
| equation | 48.2 | 78.9 | 84.5 | 89.8 | +1.4 |
| equation_n30 | 48.7 | 79.9 | 87.0 | 89.9 | +1.4 |
| equation_n100 | 47.7 | 79.7 | 85.1 | 89.8 | +1.5 |
| gated_equation | 45.8 | 79.7 | 87.5 | 90.5 | +0.8 |
| avg_lookup | 50.1 | 82.6 | 88.9 | 91.4 | -0.1 |
| avg_equation | 51.0 | 82.3 | 88.8 | 91.4 | -0.1 |
| avg_gated_lookup | 50.1 | 82.6 | 88.9 | 89.8 | +1.4 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 4096, 91.2 points over 2137 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 79733 vs 80092 (-0.4%) | 156624 vs 160184 (-2.2%) | 235336 vs 240276 (-2.1%) | 320250 vs 320368 (-0.0%) |
| avg_equation | 79980 vs 80092 (-0.1%) | 156308 vs 160184 (-2.4%) | 236979 vs 240276 (-1.4%) | 320250 vs 320368 (-0.0%) |
| avg_gated_lookup | 79733 vs 80092 (-0.4%) | 154203 vs 160184 (-3.7%) | 231234 vs 240276 (-3.8%) | 257365 vs 320368 (-19.7%) |
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 89.8 points at 80.3% of the default cost, 19.7% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
