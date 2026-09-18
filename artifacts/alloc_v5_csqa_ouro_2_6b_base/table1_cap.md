# Table 1 -- csqa (ouro_2_6b_base), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 124188 layer passes over 977 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 80.3 | +1.6 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | n/a | 81.0 (100%) | +0.9 |
| lookup | 33.2 (100%) | 75.5 | 81.2 | 82.0 | +0.0 |
| equation | 33.2 (100%) | 74.8 | 80.0 | 79.9 | +2.0 |
| equation_n30 | 33.2 (100%) | 74.8 | 80.2 | 79.9 | +2.0 |
| equation_n100 | 33.2 (100%) | 74.8 | 74.6 | 79.9 | +2.0 |
| gated_equation | 33.2 (100%) | 74.8 | 80.2 | 81.1 | +0.9 |
| avg_lookup | 34.3 | 76.0 | 81.2 | 82.0 | +0.0 |
| avg_equation | 34.3 | 74.5 | 79.8 | 80.3 | +1.6 |
| avg_gated_lookup | 34.3 | 76.0 | 81.2 | 82.0 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 0, 82.0 points over 977 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 31010 vs 31047 (-0.1%) | 61885 vs 62094 (-0.3%) | 93022 vs 93141 (-0.1%) | 117256 vs 124188 (-5.6%) |
| avg_equation | 31010 vs 31047 (-0.1%) | 62134 vs 62094 (+0.1%) | 92984 vs 93141 (-0.2%) | 123959 vs 124188 (-0.2%) |
| avg_gated_lookup | 31010 vs 31047 (-0.1%) | 61885 vs 62094 (-0.3%) | 93022 vs 93141 (-0.1%) | 117256 vs 124188 (-5.6%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 82.0 points at 94.4% of the default cost, 5.6% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 82.0 points at 94.4% of the default cost, 5.6% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
