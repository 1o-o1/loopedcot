# Table 1 -- bbh (ouro_2_6b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 197416 layer passes over 2137 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 82.5 | +0.0 |
| default_cell | n/a | 89.5 (10%) | 89.3 (21%) | 86.2 (38%) | -3.7 |
| default_at_budget | 79.6 (10%) | 89.5 (10%) | 86.9 (25%) | 69.2 (85%) | +13.3 |
| lookup | 43.0 (85%) | 55.9 | 78.8 | 81.0 | +1.4 |
| equation | 40.3 (85%) | 57.3 | 78.8 | 81.1 | +1.3 |
| equation_n30 | 40.3 (85%) | 57.3 | 78.8 | 81.2 | +1.2 |
| equation_n100 | 40.3 (85%) | 57.3 | 78.8 | 81.1 | +1.3 |
| gated_equation | 39.5 (85%) | 57.3 | 78.1 | 80.9 | +1.6 |
| avg_lookup | 43.3 | 74.1 | 81.2 | 81.2 | +1.3 |
| avg_equation | 43.3 | 74.1 | 81.0 | 81.3 | +1.2 |
| avg_gated_lookup | 43.5 | 74.5 | 81.2 | 81.2 | +1.3 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 2048, 82.5 points over 2137 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 49305 vs 49354 (-0.1%) | 97042 vs 98708 (-1.7%) | 145230 vs 148062 (-1.9%) | 145230 vs 197416 (-26.4%) |
| avg_equation | 49305 vs 49354 (-0.1%) | 97880 vs 98708 (-0.8%) | 146449 vs 148062 (-1.1%) | 150487 vs 197416 (-23.8%) |
| avg_gated_lookup | 49578 vs 49354 (+0.5%) | 103332 vs 98708 (+4.7%) | 145230 vs 148062 (-1.9%) | 145230 vs 197416 (-26.4%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 81.2 points at 73.6% of the default cost, 1.9% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 81.2 points at 73.6% of the default cost, 26.4% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 81.3 points at 76.2% of the default cost, 23.8% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 81.2 points at 73.6% of the default cost, 1.9% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 81.2 points at 73.6% of the default cost, 26.4% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
