# Table 1 -- strategyqa (ouro_2_6b_base), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 98679 layer passes over 1990 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 74.8 | +0.3 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | 74.3 (100%) | 75.2 | -0.1 |
| lookup | 59.8 | 69.7 | 73.7 | 74.7 | +0.5 |
| equation | 60.2 | 69.7 | 73.8 | 75.2 | -0.1 |
| equation_n30 | 59.8 | 69.7 | 74.3 | 75.2 | -0.1 |
| equation_n100 | 60.2 | 69.7 | 73.8 | 75.2 | -0.1 |
| gated_equation | 60.2 | 69.7 | 73.8 | 75.2 | -0.1 |
| avg_lookup | 62.5 | 70.4 | 73.5 | 74.7 | +0.5 |
| avg_equation | 61.6 | 70.4 | 73.8 | 75.1 | +0.1 |
| avg_gated_lookup | 61.6 | 71.5 | 73.5 | 74.7 | +0.5 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 128, 75.1 points over 1990 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 23861 vs 24670 (-3.3%) | 49382 vs 49339 (+0.1%) | 73101 vs 74009 (-1.2%) | 84009 vs 98679 (-14.9%) |
| avg_equation | 22192 vs 24670 (-10.0%) | 48407 vs 49339 (-1.9%) | 73492 vs 74009 (-0.7%) | 99347 vs 98679 (+0.7%) |
| avg_gated_lookup | 22192 vs 24670 (-10.0%) | 49496 vs 49339 (+0.3%) | 73101 vs 74009 (-1.2%) | 84009 vs 98679 (-14.9%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 74.7 points at 85.1% of the default cost, 14.9% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 74.7 points at 85.1% of the default cost, 14.9% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
