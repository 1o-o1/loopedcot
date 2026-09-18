# Table 1 -- bbh (mcleish_llama32_r32), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 69931 layer passes over 2137 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 43.5 | +0.2 |
| default_cell | n/a | n/a | 50.0 (10%) | 58.6 (41%) | -14.9 |
| default_at_budget | 50.0 (10%) | 57.4 (31%) | 43.6 (72%) | 43.5 (99%) | +0.3 |
| lookup | 32.9 (99%) | 42.2 | 42.8 | 43.5 | +0.2 |
| equation | 34.1 (99%) | 43.0 | 42.6 | 43.4 | +0.3 |
| equation_n30 | 34.5 (99%) | 34.7 | 34.2 | 42.8 | +0.9 |
| equation_n100 | 34.6 (99%) | 42.3 | 42.7 | 43.4 | +0.3 |
| gated_equation | 34.1 (99%) | 42.2 | 42.6 | 42.3 | +1.4 |
| avg_lookup | 36.2 | 42.9 | 43.6 | 43.6 | +0.1 |
| avg_equation | 36.6 | 43.1 | 42.9 | 43.5 | +0.2 |
| avg_gated_lookup | 35.9 | 43.0 | 43.6 | 42.3 | +1.4 |

The ORACLE GAP is the best single evaluation cell (depth 8 at cap 512, 43.7 points over 2137 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3.

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 17616 vs 17483 (+0.8%) | 34588 vs 34966 (-1.1%) | 49386 vs 52448 (-5.8%) | 49386 vs 69931 (-29.4%) |
| avg_equation | 17304 vs 17483 (-1.0%) | 34077 vs 34966 (-2.5%) | 52754 vs 52448 (+0.6%) | 69021 vs 69931 (-1.3%) |
| avg_gated_lookup | 18734 vs 17483 (+7.2%) | 37807 vs 34966 (+8.1%) | 49386 vs 52448 (-5.8%) | 41635 vs 69931 (-40.5%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 43.6 points at 70.6% of the default cost, 5.8% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 43.6 points at 70.6% of the default cost, 29.4% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 43.5 points at 98.7% of the default cost, 1.3% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 43.6 points at 70.6% of the default cost, 5.8% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 42.3 points at 59.5% of the default cost, 40.5% under the budget it was given.
- `avg_gated_lookup` at 1.00x: deviated from the default cell on family F2. Verification margin +5.6 points, sd 4.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 40.5% of the budget, 59.5% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
