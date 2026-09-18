# Table 1 -- csqa (ouro_1_4b_think), cap accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 133929 layer passes over 977 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 76.7 | +0.0 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 72.9 | 75.2 | 75.2 | +1.4 |
| lookup | 61.1 | 73.5 | 73.9 | 75.2 | +1.4 |
| equation | 61.1 | 73.9 | 75.5 | 75.2 | +1.4 |
| equation_n30 | 61.1 | 73.9 | 75.5 | 75.9 | +0.7 |
| equation_n100 | 61.1 | 73.9 | 75.5 | 75.2 | +1.4 |
| gated_equation | 61.1 | 72.9 | 72.8 | 75.2 | +1.4 |
| avg_lookup | 60.7 | 73.9 | 74.8 | 76.3 | +0.4 |
| avg_equation | 60.8 | 73.7 | 74.4 | 75.4 | +1.2 |
| avg_gated_lookup | 60.8 | 72.7 | 74.3 | 75.4 | +1.2 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 2048, 76.7 points over 977 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under cap accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 33346 vs 33482 (-0.4%) | 66692 vs 66964 (-0.4%) | 99223 vs 100446 (-1.2%) | 131584 vs 133929 (-1.8%) |
| avg_equation | 33456 vs 33482 (-0.1%) | 64824 vs 66964 (-3.2%) | 99169 vs 100446 (-1.3%) | 129673 vs 133929 (-3.2%) |
| avg_gated_lookup | 33466 vs 33482 (-0.0%) | 65823 vs 66964 (-1.7%) | 101323 vs 100446 (+0.9%) | 131132 vs 133929 (-2.1%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.
