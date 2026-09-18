# Table 1 -- strategyqa (ouro_2_6b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 194101 layer passes over 1990 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 77.8 | +1.3 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 74.6 | 78.0 | 78.2 | +0.9 |
| lookup | 59.7 | 77.5 | 79.1 | 79.1 | +0.0 |
| equation | 59.7 | 77.5 | 79.1 | 78.2 | +0.9 |
| equation_n30 | 59.7 | 77.5 | 79.1 | 78.2 | +0.9 |
| equation_n100 | 59.7 | 77.5 | 79.1 | 78.2 | +0.9 |
| gated_equation | 59.7 | 77.5 | 78.0 | 78.2 | +0.9 |
| avg_lookup | 67.5 | 76.9 | 79.2 | 78.5 | +0.6 |
| avg_equation | 66.8 | 77.8 | 79.1 | 78.7 | +0.4 |
| avg_gated_lookup | 67.5 | 76.9 | 79.1 | 79.1 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 3 at cap 512, 79.1 points over 1990 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 49083 vs 48525 (+1.2%) | 93311 vs 97050 (-3.9%) | 141950 vs 145576 (-2.5%) | 182964 vs 194101 (-5.7%) |
| avg_equation | 47391 vs 48525 (-2.3%) | 96195 vs 97050 (-0.9%) | 134022 vs 145576 (-7.9%) | 182371 vs 194101 (-6.0%) |
| avg_gated_lookup | 49083 vs 48525 (+1.2%) | 93311 vs 97050 (-3.9%) | 129391 vs 145576 (-11.1%) | 129391 vs 194101 (-33.3%) |
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 79.1 points at 66.7% of the default cost, 11.1% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 79.1 points at 66.7% of the default cost, 33.3% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
