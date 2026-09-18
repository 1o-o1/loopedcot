# Table 1 -- mmlu (mcleish_llama32_r32), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 40743 layer passes over 1700 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 37.4 | +1.1 |
| default_cell | n/a | n/a | n/a | 40.3 (80%) | -1.8 |
| default_at_budget | n/a | n/a | 39.4 (86%) | 38.1 (98%) | +0.4 |
| lookup | 33.1 (98%) | 36.6 | 36.7 | 36.7 | +1.8 |
| equation | 33.3 (98%) | 35.8 | 36.4 | 36.4 | +2.1 |
| equation_n30 | 25.3 (98%) | 35.7 | 36.4 | 36.4 | +2.1 |
| equation_n100 | 33.3 (98%) | 35.7 | 36.4 | 36.4 | +2.1 |
| gated_equation | 25.3 (98%) | 35.8 | 38.5 (86%) | 36.4 | +2.1 |
| avg_lookup | 32.3 | 36.7 | 36.7 | 36.7 | +1.8 |
| avg_equation | 32.3 | 36.6 | 36.4 | 36.4 | +2.1 |
| avg_gated_lookup | 33.4 | 36.7 | 36.7 | 36.7 | +1.8 |

The ORACLE GAP is the best single evaluation cell (depth 8 at cap 0, 38.5 points over 1700 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0, F2.

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 10146 vs 10186 (-0.4%) | 15994 vs 20371 (-21.5%) | 15994 vs 30557 (-47.7%) | 15994 vs 40743 (-60.7%) |
| avg_equation | 10146 vs 10186 (-0.4%) | 20508 vs 20371 (+0.7%) | 22884 vs 30557 (-25.1%) | 22884 vs 40743 (-43.8%) |
| avg_gated_lookup | 10142 vs 10186 (-0.4%) | 15994 vs 20371 (-21.5%) | 15994 vs 30557 (-47.7%) | 15994 vs 40743 (-60.7%) |
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 39.3% of the default cost, 21.5% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 39.3% of the default cost, 47.7% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 39.3% of the default cost, 60.7% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 36.4 points at 56.2% of the default cost, 25.1% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 36.4 points at 56.2% of the default cost, 43.8% under the budget it was given.
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 39.3% of the default cost, 21.5% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 39.3% of the default cost, 47.7% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 39.3% of the default cost, 60.7% under the budget it was given.
- `avg_gated_lookup` at 1.00x: deviated from the default cell on family F2. Verification margin +3.3 points, sd 5.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 60.7% of the budget, 39.3% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
