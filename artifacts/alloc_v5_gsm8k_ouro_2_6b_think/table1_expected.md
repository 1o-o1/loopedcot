# Table 1 -- gsm8k (ouro_2_6b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 239639 layer passes over 1056 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 21.5 | +43.5 |
| default_cell | n/a | n/a | n/a | 21.1 (99%) | +43.8 |
| default_at_budget | n/a | n/a | 18.9 | 21.7 | +43.3 |
| lookup | 58.1 | 65.0 | 65.0 | 65.0 | +0.0 |
| equation | 58.1 | 64.6 | 64.6 | 64.6 | +0.4 |
| equation_n30 | 58.1 | 64.6 | 64.6 | 64.6 | +0.4 |
| equation_n100 | 58.1 | 64.6 | 64.6 | 64.6 | +0.4 |
| gated_equation | 58.1 | 64.6 | 64.6 | 64.6 | +0.4 |
| avg_lookup | 61.7 | 65.0 | 65.0 | 65.0 | +0.0 |
| avg_equation | 61.1 | 64.6 | 64.6 | 64.6 | +0.4 |
| avg_gated_lookup | 62.2 | 65.0 | 65.0 | 25.5 | +39.5 |

The ORACLE GAP is the best single evaluation cell (depth 1 at cap 2048, 65.0 points over 1056 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F1, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 59801 vs 59910 (-0.2%) | 70856 vs 119819 (-40.9%) | 70856 vs 179729 (-60.6%) | 70856 vs 239639 (-70.4%) |
| avg_equation | 59051 vs 59910 (-1.4%) | 89171 vs 119819 (-25.6%) | 89171 vs 179729 (-50.4%) | 89171 vs 239639 (-62.8%) |
| avg_gated_lookup | 59976 vs 59910 (+0.1%) | 70856 vs 119819 (-40.9%) | 70856 vs 179729 (-60.6%) | 206256 vs 239639 (-13.9%) |
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 65.0 points at 29.6% of the default cost, 40.9% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 65.0 points at 29.6% of the default cost, 60.6% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 65.0 points at 29.6% of the default cost, 70.4% under the budget it was given.
- `avg_equation` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 64.6 points at 37.2% of the default cost, 25.6% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 64.6 points at 37.2% of the default cost, 50.4% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 64.6 points at 37.2% of the default cost, 62.8% under the budget it was given.
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 65.0 points at 29.6% of the default cost, 40.9% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 65.0 points at 29.6% of the default cost, 60.6% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 25.5 points at 86.1% of the default cost, 13.9% under the budget it was given.
- `avg_gated_lookup` at 1.00x: deviated from the default cell on family F1. Verification margin +5.1 points, sd 3.0, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 13.9% of the budget, 86.1% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
