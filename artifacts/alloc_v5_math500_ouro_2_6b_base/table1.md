# Table 1 -- math500 (ouro_2_6b_base), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 338737 layer passes over 400 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 56.0 | +0.0 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | 52.5 (98%) | 55.6 (100%) | +0.4 |
| lookup | 31.6 (100%) | 48.5 | 53.5 | 53.8 | +2.3 |
| equation | 31.6 (100%) | 48.5 | 53.5 | 53.2 | +2.8 |
| equation_n30 | 31.6 (100%) | 48.5 | 53.5 | 53.2 | +2.8 |
| equation_n100 | 31.6 (100%) | 48.5 | 53.5 | 53.2 | +2.8 |
| gated_equation | 31.6 (100%) | 48.5 | 53.4 (100%) | 53.5 | +2.5 |
| avg_lookup | 33.0 | 50.5 | 53.5 | 53.5 | +2.5 |
| avg_equation | 34.0 | 52.2 | 54.0 | 53.2 | +2.8 |
| avg_gated_lookup | 34.8 | 50.2 | 54.5 | 55.5 | +0.5 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 4096, 56.0 points over 400 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 84088 vs 84684 (-0.7%) | 167054 vs 169369 (-1.4%) | 221217 vs 254053 (-12.9%) | 221217 vs 338737 (-34.7%) |
| avg_equation | 84916 vs 84684 (+0.3%) | 170414 vs 169369 (+0.6%) | 249884 vs 254053 (-1.6%) | 339399 vs 338737 (+0.2%) |
| avg_gated_lookup | 86342 vs 84684 (+2.0%) | 165084 vs 169369 (-2.5%) | 255915 vs 254053 (+0.7%) | 294956 vs 338737 (-12.9%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 53.5 points at 65.3% of the default cost, 12.9% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 53.5 points at 65.3% of the default cost, 34.7% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 55.5 points at 87.1% of the default cost, 12.9% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
