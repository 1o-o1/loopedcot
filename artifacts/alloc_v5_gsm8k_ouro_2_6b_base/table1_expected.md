# Table 1 -- gsm8k (ouro_2_6b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 151176 layer passes over 1056 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 82.8 | +0.0 |
| default_cell | n/a | n/a | n/a | 88.2 (61%) | -5.5 |
| default_at_budget | n/a | n/a | n/a | 77.4 | +5.4 |
| lookup | 29.3 | 69.4 | 77.2 | 82.0 | +0.8 |
| equation | 29.3 | 69.4 | 77.2 | 82.0 | +0.8 |
| equation_n30 | 29.3 | 69.4 | 75.0 | 80.5 | +2.3 |
| equation_n100 | 29.3 | 69.4 | 77.2 | 82.0 | +0.8 |
| gated_equation | 29.3 | 69.1 | 77.2 | 82.0 | +0.8 |
| avg_lookup | 32.2 | 75.1 | 79.0 | 82.8 | +0.0 |
| avg_equation | 32.2 | 75.1 | 79.0 | 82.8 | +0.0 |
| avg_gated_lookup | 32.2 | 74.0 | 78.9 | 82.8 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 512, 82.8 points over 1056 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 38195 vs 37794 (+1.1%) | 76038 vs 75588 (+0.6%) | 113722 vs 113382 (+0.3%) | 148430 vs 151176 (-1.8%) |
| avg_equation | 38195 vs 37794 (+1.1%) | 76038 vs 75588 (+0.6%) | 113722 vs 113382 (+0.3%) | 148430 vs 151176 (-1.8%) |
| avg_gated_lookup | 38192 vs 37794 (+1.1%) | 76491 vs 75588 (+1.2%) | 114197 vs 113382 (+0.7%) | 150673 vs 151176 (-0.3%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 82.8 points at 98.2% of the default cost, 1.8% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 82.8 points at 98.2% of the default cost, 1.8% under the budget it was given.
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin -1.3 points, sd 1.2, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 0.3% of the budget, 99.7% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
