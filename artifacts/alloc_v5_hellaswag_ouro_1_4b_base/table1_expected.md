# Table 1 -- hellaswag (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 94580 layer passes over 1700 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 57.1 | +9.9 |
| default_cell | n/a | n/a | n/a | 63.8 (32%) | +3.1 |
| default_at_budget | n/a | n/a | 63.6 (32%) | 56.9 | +10.0 |
| lookup | 35.3 | 56.9 | 65.4 | 66.9 | +0.0 |
| equation | 31.1 | 47.3 | 55.8 | 57.2 | +9.8 |
| equation_n30 | 31.1 | 46.6 | 56.1 | 56.0 | +10.9 |
| equation_n100 | 31.1 | 46.6 | 56.0 | 57.2 | +9.8 |
| gated_equation | 31.1 | 47.4 | 67.0 (32%) | 66.9 | +0.0 |
| avg_lookup | 40.4 | 61.2 | 66.9 | 66.9 | +0.0 |
| avg_equation | 35.5 | 49.4 | 56.8 | 57.1 | +9.9 |
| avg_gated_lookup | 40.2 | 61.2 | 66.9 | 66.9 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 0, 66.9 points over 1700 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 23031 vs 23645 (-2.6%) | 47284 vs 47290 (-0.0%) | 70856 vs 70935 (-0.1%) | 73973 vs 94580 (-21.8%) |
| avg_equation | 22952 vs 23645 (-2.9%) | 46835 vs 47290 (-1.0%) | 71382 vs 70935 (+0.6%) | 95566 vs 94580 (+1.0%) |
| avg_gated_lookup | 22815 vs 23645 (-3.5%) | 47284 vs 47290 (-0.0%) | 70679 vs 70935 (-0.4%) | 73973 vs 94580 (-21.8%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 66.9 points at 78.2% of the default cost, 21.8% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 66.9 points at 78.2% of the default cost, 21.8% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
