# Table 1 -- bbh (huginn_0125), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 142482 layer passes over 2137 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 35.6 | +0.1 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | 56.4 (10%) | 60.1 (21%) | 52.0 (42%) | 36.1 (88%) | -0.4 |
| lookup | 31.4 | 34.5 | 32.4 | 33.5 | +2.2 |
| equation | 27.6 | 31.1 | 35.3 | 35.7 | -0.0 |
| equation_n30 | 31.4 | 34.5 | 32.0 | 32.2 | +3.5 |
| equation_n100 | 26.2 | 27.5 | 31.4 | 35.6 | +0.0 |
| gated_equation | 30.4 | 33.2 | 34.4 | 34.6 | +1.1 |
| avg_lookup | 34.1 | 32.1 | 31.8 | 35.0 | +0.6 |
| avg_equation | 34.2 | 35.4 | 36.5 | 35.0 | +0.6 |
| avg_gated_lookup | 34.7 | 32.3 | 31.8 | 31.8 | +3.8 |

The ORACLE GAP is the best single evaluation cell (depth 32 at cap 512, 35.7 points over 2137 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none.

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 35588 vs 35621 (-0.1%) | 71685 vs 71241 (+0.6%) | 105915 vs 106862 (-0.9%) | 140901 vs 142482 (-1.1%) |
| avg_equation | 36546 vs 35621 (+2.6%) | 71575 vs 71241 (+0.5%) | 106656 vs 106862 (-0.2%) | 141755 vs 142482 (-0.5%) |
| avg_gated_lookup | 32383 vs 35621 (-9.1%) | 74475 vs 71241 (+4.5%) | 107109 vs 106862 (+0.2%) | 107109 vs 142482 (-24.8%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 35.0 points at 98.9% of the default cost, 1.1% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 31.8 points at 75.2% of the default cost, 24.8% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
