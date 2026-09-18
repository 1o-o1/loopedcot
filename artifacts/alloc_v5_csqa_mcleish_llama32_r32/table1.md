# Table 1 -- csqa (mcleish_llama32_r32), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 35107 layer passes over 977 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 39.0 | +3.9 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | n/a | 41.1 (100%) | +1.8 |
| lookup | 20.9 (100%) | 30.0 | 42.6 | 42.9 | +0.0 |
| equation | 20.9 (100%) | 33.1 | 42.6 | 42.9 | +0.0 |
| equation_n30 | 22.0 (100%) | 22.5 | 42.6 | 42.9 | +0.0 |
| equation_n100 | 22.0 (100%) | 33.1 | 35.6 | 35.6 | +7.3 |
| gated_equation | 20.9 (100%) | 33.1 | 42.6 | 42.9 (100%) | -0.0 |
| avg_lookup | 21.7 | 40.2 | 42.7 | 42.9 | +0.0 |
| avg_equation | 21.9 | 40.1 | 42.7 | 42.9 | +0.0 |
| avg_gated_lookup | 21.7 | 40.2 | 42.6 | 42.6 | +0.3 |

The ORACLE GAP is the best single evaluation cell (depth 8 at cap 0, 42.9 points over 977 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0.

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 8705 vs 8777 (-0.8%) | 17210 vs 17553 (-2.0%) | 25320 vs 26330 (-3.8%) | 33236 vs 35107 (-5.3%) |
| avg_equation | 8672 vs 8777 (-1.2%) | 17128 vs 17553 (-2.4%) | 25320 vs 26330 (-3.8%) | 33236 vs 35107 (-5.3%) |
| avg_gated_lookup | 8705 vs 8777 (-0.8%) | 17210 vs 17553 (-2.0%) | 18992 vs 26330 (-27.9%) | 18992 vs 35107 (-45.9%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 42.9 points at 94.7% of the default cost, 5.3% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 42.9 points at 94.7% of the default cost, 5.3% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 42.6 points at 54.1% of the default cost, 27.9% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 42.6 points at 54.1% of the default cost, 45.9% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
