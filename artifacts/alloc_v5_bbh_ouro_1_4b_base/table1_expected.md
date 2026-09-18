# Table 1 -- bbh (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 100521 layer passes over 2137 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 75.8 | +0.0 |
| default_cell | n/a | 79.1 (10%) | 79.1 (10%) | 81.5 (32%) | -5.7 |
| default_at_budget | 75.5 (10%) | 79.1 (10%) | 80.7 (30%) | 64.9 (87%) | +10.9 |
| lookup | 33.2 (87%) | 48.7 | 65.8 | 72.4 | +3.4 |
| equation | 33.4 (87%) | 48.0 | 66.0 | 72.5 | +3.3 |
| equation_n30 | 33.4 (87%) | 47.4 | 58.7 | 69.3 | +6.5 |
| equation_n100 | 33.4 (87%) | 48.0 | 66.0 | 72.5 | +3.3 |
| gated_equation | 34.5 (87%) | 47.7 | 65.9 | 63.7 | +12.1 |
| avg_lookup | 31.8 | 57.3 | 70.1 | 75.4 | +0.4 |
| avg_equation | 35.0 | 57.2 | 67.0 | 75.8 | +0.0 |
| avg_gated_lookup | 33.1 | 58.1 | 71.9 | 75.4 | +0.4 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 2048, 75.8 points over 2137 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 23544 vs 25130 (-6.3%) | 49855 vs 50261 (-0.8%) | 74724 vs 75391 (-0.9%) | 94413 vs 100521 (-6.1%) |
| avg_equation | 24969 vs 25130 (-0.6%) | 49943 vs 50261 (-0.6%) | 74867 vs 75391 (-0.7%) | 99671 vs 100521 (-0.8%) |
| avg_gated_lookup | 24786 vs 25130 (-1.4%) | 52280 vs 50261 (+4.0%) | 80500 vs 75391 (+6.8%) | 94413 vs 100521 (-6.1%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 75.4 points at 93.9% of the default cost, 6.1% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 75.4 points at 93.9% of the default cost, 6.1% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
