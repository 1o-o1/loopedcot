# Table 1 -- svamp (ouro_2_6b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 249394 layer passes over 200 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 7.0 | +61.5 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 5.6 (45%) | 12.5 | 6.5 | +62.0 |
| lookup | 68.5 | 68.5 | 68.5 | 68.5 | +0.0 |
| equation | 68.5 | 68.5 | 68.5 | 68.5 | +0.0 |
| equation_n30 | 68.5 | 68.5 | 68.5 | 68.5 | +0.0 |
| equation_n100 | 68.5 | 68.5 | 68.5 | 68.5 | +0.0 |
| gated_equation | 68.5 | 68.5 | 68.5 | 68.5 | +0.0 |
| avg_lookup | 68.5 | 68.5 | 68.5 | 68.5 | +0.0 |
| avg_equation | 68.5 | 68.5 | 68.5 | 68.5 | +0.0 |
| avg_gated_lookup | 68.5 | 68.5 | 68.5 | 68.5 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 1 at cap 1024, 68.5 points over 200 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 56160 vs 62348 (-9.9%) | 56160 vs 124697 (-55.0%) | 56160 vs 187045 (-70.0%) | 56160 vs 249394 (-77.5%) |
| avg_equation | 59280 vs 62348 (-4.9%) | 97753 vs 124697 (-21.6%) | 97753 vs 187045 (-47.7%) | 97753 vs 249394 (-60.8%) |
| avg_gated_lookup | 56160 vs 62348 (-9.9%) | 56160 vs 124697 (-55.0%) | 56160 vs 187045 (-70.0%) | 56160 vs 249394 (-77.5%) |
- `avg_lookup` at 0.25x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 22.5% of the default cost, 9.9% under the budget it was given.
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 22.5% of the default cost, 55.0% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 22.5% of the default cost, 70.0% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 22.5% of the default cost, 77.5% under the budget it was given.
- `avg_equation` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 39.2% of the default cost, 21.6% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 39.2% of the default cost, 47.7% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 39.2% of the default cost, 60.8% under the budget it was given.
- `avg_gated_lookup` at 0.25x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 22.5% of the default cost, 9.9% under the budget it was given.
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 22.5% of the default cost, 55.0% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 22.5% of the default cost, 70.0% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 22.5% of the default cost, 77.5% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
