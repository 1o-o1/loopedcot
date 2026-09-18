# Table 1 -- hellaswag (ouro_1_4b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 145921 layer passes over 1700 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 74.8 | +2.9 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 68.6 (32%) | 70.8 | 75.0 | +2.6 |
| lookup | 37.9 | 76.6 | 77.6 | 77.6 | +0.0 |
| equation | 37.4 | 69.3 | 70.9 | 71.6 | +6.1 |
| equation_n30 | 36.4 | 69.3 | 70.9 | 71.6 | +6.1 |
| equation_n100 | 37.4 | 69.3 | 70.9 | 71.6 | +6.1 |
| gated_equation | 37.4 | 69.3 (32%) | 77.6 | 77.6 | +0.0 |
| avg_lookup | 56.3 | 77.5 | 77.6 | 77.6 | +0.0 |
| avg_equation | 56.7 | 67.1 | 70.8 | 71.7 | +5.9 |
| avg_gated_lookup | 54.9 | 77.2 | 76.6 | 76.6 | +1.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 0, 77.6 points over 1700 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 36074 vs 36480 (-1.1%) | 73178 vs 72960 (+0.3%) | 75221 vs 109441 (-31.3%) | 75221 vs 145921 (-48.5%) |
| avg_equation | 35956 vs 36480 (-1.4%) | 73872 vs 72960 (+1.2%) | 111213 vs 109441 (+1.6%) | 147405 vs 145921 (+1.0%) |
| avg_gated_lookup | 35939 vs 36480 (-1.5%) | 73202 vs 72960 (+0.3%) | 81365 vs 109441 (-25.7%) | 81365 vs 145921 (-44.2%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 77.6 points at 51.5% of the default cost, 31.3% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 77.6 points at 51.5% of the default cost, 48.5% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 76.6 points at 55.8% of the default cost, 25.7% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 76.6 points at 55.8% of the default cost, 44.2% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
