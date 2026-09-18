# Table 1 -- arc (mcleish_llama32_r32), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 22345 layer passes over 938 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 43.7 | +0.6 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | n/a | 42.9 (93%) | +1.4 |
| lookup | 24.2 (93%) | 36.1 | 42.0 | 42.0 | +2.3 |
| equation | 25.3 (93%) | 37.2 | 40.7 | 40.3 | +4.1 |
| equation_n30 | 22.8 (93%) | 37.2 | 40.7 | 42.2 | +2.1 |
| equation_n100 | 25.3 (93%) | 36.4 | 40.7 | 42.2 | +2.1 |
| gated_equation | 22.8 (93%) | 37.1 | 40.7 | 42.2 | +2.1 |
| avg_lookup | 26.3 | 41.8 | 42.0 | 42.0 | +2.3 |
| avg_equation | 26.3 | 38.3 | 40.0 | 43.2 | +1.2 |
| avg_gated_lookup | 26.8 | 41.8 | 42.0 | 42.0 | +2.3 |

The ORACLE GAP is the best single evaluation cell (depth 8 at cap 0, 44.3 points over 938 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none.

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 5584 vs 5586 (-0.0%) | 11135 vs 11172 (-0.3%) | 11568 vs 16758 (-31.0%) | 11568 vs 22345 (-48.2%) |
| avg_equation | 5584 vs 5586 (-0.0%) | 11199 vs 11172 (+0.2%) | 16751 vs 16758 (-0.0%) | 22242 vs 22345 (-0.5%) |
| avg_gated_lookup | 5559 vs 5586 (-0.5%) | 11135 vs 11172 (-0.3%) | 11568 vs 16758 (-31.0%) | 11568 vs 22345 (-48.2%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 42.0 points at 51.8% of the default cost, 31.0% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 42.0 points at 51.8% of the default cost, 48.2% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 42.0 points at 51.8% of the default cost, 31.0% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 42.0 points at 51.8% of the default cost, 48.2% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
