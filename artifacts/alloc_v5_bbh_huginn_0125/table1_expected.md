# Table 1 -- bbh (huginn_0125), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 142482 layer passes over 2137 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 35.6 | +0.1 |
| default_cell | n/a | 54.1 (10%) | 54.1 (10%) | 54.7 (40%) | -19.1 |
| default_at_budget | 56.4 (10%) | 60.1 (21%) | 51.9 (42%) | 36.2 (88%) | -0.6 |
| lookup | 31.4 | 34.5 | 32.4 | 33.7 | +2.0 |
| equation | 24.0 | 35.3 | 35.2 | 35.8 | -0.1 |
| equation_n30 | 31.4 | 34.5 | 32.0 | 32.2 | +3.5 |
| equation_n100 | 24.5 | 27.5 | 31.4 | 35.8 | -0.1 |
| gated_equation | 28.6 | 34.2 | 34.4 | 34.7 | +1.0 |
| avg_lookup | 34.1 | 32.1 | 31.8 | 35.0 | +0.6 |
| avg_equation | 24.3 | 35.0 | 37.2 | 35.5 | +0.1 |
| avg_gated_lookup | 34.7 | 32.3 | 31.8 | 31.8 | +3.8 |

The ORACLE GAP is the best single evaluation cell (depth 32 at cap 512, 35.7 points over 2137 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none.

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 35568 vs 35621 (-0.1%) | 71685 vs 71241 (+0.6%) | 105915 vs 106862 (-0.9%) | 125880 vs 142482 (-11.7%) |
| avg_equation | 35430 vs 35621 (-0.5%) | 72374 vs 71241 (+1.6%) | 108954 vs 106862 (+2.0%) | 140961 vs 142482 (-1.1%) |
| avg_gated_lookup | 32323 vs 35621 (-9.3%) | 74475 vs 71241 (+4.5%) | 107109 vs 106862 (+0.2%) | 107109 vs 142482 (-24.8%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 35.0 points at 88.3% of the default cost, 11.7% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 31.8 points at 75.2% of the default cost, 24.8% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
