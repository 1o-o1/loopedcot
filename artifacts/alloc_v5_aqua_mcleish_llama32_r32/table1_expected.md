# Table 1 -- aqua (mcleish_llama32_r32), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 41537 layer passes over 154 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 53.2 | +3.9 |
| default_cell | n/a | n/a | n/a | 84.2 (12%) | -27.1 |
| default_at_budget | n/a | n/a | 37.0 (35%) | 52.6 | +4.5 |
| lookup | 23.4 | 50.6 | 54.5 | 53.9 | +3.2 |
| equation | 24.0 | 48.1 | 54.5 | 54.5 | +2.6 |
| equation_n30 | 24.0 | 48.1 | 54.5 | 54.5 | +2.6 |
| equation_n100 | 24.0 | 48.1 | 54.5 | 54.5 | +2.6 |
| gated_equation | 29.9 | 48.1 | 54.5 | 52.6 | +4.5 |
| avg_lookup | 40.3 | 55.8 | 51.9 | 53.9 | +3.2 |
| avg_equation | 40.3 | 55.8 | 54.5 | 54.5 | +2.6 |
| avg_gated_lookup | 42.2 | 55.8 | 54.5 | 54.5 | +2.6 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 1024, 57.1 points over 154 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2.

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 10368 vs 10384 (-0.2%) | 20616 vs 20768 (-0.7%) | 30852 vs 31153 (-1.0%) | 35791 vs 41537 (-13.8%) |
| avg_equation | 10380 vs 10384 (-0.0%) | 20685 vs 20768 (-0.4%) | 24710 vs 31153 (-20.7%) | 24710 vs 41537 (-40.5%) |
| avg_gated_lookup | 10529 vs 10384 (+1.4%) | 20601 vs 20768 (-0.8%) | 24710 vs 31153 (-20.7%) | 24710 vs 41537 (-40.5%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 53.9 points at 86.2% of the default cost, 13.8% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 54.5 points at 59.5% of the default cost, 20.7% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 54.5 points at 59.5% of the default cost, 40.5% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 54.5 points at 59.5% of the default cost, 20.7% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 54.5 points at 59.5% of the default cost, 40.5% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
