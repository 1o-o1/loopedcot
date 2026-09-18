# Table 1 -- gsm8k (ouro_2_6b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 239639 layer passes over 1056 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 21.5 | +43.5 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | 18.6 | 25.2 | +39.8 |
| lookup | 57.1 | 62.8 | 65.0 | 65.0 | +0.0 |
| equation | 57.1 | 62.8 | 65.0 | 64.6 | +0.4 |
| equation_n30 | 57.1 | 62.8 | 65.0 | 64.6 | +0.4 |
| equation_n100 | 57.1 | 62.8 | 65.0 | 64.6 | +0.4 |
| gated_equation | 57.1 | 62.8 | 65.0 | 64.6 | +0.4 |
| avg_lookup | 57.8 | 63.8 | 65.0 | 65.0 | +0.0 |
| avg_equation | 57.4 | 64.9 | 64.8 | 64.6 | +0.4 |
| avg_gated_lookup | 58.2 | 64.1 | 65.0 | 65.0 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 1 at cap 2048, 65.0 points over 1056 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 60485 vs 59910 (+1.0%) | 111289 vs 119819 (-7.1%) | 130838 vs 179729 (-27.2%) | 130838 vs 239639 (-45.4%) |
| avg_equation | 57110 vs 59910 (-4.7%) | 119109 vs 119819 (-0.6%) | 174126 vs 179729 (-3.1%) | 229142 vs 239639 (-4.4%) |
| avg_gated_lookup | 59880 vs 59910 (-0.0%) | 118504 vs 119819 (-1.1%) | 130838 vs 179729 (-27.2%) | 130838 vs 239639 (-45.4%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 65.0 points at 54.6% of the default cost, 27.2% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 65.0 points at 54.6% of the default cost, 45.4% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 64.6 points at 95.6% of the default cost, 4.4% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 65.0 points at 54.6% of the default cost, 27.2% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 65.0 points at 54.6% of the default cost, 45.4% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
