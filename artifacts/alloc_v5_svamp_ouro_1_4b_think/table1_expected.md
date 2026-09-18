# Table 1 -- svamp (ouro_1_4b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 129897 layer passes over 200 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 89.5 | +0.5 |
| default_cell | n/a | n/a | n/a | 93.1 (50%) | -3.1 |
| default_at_budget | n/a | 59.5 (98%) | 88.5 | 89.5 | +0.5 |
| lookup | 47.5 | 87.0 | 87.5 | 87.5 | +2.5 |
| equation | 52.5 | 86.5 | 87.5 | 87.5 | +2.5 |
| equation_n30 | 52.5 | 86.5 | 87.5 | 87.5 | +2.5 |
| equation_n100 | 52.5 | 86.5 | 87.5 | 87.5 | +2.5 |
| gated_equation | 52.5 | 77.5 | 87.5 | 87.5 | +2.5 |
| avg_lookup | 61.5 | 88.0 | 87.5 | 87.5 | +2.5 |
| avg_equation | 64.0 | 87.0 | 87.5 | 87.5 | +2.5 |
| avg_gated_lookup | 64.0 | 87.0 | 87.0 | 87.0 | +3.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 2048, 90.0 points over 200 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 34920 vs 32474 (+7.5%) | 67981 vs 64949 (+4.7%) | 90826 vs 97423 (-6.8%) | 90826 vs 129897 (-30.1%) |
| avg_equation | 34470 vs 32474 (+6.1%) | 65774 vs 64949 (+1.3%) | 90826 vs 97423 (-6.8%) | 90826 vs 129897 (-30.1%) |
| avg_gated_lookup | 34470 vs 32474 (+6.1%) | 54122 vs 64949 (-16.7%) | 54122 vs 97423 (-44.4%) | 54122 vs 129897 (-58.3%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 87.5 points at 69.9% of the default cost, 6.8% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 87.5 points at 69.9% of the default cost, 30.1% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 87.5 points at 69.9% of the default cost, 6.8% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 87.5 points at 69.9% of the default cost, 30.1% under the budget it was given.
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 87.0 points at 41.7% of the default cost, 16.7% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 87.0 points at 41.7% of the default cost, 44.4% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 87.0 points at 41.7% of the default cost, 58.3% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
