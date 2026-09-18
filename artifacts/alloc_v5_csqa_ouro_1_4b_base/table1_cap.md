# Table 1 -- csqa (ouro_1_4b_base), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 61956 layer passes over 977 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 72.6 | +0.8 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | n/a | 72.6 (100%) | +0.7 |
| lookup | 32.3 (100%) | 66.1 | 72.1 | 73.4 | +0.0 |
| equation | 31.8 (100%) | 61.4 | 71.6 | 72.3 | +1.1 |
| equation_n30 | 32.3 (100%) | 66.1 | 71.8 | 71.6 | +1.7 |
| equation_n100 | 31.8 (100%) | 61.4 | 71.8 | 72.3 | +1.1 |
| gated_equation | 31.8 (100%) | 61.4 | 71.8 | 73.4 (100%) | +0.0 |
| avg_lookup | 33.1 | 66.4 | 71.4 | 73.4 | +0.0 |
| avg_equation | 31.0 | 61.4 | 71.9 | 71.8 | +1.6 |
| avg_gated_lookup | 31.7 | 65.0 | 71.4 | 73.4 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 0, 73.4 points over 977 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 15055 vs 15489 (-2.8%) | 30822 vs 30978 (-0.5%) | 46221 vs 46467 (-0.5%) | 58628 vs 61956 (-5.4%) |
| avg_equation | 15518 vs 15489 (+0.2%) | 30943 vs 30978 (-0.1%) | 46360 vs 46467 (-0.2%) | 61073 vs 61956 (-1.4%) |
| avg_gated_lookup | 15316 vs 15489 (-1.1%) | 30459 vs 30978 (-1.7%) | 46221 vs 46467 (-0.5%) | 58628 vs 61956 (-5.4%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 73.4 points at 94.6% of the default cost, 5.4% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 73.4 points at 94.6% of the default cost, 5.4% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
