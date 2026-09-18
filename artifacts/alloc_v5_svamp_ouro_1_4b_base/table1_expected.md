# Table 1 -- svamp (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 65870 layer passes over 200 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 86.5 | +0.0 |
| default_cell | n/a | n/a | n/a | 92.4 (33%) | -5.9 |
| default_at_budget | n/a | n/a | n/a | 75.0 | +11.5 |
| lookup | 30.0 | 62.5 | 76.5 | 84.0 | +2.5 |
| equation | 33.5 | 62.5 | 77.0 | 86.5 | +0.0 |
| equation_n30 | 33.5 | 62.0 | 75.0 | 86.5 | +0.0 |
| equation_n100 | 33.5 | 62.5 | 77.0 | 86.5 | +0.0 |
| gated_equation | 33.5 | 62.5 | 77.0 | 85.5 | +1.0 |
| avg_lookup | 35.5 | 70.5 | 84.0 | 84.0 | +2.5 |
| avg_equation | 34.5 | 71.0 | 85.0 | 86.0 | +0.5 |
| avg_gated_lookup | 38.0 | 70.5 | 84.0 | 85.5 | +1.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 256, 86.5 points over 200 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 16356 vs 16467 (-0.7%) | 32711 vs 32935 (-0.7%) | 49213 vs 49402 (-0.4%) | 49643 vs 65870 (-24.6%) |
| avg_equation | 16379 vs 16467 (-0.5%) | 32782 vs 32935 (-0.5%) | 49282 vs 49402 (-0.2%) | 65770 vs 65870 (-0.2%) |
| avg_gated_lookup | 16467 vs 16467 (-0.0%) | 32711 vs 32935 (-0.7%) | 49213 vs 49402 (-0.4%) | 65277 vs 65870 (-0.9%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 84.0 points at 75.4% of the default cost, 24.6% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
