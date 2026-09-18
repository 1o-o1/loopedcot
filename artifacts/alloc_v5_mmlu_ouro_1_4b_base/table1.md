# Table 1 -- mmlu (ouro_1_4b_base), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 58952 layer passes over 1700 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 68.4 | +0.0 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | 74.3 (41%) | 69.8 (89%) | -1.5 |
| lookup | 40.0 (89%) | 56.5 | 65.4 | 67.3 | +1.1 |
| equation | 40.0 (89%) | 57.6 | 64.6 | 67.6 | +0.7 |
| equation_n30 | 40.0 (89%) | 57.6 | 64.8 | 68.1 | +0.2 |
| equation_n100 | 40.0 (89%) | 57.6 | 64.8 | 68.1 | +0.2 |
| gated_equation | 40.0 (89%) | 57.6 | 65.2 | 68.7 (89%) | -0.3 |
| avg_lookup | 43.9 | 61.4 | 65.4 | 67.4 | +1.0 |
| avg_equation | 42.8 | 60.3 | 65.2 | 66.9 | +1.5 |
| avg_gated_lookup | 44.5 | 60.9 | 65.2 | 68.3 | +0.1 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 128, 68.4 points over 1700 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 14638 vs 14738 (-0.7%) | 29297 vs 29476 (-0.6%) | 44320 vs 44214 (+0.2%) | 47957 vs 58952 (-18.7%) |
| avg_equation | 14879 vs 14738 (+1.0%) | 29498 vs 29476 (+0.1%) | 44549 vs 44214 (+0.8%) | 58495 vs 58952 (-0.8%) |
| avg_gated_lookup | 14704 vs 14738 (-0.2%) | 30209 vs 29476 (+2.5%) | 44934 vs 44214 (+1.6%) | 60157 vs 58952 (+2.0%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 67.4 points at 81.3% of the default cost, 18.7% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
