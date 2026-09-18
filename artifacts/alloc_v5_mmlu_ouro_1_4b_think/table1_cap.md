# Table 1 -- mmlu (ouro_1_4b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 134380 layer passes over 1700 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 73.6 | +0.4 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 65.8 (94%) | 69.4 | 70.7 | +3.3 |
| lookup | 58.2 | 64.4 | 71.6 | 72.4 | +1.6 |
| equation | 55.6 | 64.8 | 70.6 | 72.5 | +1.5 |
| equation_n30 | 56.1 | 64.9 | 71.5 | 72.4 | +1.6 |
| equation_n100 | 55.2 | 64.8 | 70.6 | 72.5 | +1.5 |
| gated_equation | 56.1 | 65.4 | 70.6 | 70.6 | +3.4 |
| avg_lookup | 63.6 | 69.9 | 71.1 | 72.8 | +1.2 |
| avg_equation | 58.6 | 70.1 | 72.2 | 72.8 | +1.2 |
| avg_gated_lookup | 63.4 | 69.9 | 72.0 | 72.5 | +1.5 |

The ORACLE GAP is the best single evaluation cell (depth 3 at cap 4096, 74.0 points over 1700 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 33419 vs 33595 (-0.5%) | 65462 vs 67190 (-2.6%) | 99171 vs 100785 (-1.6%) | 133221 vs 134380 (-0.9%) |
| avg_equation | 32165 vs 33595 (-4.3%) | 66508 vs 67190 (-1.0%) | 100895 vs 100785 (+0.1%) | 133484 vs 134380 (-0.7%) |
| avg_gated_lookup | 33311 vs 33595 (-0.8%) | 66264 vs 67190 (-1.4%) | 101719 vs 100785 (+0.9%) | 110631 vs 134380 (-17.7%) |
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 72.5 points at 82.3% of the default cost, 17.7% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
