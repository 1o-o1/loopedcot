# Table 1 -- mmlu (ouro_1_4b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 134380 layer passes over 1700 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 73.6 | +0.4 |
| default_cell | n/a | n/a | n/a | 75.6 (44%) | -1.6 |
| default_at_budget | n/a | 66.2 (94%) | 70.6 | 73.7 | +0.3 |
| lookup | 58.2 | 70.1 | 73.4 | 73.8 | +0.2 |
| equation | 55.4 | 71.5 | 73.6 | 73.7 | +0.3 |
| equation_n30 | 56.2 | 69.2 | 73.5 | 74.0 | +0.0 |
| equation_n100 | 55.0 | 71.5 | 73.5 | 73.7 | +0.3 |
| gated_equation | 56.2 | 65.8 | 71.1 | 73.7 | +0.3 |
| avg_lookup | 63.6 | 71.7 | 73.0 | 73.6 | +0.4 |
| avg_equation | 60.2 | 71.2 | 73.6 | 73.8 | +0.2 |
| avg_gated_lookup | 63.4 | 71.6 | 72.5 | 72.5 | +1.5 |

The ORACLE GAP is the best single evaluation cell (depth 3 at cap 4096, 74.0 points over 1700 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 33419 vs 33595 (-0.5%) | 66895 vs 67190 (-0.4%) | 100879 vs 100785 (+0.1%) | 118412 vs 134380 (-11.9%) |
| avg_equation | 32467 vs 33595 (-3.4%) | 66581 vs 67190 (-0.9%) | 99026 vs 100785 (-1.7%) | 134496 vs 134380 (+0.1%) |
| avg_gated_lookup | 33311 vs 33595 (-0.8%) | 68075 vs 67190 (+1.3%) | 76239 vs 100785 (-24.4%) | 76239 vs 134380 (-43.3%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 73.6 points at 88.1% of the default cost, 11.9% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 72.5 points at 56.7% of the default cost, 24.4% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 72.5 points at 56.7% of the default cost, 43.3% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
