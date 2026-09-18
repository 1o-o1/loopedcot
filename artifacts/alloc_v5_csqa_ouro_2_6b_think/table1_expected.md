# Table 1 -- csqa (ouro_2_6b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 234088 layer passes over 977 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 80.9 | +0.0 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | 79.2 | 80.5 | +0.4 |
| lookup | 18.1 | 80.3 | 80.0 | 80.5 | +0.4 |
| equation | 20.2 | 76.7 | 76.7 | 80.5 | +0.4 |
| equation_n30 | 28.9 | 76.7 | 76.7 | 76.7 | +4.2 |
| equation_n100 | 20.2 | 76.7 | 79.4 | 80.5 | +0.4 |
| gated_equation | 20.2 | 76.7 | 79.2 | 80.5 | +0.4 |
| avg_lookup | 67.3 | 80.6 | 79.6 | 80.5 | +0.4 |
| avg_equation | 67.3 | 76.3 | 77.0 | 79.7 | +1.1 |
| avg_gated_lookup | 65.8 | 80.6 | 79.8 | 80.5 | +0.4 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 4096, 80.9 points over 977 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 57914 vs 58522 (-1.0%) | 115832 vs 117044 (-1.0%) | 176510 vs 175566 (+0.5%) | 229800 vs 234088 (-1.8%) |
| avg_equation | 57914 vs 58522 (-1.0%) | 116932 vs 117044 (-0.1%) | 173498 vs 175566 (-1.2%) | 231707 vs 234088 (-1.0%) |
| avg_gated_lookup | 56752 vs 58522 (-3.0%) | 115832 vs 117044 (-1.0%) | 167628 vs 175566 (-4.5%) | 229800 vs 234088 (-1.8%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 80.5 points at 98.2% of the default cost, 1.8% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 80.5 points at 98.2% of the default cost, 1.8% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
