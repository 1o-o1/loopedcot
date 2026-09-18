## alloc_v2_aqua_huginn_0125
# Table 1 -- aqua (huginn_0125), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 142485 layer passes over 154 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 24.7 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 13.0 (15%) | 23.4 | 23.4 |
| lookup | 22.7 | 24.7 | 24.7 | 24.7 |
| equation | 25.3 | 20.8 | 20.8 | 20.8 |
| equation_n30 | 25.3 | 20.8 | 20.8 | 20.8 |
| equation_n100 | 25.3 | 20.8 | 20.8 | 20.8 |
| gated_equation | 25.3 | 20.8 | 20.8 | 20.8 |
| avg_lookup | 24.7 | 24.7 | 24.7 | 24.7 |
| avg_equation | 24.0 | 20.8 | 20.8 | 20.8 |
| avg_gated_lookup | 24.7 | 24.7 | 24.7 | 24.7 |

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 35336 vs 35621 (-0.8%) | 35336 vs 71242 (-50.4%) | 35336 vs 106863 (-66.9%) | 35336 vs 142485 (-75.2%) |
| avg_equation | 33741 vs 35621 (-5.3%) | 51738 vs 71242 (-27.4%) | 51738 vs 106863 (-51.6%) | 51738 vs 142485 (-63.7%) |
| avg_gated_lookup | 35336 vs 35621 (-0.8%) | 35336 vs 71242 (-50.4%) | 35336 vs 106863 (-66.9%) | 35336 vs 142485 (-75.2%) |
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 24.7 points at 24.8% of the default cost, 50.4% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 24.7 points at 24.8% of the default cost, 66.9% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 24.7 points at 24.8% of the default cost, 75.2% under the budget it was given.
- `avg_equation` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 20.8 points at 36.3% of the default cost, 27.4% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 20.8 points at 36.3% of the default cost, 51.6% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 20.8 points at 36.3% of the default cost, 63.7% under the budget it was given.
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 24.7 points at 24.8% of the default cost, 50.4% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 24.7 points at 24.8% of the default cost, 66.9% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 24.7 points at 24.8% of the default cost, 75.2% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_aqua_mcleish_llama32_r32
# Table 1 -- aqua (mcleish_llama32_r32), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 41537 layer passes over 154 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 53.2 |
| default_cell | n/a | n/a | n/a | 84.2 (12%) |
| default_at_budget | n/a | n/a | 37.0 (35%) | 52.6 |
| lookup | 23.4 | 50.6 | 54.5 | 53.9 |
| equation | 24.0 | 48.1 | 54.5 | 54.5 |
| equation_n30 | 24.0 | 48.1 | 54.5 | 54.5 |
| equation_n100 | 24.0 | 48.1 | 54.5 | 54.5 |
| gated_equation | 24.0 | 48.1 | 54.5 | 52.6 |
| avg_lookup | 40.3 | 55.8 | 51.9 | 53.9 |
| avg_equation | 40.3 | 55.8 | 54.5 | 54.5 |
| avg_gated_lookup | 40.3 | 55.8 | 51.9 | 53.9 |

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 10368 vs 10384 (-0.2%) | 20616 vs 20768 (-0.7%) | 30852 vs 31153 (-1.0%) | 35791 vs 41537 (-13.8%) |
| avg_equation | 10380 vs 10384 (-0.0%) | 20685 vs 20768 (-0.4%) | 24710 vs 31153 (-20.7%) | 24710 vs 41537 (-40.5%) |
| avg_gated_lookup | 10368 vs 10384 (-0.2%) | 20616 vs 20768 (-0.7%) | 30852 vs 31153 (-1.0%) | 35791 vs 41537 (-13.8%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 53.9 points at 86.2% of the default cost, 13.8% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 54.5 points at 59.5% of the default cost, 20.7% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 54.5 points at 59.5% of the default cost, 40.5% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 53.9 points at 86.2% of the default cost, 13.8% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_aqua_ouro_1_4b_base
# Table 1 -- aqua (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 78835 layer passes over 154 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 67.5 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | 80.8 (17%) | 67.5 |
| lookup | 29.2 | 52.6 | 68.8 | 68.8 |
| equation | 24.0 | 52.6 | 68.8 | 68.2 |
| equation_n30 | 24.0 | 52.6 | 68.8 | 68.2 |
| equation_n100 | 24.0 | 52.6 | 68.8 | 68.2 |
| gated_equation | 24.0 | 52.6 | 68.8 | 68.2 |
| avg_lookup | 36.4 | 56.5 | 68.8 | 68.8 |
| avg_equation | 35.7 | 56.5 | 68.2 | 68.2 |
| avg_gated_lookup | 36.4 | 56.5 | 68.8 | 68.8 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 20737 vs 19709 (+5.2%) | 39745 vs 39418 (+0.8%) | 52245 vs 59126 (-11.6%) | 52245 vs 78835 (-33.7%) |
| avg_equation | 20357 vs 19709 (+3.3%) | 39745 vs 39418 (+0.8%) | 59882 vs 59126 (+1.3%) | 60706 vs 78835 (-23.0%) |
| avg_gated_lookup | 20737 vs 19709 (+5.2%) | 39745 vs 39418 (+0.8%) | 52245 vs 59126 (-11.6%) | 52245 vs 78835 (-33.7%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 68.8 points at 66.3% of the default cost, 11.6% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.8 points at 66.3% of the default cost, 33.7% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.2 points at 77.0% of the default cost, 23.0% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 68.8 points at 66.3% of the default cost, 11.6% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.8 points at 66.3% of the default cost, 33.7% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_aqua_ouro_1_4b_think
# Table 1 -- aqua (ouro_1_4b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 223283 layer passes over 154 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 82.5 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 58.4 | 78.6 | 83.1 |
| lookup | 52.6 | 81.2 | 84.4 | 83.1 |
| equation | 52.6 | 81.2 | 84.4 | 85.1 |
| equation_n30 | 52.6 | 81.2 | 84.4 | 85.1 |
| equation_n100 | 52.6 | 81.2 | 84.4 | 85.1 |
| gated_equation | 52.6 | 81.2 | 84.4 | 85.1 |
| avg_lookup | 64.9 | 81.2 | 82.5 | 85.1 |
| avg_equation | 64.9 | 79.9 | 85.1 | 85.1 |
| avg_gated_lookup | 64.9 | 81.2 | 82.5 | 85.1 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 52725 vs 55821 (-5.5%) | 113457 vs 111641 (+1.6%) | 168226 vs 167462 (+0.5%) | 217490 vs 223283 (-2.6%) |
| avg_equation | 52725 vs 55821 (-5.5%) | 112706 vs 111641 (+1.0%) | 166936 vs 167462 (-0.3%) | 219021 vs 223283 (-1.9%) |
| avg_gated_lookup | 52725 vs 55821 (-5.5%) | 113457 vs 111641 (+1.6%) | 168226 vs 167462 (+0.5%) | 217490 vs 223283 (-2.6%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_aqua_ouro_2_6b_base
# Table 1 -- aqua (ouro_2_6b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 158694 layer passes over 154 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 73.4 |
| default_cell | n/a | n/a | n/a | 73.4 |
| default_at_budget | n/a | n/a | 73.5 (22%) | 73.4 |
| lookup | 40.3 | 68.2 | 68.2 | 68.2 |
| equation | 50.6 | 65.6 | 66.2 | 66.2 |
| equation_n30 | 37.7 | 65.6 | 66.2 | 75.3 |
| equation_n100 | 50.6 | 65.6 | 66.2 | 66.2 |
| gated_equation | 50.6 | 65.6 | 66.2 | 73.4 |
| avg_lookup | 47.4 | 68.2 | 68.2 | 68.2 |
| avg_equation | 54.5 | 66.2 | 66.2 | 66.2 |
| avg_gated_lookup | 47.4 | 68.2 | 68.2 | 68.2 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 40712 vs 39674 (+2.6%) | 69931 vs 79347 (-11.9%) | 69931 vs 119021 (-41.2%) | 69931 vs 158694 (-55.9%) |
| avg_equation | 41923 vs 39674 (+5.7%) | 80006 vs 79347 (+0.8%) | 88368 vs 119021 (-25.8%) | 88368 vs 158694 (-44.3%) |
| avg_gated_lookup | 40712 vs 39674 (+2.6%) | 69931 vs 79347 (-11.9%) | 69931 vs 119021 (-41.2%) | 69931 vs 158694 (-55.9%) |
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 68.2 points at 44.1% of the default cost, 11.9% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 68.2 points at 44.1% of the default cost, 41.2% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.2 points at 44.1% of the default cost, 55.9% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 66.2 points at 55.7% of the default cost, 25.8% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 66.2 points at 55.7% of the default cost, 44.3% under the budget it was given.
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 68.2 points at 44.1% of the default cost, 11.9% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 68.2 points at 44.1% of the default cost, 41.2% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.2 points at 44.1% of the default cost, 55.9% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_aqua_ouro_2_6b_think
# Table 1 -- aqua (ouro_2_6b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 401640 layer passes over 154 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 89.0 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 55.8 | 85.1 | 86.4 |
| lookup | 50.0 | 80.5 | 85.1 | 86.4 |
| equation | 48.1 | 80.5 | 85.1 | 86.4 |
| equation_n30 | 50.6 | 80.5 | 85.1 | 86.4 |
| equation_n100 | 48.1 | 80.5 | 85.1 | 86.4 |
| gated_equation | 48.1 | 80.5 | 85.1 | 86.4 |
| avg_lookup | 63.6 | 83.1 | 85.1 | 87.7 |
| avg_equation | 63.0 | 83.1 | 85.1 | 87.7 |
| avg_gated_lookup | 63.6 | 83.1 | 85.1 | 87.7 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 99281 vs 100410 (-1.1%) | 196536 vs 200820 (-2.1%) | 293928 vs 301230 (-2.4%) | 394762 vs 401640 (-1.7%) |
| avg_equation | 94015 vs 100410 (-6.4%) | 196536 vs 200820 (-2.1%) | 296863 vs 301230 (-1.4%) | 394762 vs 401640 (-1.7%) |
| avg_gated_lookup | 99281 vs 100410 (-1.1%) | 196536 vs 200820 (-2.1%) | 293928 vs 301230 (-2.4%) | 394762 vs 401640 (-1.7%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_arc_huginn_0125
# Table 1 -- arc (huginn_0125), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 53810 layer passes over 1072 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 41.3 |
| default_cell | n/a | n/a | n/a | 42.3 (53%) |
| default_at_budget | n/a | n/a | n/a | 41.2 (94%) |
| lookup | 25.8 | 39.6 | 42.4 | 41.5 |
| equation | 24.5 | 39.2 | 40.4 | 40.4 |
| equation_n30 | 24.5 | 32.0 | 40.4 | 41.3 |
| equation_n100 | 24.5 | 39.2 | 40.4 | 40.4 |
| gated_equation | 24.5 | 39.2 | 40.4 | 41.3 |
| avg_lookup | 33.7 | 41.9 | 41.4 | 41.3 |
| avg_equation | 33.1 | 40.1 | 40.5 | 41.3 |
| avg_gated_lookup | 33.7 | 41.9 | 41.4 | 41.3 |

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 14432 vs 13452 (+7.3%) | 26038 vs 26905 (-3.2%) | 40445 vs 40357 (+0.2%) | 48464 vs 53810 (-9.9%) |
| avg_equation | 13874 vs 13452 (+3.1%) | 27364 vs 26905 (+1.7%) | 40630 vs 40357 (+0.7%) | 53940 vs 53810 (+0.2%) |
| avg_gated_lookup | 14432 vs 13452 (+7.3%) | 26038 vs 26905 (-3.2%) | 40445 vs 40357 (+0.2%) | 48464 vs 53810 (-9.9%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 41.3 points at 90.1% of the default cost, 9.9% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 41.3 points at 90.1% of the default cost, 9.9% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_arc_mcleish_llama32_r32
# Table 1 -- arc (mcleish_llama32_r32), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 22554 layer passes over 1072 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 44.5 |
| default_cell | n/a | n/a | n/a | 43.6 (61%) |
| default_at_budget | n/a | n/a | n/a | 44.0 (95%) |
| lookup | 24.2 (95%) | 38.0 | 42.8 | 42.8 |
| equation | 24.7 (95%) | 38.1 | 42.8 | 42.4 |
| equation_n30 | 23.4 (95%) | 38.0 | 42.8 | 42.4 |
| equation_n100 | 24.7 (95%) | 38.1 | 42.8 | 42.4 |
| gated_equation | 24.7 (95%) | 38.1 | 42.8 | 42.7 |
| avg_lookup | 26.8 | 43.1 | 42.8 | 42.8 |
| avg_equation | 26.8 | 43.1 | 41.8 | 43.9 |
| avg_gated_lookup | 26.8 | 43.1 | 42.8 | 42.8 |

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 5725 vs 5638 (+1.5%) | 11334 vs 11277 (+0.5%) | 11570 vs 16915 (-31.6%) | 11570 vs 22554 (-48.7%) |
| avg_equation | 5725 vs 5638 (+1.5%) | 11334 vs 11277 (+0.5%) | 17005 vs 16915 (+0.5%) | 22019 vs 22554 (-2.4%) |
| avg_gated_lookup | 5725 vs 5638 (+1.5%) | 11334 vs 11277 (+0.5%) | 11570 vs 16915 (-31.6%) | 11570 vs 22554 (-48.7%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 42.8 points at 51.3% of the default cost, 31.6% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 42.8 points at 51.3% of the default cost, 48.7% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 43.9 points at 97.6% of the default cost, 2.4% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 42.8 points at 51.3% of the default cost, 31.6% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 42.8 points at 51.3% of the default cost, 48.7% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_arc_ouro_1_4b_base
# Table 1 -- arc (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 38812 layer passes over 1072 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 86.5 |
| default_cell | n/a | n/a | n/a | 86.3 (55%) |
| default_at_budget | n/a | n/a | n/a | 86.6 (94%) |
| lookup | 42.9 (94%) | 75.4 | 84.0 | 86.0 |
| equation | 44.0 (94%) | 72.8 | 81.8 | 85.6 |
| equation_n30 | 44.0 (94%) | 72.8 | 84.4 | 85.7 |
| equation_n100 | 44.0 (94%) | 72.8 | 81.8 | 85.6 |
| gated_equation | 44.0 (94%) | 72.8 | 81.8 | 85.6 |
| avg_lookup | 44.8 | 78.0 | 82.6 | 86.1 |
| avg_equation | 42.6 | 75.4 | 84.6 | 86.4 |
| avg_gated_lookup | 44.8 | 78.0 | 82.6 | 86.1 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 9348 vs 9703 (-3.7%) | 18574 vs 19406 (-4.3%) | 29163 vs 29109 (+0.2%) | 38131 vs 38812 (-1.8%) |
| avg_equation | 9621 vs 9703 (-0.9%) | 19406 vs 19406 (-0.0%) | 29073 vs 29109 (-0.1%) | 38747 vs 38812 (-0.2%) |
| avg_gated_lookup | 9348 vs 9703 (-3.7%) | 18574 vs 19406 (-4.3%) | 29163 vs 29109 (+0.2%) | 38131 vs 38812 (-1.8%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 86.1 points at 98.2% of the default cost, 1.8% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 86.1 points at 98.2% of the default cost, 1.8% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_arc_ouro_1_4b_think
# Table 1 -- arc (ouro_1_4b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 85662 layer passes over 1072 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 93.4 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 87.2 (98%) | 89.1 | 93.4 |
| lookup | 74.4 | 86.3 | 89.6 | 89.6 |
| equation | 74.6 | 89.1 | 93.8 | 93.7 |
| equation_n30 | 74.6 | 89.2 | 89.4 | 89.4 |
| equation_n100 | 74.6 | 89.1 | 93.8 | 93.7 |
| gated_equation | 74.6 | 89.1 | 93.8 | 93.7 |
| avg_lookup | 74.5 | 88.1 | 89.6 | 89.6 |
| avg_equation | 76.5 | 88.5 | 93.8 | 93.7 |
| avg_gated_lookup | 74.5 | 88.1 | 89.6 | 89.6 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 21166 vs 21415 (-1.2%) | 41082 vs 42831 (-4.1%) | 45653 vs 64246 (-28.9%) | 45653 vs 85662 (-46.7%) |
| avg_equation | 21252 vs 21415 (-0.8%) | 41606 vs 42831 (-2.9%) | 63974 vs 64246 (-0.4%) | 66696 vs 85662 (-22.1%) |
| avg_gated_lookup | 21166 vs 21415 (-1.2%) | 41082 vs 42831 (-4.1%) | 45653 vs 64246 (-28.9%) | 45653 vs 85662 (-46.7%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 89.6 points at 53.3% of the default cost, 28.9% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 89.6 points at 53.3% of the default cost, 46.7% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 93.7 points at 77.9% of the default cost, 22.1% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 89.6 points at 53.3% of the default cost, 28.9% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 89.6 points at 53.3% of the default cost, 46.7% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_arc_ouro_2_6b_base
# Table 1 -- arc (ouro_2_6b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 77503 layer passes over 1072 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 93.3 |
| default_cell | n/a | n/a | n/a | 93.1 (57%) |
| default_at_budget | n/a | n/a | n/a | 93.2 (93%) |
| lookup | 63.0 (93%) | 86.6 | 88.1 | 88.1 |
| equation | 56.6 (93%) | 85.8 | 90.6 | 91.9 |
| equation_n30 | 56.6 (93%) | 85.9 | 91.0 | 92.4 |
| equation_n100 | 56.6 (93%) | 85.8 | 90.6 | 91.9 |
| gated_equation | 56.6 (93%) | 85.8 | 90.6 | 91.9 |
| avg_lookup | 64.8 | 88.1 | 88.1 | 88.1 |
| avg_equation | 57.6 | 88.0 | 91.9 | 91.9 |
| avg_gated_lookup | 64.8 | 88.1 | 88.1 | 88.1 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 18696 vs 19376 (-3.5%) | 35100 vs 38752 (-9.4%) | 35100 vs 58127 (-39.6%) | 35100 vs 77503 (-54.7%) |
| avg_equation | 19108 vs 19376 (-1.4%) | 38325 vs 38752 (-1.1%) | 58095 vs 58127 (-0.1%) | 58142 vs 77503 (-25.0%) |
| avg_gated_lookup | 18696 vs 19376 (-3.5%) | 35100 vs 38752 (-9.4%) | 35100 vs 58127 (-39.6%) | 35100 vs 77503 (-54.7%) |
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 88.1 points at 45.3% of the default cost, 9.4% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 88.1 points at 45.3% of the default cost, 39.6% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 88.1 points at 45.3% of the default cost, 54.7% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 91.9 points at 75.0% of the default cost, 25.0% under the budget it was given.
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 88.1 points at 45.3% of the default cost, 9.4% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 88.1 points at 45.3% of the default cost, 39.6% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 88.1 points at 45.3% of the default cost, 54.7% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_arc_ouro_2_6b_think
# Table 1 -- arc (ouro_2_6b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 161239 layer passes over 1072 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 96.5 |
| default_cell | n/a | n/a | n/a | 96.0 (60%) |
| default_at_budget | n/a | 92.0 (91%) | 93.2 | 96.4 |
| lookup | 83.8 | 92.4 | 95.2 | 96.5 |
| equation | 74.3 | 91.9 | 96.4 | 96.5 |
| equation_n30 | 74.3 | 91.8 | 96.1 | 96.2 |
| equation_n100 | 74.3 | 91.9 | 96.4 | 96.5 |
| gated_equation | 74.3 | 91.9 | 96.4 | 96.5 |
| avg_lookup | 87.6 | 93.3 | 96.5 | 96.5 |
| avg_equation | 87.6 | 94.1 | 96.5 | 96.5 |
| avg_gated_lookup | 87.6 | 93.3 | 96.5 | 96.5 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 39959 vs 40310 (-0.9%) | 78887 vs 80620 (-2.1%) | 117565 vs 120930 (-2.8%) | 117565 vs 161239 (-27.1%) |
| avg_equation | 39959 vs 40310 (-0.9%) | 80069 vs 80620 (-0.7%) | 117565 vs 120930 (-2.8%) | 117565 vs 161239 (-27.1%) |
| avg_gated_lookup | 39959 vs 40310 (-0.9%) | 78887 vs 80620 (-2.1%) | 117565 vs 120930 (-2.8%) | 117565 vs 161239 (-27.1%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 96.5 points at 72.9% of the default cost, 2.8% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 96.5 points at 72.9% of the default cost, 27.1% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 96.5 points at 72.9% of the default cost, 2.8% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 96.5 points at 72.9% of the default cost, 27.1% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 96.5 points at 72.9% of the default cost, 2.8% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 96.5 points at 72.9% of the default cost, 27.1% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_bbh_huginn_0125
# Table 1 -- bbh (huginn_0125), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 142666 layer passes over 2337 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 35.7 |
| default_cell | n/a | 55.4 (10%) | 62.9 (21%) | 54.1 (42%) |
| default_at_budget | 55.8 (10%) | 61.0 (21%) | 52.4 (42%) | 36.2 (88%) |
| lookup | 30.6 | 31.4 | 33.8 | 35.6 |
| equation | 23.5 | 24.7 | 29.2 | 35.8 |
| equation_n30 | 28.8 | 30.5 | 33.0 | 35.4 |
| equation_n100 | 23.5 | 24.7 | 29.2 | 35.8 |
| gated_equation | 23.5 | 24.7 | 30.3 | 35.9 |
| avg_lookup | 32.4 | 35.0 | 36.9 | 35.8 |
| avg_equation | 24.7 | 33.7 | 35.8 | 35.6 |
| avg_gated_lookup | 32.4 | 35.0 | 36.9 | 35.8 |

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 35202 vs 35667 (-1.3%) | 72906 vs 71333 (+2.2%) | 104528 vs 107000 (-2.3%) | 128915 vs 142666 (-9.6%) |
| avg_equation | 35374 vs 35667 (-0.8%) | 74818 vs 71333 (+4.9%) | 105939 vs 107000 (-1.0%) | 141003 vs 142666 (-1.2%) |
| avg_gated_lookup | 35202 vs 35667 (-1.3%) | 72906 vs 71333 (+2.2%) | 104528 vs 107000 (-2.3%) | 128915 vs 142666 (-9.6%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 35.8 points at 90.4% of the default cost, 9.6% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 35.8 points at 90.4% of the default cost, 9.6% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_bbh_mcleish_llama32_r32
# Table 1 -- bbh (mcleish_llama32_r32), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 69981 layer passes over 2337 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 43.5 |
| default_cell | n/a | n/a | 49.2 (10%) | 55.9 (46%) |
| default_at_budget | 49.2 (10%) | 57.5 (31%) | 44.1 (72%) | 43.4 (99%) |
| lookup | 34.4 (99%) | 37.7 | 40.2 | 40.0 |
| equation | 33.8 (99%) | 37.3 | 40.9 | 43.4 |
| equation_n30 | 33.3 (99%) | 42.1 | 43.4 | 43.4 |
| equation_n100 | 33.8 (99%) | 37.3 | 40.9 | 43.4 |
| gated_equation | 33.7 (99%) | 37.4 | 40.9 | 43.4 |
| avg_lookup | 36.3 | 40.3 | 40.1 | 40.1 |
| avg_equation | 36.5 | 40.2 | 43.5 | 43.5 |
| avg_gated_lookup | 36.3 | 40.3 | 40.1 | 43.5 |

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 18026 vs 17495 (+3.0%) | 35010 vs 34990 (+0.1%) | 47666 vs 52485 (-9.2%) | 47666 vs 69981 (-31.9%) |
| avg_equation | 17333 vs 17495 (-0.9%) | 34984 vs 34990 (-0.0%) | 52080 vs 52485 (-0.8%) | 66969 vs 69981 (-4.3%) |
| avg_gated_lookup | 18026 vs 17495 (+3.0%) | 35010 vs 34990 (+0.1%) | 47666 vs 52485 (-9.2%) | 66969 vs 69981 (-4.3%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 40.1 points at 68.1% of the default cost, 9.2% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 40.1 points at 68.1% of the default cost, 31.9% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 43.5 points at 95.7% of the default cost, 4.3% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 40.1 points at 68.1% of the default cost, 9.2% under the budget it was given.
- `avg_gated_lookup` reverted to the default cell for every question at 1.00x: the predicted calibration margin did not clear 0.50 of its own SD.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_bbh_ouro_1_4b_base
# Table 1 -- bbh (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 100844 layer passes over 2337 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 75.6 |
| default_cell | n/a | 79.6 (10%) | 84.6 (21%) | 81.6 (34%) |
| default_at_budget | 76.7 (10%) | 79.6 (10%) | 80.3 (30%) | 64.9 (86%) |
| lookup | 33.8 (86%) | 49.3 | 63.2 | 72.3 |
| equation | 33.8 (86%) | 48.0 | 65.9 | 72.4 |
| equation_n30 | 33.8 (86%) | 48.0 | 66.0 | 70.3 |
| equation_n100 | 33.8 (86%) | 48.0 | 65.9 | 72.4 |
| gated_equation | 33.8 (86%) | 48.0 | 65.9 | 72.4 |
| avg_lookup | 33.1 | 55.2 | 70.6 | 75.3 |
| avg_equation | 36.5 | 56.7 | 70.0 | 75.6 |
| avg_gated_lookup | 33.1 | 55.2 | 70.6 | 75.3 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 24499 vs 25211 (-2.8%) | 50229 vs 50422 (-0.4%) | 74979 vs 75633 (-0.9%) | 94123 vs 100844 (-6.7%) |
| avg_equation | 25681 vs 25211 (+1.9%) | 49594 vs 50422 (-1.6%) | 75395 vs 75633 (-0.3%) | 100462 vs 100844 (-0.4%) |
| avg_gated_lookup | 24499 vs 25211 (-2.8%) | 50229 vs 50422 (-0.4%) | 74979 vs 75633 (-0.9%) | 94123 vs 100844 (-6.7%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 75.3 points at 93.3% of the default cost, 6.7% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 75.3 points at 93.3% of the default cost, 6.7% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_bbh_ouro_1_4b_think
# Table 1 -- bbh (ouro_1_4b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 182991 layer passes over 2337 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 84.4 |
| default_cell | n/a | n/a | 69.6 (10%) | 83.4 (72%) |
| default_at_budget | 66.2 (10%) | 52.8 (72%) | 66.6 | 84.2 |
| lookup | 35.1 | 66.9 | 81.3 | 82.5 |
| equation | 35.5 | 66.9 | 81.0 | 83.4 |
| equation_n30 | 35.5 | 66.9 | 81.3 | 82.5 |
| equation_n100 | 35.5 | 66.9 | 81.0 | 83.4 |
| gated_equation | 35.5 | 66.9 | 81.1 | 83.5 |
| avg_lookup | 45.5 | 74.1 | 82.5 | 82.5 |
| avg_equation | 43.9 | 75.9 | 81.7 | 84.4 |
| avg_gated_lookup | 45.5 | 74.1 | 82.5 | 82.5 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 47551 vs 45748 (+3.9%) | 91402 vs 91495 (-0.1%) | 136068 vs 137243 (-0.9%) | 155563 vs 182991 (-15.0%) |
| avg_equation | 47332 vs 45748 (+3.5%) | 92646 vs 91495 (+1.3%) | 137464 vs 137243 (+0.2%) | 173767 vs 182991 (-5.0%) |
| avg_gated_lookup | 47551 vs 45748 (+3.9%) | 91402 vs 91495 (-0.1%) | 136068 vs 137243 (-0.9%) | 155563 vs 182991 (-15.0%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 82.5 points at 85.0% of the default cost, 15.0% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 84.4 points at 95.0% of the default cost, 5.0% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 82.5 points at 85.0% of the default cost, 15.0% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_bbh_ouro_2_6b_base
# Table 1 -- bbh (ouro_2_6b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 197932 layer passes over 2337 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 82.6 |
| default_cell | n/a | 90.4 (10%) | 90.2 (21%) | 84.4 (53%) |
| default_at_budget | 81.0 (10%) | 90.4 (10%) | 87.1 (26%) | 70.0 (85%) |
| lookup | 43.4 (85%) | 56.5 | 79.6 | 81.0 |
| equation | 40.3 (85%) | 57.8 | 79.6 | 81.2 |
| equation_n30 | 40.3 (85%) | 57.8 | 79.6 | 81.2 |
| equation_n100 | 40.3 (85%) | 57.8 | 79.6 | 81.2 |
| gated_equation | 40.3 (85%) | 57.8 | 79.6 | 81.2 |
| avg_lookup | 44.1 | 74.3 | 81.3 | 81.3 |
| avg_equation | 44.1 | 74.3 | 81.4 | 81.4 |
| avg_gated_lookup | 44.1 | 74.3 | 81.3 | 81.3 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 49558 vs 49483 (+0.2%) | 97272 vs 98966 (-1.7%) | 143429 vs 148449 (-3.4%) | 143429 vs 197932 (-27.5%) |
| avg_equation | 49558 vs 49483 (+0.2%) | 97294 vs 98966 (-1.7%) | 143648 vs 148449 (-3.2%) | 143648 vs 197932 (-27.4%) |
| avg_gated_lookup | 49558 vs 49483 (+0.2%) | 97272 vs 98966 (-1.7%) | 143429 vs 148449 (-3.4%) | 143429 vs 197932 (-27.5%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 81.3 points at 72.5% of the default cost, 3.4% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 81.3 points at 72.5% of the default cost, 27.5% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 81.4 points at 72.6% of the default cost, 3.2% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 81.4 points at 72.6% of the default cost, 27.4% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 81.3 points at 72.5% of the default cost, 3.4% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 81.3 points at 72.5% of the default cost, 27.5% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_bbh_ouro_2_6b_think
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

## alloc_v2_csqa_huginn_0125
# Table 1 -- csqa (huginn_0125), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 87279 layer passes over 1121 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 43.6 |
| default_cell | n/a | n/a | n/a | 43.8 (60%) |
| default_at_budget | n/a | n/a | n/a | 42.8 |
| lookup | 19.0 | 30.9 | 42.6 | 43.1 |
| equation | 19.0 | 31.4 | 42.6 | 42.6 |
| equation_n30 | 19.0 | 31.4 | 42.6 | 42.6 |
| equation_n100 | 19.0 | 31.4 | 42.6 | 42.6 |
| gated_equation | 19.0 | 31.4 | 42.6 | 43.6 |
| avg_lookup | 25.9 | 41.9 | 42.3 | 43.1 |
| avg_equation | 27.2 | 42.2 | 42.6 | 42.6 |
| avg_gated_lookup | 25.9 | 41.9 | 42.3 | 43.1 |

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 21618 vs 21820 (-0.9%) | 42949 vs 43639 (-1.6%) | 61841 vs 65459 (-5.5%) | 86310 vs 87279 (-1.1%) |
| avg_equation | 21773 vs 21820 (-0.2%) | 42966 vs 43639 (-1.5%) | 44939 vs 65459 (-31.3%) | 44939 vs 87279 (-48.5%) |
| avg_gated_lookup | 21618 vs 21820 (-0.9%) | 42949 vs 43639 (-1.6%) | 61841 vs 65459 (-5.5%) | 86310 vs 87279 (-1.1%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 43.1 points at 98.9% of the default cost, 1.1% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 42.6 points at 51.5% of the default cost, 31.3% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 42.6 points at 51.5% of the default cost, 48.5% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 43.1 points at 98.9% of the default cost, 1.1% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_csqa_mcleish_llama32_r32
# Table 1 -- csqa (mcleish_llama32_r32), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 35104 layer passes over 1121 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 38.1 |
| default_cell | n/a | n/a | n/a | 39.7 (56%) |
| default_at_budget | n/a | n/a | n/a | 39.7 (100%) |
| lookup | 21.4 (100%) | 30.0 | 42.2 | 42.2 |
| equation | 21.4 (100%) | 32.7 | 42.2 | 42.2 |
| equation_n30 | 21.4 (100%) | 28.0 | 42.2 | 42.2 |
| equation_n100 | 21.4 (100%) | 32.7 | 42.2 | 42.2 |
| gated_equation | 21.4 (100%) | 32.7 | 42.2 | 42.2 |
| avg_lookup | 22.1 | 39.9 | 42.4 | 42.2 |
| avg_equation | 22.2 | 39.9 | 42.4 | 42.2 |
| avg_gated_lookup | 22.1 | 39.9 | 42.4 | 42.2 |

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 8701 vs 8776 (-0.9%) | 17229 vs 17552 (-1.8%) | 25337 vs 26328 (-3.8%) | 33234 vs 35104 (-5.3%) |
| avg_equation | 8669 vs 8776 (-1.2%) | 17147 vs 17552 (-2.3%) | 25337 vs 26328 (-3.8%) | 33234 vs 35104 (-5.3%) |
| avg_gated_lookup | 8701 vs 8776 (-0.9%) | 17229 vs 17552 (-1.8%) | 25337 vs 26328 (-3.8%) | 33234 vs 35104 (-5.3%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 42.2 points at 94.7% of the default cost, 5.3% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 42.2 points at 94.7% of the default cost, 5.3% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 42.2 points at 94.7% of the default cost, 5.3% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_csqa_ouro_1_4b_base
# Table 1 -- csqa (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 61952 layer passes over 1121 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 72.3 |
| default_cell | n/a | n/a | n/a | 73.6 (55%) |
| default_at_budget | n/a | n/a | n/a | 72.1 |
| lookup | 33.6 | 65.6 | 71.8 | 73.1 |
| equation | 33.0 | 61.6 | 71.1 | 72.0 |
| equation_n30 | 32.3 | 61.6 | 71.3 | 73.1 |
| equation_n100 | 33.0 | 61.6 | 71.1 | 72.0 |
| gated_equation | 33.0 | 61.6 | 71.1 | 72.2 |
| avg_lookup | 31.0 | 65.7 | 71.3 | 73.1 |
| avg_equation | 33.6 | 61.8 | 71.4 | 72.3 |
| avg_gated_lookup | 31.0 | 65.7 | 71.3 | 73.1 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 15240 vs 15488 (-1.6%) | 30124 vs 30976 (-2.8%) | 46214 vs 46464 (-0.5%) | 58626 vs 61952 (-5.4%) |
| avg_equation | 15475 vs 15488 (-0.1%) | 31071 vs 30976 (+0.3%) | 46531 vs 46464 (+0.1%) | 61970 vs 61952 (+0.0%) |
| avg_gated_lookup | 15240 vs 15488 (-1.6%) | 30124 vs 30976 (-2.8%) | 46214 vs 46464 (-0.5%) | 58626 vs 61952 (-5.4%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 73.1 points at 94.6% of the default cost, 5.4% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 73.1 points at 94.6% of the default cost, 5.4% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_csqa_ouro_1_4b_think
# Table 1 -- csqa (ouro_1_4b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 131275 layer passes over 1121 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 77.4 |
| default_cell | n/a | n/a | n/a | 77.4 |
| default_at_budget | n/a | 70.9 | 76.0 | 77.4 |
| lookup | 55.8 | 70.2 | 74.2 | 74.2 |
| equation | 55.6 | 74.0 | 76.7 | 77.4 |
| equation_n30 | 55.6 | 74.0 | 76.7 | 77.4 |
| equation_n100 | 55.6 | 74.0 | 76.7 | 77.4 |
| gated_equation | 55.6 | 74.0 | 76.7 | 77.4 |
| avg_lookup | 56.0 | 73.1 | 74.2 | 74.2 |
| avg_equation | 60.1 | 74.8 | 76.0 | 77.4 |
| avg_gated_lookup | 56.0 | 73.1 | 74.2 | 74.2 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 32413 vs 32819 (-1.2%) | 64893 vs 65638 (-1.1%) | 66690 vs 98456 (-32.3%) | 66690 vs 131275 (-49.2%) |
| avg_equation | 32562 vs 32819 (-0.8%) | 63586 vs 65638 (-3.1%) | 96400 vs 98456 (-2.1%) | 113240 vs 131275 (-13.7%) |
| avg_gated_lookup | 32413 vs 32819 (-1.2%) | 64893 vs 65638 (-1.1%) | 66690 vs 98456 (-32.3%) | 66690 vs 131275 (-49.2%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 74.2 points at 50.8% of the default cost, 32.3% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 74.2 points at 50.8% of the default cost, 49.2% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 77.4 points at 86.3% of the default cost, 13.7% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 74.2 points at 50.8% of the default cost, 32.3% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 74.2 points at 50.8% of the default cost, 49.2% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_csqa_ouro_2_6b_base
# Table 1 -- csqa (ouro_2_6b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 124178 layer passes over 1121 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 80.0 |
| default_cell | n/a | n/a | n/a | 79.6 (55%) |
| default_at_budget | n/a | n/a | n/a | 80.9 |
| lookup | 36.7 | 75.2 | 80.6 | 80.6 |
| equation | 36.7 | 74.0 | 74.0 | 74.0 |
| equation_n30 | 36.7 | 74.0 | 74.0 | 74.0 |
| equation_n100 | 36.7 | 74.0 | 74.0 | 74.0 |
| gated_equation | 36.7 | 74.0 | 74.0 | 77.3 |
| avg_lookup | 40.2 | 75.2 | 80.6 | 80.6 |
| avg_equation | 40.2 | 74.0 | 74.0 | 74.0 |
| avg_gated_lookup | 40.2 | 75.2 | 80.6 | 80.6 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 31001 vs 31044 (-0.1%) | 60965 vs 62089 (-1.8%) | 87939 vs 93133 (-5.6%) | 87939 vs 124178 (-29.2%) |
| avg_equation | 31001 vs 31044 (-0.1%) | 61654 vs 62089 (-0.7%) | 61654 vs 93133 (-33.8%) | 61654 vs 124178 (-50.4%) |
| avg_gated_lookup | 31001 vs 31044 (-0.1%) | 60965 vs 62089 (-1.8%) | 87939 vs 93133 (-5.6%) | 87939 vs 124178 (-29.2%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 80.6 points at 70.8% of the default cost, 5.6% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 80.6 points at 70.8% of the default cost, 29.2% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 74.0 points at 49.6% of the default cost, 33.8% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 74.0 points at 49.6% of the default cost, 50.4% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 80.6 points at 70.8% of the default cost, 5.6% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 80.6 points at 70.8% of the default cost, 29.2% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_csqa_ouro_2_6b_think
# Table 1 -- csqa (ouro_2_6b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 235620 layer passes over 1121 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 80.8 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | 79.2 | 80.5 |
| lookup | 27.4 | 77.4 | 79.2 | 80.6 |
| equation | 19.6 | 76.7 | 77.1 | 80.5 |
| equation_n30 | 27.4 | 76.7 | 78.8 | 80.5 |
| equation_n100 | 19.6 | 76.7 | 77.1 | 80.5 |
| gated_equation | 19.6 | 76.7 | 77.1 | 80.5 |
| avg_lookup | 66.9 | 77.6 | 79.1 | 80.6 |
| avg_equation | 66.9 | 76.7 | 77.2 | 80.5 |
| avg_gated_lookup | 66.9 | 77.6 | 79.1 | 80.6 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 57972 vs 58905 (-1.6%) | 112902 vs 117810 (-4.2%) | 174462 vs 176715 (-1.3%) | 213213 vs 235620 (-9.5%) |
| avg_equation | 57972 vs 58905 (-1.6%) | 117634 vs 117810 (-0.1%) | 166452 vs 176715 (-5.8%) | 235143 vs 235620 (-0.2%) |
| avg_gated_lookup | 57972 vs 58905 (-1.6%) | 112902 vs 117810 (-4.2%) | 174462 vs 176715 (-1.3%) | 213213 vs 235620 (-9.5%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 80.6 points at 90.5% of the default cost, 9.5% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 80.6 points at 90.5% of the default cost, 9.5% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_gsm8k_huginn_0125
# Table 1 -- gsm8k (huginn_0125), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 104580 layer passes over 1219 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 26.3 |
| default_cell | n/a | n/a | n/a | 27.2 (95%) |
| default_at_budget | n/a | n/a | 2.1 (12%) | 26.3 |
| lookup | 7.9 | 21.5 | 21.3 | 26.5 |
| equation | 8.1 | 21.3 | 21.2 | 26.5 |
| equation_n30 | 8.0 | 21.4 | 21.2 | 26.5 |
| equation_n100 | 8.1 | 21.3 | 21.2 | 26.5 |
| gated_equation | 8.1 | 21.3 | 21.2 | 26.4 |
| avg_lookup | 13.8 | 22.4 | 24.6 | 26.4 |
| avg_equation | 13.0 | 21.4 | 24.6 | 26.4 |
| avg_gated_lookup | 13.8 | 22.4 | 24.6 | 26.3 |

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 26271 vs 26145 (+0.5%) | 52055 vs 52290 (-0.4%) | 78041 vs 78435 (-0.5%) | 94504 vs 104580 (-9.6%) |
| avg_equation | 25362 vs 26145 (-3.0%) | 52074 vs 52290 (-0.4%) | 77863 vs 78435 (-0.7%) | 95263 vs 104580 (-8.9%) |
| avg_gated_lookup | 26271 vs 26145 (+0.5%) | 52055 vs 52290 (-0.4%) | 78041 vs 78435 (-0.5%) | 99015 vs 104580 (-5.3%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 26.4 points at 90.4% of the default cost, 9.6% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 26.4 points at 91.1% of the default cost, 8.9% under the budget it was given.
- `avg_gated_lookup` reverted to the default cell for every question at 1.00x: the predicted calibration margin did not clear 0.50 of its own SD.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_gsm8k_mcleish_llama32_r32
# Table 1 -- gsm8k (mcleish_llama32_r32), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 140290 layer passes over 1219 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 49.2 |
| default_cell | n/a | n/a | n/a | 65.4 (18%) |
| default_at_budget | n/a | n/a | 6.7 (2%) | 48.8 |
| lookup | 47.1 | 48.6 | 49.1 | 49.1 |
| equation | 47.2 | 49.8 | 49.1 | 49.1 |
| equation_n30 | 47.2 | 49.5 | 49.1 | 49.1 |
| equation_n100 | 47.2 | 49.8 | 49.1 | 49.1 |
| gated_equation | 47.2 | 49.8 | 49.1 | 49.1 |
| avg_lookup | 48.1 | 49.1 | 49.1 | 49.1 |
| avg_equation | 48.5 | 49.1 | 49.1 | 49.1 |
| avg_gated_lookup | 48.1 | 49.1 | 49.1 | 49.1 |

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 34502 vs 35073 (-1.6%) | 69768 vs 70145 (-0.5%) | 70645 vs 105218 (-32.9%) | 70645 vs 140290 (-49.6%) |
| avg_equation | 34510 vs 35073 (-1.6%) | 68324 vs 70145 (-2.6%) | 74904 vs 105218 (-28.8%) | 74904 vs 140290 (-46.6%) |
| avg_gated_lookup | 34502 vs 35073 (-1.6%) | 69768 vs 70145 (-0.5%) | 70645 vs 105218 (-32.9%) | 70645 vs 140290 (-49.6%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 49.1 points at 50.4% of the default cost, 32.9% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 49.1 points at 50.4% of the default cost, 49.6% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 49.1 points at 53.4% of the default cost, 28.8% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 49.1 points at 53.4% of the default cost, 46.6% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 49.1 points at 50.4% of the default cost, 32.9% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 49.1 points at 50.4% of the default cost, 49.6% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_gsm8k_ouro_1_4b_base
# Table 1 -- gsm8k (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 77130 layer passes over 1219 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 76.9 |
| default_cell | n/a | n/a | n/a | 79.4 (86%) |
| default_at_budget | n/a | n/a | n/a | 73.3 |
| lookup | 22.1 | 61.9 | 71.7 | 76.8 |
| equation | 22.2 | 61.9 | 71.7 | 76.2 |
| equation_n30 | 22.2 | 61.6 | 70.7 | 73.7 |
| equation_n100 | 22.2 | 61.9 | 71.7 | 76.2 |
| gated_equation | 22.2 | 61.9 | 71.7 | 76.2 |
| avg_lookup | 24.0 | 64.9 | 70.1 | 76.9 |
| avg_equation | 24.0 | 65.2 | 73.7 | 76.9 |
| avg_gated_lookup | 24.0 | 64.9 | 70.1 | 76.9 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 19484 vs 19283 (+1.0%) | 38404 vs 38565 (-0.4%) | 57797 vs 57848 (-0.1%) | 74850 vs 77130 (-3.0%) |
| avg_equation | 19484 vs 19283 (+1.0%) | 38704 vs 38565 (+0.4%) | 57697 vs 57848 (-0.3%) | 74850 vs 77130 (-3.0%) |
| avg_gated_lookup | 19484 vs 19283 (+1.0%) | 38404 vs 38565 (-0.4%) | 57797 vs 57848 (-0.1%) | 74850 vs 77130 (-3.0%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 76.9 points at 97.0% of the default cost, 3.0% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 76.9 points at 97.0% of the default cost, 3.0% under the budget it was given.
- `avg_gated_lookup` reverted to the default cell for every question at 1.00x: the predicted calibration margin did not clear 0.50 of its own SD.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_gsm8k_ouro_1_4b_think
# Table 1 -- gsm8k (ouro_1_4b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 127112 layer passes over 1219 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 93.1 |
| default_cell | n/a | n/a | n/a | 93.5 (95%) |
| default_at_budget | n/a | 25.7 (28%) | 59.7 | 93.1 |
| lookup | 31.7 | 85.9 | 91.5 | 93.0 |
| equation | 31.7 | 85.9 | 91.8 | 93.0 |
| equation_n30 | 31.7 | 85.9 | 91.8 | 91.8 |
| equation_n100 | 31.7 | 85.9 | 91.8 | 93.0 |
| gated_equation | 31.7 | 85.9 | 91.8 | 93.1 |
| avg_lookup | 37.6 | 86.9 | 91.8 | 93.0 |
| avg_equation | 37.6 | 86.9 | 91.8 | 93.0 |
| avg_gated_lookup | 37.6 | 86.9 | 91.8 | 93.1 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 30863 vs 31778 (-2.9%) | 63695 vs 63556 (+0.2%) | 95648 vs 95334 (+0.3%) | 118650 vs 127112 (-6.7%) |
| avg_equation | 30863 vs 31778 (-2.9%) | 63853 vs 63556 (+0.5%) | 95648 vs 95334 (+0.3%) | 118650 vs 127112 (-6.7%) |
| avg_gated_lookup | 30863 vs 31778 (-2.9%) | 63695 vs 63556 (+0.2%) | 95648 vs 95334 (+0.3%) | 122882 vs 127112 (-3.3%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 93.0 points at 93.3% of the default cost, 6.7% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 93.0 points at 93.3% of the default cost, 6.7% under the budget it was given.
- `avg_gated_lookup` reverted to the default cell for every question at 1.00x: the predicted calibration margin did not clear 0.50 of its own SD.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_gsm8k_ouro_2_6b_base
# Table 1 -- gsm8k (ouro_2_6b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 151460 layer passes over 1219 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 82.7 |
| default_cell | n/a | n/a | n/a | 84.3 (87%) |
| default_at_budget | n/a | n/a | n/a | 77.9 |
| lookup | 29.8 | 68.7 | 76.9 | 82.0 |
| equation | 29.9 | 68.9 | 77.4 | 82.0 |
| equation_n30 | 29.9 | 68.9 | 77.4 | 82.0 |
| equation_n100 | 29.9 | 68.9 | 77.4 | 82.0 |
| gated_equation | 29.9 | 68.9 | 77.4 | 82.1 |
| avg_lookup | 31.7 | 73.6 | 78.9 | 82.3 |
| avg_equation | 31.7 | 74.5 | 78.1 | 82.3 |
| avg_gated_lookup | 31.7 | 73.6 | 78.9 | 82.7 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 37683 vs 37865 (-0.5%) | 75590 vs 75730 (-0.2%) | 113426 vs 113595 (-0.1%) | 146701 vs 151460 (-3.1%) |
| avg_equation | 37686 vs 37865 (-0.5%) | 75807 vs 75730 (+0.1%) | 110285 vs 113595 (-2.9%) | 146701 vs 151460 (-3.1%) |
| avg_gated_lookup | 37683 vs 37865 (-0.5%) | 75590 vs 75730 (-0.2%) | 113426 vs 113595 (-0.1%) | 146701 vs 151460 (-3.1%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 82.3 points at 96.9% of the default cost, 3.1% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 82.3 points at 96.9% of the default cost, 3.1% under the budget it was given.
- `avg_gated_lookup` reverted to the default cell for every question at 1.00x: the predicted calibration margin did not clear 0.50 of its own SD.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_gsm8k_ouro_2_6b_think
# Table 1 -- gsm8k (ouro_2_6b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 237574 layer passes over 1219 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 21.7 |
| default_cell | n/a | n/a | n/a | 19.6 (91%) |
| default_at_budget | n/a | n/a | 16.8 | 21.8 |
| lookup | 57.9 | 65.1 | 65.1 | 65.1 |
| equation | 57.9 | 64.8 | 64.8 | 64.8 |
| equation_n30 | 57.9 | 64.8 | 64.8 | 64.8 |
| equation_n100 | 57.9 | 64.8 | 64.8 | 64.8 |
| gated_equation | 57.9 | 64.8 | 64.8 | 64.8 |
| avg_lookup | 61.7 | 65.1 | 65.1 | 65.1 |
| avg_equation | 61.2 | 64.8 | 64.8 | 64.8 |
| avg_gated_lookup | 61.7 | 65.1 | 65.1 | 65.1 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 59976 vs 59394 (+1.0%) | 72428 vs 118787 (-39.0%) | 72428 vs 178181 (-59.4%) | 72428 vs 237574 (-69.5%) |
| avg_equation | 58026 vs 59394 (-2.3%) | 91106 vs 118787 (-23.3%) | 91106 vs 178181 (-48.9%) | 91106 vs 237574 (-61.7%) |
| avg_gated_lookup | 59976 vs 59394 (+1.0%) | 72428 vs 118787 (-39.0%) | 72428 vs 178181 (-59.4%) | 72428 vs 237574 (-69.5%) |
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 65.1 points at 30.5% of the default cost, 39.0% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 65.1 points at 30.5% of the default cost, 59.4% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 65.1 points at 30.5% of the default cost, 69.5% under the budget it was given.
- `avg_equation` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 64.8 points at 38.3% of the default cost, 23.3% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 64.8 points at 38.3% of the default cost, 48.9% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 64.8 points at 38.3% of the default cost, 61.7% under the budget it was given.
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 65.1 points at 30.5% of the default cost, 39.0% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 65.1 points at 30.5% of the default cost, 59.4% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 65.1 points at 30.5% of the default cost, 69.5% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_hellaswag_huginn_0125
# Table 1 -- hellaswag (huginn_0125), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 116966 layer passes over 1900 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 34.4 |
| default_cell | n/a | n/a | n/a | 41.2 (51%) |
| default_at_budget | n/a | n/a | 57.1 (12%) | 34.9 (100%) |
| lookup | 27.8 | 39.1 | 39.4 | 40.3 |
| equation | 28.1 | 33.6 | 33.0 | 33.0 |
| equation_n30 | 28.1 | 33.6 | 33.0 | 33.0 |
| equation_n100 | 28.1 | 33.6 | 33.0 | 33.0 |
| gated_equation | 28.1 | 33.6 | 33.3 | 34.6 |
| avg_lookup | 33.8 | 39.4 | 39.9 | 40.3 |
| avg_equation | 31.3 | 33.0 | 33.0 | 33.0 |
| avg_gated_lookup | 33.8 | 39.4 | 39.9 | 40.3 |

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 26834 vs 29241 (-8.2%) | 56146 vs 58483 (-4.0%) | 87098 vs 87724 (-0.7%) | 102349 vs 116966 (-12.5%) |
| avg_equation | 25664 vs 29241 (-12.2%) | 59588 vs 58483 (+1.9%) | 62244 vs 87724 (-29.0%) | 62244 vs 116966 (-46.8%) |
| avg_gated_lookup | 26834 vs 29241 (-8.2%) | 56146 vs 58483 (-4.0%) | 87098 vs 87724 (-0.7%) | 102349 vs 116966 (-12.5%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 40.3 points at 87.5% of the default cost, 12.5% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 33.0 points at 53.2% of the default cost, 29.0% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 33.0 points at 53.2% of the default cost, 46.8% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 40.3 points at 87.5% of the default cost, 12.5% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_hellaswag_mcleish_llama32_r32
# Table 1 -- hellaswag (mcleish_llama32_r32), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 45831 layer passes over 1900 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 28.9 |
| default_cell | n/a | n/a | n/a | 32.4 (41%) |
| default_at_budget | n/a | n/a | 40.7 (16%) | 29.2 (99%) |
| lookup | 24.8 (99%) | 30.9 | 31.5 | 28.6 |
| equation | 24.8 (99%) | 26.4 | 26.5 | 29.1 |
| equation_n30 | 26.0 (99%) | 27.9 | 28.1 | 29.1 |
| equation_n100 | 24.8 (99%) | 26.4 | 26.5 | 29.1 |
| gated_equation | 24.8 (99%) | 26.4 | 27.4 | 29.1 |
| avg_lookup | 27.2 | 31.6 | 28.5 | 28.7 |
| avg_equation | 26.1 | 27.2 | 28.2 | 28.9 |
| avg_gated_lookup | 27.2 | 31.6 | 28.5 | 28.9 |

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 11323 vs 11458 (-1.2%) | 23027 vs 22916 (+0.5%) | 33768 vs 34373 (-1.8%) | 41852 vs 45831 (-8.7%) |
| avg_equation | 11251 vs 11458 (-1.8%) | 21453 vs 22916 (-6.4%) | 33876 vs 34373 (-1.4%) | 42685 vs 45831 (-6.9%) |
| avg_gated_lookup | 11323 vs 11458 (-1.2%) | 23027 vs 22916 (+0.5%) | 33768 vs 34373 (-1.8%) | 44835 vs 45831 (-2.2%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 28.7 points at 91.3% of the default cost, 8.7% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 28.9 points at 93.1% of the default cost, 6.9% under the budget it was given.
- `avg_gated_lookup` reverted to the default cell for every question at 1.00x: the predicted calibration margin did not clear 0.50 of its own SD.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_hellaswag_ouro_1_4b_base
# Table 1 -- hellaswag (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 94300 layer passes over 1900 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 57.4 |
| default_cell | n/a | n/a | n/a | 70.6 (4%) |
| default_at_budget | n/a | n/a | 63.6 (32%) | 57.6 |
| lookup | 34.7 | 56.9 | 65.4 | 65.4 |
| equation | 31.5 | 46.8 | 56.1 | 57.5 |
| equation_n30 | 31.5 | 46.8 | 56.4 | 56.3 |
| equation_n100 | 31.5 | 46.8 | 56.1 | 57.5 |
| gated_equation | 31.5 | 46.8 | 56.1 | 57.6 |
| avg_lookup | 39.8 | 61.5 | 65.4 | 65.4 |
| avg_equation | 35.5 | 49.7 | 56.8 | 57.4 |
| avg_gated_lookup | 39.8 | 61.5 | 65.4 | 65.4 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 22538 vs 23575 (-4.4%) | 47077 vs 47150 (-0.2%) | 55423 vs 70725 (-21.6%) | 55423 vs 94300 (-41.2%) |
| avg_equation | 22659 vs 23575 (-3.9%) | 46585 vs 47150 (-1.2%) | 70414 vs 70725 (-0.4%) | 94499 vs 94300 (+0.2%) |
| avg_gated_lookup | 22538 vs 23575 (-4.4%) | 47077 vs 47150 (-0.2%) | 55423 vs 70725 (-21.6%) | 55423 vs 94300 (-41.2%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 65.4 points at 58.8% of the default cost, 21.6% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 65.4 points at 58.8% of the default cost, 41.2% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 65.4 points at 58.8% of the default cost, 21.6% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 65.4 points at 58.8% of the default cost, 41.2% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_hellaswag_ouro_1_4b_think
# Table 1 -- hellaswag (ouro_1_4b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 145803 layer passes over 1900 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 74.5 |
| default_cell | n/a | n/a | n/a | 74.3 (81%) |
| default_at_budget | n/a | 69.4 (33%) | 72.8 | 74.5 |
| lookup | 38.3 | 76.9 | 76.3 | 76.3 |
| equation | 37.8 | 69.5 | 71.9 | 74.4 |
| equation_n30 | 37.8 | 69.6 | 71.9 | 71.9 |
| equation_n100 | 37.8 | 69.5 | 71.9 | 74.4 |
| gated_equation | 37.8 | 69.5 | 73.5 | 74.5 |
| avg_lookup | 54.5 | 76.7 | 76.3 | 76.3 |
| avg_equation | 56.8 | 73.8 | 73.4 | 74.4 |
| avg_gated_lookup | 54.5 | 76.7 | 76.3 | 76.3 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 36067 vs 36451 (-1.1%) | 73256 vs 72901 (+0.5%) | 76682 vs 109352 (-29.9%) | 76682 vs 145803 (-47.4%) |
| avg_equation | 36136 vs 36451 (-0.9%) | 74236 vs 72901 (+1.8%) | 107352 vs 109352 (-1.8%) | 131879 vs 145803 (-9.5%) |
| avg_gated_lookup | 36067 vs 36451 (-1.1%) | 73256 vs 72901 (+0.5%) | 76682 vs 109352 (-29.9%) | 76682 vs 145803 (-47.4%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 76.3 points at 52.6% of the default cost, 29.9% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 76.3 points at 52.6% of the default cost, 47.4% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 74.4 points at 90.5% of the default cost, 9.5% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 76.3 points at 52.6% of the default cost, 29.9% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 76.3 points at 52.6% of the default cost, 47.4% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_hellaswag_ouro_2_6b_base
# Table 1 -- hellaswag (ouro_2_6b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 170694 layer passes over 1900 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 76.4 |
| default_cell | n/a | n/a | n/a | 74.3 (31%) |
| default_at_budget | n/a | n/a | 76.3 (16%) | 76.3 (100%) |
| lookup | 32.1 (100%) | 66.4 | 81.8 | 81.8 |
| equation | 34.4 (100%) | 58.7 | 75.1 | 76.3 |
| equation_n30 | 34.4 (100%) | 58.7 | 81.7 | 76.3 |
| equation_n100 | 34.4 (100%) | 58.7 | 75.1 | 76.3 |
| gated_equation | 34.4 (100%) | 58.7 | 75.1 | 76.4 |
| avg_lookup | 33.9 | 69.4 | 82.2 | 81.8 |
| avg_equation | 35.6 | 60.8 | 74.9 | 76.3 |
| avg_gated_lookup | 33.9 | 69.4 | 82.2 | 81.8 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 40877 vs 42674 (-4.2%) | 85032 vs 85347 (-0.4%) | 127547 vs 128021 (-0.4%) | 147796 vs 170694 (-13.4%) |
| avg_equation | 40676 vs 42674 (-4.7%) | 84407 vs 85347 (-1.1%) | 127655 vs 128021 (-0.3%) | 159043 vs 170694 (-6.8%) |
| avg_gated_lookup | 40877 vs 42674 (-4.2%) | 85032 vs 85347 (-0.4%) | 127547 vs 128021 (-0.4%) | 147796 vs 170694 (-13.4%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 81.8 points at 86.6% of the default cost, 13.4% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 76.3 points at 93.2% of the default cost, 6.8% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 81.8 points at 86.6% of the default cost, 13.4% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_hellaswag_ouro_2_6b_think
# Table 1 -- hellaswag (ouro_2_6b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 280144 layer passes over 1900 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 81.2 |
| default_cell | n/a | n/a | n/a | 77.5 (32%) |
| default_at_budget | n/a | 74.9 (31%) | 81.3 | 81.4 |
| lookup | 40.5 | 80.7 | 79.8 | 79.8 |
| equation | 39.9 | 74.6 | 79.1 | 79.1 |
| equation_n30 | 39.9 | 74.6 | 74.2 | 74.2 |
| equation_n100 | 39.9 | 74.6 | 79.1 | 79.1 |
| gated_equation | 39.9 | 74.6 | 79.1 | 79.1 |
| avg_lookup | 64.4 | 79.5 | 79.8 | 79.8 |
| avg_equation | 64.6 | 74.2 | 79.1 | 79.1 |
| avg_gated_lookup | 64.4 | 79.5 | 79.8 | 79.8 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 69498 vs 70036 (-0.8%) | 143386 vs 140072 (+2.4%) | 149520 vs 210108 (-28.8%) | 149520 vs 280144 (-46.6%) |
| avg_equation | 69391 vs 70036 (-0.9%) | 137646 vs 140072 (-1.7%) | 200449 vs 210108 (-4.6%) | 200449 vs 280144 (-28.4%) |
| avg_gated_lookup | 69498 vs 70036 (-0.8%) | 143386 vs 140072 (+2.4%) | 149520 vs 210108 (-28.8%) | 149520 vs 280144 (-46.6%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 79.8 points at 53.4% of the default cost, 28.8% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 79.8 points at 53.4% of the default cost, 46.6% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 79.1 points at 71.6% of the default cost, 4.6% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 79.1 points at 71.6% of the default cost, 28.4% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 79.8 points at 53.4% of the default cost, 28.8% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 79.8 points at 53.4% of the default cost, 46.6% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_math500_huginn_0125
# Table 1 -- math500 (huginn_0125), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 224131 layer passes over 400 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 15.0 |
| default_cell | n/a | n/a | n/a | 17.1 (84%) |
| default_at_budget | n/a | n/a | 15.5 (98%) | 15.1 (99%) |
| lookup | 8.2 | 15.2 | 15.5 | 15.8 |
| equation | 7.2 | 13.5 | 15.5 | 15.0 |
| equation_n30 | 7.2 | 6.2 | 15.2 | 15.0 |
| equation_n100 | 7.2 | 13.5 | 15.5 | 15.0 |
| gated_equation | 7.2 | 13.5 | 15.2 | 15.0 |
| avg_lookup | 13.2 | 15.5 | 15.8 | 15.8 |
| avg_equation | 12.8 | 15.5 | 15.2 | 15.0 |
| avg_gated_lookup | 13.2 | 15.5 | 15.8 | 15.8 |

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 56995 vs 56033 (+1.7%) | 111911 vs 112065 (-0.1%) | 155466 vs 168098 (-7.5%) | 155466 vs 224131 (-30.6%) |
| avg_equation | 57531 vs 56033 (+2.7%) | 112240 vs 112065 (+0.2%) | 156677 vs 168098 (-6.8%) | 221433 vs 224131 (-1.2%) |
| avg_gated_lookup | 56995 vs 56033 (+1.7%) | 111911 vs 112065 (-0.1%) | 155466 vs 168098 (-7.5%) | 155466 vs 224131 (-30.6%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 15.8 points at 69.4% of the default cost, 7.5% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 15.8 points at 69.4% of the default cost, 30.6% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 15.0 points at 98.8% of the default cost, 1.2% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 15.8 points at 69.4% of the default cost, 7.5% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 15.8 points at 69.4% of the default cost, 30.6% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_math500_mcleish_llama32_r32
# Table 1 -- math500 (mcleish_llama32_r32), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 96379 layer passes over 400 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 30.2 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | 30.6 (99%) | 30.0 |
| lookup | 23.2 | 32.0 | 28.7 | 28.7 |
| equation | 26.2 | 30.8 | 30.8 | 30.8 |
| equation_n30 | 26.2 | 30.8 | 29.8 | 30.0 |
| equation_n100 | 26.2 | 30.8 | 30.8 | 30.8 |
| gated_equation | 26.2 | 30.8 | 30.8 | 30.8 |
| avg_lookup | 26.5 | 30.8 | 28.7 | 28.7 |
| avg_equation | 24.8 | 30.8 | 30.2 | 31.0 |
| avg_gated_lookup | 26.5 | 30.8 | 28.7 | 28.7 |

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 24717 vs 24095 (+2.6%) | 49327 vs 48189 (+2.4%) | 62558 vs 72284 (-13.5%) | 62558 vs 96379 (-35.1%) |
| avg_equation | 24581 vs 24095 (+2.0%) | 47988 vs 48189 (-0.4%) | 69440 vs 72284 (-3.9%) | 95287 vs 96379 (-1.1%) |
| avg_gated_lookup | 24717 vs 24095 (+2.6%) | 49327 vs 48189 (+2.4%) | 62558 vs 72284 (-13.5%) | 62558 vs 96379 (-35.1%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 28.7 points at 64.9% of the default cost, 13.5% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 28.7 points at 64.9% of the default cost, 35.1% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 28.7 points at 64.9% of the default cost, 13.5% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 28.7 points at 64.9% of the default cost, 35.1% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_math500_ouro_1_4b_base
# Table 1 -- math500 (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 178329 layer passes over 400 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 63.5 |
| default_cell | n/a | n/a | n/a | 67.5 (92%) |
| default_at_budget | n/a | n/a | 56.3 (99%) | 63.9 (100%) |
| lookup | 24.1 (100%) | 64.8 | 65.8 | 65.5 |
| equation | 25.6 (100%) | 64.2 | 66.2 | 66.0 |
| equation_n30 | 25.6 (100%) | 64.2 | 66.0 | 66.0 |
| equation_n100 | 25.6 (100%) | 64.2 | 66.2 | 66.0 |
| gated_equation | 25.6 (100%) | 64.2 | 66.2 | 66.0 |
| avg_lookup | 30.2 | 66.2 | 65.5 | 65.5 |
| avg_equation | 29.5 | 64.5 | 66.0 | 66.0 |
| avg_gated_lookup | 30.2 | 66.2 | 65.5 | 63.5 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 43608 vs 44582 (-2.2%) | 88144 vs 89164 (-1.1%) | 109654 vs 133746 (-18.0%) | 109654 vs 178329 (-38.5%) |
| avg_equation | 44948 vs 44582 (+0.8%) | 89988 vs 89164 (+0.9%) | 132753 vs 133746 (-0.7%) | 132753 vs 178329 (-25.6%) |
| avg_gated_lookup | 43608 vs 44582 (-2.2%) | 88144 vs 89164 (-1.1%) | 109654 vs 133746 (-18.0%) | 167182 vs 178329 (-6.3%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 65.5 points at 61.5% of the default cost, 18.0% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 65.5 points at 61.5% of the default cost, 38.5% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 66.0 points at 74.4% of the default cost, 25.6% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 65.5 points at 61.5% of the default cost, 18.0% under the budget it was given.
- `avg_gated_lookup` reverted to the default cell for every question at 1.00x: the predicted calibration margin did not clear 0.50 of its own SD.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_math500_ouro_1_4b_think
# Table 1 -- math500 (ouro_1_4b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 278580 layer passes over 400 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 89.8 |
| default_cell | n/a | n/a | n/a | 92.2 (90%) |
| default_at_budget | n/a | 36.9 (99%) | 75.8 | 88.0 |
| lookup | 32.2 | 76.8 | 86.2 | 89.8 |
| equation | 32.2 | 76.8 | 85.5 | 89.8 |
| equation_n30 | 32.2 | 76.8 | 77.0 | 77.0 |
| equation_n100 | 32.2 | 76.8 | 85.5 | 89.8 |
| gated_equation | 32.2 | 76.8 | 85.5 | 89.8 |
| avg_lookup | 58.8 | 77.5 | 87.2 | 89.8 |
| avg_equation | 59.0 | 76.8 | 80.5 | 89.8 |
| avg_gated_lookup | 58.8 | 77.5 | 87.2 | 89.8 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 72388 vs 69645 (+3.9%) | 135279 vs 139290 (-2.9%) | 210098 vs 208935 (+0.6%) | 270654 vs 278580 (-2.8%) |
| avg_equation | 71867 vs 69645 (+3.2%) | 139407 vs 139290 (+0.1%) | 212413 vs 208935 (+1.7%) | 270654 vs 278580 (-2.8%) |
| avg_gated_lookup | 72388 vs 69645 (+3.9%) | 135279 vs 139290 (-2.9%) | 210098 vs 208935 (+0.6%) | 270654 vs 278580 (-2.8%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 89.8 points at 97.2% of the default cost, 2.8% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 89.8 points at 97.2% of the default cost, 2.8% under the budget it was given.
- `avg_gated_lookup` reverted to the default cell for every question at 1.00x: the predicted calibration margin did not clear 0.50 of its own SD.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_math500_ouro_2_6b_base
# Table 1 -- math500 (ouro_2_6b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 338737 layer passes over 400 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 56.0 |
| default_cell | n/a | n/a | n/a | 56.6 (98%) |
| default_at_budget | n/a | n/a | 55.1 (98%) | 56.1 (100%) |
| lookup | 31.3 (100%) | 53.0 | 53.8 | 53.5 |
| equation | 34.8 (100%) | 53.0 | 52.5 | 55.8 |
| equation_n30 | 34.8 (100%) | 53.0 | 52.5 | 52.5 |
| equation_n100 | 34.8 (100%) | 53.0 | 52.5 | 55.8 |
| gated_equation | 34.8 (100%) | 53.0 | 53.2 | 56.2 |
| avg_lookup | 35.2 | 53.8 | 53.5 | 53.5 |
| avg_equation | 36.8 | 52.5 | 54.5 | 56.0 |
| avg_gated_lookup | 35.2 | 53.8 | 53.5 | 56.0 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 83347 vs 84684 (-1.6%) | 170761 vs 169369 (+0.8%) | 181071 vs 254053 (-28.7%) | 181071 vs 338737 (-46.5%) |
| avg_equation | 85709 vs 84684 (+1.2%) | 167582 vs 169369 (-1.1%) | 258292 vs 254053 (+1.7%) | 290726 vs 338737 (-14.2%) |
| avg_gated_lookup | 83347 vs 84684 (-1.6%) | 170761 vs 169369 (+0.8%) | 181071 vs 254053 (-28.7%) | 290726 vs 338737 (-14.2%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 53.5 points at 53.5% of the default cost, 28.7% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 53.5 points at 53.5% of the default cost, 46.5% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 56.0 points at 85.8% of the default cost, 14.2% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 53.5 points at 53.5% of the default cost, 28.7% under the budget it was given.
- `avg_gated_lookup` reverted to the default cell for every question at 1.00x: the predicted calibration margin did not clear 0.50 of its own SD.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_math500_ouro_2_6b_think
# Table 1 -- math500 (ouro_2_6b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 563241 layer passes over 400 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 91.2 |
| default_cell | n/a | n/a | n/a | 92.8 (93%) |
| default_at_budget | n/a | 41.7 (99%) | 75.8 | 90.0 |
| lookup | 44.2 | 78.8 | 83.8 | 90.0 |
| equation | 44.2 | 78.8 | 87.8 | 91.5 |
| equation_n30 | 44.2 | 78.8 | 81.8 | 89.8 |
| equation_n100 | 44.2 | 78.8 | 87.8 | 91.5 |
| gated_equation | 44.2 | 78.8 | 87.8 | 91.5 |
| avg_lookup | 51.0 | 79.8 | 85.0 | 91.2 |
| avg_equation | 48.2 | 81.2 | 84.5 | 91.2 |
| avg_gated_lookup | 51.0 | 79.8 | 85.0 | 91.2 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 134887 vs 140810 (-4.2%) | 282470 vs 281621 (+0.3%) | 438666 vs 422431 (+3.8%) | 537649 vs 563241 (-4.5%) |
| avg_equation | 143080 vs 140810 (+1.6%) | 279695 vs 281621 (-0.7%) | 431373 vs 422431 (+2.1%) | 537649 vs 563241 (-4.5%) |
| avg_gated_lookup | 134887 vs 140810 (-4.2%) | 282470 vs 281621 (+0.3%) | 438666 vs 422431 (+3.8%) | 537649 vs 563241 (-4.5%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 91.2 points at 95.5% of the default cost, 4.5% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 91.2 points at 95.5% of the default cost, 4.5% under the budget it was given.
- `avg_gated_lookup` reverted to the default cell for every question at 1.00x: the predicted calibration margin did not clear 0.50 of its own SD.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_mmlu_huginn_0125
# Table 1 -- mmlu (huginn_0125), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 85934 layer passes over 1900 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 36.4 |
| default_cell | n/a | n/a | n/a | 45.3 (21%) |
| default_at_budget | n/a | n/a | 39.8 (71%) | 37.4 (92%) |
| lookup | 24.8 | 35.5 | 35.8 | 35.8 |
| equation | 24.3 | 35.2 | 35.4 | 35.5 |
| equation_n30 | 24.3 | 35.2 | 35.4 | 35.5 |
| equation_n100 | 24.3 | 35.2 | 35.4 | 35.5 |
| gated_equation | 24.3 | 35.2 | 35.4 | 35.5 |
| avg_lookup | 33.3 | 35.8 | 35.8 | 35.8 |
| avg_equation | 33.3 | 35.9 | 35.5 | 35.5 |
| avg_gated_lookup | 33.3 | 35.8 | 35.8 | 35.8 |

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 22314 vs 21483 (+3.9%) | 36262 vs 42967 (-15.6%) | 36262 vs 64450 (-43.7%) | 36262 vs 85934 (-57.8%) |
| avg_equation | 22314 vs 21483 (+3.9%) | 42165 vs 42967 (-1.9%) | 48397 vs 64450 (-24.9%) | 48397 vs 85934 (-43.7%) |
| avg_gated_lookup | 22314 vs 21483 (+3.9%) | 36262 vs 42967 (-15.6%) | 36262 vs 64450 (-43.7%) | 36262 vs 85934 (-57.8%) |
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 35.8 points at 42.2% of the default cost, 15.6% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 35.8 points at 42.2% of the default cost, 43.7% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 35.8 points at 42.2% of the default cost, 57.8% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 35.5 points at 56.3% of the default cost, 24.9% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 35.5 points at 56.3% of the default cost, 43.7% under the budget it was given.
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 35.8 points at 42.2% of the default cost, 15.6% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 35.8 points at 42.2% of the default cost, 43.7% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 35.8 points at 42.2% of the default cost, 57.8% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_mmlu_mcleish_llama32_r32
# Table 1 -- mmlu (mcleish_llama32_r32), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 40492 layer passes over 1900 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 37.3 |
| default_cell | n/a | n/a | n/a | 39.4 (83%) |
| default_at_budget | n/a | n/a | 39.1 (86%) | 38.1 (98%) |
| lookup | 26.4 (98%) | 36.1 | 36.7 | 36.7 |
| equation | 28.2 (98%) | 36.8 | 36.8 | 36.6 |
| equation_n30 | 32.9 (98%) | 36.4 | 36.8 | 36.6 |
| equation_n100 | 28.2 (98%) | 36.8 | 36.8 | 36.6 |
| gated_equation | 28.2 (98%) | 36.8 | 36.8 | 36.6 |
| avg_lookup | 32.5 | 36.7 | 36.7 | 36.7 |
| avg_equation | 32.2 | 36.9 | 36.6 | 36.6 |
| avg_gated_lookup | 32.5 | 36.7 | 36.7 | 36.7 |

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 10018 vs 10123 (-1.0%) | 16424 vs 20246 (-18.9%) | 16424 vs 30369 (-45.9%) | 16424 vs 40492 (-59.4%) |
| avg_equation | 9951 vs 10123 (-1.7%) | 20235 vs 20246 (-0.1%) | 25026 vs 30369 (-17.6%) | 25026 vs 40492 (-38.2%) |
| avg_gated_lookup | 10018 vs 10123 (-1.0%) | 16424 vs 20246 (-18.9%) | 16424 vs 30369 (-45.9%) | 16424 vs 40492 (-59.4%) |
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 40.6% of the default cost, 18.9% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 40.6% of the default cost, 45.9% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 40.6% of the default cost, 59.4% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 36.6 points at 61.8% of the default cost, 17.6% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 36.6 points at 61.8% of the default cost, 38.2% under the budget it was given.
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 40.6% of the default cost, 18.9% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 40.6% of the default cost, 45.9% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 36.7 points at 40.6% of the default cost, 59.4% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_mmlu_ouro_1_4b_base
# Table 1 -- mmlu (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 58295 layer passes over 1900 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 68.7 |
| default_cell | n/a | n/a | n/a | 72.9 (70%) |
| default_at_budget | n/a | n/a | 74.4 (38%) | 70.3 (88%) |
| lookup | 41.2 (88%) | 56.2 | 66.0 | 67.2 |
| equation | 41.4 (88%) | 58.3 | 64.5 | 65.9 |
| equation_n30 | 41.4 (88%) | 58.3 | 64.6 | 66.1 |
| equation_n100 | 41.4 (88%) | 58.3 | 64.5 | 65.9 |
| gated_equation | 41.4 (88%) | 58.3 | 64.5 | 68.2 |
| avg_lookup | 43.2 | 61.4 | 65.7 | 67.7 |
| avg_equation | 43.9 | 61.5 | 66.0 | 65.8 |
| avg_gated_lookup | 43.2 | 61.4 | 65.7 | 67.7 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 13986 vs 14574 (-4.0%) | 28834 vs 29148 (-1.1%) | 43006 vs 43721 (-1.6%) | 47839 vs 58295 (-17.9%) |
| avg_equation | 14186 vs 14574 (-2.7%) | 28899 vs 29148 (-0.9%) | 43315 vs 43721 (-0.9%) | 48721 vs 58295 (-16.4%) |
| avg_gated_lookup | 13986 vs 14574 (-4.0%) | 28834 vs 29148 (-1.1%) | 43006 vs 43721 (-1.6%) | 47839 vs 58295 (-17.9%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 67.7 points at 82.1% of the default cost, 17.9% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 65.8 points at 83.6% of the default cost, 16.4% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 67.7 points at 82.1% of the default cost, 17.9% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_mmlu_ouro_1_4b_think
# Table 1 -- mmlu (ouro_1_4b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 134109 layer passes over 1900 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 73.7 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 65.9 (95%) | 70.7 | 73.7 |
| lookup | 58.4 | 70.6 | 72.5 | 73.5 |
| equation | 56.9 | 71.7 | 71.3 | 73.7 |
| equation_n30 | 55.9 | 68.3 | 72.7 | 73.7 |
| equation_n100 | 56.9 | 71.7 | 71.3 | 73.7 |
| gated_equation | 56.9 | 71.7 | 71.3 | 73.7 |
| avg_lookup | 63.8 | 70.3 | 72.8 | 73.5 |
| avg_equation | 63.4 | 71.6 | 73.3 | 73.6 |
| avg_gated_lookup | 63.8 | 70.3 | 72.8 | 73.5 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 33251 vs 33527 (-0.8%) | 67868 vs 67055 (+1.2%) | 98907 vs 100582 (-1.7%) | 135002 vs 134109 (+0.7%) |
| avg_equation | 33052 vs 33527 (-1.4%) | 66523 vs 67055 (-0.8%) | 100635 vs 100582 (+0.1%) | 133389 vs 134109 (-0.5%) |
| avg_gated_lookup | 33251 vs 33527 (-0.8%) | 67868 vs 67055 (+1.2%) | 98907 vs 100582 (-1.7%) | 135002 vs 134109 (+0.7%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_mmlu_ouro_2_6b_base
# Table 1 -- mmlu (ouro_2_6b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 118165 layer passes over 1900 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 74.6 |
| default_cell | n/a | n/a | n/a | 76.9 (82%) |
| default_at_budget | n/a | n/a | 79.9 (42%) | 76.4 (90%) |
| lookup | 52.3 (90%) | 65.9 | 73.2 | 74.8 |
| equation | 51.7 (90%) | 65.9 | 72.5 | 74.3 |
| equation_n30 | 51.7 (90%) | 65.9 | 68.5 | 73.4 |
| equation_n100 | 51.7 (90%) | 65.9 | 72.5 | 74.3 |
| gated_equation | 51.7 (90%) | 65.9 | 72.8 | 74.4 |
| avg_lookup | 55.7 | 69.3 | 73.2 | 74.6 |
| avg_equation | 54.8 | 68.2 | 72.3 | 74.6 |
| avg_gated_lookup | 55.7 | 69.3 | 73.2 | 74.6 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 28196 vs 29541 (-4.6%) | 58548 vs 59082 (-0.9%) | 87557 vs 88623 (-1.2%) | 107117 vs 118165 (-9.3%) |
| avg_equation | 28336 vs 29541 (-4.1%) | 58279 vs 59082 (-1.4%) | 87448 vs 88623 (-1.3%) | 107117 vs 118165 (-9.3%) |
| avg_gated_lookup | 28196 vs 29541 (-4.6%) | 58548 vs 59082 (-0.9%) | 87557 vs 88623 (-1.2%) | 107117 vs 118165 (-9.3%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 74.6 points at 90.7% of the default cost, 9.3% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 74.6 points at 90.7% of the default cost, 9.3% under the budget it was given.
- `avg_gated_lookup` reverted to the default cell for every question at 1.00x: the predicted calibration margin did not clear 0.50 of its own SD.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_mmlu_ouro_2_6b_think
# Table 1 -- mmlu (ouro_2_6b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 242015 layer passes over 1900 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 80.1 |
| default_cell | n/a | n/a | n/a | 82.6 (54%) |
| default_at_budget | n/a | 75.2 (90%) | 77.6 | 79.7 |
| lookup | 65.9 | 73.9 | 80.8 | 81.1 |
| equation | 46.3 | 75.3 | 81.8 | 82.0 |
| equation_n30 | 46.3 | 75.1 | 81.8 | 82.0 |
| equation_n100 | 46.3 | 75.3 | 81.8 | 82.0 |
| gated_equation | 46.3 | 75.4 | 81.8 | 82.0 |
| avg_lookup | 70.1 | 78.1 | 81.1 | 81.1 |
| avg_equation | 64.6 | 75.6 | 82.0 | 82.0 |
| avg_gated_lookup | 70.1 | 78.1 | 81.1 | 81.1 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 59953 vs 60504 (-0.9%) | 118045 vs 121007 (-2.4%) | 150903 vs 181511 (-16.9%) | 150903 vs 242015 (-37.6%) |
| avg_equation | 59772 vs 60504 (-1.2%) | 118367 vs 121007 (-2.2%) | 174024 vs 181511 (-4.1%) | 174024 vs 242015 (-28.1%) |
| avg_gated_lookup | 59953 vs 60504 (-0.9%) | 118045 vs 121007 (-2.4%) | 150903 vs 181511 (-16.9%) | 150903 vs 242015 (-37.6%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 81.1 points at 62.4% of the default cost, 16.9% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 81.1 points at 62.4% of the default cost, 37.6% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 82.0 points at 71.9% of the default cost, 4.1% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 82.0 points at 71.9% of the default cost, 28.1% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 81.1 points at 62.4% of the default cost, 16.9% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 81.1 points at 62.4% of the default cost, 37.6% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_strategyqa_huginn_0125
# Table 1 -- strategyqa (huginn_0125), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 119422 layer passes over 2190 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 55.5 |
| default_cell | n/a | n/a | n/a | 55.5 |
| default_at_budget | n/a | 56.3 | 56.4 | 55.5 |
| lookup | 56.4 | 56.0 | 56.0 | 56.0 |
| equation | 56.3 | 56.3 | 56.3 | 55.5 |
| equation_n30 | 56.3 | 56.4 | 56.3 | 56.3 |
| equation_n100 | 56.3 | 56.3 | 56.3 | 55.5 |
| gated_equation | 56.3 | 56.3 | 56.4 | 55.5 |
| avg_lookup | 53.3 | 56.0 | 56.0 | 56.0 |
| avg_equation | 56.5 | 55.9 | 56.0 | 55.5 |
| avg_gated_lookup | 53.3 | 56.0 | 56.0 | 56.0 |

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 23210 vs 29855 (-22.3%) | 53070 vs 59711 (-11.1%) | 53070 vs 89566 (-40.7%) | 53070 vs 119422 (-55.6%) |
| avg_equation | 29384 vs 29855 (-1.6%) | 59822 vs 59711 (+0.2%) | 79169 vs 89566 (-11.6%) | 116097 vs 119422 (-2.8%) |
| avg_gated_lookup | 23210 vs 29855 (-22.3%) | 53070 vs 59711 (-11.1%) | 53070 vs 89566 (-40.7%) | 53070 vs 119422 (-55.6%) |
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 56.0 points at 44.4% of the default cost, 11.1% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 56.0 points at 44.4% of the default cost, 40.7% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 56.0 points at 44.4% of the default cost, 55.6% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 55.5 points at 97.2% of the default cost, 2.8% under the budget it was given.
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 56.0 points at 44.4% of the default cost, 11.1% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 56.0 points at 44.4% of the default cost, 40.7% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 56.0 points at 44.4% of the default cost, 55.6% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_strategyqa_mcleish_llama32_r32
# Table 1 -- strategyqa (mcleish_llama32_r32), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 59637 layer passes over 2190 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 50.3 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 51.0 | 50.8 | 50.8 |
| lookup | 52.3 | 52.3 | 52.3 | 52.3 |
| equation | 50.0 | 49.9 | 49.5 | 49.5 |
| equation_n30 | 50.0 | 49.9 | 50.8 | 50.8 |
| equation_n100 | 50.0 | 49.9 | 49.5 | 49.5 |
| gated_equation | 50.0 | 49.9 | 49.5 | 49.5 |
| avg_lookup | 52.3 | 52.3 | 52.3 | 52.3 |
| avg_equation | 50.3 | 49.5 | 49.5 | 49.5 |
| avg_gated_lookup | 52.3 | 52.3 | 52.3 | 52.3 |

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 7768 vs 14909 (-47.9%) | 7768 vs 29819 (-73.9%) | 7768 vs 44728 (-82.6%) | 7768 vs 59637 (-87.0%) |
| avg_equation | 14714 vs 14909 (-1.3%) | 28062 vs 29819 (-5.9%) | 36404 vs 44728 (-18.6%) | 36404 vs 59637 (-39.0%) |
| avg_gated_lookup | 7768 vs 14909 (-47.9%) | 7768 vs 29819 (-73.9%) | 7768 vs 44728 (-82.6%) | 7768 vs 59637 (-87.0%) |
- `avg_lookup` at 0.25x: the multiplier is 0, so the budget never binds. The row is the same 52.3 points at 13.0% of the default cost, 47.9% under the budget it was given.
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 52.3 points at 13.0% of the default cost, 73.9% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 52.3 points at 13.0% of the default cost, 82.6% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 52.3 points at 13.0% of the default cost, 87.0% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 49.5 points at 61.0% of the default cost, 18.6% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 49.5 points at 61.0% of the default cost, 39.0% under the budget it was given.
- `avg_gated_lookup` at 0.25x: the multiplier is 0, so the budget never binds. The row is the same 52.3 points at 13.0% of the default cost, 47.9% under the budget it was given.
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 52.3 points at 13.0% of the default cost, 73.9% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 52.3 points at 13.0% of the default cost, 82.6% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 52.3 points at 13.0% of the default cost, 87.0% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_strategyqa_ouro_1_4b_base
# Table 1 -- strategyqa (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 58978 layer passes over 2190 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 66.3 |
| default_cell | n/a | n/a | n/a | 66.3 |
| default_at_budget | n/a | n/a | 66.4 | 66.3 |
| lookup | 55.6 | 63.9 | 65.8 | 65.8 |
| equation | 54.0 | 66.6 | 66.4 | 66.4 |
| equation_n30 | 55.3 | 66.6 | 66.4 | 66.4 |
| equation_n100 | 54.0 | 66.6 | 66.4 | 66.4 |
| gated_equation | 54.0 | 66.6 | 66.4 | 66.3 |
| avg_lookup | 60.0 | 64.3 | 65.8 | 65.8 |
| avg_equation | 55.4 | 67.2 | 66.4 | 66.4 |
| avg_gated_lookup | 60.0 | 64.3 | 65.8 | 65.8 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 13935 vs 14744 (-5.5%) | 28500 vs 29489 (-3.4%) | 37381 vs 44233 (-15.5%) | 37381 vs 58978 (-36.6%) |
| avg_equation | 13226 vs 14744 (-10.3%) | 29138 vs 29489 (-1.2%) | 41498 vs 44233 (-6.2%) | 41498 vs 58978 (-29.6%) |
| avg_gated_lookup | 13935 vs 14744 (-5.5%) | 28500 vs 29489 (-3.4%) | 37381 vs 44233 (-15.5%) | 37381 vs 58978 (-36.6%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 65.8 points at 63.4% of the default cost, 15.5% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 65.8 points at 63.4% of the default cost, 36.6% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 66.4 points at 70.4% of the default cost, 6.2% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 66.4 points at 70.4% of the default cost, 29.6% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 65.8 points at 63.4% of the default cost, 15.5% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 65.8 points at 63.4% of the default cost, 36.6% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_strategyqa_ouro_1_4b_think
# Table 1 -- strategyqa (ouro_1_4b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 109309 layer passes over 2190 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 72.5 |
| default_cell | n/a | n/a | n/a | 72.5 |
| default_at_budget | n/a | 69.5 | 72.2 | 72.5 |
| lookup | 61.0 | 69.5 | 69.5 | 69.5 |
| equation | 61.0 | 69.4 | 71.2 | 71.2 |
| equation_n30 | 61.0 | 69.4 | 71.2 | 71.2 |
| equation_n100 | 61.0 | 69.4 | 71.2 | 71.2 |
| gated_equation | 61.0 | 69.4 | 71.2 | 72.5 |
| avg_lookup | 62.3 | 69.5 | 69.5 | 69.5 |
| avg_equation | 61.3 | 70.7 | 71.2 | 71.2 |
| avg_gated_lookup | 62.3 | 69.5 | 69.5 | 72.5 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 25330 vs 27327 (-7.3%) | 49399 vs 54655 (-9.6%) | 49399 vs 81982 (-39.7%) | 49399 vs 109309 (-54.8%) |
| avg_equation | 26098 vs 27327 (-4.5%) | 52772 vs 54655 (-3.4%) | 71784 vs 81982 (-12.4%) | 71784 vs 109309 (-34.3%) |
| avg_gated_lookup | 25330 vs 27327 (-7.3%) | 49399 vs 54655 (-9.6%) | 49399 vs 81982 (-39.7%) | 107291 vs 109309 (-1.8%) |
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 69.5 points at 45.2% of the default cost, 9.6% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 69.5 points at 45.2% of the default cost, 39.7% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 69.5 points at 45.2% of the default cost, 54.8% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 71.2 points at 65.7% of the default cost, 12.4% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 71.2 points at 65.7% of the default cost, 34.3% under the budget it was given.
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 69.5 points at 45.2% of the default cost, 9.6% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 69.5 points at 45.2% of the default cost, 39.7% under the budget it was given.
- `avg_gated_lookup` reverted to the default cell for every question at 1.00x: the predicted calibration margin did not clear 0.50 of its own SD.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_strategyqa_ouro_2_6b_base
# Table 1 -- strategyqa (ouro_2_6b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 99332 layer passes over 2190 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 74.7 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | 73.1 (100%) | 74.7 |
| lookup | 59.5 | 66.9 | 73.6 | 75.0 |
| equation | 59.1 | 69.7 | 73.7 | 74.7 |
| equation_n30 | 59.1 | 66.4 | 73.3 | 74.7 |
| equation_n100 | 59.1 | 69.7 | 73.7 | 74.7 |
| gated_equation | 59.1 | 69.7 | 73.3 | 74.7 |
| avg_lookup | 61.1 | 68.1 | 73.4 | 75.0 |
| avg_equation | 61.1 | 70.9 | 74.1 | 74.7 |
| avg_gated_lookup | 61.1 | 68.1 | 73.4 | 75.0 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 21870 vs 24833 (-11.9%) | 46509 vs 49666 (-6.4%) | 73453 vs 74499 (-1.4%) | 82364 vs 99332 (-17.1%) |
| avg_equation | 23649 vs 24833 (-4.8%) | 48020 vs 49666 (-3.3%) | 72569 vs 74499 (-2.6%) | 98880 vs 99332 (-0.5%) |
| avg_gated_lookup | 21870 vs 24833 (-11.9%) | 46509 vs 49666 (-6.4%) | 73453 vs 74499 (-1.4%) | 82364 vs 99332 (-17.1%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 75.0 points at 82.9% of the default cost, 17.1% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 75.0 points at 82.9% of the default cost, 17.1% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_strategyqa_ouro_2_6b_think
# Table 1 -- strategyqa (ouro_2_6b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 194662 layer passes over 2190 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 77.8 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 74.6 | 77.9 | 77.9 |
| lookup | 59.5 | 74.9 | 74.9 | 74.9 |
| equation | 59.9 | 77.4 | 78.8 | 77.8 |
| equation_n30 | 59.9 | 77.4 | 77.9 | 77.8 |
| equation_n100 | 59.9 | 77.4 | 78.8 | 77.8 |
| gated_equation | 59.9 | 77.4 | 78.8 | 77.9 |
| avg_lookup | 66.4 | 74.9 | 74.9 | 74.9 |
| avg_equation | 66.4 | 77.4 | 78.5 | 77.8 |
| avg_gated_lookup | 66.4 | 74.9 | 74.9 | 74.9 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 47159 vs 48665 (-3.1%) | 80365 vs 97331 (-17.4%) | 80365 vs 145996 (-45.0%) | 80365 vs 194662 (-58.7%) |
| avg_equation | 47159 vs 48665 (-3.1%) | 92483 vs 97331 (-5.0%) | 141891 vs 145996 (-2.8%) | 177957 vs 194662 (-8.6%) |
| avg_gated_lookup | 47159 vs 48665 (-3.1%) | 80365 vs 97331 (-17.4%) | 80365 vs 145996 (-45.0%) | 80365 vs 194662 (-58.7%) |
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 74.9 points at 41.3% of the default cost, 17.4% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 74.9 points at 41.3% of the default cost, 45.0% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 74.9 points at 41.3% of the default cost, 58.7% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 77.8 points at 91.4% of the default cost, 8.6% under the budget it was given.
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 74.9 points at 41.3% of the default cost, 17.4% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 74.9 points at 41.3% of the default cost, 45.0% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 74.9 points at 41.3% of the default cost, 58.7% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_svamp_huginn_0125
# Table 1 -- svamp (huginn_0125), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 84875 layer passes over 200 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 44.5 |
| default_cell | n/a | n/a | n/a | 58.8 (40%) |
| default_at_budget | n/a | n/a | n/a | 40.0 |
| lookup | 4.5 | 27.5 | 39.5 | 39.5 |
| equation | 3.5 | 28.0 | 39.5 | 41.0 |
| equation_n30 | 3.5 | 20.0 | 20.0 | 20.0 |
| equation_n100 | 3.5 | 28.0 | 39.5 | 41.0 |
| gated_equation | 3.5 | 28.0 | 39.5 | 41.0 |
| avg_lookup | 18.0 | 38.0 | 39.5 | 39.5 |
| avg_equation | 19.5 | 38.0 | 41.5 | 45.0 |
| avg_gated_lookup | 18.0 | 38.0 | 39.5 | 39.5 |

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 21280 vs 21219 (+0.3%) | 42712 vs 42438 (+0.6%) | 43791 vs 63657 (-31.2%) | 43791 vs 84875 (-48.4%) |
| avg_equation | 21562 vs 21219 (+1.6%) | 42728 vs 42438 (+0.7%) | 67841 vs 63657 (+6.6%) | 83838 vs 84875 (-1.2%) |
| avg_gated_lookup | 21280 vs 21219 (+0.3%) | 42712 vs 42438 (+0.6%) | 43791 vs 63657 (-31.2%) | 43791 vs 84875 (-48.4%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 39.5 points at 51.6% of the default cost, 31.2% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 39.5 points at 51.6% of the default cost, 48.4% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 39.5 points at 51.6% of the default cost, 31.2% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 39.5 points at 51.6% of the default cost, 48.4% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_svamp_mcleish_llama32_r32
# Table 1 -- svamp (mcleish_llama32_r32), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 32123 layer passes over 200 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 69.0 |
| default_cell | n/a | n/a | n/a | 77.2 (50%) |
| default_at_budget | n/a | n/a | n/a | 56.5 |
| lookup | 22.5 | 33.0 | 62.0 | 66.5 |
| equation | 24.0 | 39.0 | 63.0 | 67.0 |
| equation_n30 | 24.0 | 39.0 | 63.0 | 67.0 |
| equation_n100 | 24.0 | 39.0 | 63.0 | 67.0 |
| gated_equation | 24.0 | 39.0 | 63.0 | 67.0 |
| avg_lookup | 26.5 | 53.5 | 66.5 | 68.5 |
| avg_equation | 25.5 | 56.5 | 67.0 | 68.5 |
| avg_gated_lookup | 26.5 | 53.5 | 66.5 | 68.5 |

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 8144 vs 8031 (+1.4%) | 16543 vs 16062 (+3.0%) | 25213 vs 24092 (+4.7%) | 32048 vs 32123 (-0.2%) |
| avg_equation | 7994 vs 8031 (-0.5%) | 16737 vs 16062 (+4.2%) | 25471 vs 24092 (+5.7%) | 32062 vs 32123 (-0.2%) |
| avg_gated_lookup | 8144 vs 8031 (+1.4%) | 16543 vs 16062 (+3.0%) | 25213 vs 24092 (+4.7%) | 32048 vs 32123 (-0.2%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_svamp_ouro_1_4b_base
# Table 1 -- svamp (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 65870 layer passes over 200 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 86.5 |
| default_cell | n/a | n/a | n/a | 92.4 (33%) |
| default_at_budget | n/a | n/a | n/a | 75.0 |
| lookup | 30.0 | 62.5 | 76.5 | 84.0 |
| equation | 33.5 | 62.5 | 77.0 | 86.5 |
| equation_n30 | 33.5 | 62.0 | 75.0 | 86.5 |
| equation_n100 | 33.5 | 62.5 | 77.0 | 86.5 |
| gated_equation | 33.5 | 62.5 | 77.0 | 86.5 |
| avg_lookup | 35.5 | 70.5 | 84.0 | 84.0 |
| avg_equation | 34.5 | 71.0 | 85.0 | 86.0 |
| avg_gated_lookup | 35.5 | 70.5 | 84.0 | 84.0 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 16356 vs 16467 (-0.7%) | 32711 vs 32935 (-0.7%) | 49213 vs 49402 (-0.4%) | 49643 vs 65870 (-24.6%) |
| avg_equation | 16379 vs 16467 (-0.5%) | 32782 vs 32935 (-0.5%) | 49282 vs 49402 (-0.2%) | 65770 vs 65870 (-0.2%) |
| avg_gated_lookup | 16356 vs 16467 (-0.7%) | 32711 vs 32935 (-0.7%) | 49213 vs 49402 (-0.4%) | 49643 vs 65870 (-24.6%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 84.0 points at 75.4% of the default cost, 24.6% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 84.0 points at 75.4% of the default cost, 24.6% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_svamp_ouro_1_4b_think
# Table 1 -- svamp (ouro_1_4b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 129897 layer passes over 200 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 89.5 |
| default_cell | n/a | n/a | n/a | 93.1 (50%) |
| default_at_budget | n/a | 59.5 (98%) | 88.5 | 89.5 |
| lookup | 47.5 | 87.0 | 87.5 | 87.5 |
| equation | 52.5 | 86.5 | 87.5 | 87.5 |
| equation_n30 | 52.5 | 86.5 | 87.5 | 87.5 |
| equation_n100 | 52.5 | 86.5 | 87.5 | 87.5 |
| gated_equation | 52.5 | 86.5 | 87.5 | 87.5 |
| avg_lookup | 61.5 | 88.0 | 87.5 | 87.5 |
| avg_equation | 64.0 | 87.0 | 87.5 | 87.5 |
| avg_gated_lookup | 61.5 | 88.0 | 87.5 | 87.5 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 34920 vs 32474 (+7.5%) | 67981 vs 64949 (+4.7%) | 90826 vs 97423 (-6.8%) | 90826 vs 129897 (-30.1%) |
| avg_equation | 34470 vs 32474 (+6.1%) | 65774 vs 64949 (+1.3%) | 90826 vs 97423 (-6.8%) | 90826 vs 129897 (-30.1%) |
| avg_gated_lookup | 34920 vs 32474 (+7.5%) | 67981 vs 64949 (+4.7%) | 90826 vs 97423 (-6.8%) | 90826 vs 129897 (-30.1%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 87.5 points at 69.9% of the default cost, 6.8% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 87.5 points at 69.9% of the default cost, 30.1% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 87.5 points at 69.9% of the default cost, 6.8% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 87.5 points at 69.9% of the default cost, 30.1% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 87.5 points at 69.9% of the default cost, 6.8% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 87.5 points at 69.9% of the default cost, 30.1% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_svamp_ouro_2_6b_base
# Table 1 -- svamp (ouro_2_6b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 131236 layer passes over 200 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 83.0 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | n/a | 72.0 |
| lookup | 40.0 | 68.0 | 76.0 | 82.5 |
| equation | 40.5 | 67.5 | 76.5 | 82.5 |
| equation_n30 | 40.5 | 68.5 | 76.5 | 83.5 |
| equation_n100 | 40.5 | 67.5 | 76.5 | 82.5 |
| gated_equation | 40.5 | 67.5 | 76.5 | 82.5 |
| avg_lookup | 47.0 | 79.5 | 82.5 | 82.5 |
| avg_equation | 37.0 | 80.0 | 83.0 | 82.5 |
| avg_gated_lookup | 47.0 | 79.5 | 82.5 | 82.5 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 32852 vs 32809 (+0.1%) | 65206 vs 65618 (-0.6%) | 97963 vs 98427 (-0.5%) | 98646 vs 131236 (-24.8%) |
| avg_equation | 32554 vs 32809 (-0.8%) | 65209 vs 65618 (-0.6%) | 98721 vs 98427 (+0.3%) | 99958 vs 131236 (-23.8%) |
| avg_gated_lookup | 32852 vs 32809 (+0.1%) | 65206 vs 65618 (-0.6%) | 97963 vs 98427 (-0.5%) | 98646 vs 131236 (-24.8%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 82.5 points at 75.2% of the default cost, 24.8% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 82.5 points at 76.2% of the default cost, 23.8% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 82.5 points at 75.2% of the default cost, 24.8% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v2_svamp_ouro_2_6b_think
# Table 1 -- svamp (ouro_2_6b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 249394 layer passes over 200 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 7.0 |
| default_cell | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 5.6 (45%) | 12.5 | 6.5 |
| lookup | 68.5 | 68.5 | 68.5 | 68.5 |
| equation | 68.5 | 68.5 | 68.5 | 68.5 |
| equation_n30 | 68.5 | 68.5 | 68.5 | 68.5 |
| equation_n100 | 68.5 | 68.5 | 68.5 | 68.5 |
| gated_equation | 68.5 | 68.5 | 68.5 | 68.5 |
| avg_lookup | 68.5 | 68.5 | 68.5 | 68.5 |
| avg_equation | 68.5 | 68.5 | 68.5 | 68.5 |
| avg_gated_lookup | 68.5 | 68.5 | 68.5 | 68.5 |

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 56160 vs 62348 (-9.9%) | 56160 vs 124697 (-55.0%) | 56160 vs 187045 (-70.0%) | 56160 vs 249394 (-77.5%) |
| avg_equation | 59280 vs 62348 (-4.9%) | 97753 vs 124697 (-21.6%) | 97753 vs 187045 (-47.7%) | 97753 vs 249394 (-60.8%) |
| avg_gated_lookup | 56160 vs 62348 (-9.9%) | 56160 vs 124697 (-55.0%) | 56160 vs 187045 (-70.0%) | 56160 vs 249394 (-77.5%) |
- `avg_lookup` at 0.25x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 22.5% of the default cost, 9.9% under the budget it was given.
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 22.5% of the default cost, 55.0% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 22.5% of the default cost, 70.0% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 22.5% of the default cost, 77.5% under the budget it was given.
- `avg_equation` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 39.2% of the default cost, 21.6% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 39.2% of the default cost, 47.7% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 39.2% of the default cost, 60.8% under the budget it was given.
- `avg_gated_lookup` at 0.25x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 22.5% of the default cost, 9.9% under the budget it was given.
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 22.5% of the default cost, 55.0% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 22.5% of the default cost, 70.0% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.5 points at 22.5% of the default cost, 77.5% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

