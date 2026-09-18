# Table 1 -- bbh (ouro_2_6b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 322452 layer passes over 2337 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 91.1 |
| default_cell | n/a | n/a | 84.2 (10%) | 93.0 (69%) |
| default_at_budget | 85.4 (10%) | 78.5 (40%) | 63.3 (97%) | 91.0 |
| lookup | 48.3 | 79.9 | 86.0 | 91.0 |
| equation | 48.7 | 79.2 | 84.6 | 90.8 |
| equation_n30 | 42.1 | 79.2 | 83.6 | 83.6 |
| equation_n100 | 48.7 | 79.2 | 84.6 | 90.8 |
| gated_equation | 48.7 | 79.2 | 84.5 | 91.0 |
| avg_lookup | 52.4 | 83.1 | 86.6 | 91.1 |
| avg_equation | 52.4 | 83.1 | 85.8 | 91.1 |
| avg_gated_lookup | 52.4 | 83.1 | 86.6 | 91.1 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 81331 vs 80613 (+0.9%) | 159792 vs 161226 (-0.9%) | 237395 vs 241839 (-1.8%) | 310195 vs 322452 (-3.8%) |
| avg_equation | 81331 vs 80613 (+0.9%) | 160614 vs 161226 (-0.4%) | 242856 vs 241839 (+0.4%) | 310195 vs 322452 (-3.8%) |
| avg_gated_lookup | 81331 vs 80613 (+0.9%) | 159792 vs 161226 (-0.9%) | 237395 vs 241839 (-1.8%) | 310195 vs 322452 (-3.8%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 91.1 points at 96.2% of the default cost, 3.8% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 91.1 points at 96.2% of the default cost, 3.8% under the budget it was given.
- `avg_gated_lookup` reverted to the default cell for every question at 1.00x: the predicted calibration margin did not clear 0.50 of its own SD.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
