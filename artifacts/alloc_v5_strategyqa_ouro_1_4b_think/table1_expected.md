# Table 1 -- strategyqa (ouro_1_4b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 108565 layer passes over 1990 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 72.4 | +0.2 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 69.7 | 72.2 | 72.6 | +0.0 |
| lookup | 61.0 | 69.7 | 71.0 | 71.0 | +1.6 |
| equation | 61.0 | 69.7 | 71.0 | 72.6 | +0.0 |
| equation_n30 | 61.0 | 67.5 | 72.2 | 72.6 | +0.0 |
| equation_n100 | 61.0 | 67.5 | 72.2 | 72.6 | +0.0 |
| gated_equation | 61.0 | 69.7 | 72.2 | 72.6 | +0.0 |
| avg_lookup | 63.3 | 69.6 | 71.0 | 71.0 | +1.6 |
| avg_equation | 63.0 | 70.9 | 70.6 | 72.3 | +0.3 |
| avg_gated_lookup | 63.4 | 68.4 | 71.0 | 71.0 | +1.6 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 2048, 72.6 points over 1990 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 27219 vs 27141 (+0.3%) | 53763 vs 54283 (-1.0%) | 75772 vs 81424 (-6.9%) | 75772 vs 108565 (-30.2%) |
| avg_equation | 26631 vs 27141 (-1.9%) | 53450 vs 54283 (-1.5%) | 80302 vs 81424 (-1.4%) | 108728 vs 108565 (+0.1%) |
| avg_gated_lookup | 26669 vs 27141 (-1.7%) | 53301 vs 54283 (-1.8%) | 75772 vs 81424 (-6.9%) | 75772 vs 108565 (-30.2%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 71.0 points at 69.8% of the default cost, 6.9% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 71.0 points at 69.8% of the default cost, 30.2% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 71.0 points at 69.8% of the default cost, 6.9% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 71.0 points at 69.8% of the default cost, 30.2% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
