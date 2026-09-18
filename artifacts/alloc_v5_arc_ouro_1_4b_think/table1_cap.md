# Table 1 -- arc (ouro_1_4b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 85664 layer passes over 938 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 93.7 | +0.4 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 87.5 (98%) | 89.0 | 90.8 | +3.3 |
| lookup | 74.5 | 88.0 | 91.0 | 93.3 | +0.9 |
| equation | 74.9 | 86.7 | 91.0 | 93.3 | +0.9 |
| equation_n30 | 74.9 | 84.0 | 90.6 | 89.6 | +4.6 |
| equation_n100 | 74.9 | 86.7 | 91.0 | 93.3 | +0.9 |
| gated_equation | 74.9 | 86.9 (98%) | 87.0 | 93.3 | +0.9 |
| avg_lookup | 78.4 | 88.9 | 93.0 | 93.3 | +0.9 |
| avg_equation | 77.1 | 87.8 | 92.6 | 93.8 | +0.3 |
| avg_gated_lookup | 77.7 | 89.0 | 93.3 | 93.5 | +0.6 |

The ORACLE GAP is the best single evaluation cell (depth 3 at cap 1024, 94.1 points over 938 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0, F2.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 21441 vs 21416 (+0.1%) | 42969 vs 42832 (+0.3%) | 63660 vs 64248 (-0.9%) | 64623 vs 85664 (-24.6%) |
| avg_equation | 21255 vs 21416 (-0.8%) | 42222 vs 42832 (-1.4%) | 61106 vs 64248 (-4.9%) | 84156 vs 85664 (-1.8%) |
| avg_gated_lookup | 21063 vs 21416 (-1.7%) | 42709 vs 42832 (-0.3%) | 64152 vs 64248 (-0.2%) | 85217 vs 85664 (-0.5%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 93.3 points at 75.4% of the default cost, 24.6% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
