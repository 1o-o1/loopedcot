# Table 1 -- strategyqa (mcleish_llama32_r32), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 59356 layer passes over 1990 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 49.7 | +2.6 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 50.7 | 50.8 | 50.7 | +1.7 |
| lookup | 51.5 | 51.5 | 49.4 | 49.4 | +2.9 |
| equation | 50.6 | 50.7 | 50.8 | 50.7 | +1.7 |
| equation_n30 | 50.6 | 50.7 | 50.8 | 50.7 | +1.7 |
| equation_n100 | 50.6 | 50.7 | 50.8 | 50.7 | +1.7 |
| gated_equation | 50.6 | 50.7 | 50.8 | 50.7 | +1.7 |
| avg_lookup | 51.4 | 50.2 | 49.4 | 49.9 | +2.4 |
| avg_equation | 50.2 | 50.8 | 50.7 | 50.5 | +1.9 |
| avg_gated_lookup | 52.1 | 50.9 | 49.4 | 49.4 | +2.9 |

The ORACLE GAP is the best single evaluation cell (depth 2 at cap 128, 52.3 points over 1990 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none.

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 13293 vs 14839 (-10.4%) | 29187 vs 29678 (-1.7%) | 43581 vs 44517 (-2.1%) | 57624 vs 59356 (-2.9%) |
| avg_equation | 14366 vs 14839 (-3.2%) | 28070 vs 29678 (-5.4%) | 41584 vs 44517 (-6.6%) | 58856 vs 59356 (-0.8%) |
| avg_gated_lookup | 12873 vs 14839 (-13.3%) | 28057 vs 29678 (-5.5%) | 43112 vs 44517 (-3.2%) | 43112 vs 59356 (-27.4%) |
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 49.4 points at 72.6% of the default cost, 3.2% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 49.4 points at 72.6% of the default cost, 27.4% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
