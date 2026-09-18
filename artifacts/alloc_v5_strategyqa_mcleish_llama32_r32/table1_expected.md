# Table 1 -- strategyqa (mcleish_llama32_r32), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 59356 layer passes over 1990 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 49.7 | +2.6 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 50.7 | 50.3 | 50.3 | +2.0 |
| lookup | 51.5 | 49.4 | 50.4 | 50.4 | +1.9 |
| equation | 49.8 | 50.7 | 50.3 | 50.3 | +2.0 |
| equation_n30 | 49.8 | 50.7 | 50.3 | 50.3 | +2.0 |
| equation_n100 | 50.1 | 50.7 | 50.3 | 50.3 | +2.0 |
| gated_equation | 49.8 | 50.7 | 50.3 | 50.3 | +2.0 |
| avg_lookup | 50.5 | 50.9 | 50.4 | 50.4 | +1.9 |
| avg_equation | 50.3 | 50.9 | 50.2 | 49.6 | +2.7 |
| avg_gated_lookup | 50.8 | 49.4 | 49.4 | 49.4 | +2.9 |

The ORACLE GAP is the best single evaluation cell (depth 2 at cap 128, 52.3 points over 1990 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none.

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 14745 vs 14839 (-0.6%) | 29150 vs 29678 (-1.8%) | 30617 vs 44517 (-31.2%) | 30617 vs 59356 (-48.4%) |
| avg_equation | 14789 vs 14839 (-0.3%) | 29150 vs 29678 (-1.8%) | 43529 vs 44517 (-2.2%) | 58596 vs 59356 (-1.3%) |
| avg_gated_lookup | 14540 vs 14839 (-2.0%) | 17901 vs 29678 (-39.7%) | 17901 vs 44517 (-59.8%) | 17901 vs 59356 (-69.8%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 50.4 points at 51.6% of the default cost, 31.2% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 50.4 points at 51.6% of the default cost, 48.4% under the budget it was given.
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 49.4 points at 30.2% of the default cost, 39.7% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 49.4 points at 30.2% of the default cost, 59.8% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 49.4 points at 30.2% of the default cost, 69.8% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
