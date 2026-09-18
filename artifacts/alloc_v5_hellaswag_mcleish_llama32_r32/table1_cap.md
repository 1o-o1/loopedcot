# Table 1 -- hellaswag (mcleish_llama32_r32), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 45837 layer passes over 1700 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 28.6 | +2.9 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | 40.5 (15%) | 28.6 (99%) | +2.9 |
| lookup | 24.6 (99%) | 29.9 | 30.9 | 31.5 | +0.0 |
| equation | 24.6 (99%) | 29.9 | 30.7 | 28.4 | +3.1 |
| equation_n30 | 24.6 (99%) | 29.9 | 30.7 | 28.4 | +3.1 |
| equation_n100 | 24.6 (99%) | 29.9 | 30.9 | 31.5 | +0.0 |
| gated_equation | 24.6 (99%) | 29.9 | 30.7 | 31.6 (99%) | -0.2 |
| avg_lookup | 25.9 | 30.8 | 30.9 | 31.5 | +0.0 |
| avg_equation | 26.0 | 30.9 | 28.5 | 28.6 | +2.8 |
| avg_gated_lookup | 25.9 | 30.8 | 30.9 | 31.5 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 8 at cap 0, 31.5 points over 1700 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0, F2.

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 11427 vs 11459 (-0.3%) | 23043 vs 22918 (+0.5%) | 34109 vs 34378 (-0.8%) | 40123 vs 45837 (-12.5%) |
| avg_equation | 11400 vs 11459 (-0.5%) | 23051 vs 22918 (+0.6%) | 34177 vs 34378 (-0.6%) | 46290 vs 45837 (+1.0%) |
| avg_gated_lookup | 11440 vs 11459 (-0.2%) | 23043 vs 22918 (+0.5%) | 34109 vs 34378 (-0.8%) | 40123 vs 45837 (-12.5%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 31.5 points at 87.5% of the default cost, 12.5% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 31.5 points at 87.5% of the default cost, 12.5% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
