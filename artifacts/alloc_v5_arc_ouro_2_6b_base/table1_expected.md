# Table 1 -- arc (ouro_2_6b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 77524 layer passes over 938 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 93.1 | +0.0 |
| default_cell | n/a | n/a | n/a | 92.6 (57%) | +0.5 |
| default_at_budget | n/a | n/a | n/a | 92.9 (93%) | +0.2 |
| lookup | 63.3 (93%) | 86.8 | 91.0 | 92.0 | +1.1 |
| equation | 56.3 (93%) | 85.7 | 91.2 | 91.7 | +1.4 |
| equation_n30 | 56.3 (93%) | 85.7 | 91.2 | 91.9 | +1.2 |
| equation_n100 | 56.3 (93%) | 85.7 | 91.2 | 91.7 | +1.4 |
| gated_equation | 56.3 (93%) | 85.9 | 91.2 | 92.2 (93%) | +0.9 |
| avg_lookup | 66.1 | 88.5 | 91.8 | 92.2 | +0.9 |
| avg_equation | 57.0 | 88.1 | 91.7 | 91.7 | +1.4 |
| avg_gated_lookup | 65.4 | 88.7 | 91.3 | 91.3 | +1.8 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 128, 93.1 points over 938 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 19186 vs 19381 (-1.0%) | 38281 vs 38762 (-1.2%) | 57835 vs 58143 (-0.5%) | 70185 vs 77524 (-9.5%) |
| avg_equation | 19305 vs 19381 (-0.4%) | 38579 vs 38762 (-0.5%) | 58018 vs 58143 (-0.2%) | 58072 vs 77524 (-25.1%) |
| avg_gated_lookup | 18996 vs 19381 (-2.0%) | 38401 vs 38762 (-0.9%) | 57194 vs 58143 (-1.6%) | 57194 vs 77524 (-26.2%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 92.2 points at 90.5% of the default cost, 9.5% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 91.7 points at 74.9% of the default cost, 25.1% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 91.3 points at 73.8% of the default cost, 1.6% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 91.3 points at 73.8% of the default cost, 26.2% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
