# Table 1 -- svamp (ouro_1_4b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 129897 layer passes over 200 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 89.5 | +0.5 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 59.5 (98%) | 87.0 | 89.0 | +1.0 |
| lookup | 47.5 | 85.5 | 87.0 | 87.0 | +3.0 |
| equation | 52.5 | 85.5 | 86.0 | 84.5 | +5.5 |
| equation_n30 | 52.5 | 85.0 | 86.0 | 86.5 | +3.5 |
| equation_n100 | 52.5 | 85.5 | 86.0 | 84.5 | +5.5 |
| gated_equation | 52.5 | 71.5 | 86.0 | 86.5 | +3.5 |
| avg_lookup | 64.0 | 86.0 | 87.5 | 88.5 | +1.5 |
| avg_equation | 64.0 | 86.5 | 87.0 | 86.5 | +3.5 |
| avg_gated_lookup | 64.0 | 86.0 | 87.0 | 87.0 | +3.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 2048, 90.0 points over 200 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 34996 vs 32474 (+7.8%) | 63380 vs 64949 (-2.4%) | 114001 vs 97423 (+17.0%) | 142469 vs 129897 (+9.7%) |
| avg_equation | 34996 vs 32474 (+7.8%) | 64486 vs 64949 (-0.7%) | 96435 vs 97423 (-1.0%) | 129934 vs 129897 (+0.0%) |
| avg_gated_lookup | 34996 vs 32474 (+7.8%) | 62643 vs 64949 (-3.6%) | 80460 vs 97423 (-17.4%) | 80460 vs 129897 (-38.1%) |
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 87.0 points at 61.9% of the default cost, 17.4% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 87.0 points at 61.9% of the default cost, 38.1% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
