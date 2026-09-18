# Table 1 -- svamp (ouro_2_6b_base), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 131236 layer passes over 200 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 83.0 | +0.0 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | n/a | 56.5 | +26.5 |
| lookup | 26.5 | 51.5 | 80.0 | 82.5 | +0.5 |
| equation | 28.5 | 44.5 | 81.0 | 82.5 | +0.5 |
| equation_n30 | 28.5 | 52.0 | 81.0 | 82.0 | +1.0 |
| equation_n100 | 28.5 | 44.5 | 81.0 | 82.5 | +0.5 |
| gated_equation | 28.5 | 51.5 | 80.0 | 82.5 | +0.5 |
| avg_lookup | 41.5 | 77.5 | 80.0 | 82.5 | +0.5 |
| avg_equation | 35.0 | 77.5 | 80.0 | 82.5 | +0.5 |
| avg_gated_lookup | 41.5 | 74.0 | 80.5 | 82.5 | +0.5 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 128, 83.0 points over 200 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 32668 vs 32809 (-0.4%) | 67391 vs 65618 (+2.7%) | 100836 vs 98427 (+2.4%) | 109189 vs 131236 (-16.8%) |
| avg_equation | 32510 vs 32809 (-0.9%) | 67391 vs 65618 (+2.7%) | 100836 vs 98427 (+2.4%) | 121447 vs 131236 (-7.5%) |
| avg_gated_lookup | 32783 vs 32809 (-0.1%) | 64992 vs 65618 (-1.0%) | 100468 vs 98427 (+2.1%) | 109189 vs 131236 (-16.8%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 82.5 points at 83.2% of the default cost, 16.8% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 82.5 points at 83.2% of the default cost, 16.8% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
