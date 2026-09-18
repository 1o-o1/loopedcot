# Table 1 -- bbh (mcleish_llama32_r32), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 69931 layer passes over 2137 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 43.5 | +0.2 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 50.0 (10%) | 54.8 (31%) | 42.8 (72%) | 43.6 (99%) | +0.1 |
| lookup | 33.0 (99%) | 40.1 | 42.7 | 43.5 | +0.2 |
| equation | 34.5 (99%) | 40.1 | 43.0 | 44.1 | -0.4 |
| equation_n30 | 34.9 (99%) | 35.0 | 34.4 | 34.4 | +9.3 |
| equation_n100 | 34.5 (99%) | 38.4 | 42.2 | 43.6 | +0.1 |
| gated_equation | 34.5 (99%) | 40.1 | 42.7 | 42.7 | +1.0 |
| avg_lookup | 34.8 | 42.0 | 43.9 | 43.6 | +0.1 |
| avg_equation | 35.1 | 42.3 | 43.9 | 43.8 | -0.0 |
| avg_gated_lookup | 34.2 | 40.4 | 43.6 | 43.6 | +0.1 |

The ORACLE GAP is the best single evaluation cell (depth 8 at cap 512, 43.7 points over 2137 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3.

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 17530 vs 17483 (+0.3%) | 34684 vs 34966 (-0.8%) | 52405 vs 52448 (-0.1%) | 56665 vs 69931 (-19.0%) |
| avg_equation | 17290 vs 17483 (-1.1%) | 33589 vs 34966 (-3.9%) | 52405 vs 52448 (-0.1%) | 67955 vs 69931 (-2.8%) |
| avg_gated_lookup | 17879 vs 17483 (+2.3%) | 36016 vs 34966 (+3.0%) | 56665 vs 52448 (+8.0%) | 56665 vs 69931 (-19.0%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 43.6 points at 81.0% of the default cost, 19.0% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 43.6 points at 81.0% of the default cost, 19.0% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
