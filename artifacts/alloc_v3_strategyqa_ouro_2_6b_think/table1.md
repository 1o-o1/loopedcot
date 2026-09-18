# Table 1 -- strategyqa (ouro_2_6b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 194662 layer passes over 2190 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 77.8 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 74.6 | 77.9 | 78.0 |
| lookup | 59.5 | 74.9 | 74.9 | 74.9 |
| equation | 59.9 | 77.4 | 77.9 | 78.0 |
| equation_n30 | 59.9 | 77.4 | 77.9 | 78.0 |
| equation_n100 | 59.9 | 77.4 | 77.9 | 78.0 |
| gated_equation | 60.5 | 74.6 | 77.9 | 78.0 |
| avg_lookup | 66.4 | 74.9 | 74.9 | 74.9 |
| avg_equation | 66.4 | 77.4 | 78.1 | 77.8 |
| avg_gated_lookup | 65.9 | 76.2 | 76.2 | 78.0 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 47159 vs 48665 (-3.1%) | 80365 vs 97331 (-17.4%) | 80365 vs 145996 (-45.0%) | 80365 vs 194662 (-58.7%) |
| avg_equation | 47159 vs 48665 (-3.1%) | 95952 vs 97331 (-1.4%) | 144852 vs 145996 (-0.8%) | 193443 vs 194662 (-0.6%) |
| avg_gated_lookup | 44977 vs 48665 (-7.6%) | 99513 vs 97331 (+2.2%) | 133978 vs 145996 (-8.2%) | 172525 vs 194662 (-11.4%) |
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 74.9 points at 41.3% of the default cost, 17.4% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 74.9 points at 41.3% of the default cost, 45.0% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 74.9 points at 41.3% of the default cost, 58.7% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 78.0 points at 88.6% of the default cost, 11.4% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
