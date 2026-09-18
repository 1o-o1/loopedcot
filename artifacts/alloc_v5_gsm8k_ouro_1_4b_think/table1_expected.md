# Table 1 -- gsm8k (ouro_1_4b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 127642 layer passes over 1056 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 93.0 | +0.0 |
| default_cell | n/a | n/a | n/a | 93.3 (95%) | -0.3 |
| default_at_budget | n/a | 26.9 (31%) | 59.7 | 93.0 | +0.0 |
| lookup | 32.4 | 85.5 | 91.4 | 91.4 | +1.6 |
| equation | 32.4 | 85.5 | 91.4 | 92.9 | +0.1 |
| equation_n30 | 32.4 | 85.5 | 91.4 | 93.0 | +0.0 |
| equation_n100 | 32.4 | 85.5 | 91.4 | 93.0 | +0.0 |
| gated_equation | 32.4 | 26.6 (31%) | 91.4 | 91.4 | +1.6 |
| avg_lookup | 40.2 | 85.4 | 91.4 | 91.4 | +1.6 |
| avg_equation | 37.9 | 86.8 | 91.5 | 93.0 | +0.0 |
| avg_gated_lookup | 39.3 | 85.4 | 91.5 | 91.4 | +1.6 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 4096, 93.0 points over 1056 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0, F2.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 31941 vs 31910 (+0.1%) | 63972 vs 63821 (+0.2%) | 94621 vs 95731 (-1.2%) | 94621 vs 127642 (-25.9%) |
| avg_equation | 30778 vs 31910 (-3.5%) | 63486 vs 63821 (-0.5%) | 96219 vs 95731 (+0.5%) | 123535 vs 127642 (-3.2%) |
| avg_gated_lookup | 31425 vs 31910 (-1.5%) | 63972 vs 63821 (+0.2%) | 96358 vs 95731 (+0.7%) | 94621 vs 127642 (-25.9%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 91.4 points at 74.1% of the default cost, 1.2% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 91.4 points at 74.1% of the default cost, 25.9% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 93.0 points at 96.8% of the default cost, 3.2% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 91.4 points at 74.1% of the default cost, 25.9% under the budget it was given.
- `avg_gated_lookup` at 1.00x: deviated from the default cell on family F2. Verification margin +1.3 points, sd 2.2, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 25.9% of the budget, 74.1% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
