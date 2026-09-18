# Table 1 -- strategyqa (ouro_1_4b_base), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 58978 layer passes over 2190 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 66.3 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | 66.4 | 66.4 |
| lookup | 55.6 | 63.9 | 65.8 | 65.8 |
| equation | 53.9 | 66.8 | 68.5 | 66.4 |
| equation_n30 | 55.3 | 66.8 | 66.4 | 66.4 |
| equation_n100 | 53.9 | 66.8 | 68.5 | 66.4 |
| gated_equation | 53.9 | 63.5 | 66.4 | 66.4 |
| avg_lookup | 60.0 | 64.3 | 65.8 | 65.8 |
| avg_equation | 55.3 | 66.2 | 66.6 | 66.4 |
| avg_gated_lookup | 60.0 | 63.9 | 63.9 | 63.9 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 14028 vs 14744 (-4.9%) | 28509 vs 29489 (-3.3%) | 37399 vs 44233 (-15.5%) | 37399 vs 58978 (-36.6%) |
| avg_equation | 14187 vs 14744 (-3.8%) | 28725 vs 29489 (-2.6%) | 43742 vs 44233 (-1.1%) | 48151 vs 58978 (-18.4%) |
| avg_gated_lookup | 14028 vs 14744 (-4.9%) | 18699 vs 29489 (-36.6%) | 18699 vs 44233 (-57.7%) | 18699 vs 58978 (-68.3%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 65.8 points at 63.4% of the default cost, 15.5% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 65.8 points at 63.4% of the default cost, 36.6% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 66.4 points at 81.6% of the default cost, 18.4% under the budget it was given.
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 63.9 points at 31.7% of the default cost, 36.6% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 63.9 points at 31.7% of the default cost, 57.7% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 63.9 points at 31.7% of the default cost, 68.3% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
