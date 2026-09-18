# Table 1 -- svamp (ouro_1_4b_base), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 65870 layer passes over 200 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 86.5 | +0.0 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | n/a | 63.0 | +23.5 |
| lookup | 24.5 | 50.5 | 72.0 | 84.0 | +2.5 |
| equation | 28.0 | 50.5 | 72.0 | 85.5 | +1.0 |
| equation_n30 | 28.0 | 50.5 | 57.0 | 85.5 | +1.0 |
| equation_n100 | 28.0 | 50.5 | 72.0 | 85.5 | +1.0 |
| gated_equation | 28.0 | 50.5 | 72.0 | 85.5 | +1.0 |
| avg_lookup | 27.0 | 61.5 | 79.5 | 84.0 | +2.5 |
| avg_equation | 28.0 | 61.5 | 77.0 | 86.0 | +0.5 |
| avg_gated_lookup | 31.0 | 68.5 | 79.5 | 86.0 | +0.5 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 256, 86.5 points over 200 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 16661 vs 16467 (+1.2%) | 32872 vs 32935 (-0.2%) | 50418 vs 49402 (+2.1%) | 54595 vs 65870 (-17.1%) |
| avg_equation | 16205 vs 16467 (-1.6%) | 32891 vs 32935 (-0.1%) | 50049 vs 49402 (+1.3%) | 67057 vs 65870 (+1.8%) |
| avg_gated_lookup | 16363 vs 16467 (-0.6%) | 32496 vs 32935 (-1.3%) | 50234 vs 49402 (+1.7%) | 67057 vs 65870 (+1.8%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 84.0 points at 82.9% of the default cost, 17.1% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
