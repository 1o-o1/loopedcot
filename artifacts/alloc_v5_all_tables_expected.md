## alloc_v5_aqua_huginn_0125
# Table 1 -- aqua (huginn_0125), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 142485 layer passes over 154 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 24.7 | +3.2 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 13.0 (15%) | 23.4 | 23.4 | +4.5 |
| lookup | 22.7 | 24.7 | 24.7 | 24.7 | +3.2 |
| equation | 25.3 | 20.8 | 20.8 | 20.8 | +7.1 |
| equation_n30 | 25.3 | 20.8 | 20.8 | 20.8 | +7.1 |
| equation_n100 | 25.3 | 20.8 | 20.8 | 20.8 | +7.1 |
| gated_equation | 21.4 | 20.8 | 23.4 | 23.4 | +4.5 |
| avg_lookup | 24.7 | 24.7 | 24.7 | 24.7 | +3.2 |
| avg_equation | 24.0 | 20.8 | 20.8 | 20.8 | +7.1 |
| avg_gated_lookup | 23.4 | 23.4 | 23.4 | 23.4 | +4.5 |

The ORACLE GAP is the best single evaluation cell (depth 2 at cap 0, 27.9 points over 154 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F3.

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 35336 vs 35621 (-0.8%) | 35336 vs 71242 (-50.4%) | 35336 vs 106863 (-66.9%) | 35336 vs 142485 (-75.2%) |
| avg_equation | 33741 vs 35621 (-5.3%) | 51738 vs 71242 (-27.4%) | 51738 vs 106863 (-51.6%) | 51738 vs 142485 (-63.7%) |
| avg_gated_lookup | 7451 vs 35621 (-79.1%) | 7451 vs 71242 (-89.5%) | 7451 vs 106863 (-93.0%) | 7451 vs 142485 (-94.8%) |
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 24.7 points at 24.8% of the default cost, 50.4% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 24.7 points at 24.8% of the default cost, 66.9% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 24.7 points at 24.8% of the default cost, 75.2% under the budget it was given.
- `avg_equation` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 20.8 points at 36.3% of the default cost, 27.4% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 20.8 points at 36.3% of the default cost, 51.6% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 20.8 points at 36.3% of the default cost, 63.7% under the budget it was given.
- `avg_gated_lookup` at 0.25x: the multiplier is 0, so the budget never binds. The row is the same 23.4 points at 5.2% of the default cost, 79.1% under the budget it was given.
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 23.4 points at 5.2% of the default cost, 89.5% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 23.4 points at 5.2% of the default cost, 93.0% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 23.4 points at 5.2% of the default cost, 94.8% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_aqua_mcleish_llama32_r32
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

## alloc_v5_aqua_ouro_1_4b_base
# Table 1 -- aqua (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 78835 layer passes over 154 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 67.5 | +1.3 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | 80.8 (17%) | 67.5 | +1.3 |
| lookup | 29.2 | 52.6 | 68.8 | 68.8 | +0.0 |
| equation | 24.0 | 52.6 | 68.8 | 68.2 | +0.6 |
| equation_n30 | 24.0 | 52.6 | 68.8 | 68.2 | +0.6 |
| equation_n100 | 24.0 | 52.6 | 68.8 | 68.2 | +0.6 |
| gated_equation | 24.0 | 52.6 | 80.8 (17%) | 68.2 | +0.6 |
| avg_lookup | 36.4 | 56.5 | 68.8 | 68.8 | +0.0 |
| avg_equation | 35.7 | 56.5 | 68.2 | 68.2 | +0.6 |
| avg_gated_lookup | 36.4 | 56.5 | 68.8 | 68.8 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 3 at cap 256, 68.8 points over 154 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0, F2.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 20737 vs 19709 (+5.2%) | 39745 vs 39418 (+0.8%) | 52245 vs 59126 (-11.6%) | 52245 vs 78835 (-33.7%) |
| avg_equation | 20357 vs 19709 (+3.3%) | 39745 vs 39418 (+0.8%) | 59882 vs 59126 (+1.3%) | 60706 vs 78835 (-23.0%) |
| avg_gated_lookup | 20943 vs 19709 (+6.3%) | 40476 vs 39418 (+2.7%) | 52245 vs 59126 (-11.6%) | 52245 vs 78835 (-33.7%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 68.8 points at 66.3% of the default cost, 11.6% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.8 points at 66.3% of the default cost, 33.7% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.2 points at 77.0% of the default cost, 23.0% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 68.8 points at 66.3% of the default cost, 11.6% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.8 points at 66.3% of the default cost, 33.7% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_aqua_ouro_1_4b_think
# Table 1 -- aqua (ouro_1_4b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 223283 layer passes over 154 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 82.5 | +2.6 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 58.4 | 78.6 | 83.1 | +1.9 |
| lookup | 52.6 | 81.2 | 84.4 | 83.1 | +1.9 |
| equation | 52.6 | 81.2 | 84.4 | 85.1 | +0.0 |
| equation_n30 | 52.6 | 81.2 | 84.4 | 85.1 | +0.0 |
| equation_n100 | 52.6 | 81.2 | 84.4 | 85.1 | +0.0 |
| gated_equation | 51.3 | 81.2 | 84.4 | 85.1 | +0.0 |
| avg_lookup | 64.9 | 81.2 | 82.5 | 85.1 | +0.0 |
| avg_equation | 64.9 | 79.9 | 85.1 | 85.1 | +0.0 |
| avg_gated_lookup | 64.3 | 81.2 | 84.4 | 81.8 | +3.2 |

The ORACLE GAP is the best single evaluation cell (depth 3 at cap 4096, 85.1 points over 154 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 52725 vs 55821 (-5.5%) | 113457 vs 111641 (+1.6%) | 168226 vs 167462 (+0.5%) | 217490 vs 223283 (-2.6%) |
| avg_equation | 52725 vs 55821 (-5.5%) | 112706 vs 111641 (+1.0%) | 166936 vs 167462 (-0.3%) | 219021 vs 223283 (-1.9%) |
| avg_gated_lookup | 53478 vs 55821 (-4.2%) | 118936 vs 111641 (+6.5%) | 163463 vs 167462 (-2.4%) | 216802 vs 223283 (-2.9%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_aqua_ouro_2_6b_base
# Table 1 -- aqua (ouro_2_6b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 158694 layer passes over 154 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 73.4 | +1.9 |
| default_cell | n/a | n/a | n/a | 73.4 | +1.9 |
| default_at_budget | n/a | n/a | 73.5 (22%) | 73.4 | +1.9 |
| lookup | 40.3 | 68.2 | 68.2 | 68.2 | +7.1 |
| equation | 50.6 | 65.6 | 66.2 | 66.2 | +9.1 |
| equation_n30 | 37.7 | 65.6 | 66.2 | 75.3 | +0.0 |
| equation_n100 | 50.6 | 65.6 | 66.2 | 66.2 | +9.1 |
| gated_equation | 37.7 | 65.6 | 66.2 | 73.4 | +1.9 |
| avg_lookup | 47.4 | 68.2 | 68.2 | 68.2 | +7.1 |
| avg_equation | 54.5 | 66.2 | 66.2 | 66.2 | +9.1 |
| avg_gated_lookup | 48.7 | 69.5 | 71.4 | 72.1 | +3.2 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 256, 75.3 points over 154 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F1, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 40712 vs 39674 (+2.6%) | 69931 vs 79347 (-11.9%) | 69931 vs 119021 (-41.2%) | 69931 vs 158694 (-55.9%) |
| avg_equation | 41923 vs 39674 (+5.7%) | 80006 vs 79347 (+0.8%) | 88368 vs 119021 (-25.8%) | 88368 vs 158694 (-44.3%) |
| avg_gated_lookup | 41720 vs 39674 (+5.2%) | 82512 vs 79347 (+4.0%) | 114151 vs 119021 (-4.1%) | 137161 vs 158694 (-13.6%) |
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 68.2 points at 44.1% of the default cost, 11.9% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 68.2 points at 44.1% of the default cost, 41.2% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.2 points at 44.1% of the default cost, 55.9% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 66.2 points at 55.7% of the default cost, 25.8% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 66.2 points at 55.7% of the default cost, 44.3% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 72.1 points at 86.4% of the default cost, 13.6% under the budget it was given.
- `avg_gated_lookup` at 1.00x: deviated from the default cell on family F1. Verification margin +3.3 points, sd 3.3, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 13.6% of the budget, 86.4% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_aqua_ouro_2_6b_think
# Table 1 -- aqua (ouro_2_6b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 401640 layer passes over 154 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 89.0 | +0.0 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 55.8 | 85.1 | 86.4 | +2.6 |
| lookup | 50.0 | 80.5 | 85.1 | 86.4 | +2.6 |
| equation | 48.1 | 80.5 | 85.1 | 86.4 | +2.6 |
| equation_n30 | 50.6 | 80.5 | 85.1 | 86.4 | +2.6 |
| equation_n100 | 48.1 | 80.5 | 85.1 | 86.4 | +2.6 |
| gated_equation | 51.3 | 53.2 | 85.7 | 86.4 | +2.6 |
| avg_lookup | 63.6 | 83.1 | 85.1 | 87.7 | +1.3 |
| avg_equation | 63.0 | 83.1 | 85.1 | 87.7 | +1.3 |
| avg_gated_lookup | 64.3 | 83.1 | 85.7 | 87.7 | +1.3 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 4096, 89.0 points over 154 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0, F2.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 99281 vs 100410 (-1.1%) | 196536 vs 200820 (-2.1%) | 293928 vs 301230 (-2.4%) | 394762 vs 401640 (-1.7%) |
| avg_equation | 94015 vs 100410 (-6.4%) | 196536 vs 200820 (-2.1%) | 296863 vs 301230 (-1.4%) | 394762 vs 401640 (-1.7%) |
| avg_gated_lookup | 100704 vs 100410 (+0.3%) | 197007 vs 200820 (-1.9%) | 298858 vs 301230 (-0.8%) | 397268 vs 401640 (-1.1%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_arc_huginn_0125
# Table 1 -- arc (huginn_0125), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 53783 layer passes over 938 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 40.5 | +1.3 |
| default_cell | n/a | n/a | n/a | 41.4 (53%) | +0.4 |
| default_at_budget | n/a | n/a | n/a | 40.8 (94%) | +1.0 |
| lookup | 29.2 | 39.9 | 41.8 | 41.9 | -0.1 |
| equation | 28.0 | 39.0 | 39.4 | 39.8 | +2.0 |
| equation_n30 | 26.0 | 26.0 | 26.0 | 39.3 | +2.5 |
| equation_n100 | 23.9 | 37.8 | 39.4 | 40.8 | +1.0 |
| gated_equation | 27.5 | 38.8 | 39.4 | 40.6 (94%) | +1.2 |
| avg_lookup | 32.4 | 41.9 | 42.6 | 40.6 | +1.2 |
| avg_equation | 32.2 | 38.7 | 39.6 | 40.6 | +1.2 |
| avg_gated_lookup | 33.2 | 38.6 | 39.6 | 40.5 | +1.3 |

The ORACLE GAP is the best single evaluation cell (depth 16 at cap 0, 41.8 points over 938 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0.

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 13466 vs 13446 (+0.1%) | 26702 vs 26892 (-0.7%) | 40736 vs 40337 (+1.0%) | 53850 vs 53783 (+0.1%) |
| avg_equation | 13586 vs 13446 (+1.0%) | 26930 vs 26892 (+0.1%) | 40622 vs 40337 (+0.7%) | 53619 vs 53783 (-0.3%) |
| avg_gated_lookup | 13246 vs 13446 (-1.5%) | 26925 vs 26892 (+0.1%) | 40622 vs 40337 (+0.7%) | 53856 vs 53783 (+0.1%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_arc_mcleish_llama32_r32
# Table 1 -- arc (mcleish_llama32_r32), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 22345 layer passes over 938 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 43.7 | +0.6 |
| default_cell | n/a | n/a | n/a | 40.3 (26%) | +4.0 |
| default_at_budget | n/a | n/a | n/a | 43.4 (93%) | +1.0 |
| lookup | 24.2 (93%) | 36.1 | 42.0 | 42.0 | +2.3 |
| equation | 25.3 (93%) | 37.2 | 40.7 | 40.7 | +3.6 |
| equation_n30 | 23.7 (93%) | 37.2 | 40.7 | 42.6 | +1.7 |
| equation_n100 | 25.3 (93%) | 36.4 | 40.7 | 42.6 | +1.7 |
| gated_equation | 23.4 (93%) | 37.1 | 40.7 | 42.6 | +1.7 |
| avg_lookup | 26.3 | 41.8 | 42.0 | 42.0 | +2.3 |
| avg_equation | 26.3 | 38.7 | 40.5 | 43.6 | +0.7 |
| avg_gated_lookup | 26.8 | 41.8 | 42.0 | 42.0 | +2.3 |

The ORACLE GAP is the best single evaluation cell (depth 8 at cap 0, 44.3 points over 938 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none.

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 5584 vs 5586 (-0.0%) | 11135 vs 11172 (-0.3%) | 11568 vs 16758 (-31.0%) | 11568 vs 22345 (-48.2%) |
| avg_equation | 5584 vs 5586 (-0.0%) | 11218 vs 11172 (+0.4%) | 16462 vs 16758 (-1.8%) | 22301 vs 22345 (-0.2%) |
| avg_gated_lookup | 5559 vs 5586 (-0.5%) | 11135 vs 11172 (-0.3%) | 11568 vs 16758 (-31.0%) | 11568 vs 22345 (-48.2%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 42.0 points at 51.8% of the default cost, 31.0% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 42.0 points at 51.8% of the default cost, 48.2% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 42.0 points at 51.8% of the default cost, 31.0% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 42.0 points at 51.8% of the default cost, 48.2% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_arc_ouro_1_4b_base
# Table 1 -- arc (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 38814 layer passes over 938 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 86.4 | +0.0 |
| default_cell | n/a | n/a | n/a | 85.7 (57%) | +0.7 |
| default_at_budget | n/a | n/a | n/a | 86.6 (93%) | -0.3 |
| lookup | 42.7 (93%) | 75.3 | 83.9 | 85.6 | +0.7 |
| equation | 43.7 (93%) | 73.0 | 83.6 | 85.3 | +1.1 |
| equation_n30 | 43.7 (93%) | 73.0 | 84.5 | 84.4 | +1.9 |
| equation_n100 | 43.7 (93%) | 73.0 | 83.6 | 84.4 | +1.9 |
| gated_equation | 43.7 (93%) | 73.0 | 84.5 | 86.4 (93%) | -0.1 |
| avg_lookup | 45.2 | 78.1 | 84.4 | 85.9 | +0.4 |
| avg_equation | 43.3 | 75.2 | 84.4 | 86.2 | +0.1 |
| avg_gated_lookup | 45.2 | 79.1 | 84.4 | 85.9 | +0.4 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 128, 86.4 points over 938 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 9593 vs 9704 (-1.1%) | 19232 vs 19407 (-0.9%) | 29051 vs 29111 (-0.2%) | 38122 vs 38814 (-1.8%) |
| avg_equation | 9587 vs 9704 (-1.2%) | 19433 vs 19407 (+0.1%) | 29055 vs 29111 (-0.2%) | 38707 vs 38814 (-0.3%) |
| avg_gated_lookup | 9498 vs 9704 (-2.1%) | 19278 vs 19407 (-0.7%) | 29051 vs 29111 (-0.2%) | 38122 vs 38814 (-1.8%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 85.9 points at 98.2% of the default cost, 1.8% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 85.9 points at 98.2% of the default cost, 1.8% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_arc_ouro_1_4b_think
# Table 1 -- arc (ouro_1_4b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 85664 layer passes over 938 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 93.7 | +0.4 |
| default_cell | n/a | n/a | n/a | 91.3 (20%) | +2.9 |
| default_at_budget | n/a | 87.5 (98%) | 89.1 | 93.7 | +0.4 |
| lookup | 74.5 | 89.4 | 93.3 | 93.3 | +0.9 |
| equation | 74.9 | 89.4 | 94.1 | 93.9 | +0.2 |
| equation_n30 | 74.9 | 89.4 | 94.0 | 93.9 | +0.2 |
| equation_n100 | 74.9 | 89.4 | 94.0 | 93.9 | +0.2 |
| gated_equation | 74.9 | 86.9 (98%) | 87.0 | 93.7 | +0.4 |
| avg_lookup | 78.4 | 88.8 | 93.3 | 93.3 | +0.9 |
| avg_equation | 77.1 | 90.0 | 94.2 | 93.9 | +0.2 |
| avg_gated_lookup | 77.7 | 89.0 | 94.1 | 94.1 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 3 at cap 1024, 94.1 points over 938 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 21441 vs 21416 (+0.1%) | 41759 vs 42832 (-2.5%) | 54345 vs 64248 (-15.4%) | 54345 vs 85664 (-36.6%) |
| avg_equation | 21255 vs 21416 (-0.8%) | 42681 vs 42832 (-0.4%) | 64264 vs 64248 (+0.0%) | 69698 vs 85664 (-18.6%) |
| avg_gated_lookup | 21063 vs 21416 (-1.7%) | 42123 vs 42832 (-1.7%) | 58945 vs 64248 (-8.3%) | 58945 vs 85664 (-31.2%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 93.3 points at 63.4% of the default cost, 15.4% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 93.3 points at 63.4% of the default cost, 36.6% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 93.9 points at 81.4% of the default cost, 18.6% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 94.1 points at 68.8% of the default cost, 8.3% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 94.1 points at 68.8% of the default cost, 31.2% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_arc_ouro_2_6b_base
# Table 1 -- arc (ouro_2_6b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 77524 layer passes over 938 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 93.1 | +0.0 |
| default_cell | n/a | n/a | n/a | 92.6 (57%) | +0.5 |
| default_at_budget | n/a | n/a | n/a | 92.9 (93%) | +0.2 |
| lookup | 63.3 (93%) | 86.8 | 91.0 | 92.0 | +1.1 |
| equation | 56.3 (93%) | 85.7 | 91.2 | 91.7 | +1.4 |
| equation_n30 | 56.3 (93%) | 85.7 | 91.2 | 91.9 | +1.2 |
| equation_n100 | 56.3 (93%) | 85.7 | 91.2 | 91.7 | +1.4 |
| gated_equation | 56.3 (93%) | 85.9 | 91.2 | 92.2 (93%) | +0.9 |
| avg_lookup | 66.1 | 88.5 | 91.8 | 92.2 | +0.9 |
| avg_equation | 57.0 | 88.1 | 91.7 | 91.7 | +1.4 |
| avg_gated_lookup | 65.4 | 88.7 | 91.3 | 91.3 | +1.8 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 128, 93.1 points over 938 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 19186 vs 19381 (-1.0%) | 38281 vs 38762 (-1.2%) | 57835 vs 58143 (-0.5%) | 70185 vs 77524 (-9.5%) |
| avg_equation | 19305 vs 19381 (-0.4%) | 38579 vs 38762 (-0.5%) | 58018 vs 58143 (-0.2%) | 58072 vs 77524 (-25.1%) |
| avg_gated_lookup | 18996 vs 19381 (-2.0%) | 38401 vs 38762 (-0.9%) | 57194 vs 58143 (-1.6%) | 57194 vs 77524 (-26.2%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 92.2 points at 90.5% of the default cost, 9.5% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 91.7 points at 74.9% of the default cost, 25.1% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 91.3 points at 73.8% of the default cost, 1.6% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 91.3 points at 73.8% of the default cost, 26.2% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_arc_ouro_2_6b_think
# Table 1 -- arc (ouro_2_6b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 160919 layer passes over 938 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 96.8 | +0.0 |
| default_cell | n/a | n/a | n/a | 95.9 (42%) | +0.9 |
| default_at_budget | n/a | 91.9 (91%) | 93.3 | 96.7 | +0.1 |
| lookup | 83.5 | 92.2 | 96.5 | 96.7 | +0.1 |
| equation | 70.0 | 92.2 | 96.5 | 96.7 | +0.1 |
| equation_n30 | 70.0 | 91.7 | 94.7 | 96.6 | +0.2 |
| equation_n100 | 70.0 | 88.1 | 96.5 | 96.7 | +0.1 |
| gated_equation | 70.0 | 91.7 | 91.0 | 96.4 | +0.4 |
| avg_lookup | 87.7 | 93.4 | 96.7 | 96.7 | +0.1 |
| avg_equation | 87.5 | 93.5 | 96.7 | 96.7 | +0.1 |
| avg_gated_lookup | 87.7 | 94.1 | 96.7 | 96.7 | +0.1 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 4096, 96.8 points over 938 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0, F1.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 40114 vs 40230 (-0.3%) | 80009 vs 80459 (-0.6%) | 117024 vs 120689 (-3.0%) | 117024 vs 160919 (-27.3%) |
| avg_equation | 39968 vs 40230 (-0.6%) | 79786 vs 80459 (-0.8%) | 117024 vs 120689 (-3.0%) | 117024 vs 160919 (-27.3%) |
| avg_gated_lookup | 39384 vs 40230 (-2.1%) | 81514 vs 80459 (+1.3%) | 117024 vs 120689 (-3.0%) | 117024 vs 160919 (-27.3%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 96.7 points at 72.7% of the default cost, 3.0% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 96.7 points at 72.7% of the default cost, 27.3% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 96.7 points at 72.7% of the default cost, 3.0% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 96.7 points at 72.7% of the default cost, 27.3% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 96.7 points at 72.7% of the default cost, 3.0% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 96.7 points at 72.7% of the default cost, 27.3% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_bbh_huginn_0125
# Table 1 -- bbh (huginn_0125), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 142482 layer passes over 2137 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 35.6 | +0.1 |
| default_cell | n/a | 54.1 (10%) | 54.1 (10%) | 54.7 (40%) | -19.1 |
| default_at_budget | 56.4 (10%) | 60.1 (21%) | 51.9 (42%) | 36.2 (88%) | -0.6 |
| lookup | 31.4 | 34.5 | 32.4 | 33.7 | +2.0 |
| equation | 24.0 | 35.3 | 35.2 | 35.8 | -0.1 |
| equation_n30 | 31.4 | 34.5 | 32.0 | 32.2 | +3.5 |
| equation_n100 | 24.5 | 27.5 | 31.4 | 35.8 | -0.1 |
| gated_equation | 28.6 | 34.2 | 34.4 | 34.7 | +1.0 |
| avg_lookup | 34.1 | 32.1 | 31.8 | 35.0 | +0.6 |
| avg_equation | 24.3 | 35.0 | 37.2 | 35.5 | +0.1 |
| avg_gated_lookup | 34.7 | 32.3 | 31.8 | 31.8 | +3.8 |

The ORACLE GAP is the best single evaluation cell (depth 32 at cap 512, 35.7 points over 2137 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none.

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 35568 vs 35621 (-0.1%) | 71685 vs 71241 (+0.6%) | 105915 vs 106862 (-0.9%) | 125880 vs 142482 (-11.7%) |
| avg_equation | 35430 vs 35621 (-0.5%) | 72374 vs 71241 (+1.6%) | 108954 vs 106862 (+2.0%) | 140961 vs 142482 (-1.1%) |
| avg_gated_lookup | 32323 vs 35621 (-9.3%) | 74475 vs 71241 (+4.5%) | 107109 vs 106862 (+0.2%) | 107109 vs 142482 (-24.8%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 35.0 points at 88.3% of the default cost, 11.7% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 31.8 points at 75.2% of the default cost, 24.8% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_bbh_mcleish_llama32_r32
# Table 1 -- bbh (mcleish_llama32_r32), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 69931 layer passes over 2137 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 43.5 | +0.2 |
| default_cell | n/a | n/a | 50.0 (10%) | 58.6 (41%) | -14.9 |
| default_at_budget | 50.0 (10%) | 57.4 (31%) | 43.6 (72%) | 43.5 (99%) | +0.3 |
| lookup | 32.9 (99%) | 42.2 | 42.8 | 43.5 | +0.2 |
| equation | 34.1 (99%) | 43.0 | 42.6 | 43.4 | +0.3 |
| equation_n30 | 34.5 (99%) | 34.7 | 34.2 | 42.8 | +0.9 |
| equation_n100 | 34.6 (99%) | 42.3 | 42.7 | 43.4 | +0.3 |
| gated_equation | 34.1 (99%) | 42.2 | 42.6 | 42.3 | +1.4 |
| avg_lookup | 36.2 | 42.9 | 43.6 | 43.6 | +0.1 |
| avg_equation | 36.6 | 43.1 | 42.9 | 43.5 | +0.2 |
| avg_gated_lookup | 35.9 | 43.0 | 43.6 | 42.3 | +1.4 |

The ORACLE GAP is the best single evaluation cell (depth 8 at cap 512, 43.7 points over 2137 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3.

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 17616 vs 17483 (+0.8%) | 34588 vs 34966 (-1.1%) | 49386 vs 52448 (-5.8%) | 49386 vs 69931 (-29.4%) |
| avg_equation | 17304 vs 17483 (-1.0%) | 34077 vs 34966 (-2.5%) | 52754 vs 52448 (+0.6%) | 69021 vs 69931 (-1.3%) |
| avg_gated_lookup | 18734 vs 17483 (+7.2%) | 37807 vs 34966 (+8.1%) | 49386 vs 52448 (-5.8%) | 41635 vs 69931 (-40.5%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 43.6 points at 70.6% of the default cost, 5.8% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 43.6 points at 70.6% of the default cost, 29.4% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 43.5 points at 98.7% of the default cost, 1.3% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 43.6 points at 70.6% of the default cost, 5.8% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 42.3 points at 59.5% of the default cost, 40.5% under the budget it was given.
- `avg_gated_lookup` at 1.00x: deviated from the default cell on family F2. Verification margin +5.6 points, sd 4.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 40.5% of the budget, 59.5% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_bbh_ouro_1_4b_base
# Table 1 -- bbh (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 100521 layer passes over 2137 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 75.8 | +0.0 |
| default_cell | n/a | 79.1 (10%) | 79.1 (10%) | 81.5 (32%) | -5.7 |
| default_at_budget | 75.5 (10%) | 79.1 (10%) | 80.7 (30%) | 64.9 (87%) | +10.9 |
| lookup | 33.2 (87%) | 48.7 | 65.8 | 72.4 | +3.4 |
| equation | 33.4 (87%) | 48.0 | 66.0 | 72.5 | +3.3 |
| equation_n30 | 33.4 (87%) | 47.4 | 58.7 | 69.3 | +6.5 |
| equation_n100 | 33.4 (87%) | 48.0 | 66.0 | 72.5 | +3.3 |
| gated_equation | 34.5 (87%) | 47.7 | 65.9 | 63.7 | +12.1 |
| avg_lookup | 31.8 | 57.3 | 70.1 | 75.4 | +0.4 |
| avg_equation | 35.0 | 57.2 | 67.0 | 75.8 | +0.0 |
| avg_gated_lookup | 33.1 | 58.1 | 71.9 | 75.4 | +0.4 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 2048, 75.8 points over 2137 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 23544 vs 25130 (-6.3%) | 49855 vs 50261 (-0.8%) | 74724 vs 75391 (-0.9%) | 94413 vs 100521 (-6.1%) |
| avg_equation | 24969 vs 25130 (-0.6%) | 49943 vs 50261 (-0.6%) | 74867 vs 75391 (-0.7%) | 99671 vs 100521 (-0.8%) |
| avg_gated_lookup | 24786 vs 25130 (-1.4%) | 52280 vs 50261 (+4.0%) | 80500 vs 75391 (+6.8%) | 94413 vs 100521 (-6.1%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 75.4 points at 93.9% of the default cost, 6.1% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 75.4 points at 93.9% of the default cost, 6.1% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_bbh_ouro_1_4b_think
# Table 1 -- bbh (ouro_1_4b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 183913 layer passes over 2137 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 84.3 | +0.0 |
| default_cell | n/a | n/a | 68.2 (10%) | 83.3 (72%) | +1.0 |
| default_at_budget | 65.5 (10%) | 52.4 (72%) | 66.3 | 84.1 | +0.1 |
| lookup | 32.5 | 66.5 | 81.0 | 83.2 | +1.1 |
| equation | 40.1 | 66.7 | 80.9 | 83.3 | +1.0 |
| equation_n30 | 34.3 | 66.7 | 81.1 | 82.3 | +2.0 |
| equation_n100 | 34.3 | 66.5 | 81.0 | 83.3 | +0.9 |
| gated_equation | 35.0 | 49.4 (72%) | 81.1 | 84.1 | +0.1 |
| avg_lookup | 45.1 | 73.3 | 81.0 | 84.1 | +0.1 |
| avg_equation | 41.2 | 73.5 | 81.4 | 84.3 | +0.0 |
| avg_gated_lookup | 41.7 | 76.8 | 82.4 | 84.3 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 4096, 84.3 points over 2137 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0, F2.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 47495 vs 45978 (+3.3%) | 91032 vs 91957 (-1.0%) | 135467 vs 137935 (-1.8%) | 161449 vs 183913 (-12.2%) |
| avg_equation | 45951 vs 45978 (-0.1%) | 91248 vs 91957 (-0.8%) | 138414 vs 137935 (+0.3%) | 173159 vs 183913 (-5.8%) |
| avg_gated_lookup | 44126 vs 45978 (-4.0%) | 97844 vs 91957 (+6.4%) | 142908 vs 137935 (+3.6%) | 173159 vs 183913 (-5.8%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 84.1 points at 87.8% of the default cost, 12.2% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 84.3 points at 94.2% of the default cost, 5.8% under the budget it was given.
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin -2.2 points, sd 3.2, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 5.8% of the budget, 94.2% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_bbh_ouro_2_6b_base
# Table 1 -- bbh (ouro_2_6b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 197416 layer passes over 2137 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 82.5 | +0.0 |
| default_cell | n/a | 89.5 (10%) | 89.3 (21%) | 86.2 (38%) | -3.7 |
| default_at_budget | 79.6 (10%) | 89.5 (10%) | 86.9 (25%) | 69.2 (85%) | +13.3 |
| lookup | 43.0 (85%) | 55.9 | 78.8 | 81.0 | +1.4 |
| equation | 40.3 (85%) | 57.3 | 78.8 | 81.1 | +1.3 |
| equation_n30 | 40.3 (85%) | 57.3 | 78.8 | 81.2 | +1.2 |
| equation_n100 | 40.3 (85%) | 57.3 | 78.8 | 81.1 | +1.3 |
| gated_equation | 39.5 (85%) | 57.3 | 78.1 | 80.9 | +1.6 |
| avg_lookup | 43.3 | 74.1 | 81.2 | 81.2 | +1.3 |
| avg_equation | 43.3 | 74.1 | 81.0 | 81.3 | +1.2 |
| avg_gated_lookup | 43.5 | 74.5 | 81.2 | 81.2 | +1.3 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 2048, 82.5 points over 2137 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 49305 vs 49354 (-0.1%) | 97042 vs 98708 (-1.7%) | 145230 vs 148062 (-1.9%) | 145230 vs 197416 (-26.4%) |
| avg_equation | 49305 vs 49354 (-0.1%) | 97880 vs 98708 (-0.8%) | 146449 vs 148062 (-1.1%) | 150487 vs 197416 (-23.8%) |
| avg_gated_lookup | 49578 vs 49354 (+0.5%) | 103332 vs 98708 (+4.7%) | 145230 vs 148062 (-1.9%) | 145230 vs 197416 (-26.4%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 81.2 points at 73.6% of the default cost, 1.9% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 81.2 points at 73.6% of the default cost, 26.4% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 81.3 points at 76.2% of the default cost, 23.8% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 81.2 points at 73.6% of the default cost, 1.9% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 81.2 points at 73.6% of the default cost, 26.4% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_bbh_ouro_2_6b_think
# Table 1 -- bbh (ouro_2_6b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 320368 layer passes over 2137 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 91.2 | +0.0 |
| default_cell | n/a | n/a | 84.1 (10%) | 91.9 (21%) | -0.6 |
| default_at_budget | 85.9 (10%) | 79.3 (38%) | 62.8 (95%) | 90.4 | +0.9 |
| lookup | 48.1 | 79.7 | 87.1 | 89.9 | +1.3 |
| equation | 48.2 | 78.9 | 84.5 | 89.8 | +1.4 |
| equation_n30 | 48.7 | 79.9 | 87.0 | 89.9 | +1.4 |
| equation_n100 | 47.7 | 79.7 | 85.1 | 89.8 | +1.5 |
| gated_equation | 45.8 | 79.7 | 87.5 | 90.5 | +0.8 |
| avg_lookup | 50.1 | 82.6 | 88.9 | 91.4 | -0.1 |
| avg_equation | 51.0 | 82.3 | 88.8 | 91.4 | -0.1 |
| avg_gated_lookup | 50.1 | 82.6 | 88.9 | 89.8 | +1.4 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 4096, 91.2 points over 2137 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 79733 vs 80092 (-0.4%) | 156624 vs 160184 (-2.2%) | 235336 vs 240276 (-2.1%) | 320250 vs 320368 (-0.0%) |
| avg_equation | 79980 vs 80092 (-0.1%) | 156308 vs 160184 (-2.4%) | 236979 vs 240276 (-1.4%) | 320250 vs 320368 (-0.0%) |
| avg_gated_lookup | 79733 vs 80092 (-0.4%) | 154203 vs 160184 (-3.7%) | 231234 vs 240276 (-3.8%) | 257365 vs 320368 (-19.7%) |
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 89.8 points at 80.3% of the default cost, 19.7% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_csqa_huginn_0125
# Table 1 -- csqa (huginn_0125), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 87288 layer passes over 977 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 42.8 | +0.0 |
| default_cell | n/a | n/a | n/a | 42.8 (60%) | -0.0 |
| default_at_budget | n/a | n/a | n/a | 42.3 (100%) | +0.5 |
| lookup | 19.5 | 36.7 | 41.7 | 42.4 | +0.4 |
| equation | 18.9 | 32.5 | 41.7 | 42.4 | +0.4 |
| equation_n30 | 20.6 | 32.8 | 41.7 | 42.4 | +0.4 |
| equation_n100 | 19.4 | 31.8 | 41.7 | 41.7 | +1.1 |
| gated_equation | 18.9 | 32.5 | 41.7 | 41.7 | +1.1 |
| avg_lookup | 26.0 | 41.1 | 41.4 | 42.0 | +0.8 |
| avg_equation | 24.5 | 40.9 | 42.2 | 42.8 | +0.0 |
| avg_gated_lookup | 24.5 | 40.9 | 41.4 | 42.0 | +0.8 |

The ORACLE GAP is the best single evaluation cell (depth 32 at cap 64, 42.8 points over 977 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F1, F2.

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 19972 vs 21822 (-8.5%) | 42979 vs 43644 (-1.5%) | 61768 vs 65466 (-5.6%) | 86310 vs 87288 (-1.1%) |
| avg_equation | 19812 vs 21822 (-9.2%) | 42967 vs 43644 (-1.6%) | 62156 vs 65466 (-5.1%) | 87256 vs 87288 (-0.0%) |
| avg_gated_lookup | 19812 vs 21822 (-9.2%) | 42967 vs 43644 (-1.6%) | 61768 vs 65466 (-5.6%) | 86310 vs 87288 (-1.1%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 42.0 points at 98.9% of the default cost, 1.1% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 42.0 points at 98.9% of the default cost, 1.1% under the budget it was given.
- `avg_gated_lookup` at 1.00x: deviated from the default cell on family F1. Verification margin +1.4 points, sd 1.3, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 1.1% of the budget, 98.9% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_csqa_mcleish_llama32_r32
# Table 1 -- csqa (mcleish_llama32_r32), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 35107 layer passes over 977 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 39.0 | +3.9 |
| default_cell | n/a | n/a | n/a | 40.0 (56%) | +2.9 |
| default_at_budget | n/a | n/a | n/a | 40.8 (100%) | +2.1 |
| lookup | 20.9 (100%) | 30.0 | 42.6 | 42.9 | +0.0 |
| equation | 20.9 (100%) | 33.1 | 42.6 | 42.9 | +0.0 |
| equation_n30 | 23.0 (100%) | 22.5 | 42.6 | 42.9 | +0.0 |
| equation_n100 | 23.0 (100%) | 33.1 | 35.6 | 35.6 | +7.3 |
| gated_equation | 20.9 (100%) | 33.1 | 42.6 | 42.9 (100%) | -0.0 |
| avg_lookup | 21.7 | 40.2 | 42.7 | 42.9 | +0.0 |
| avg_equation | 21.9 | 40.1 | 42.7 | 42.9 | +0.0 |
| avg_gated_lookup | 21.7 | 40.2 | 42.6 | 42.9 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 8 at cap 0, 42.9 points over 977 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0.

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 8705 vs 8777 (-0.8%) | 17210 vs 17553 (-2.0%) | 25320 vs 26330 (-3.8%) | 33236 vs 35107 (-5.3%) |
| avg_equation | 8672 vs 8777 (-1.2%) | 17128 vs 17553 (-2.4%) | 25320 vs 26330 (-3.8%) | 33236 vs 35107 (-5.3%) |
| avg_gated_lookup | 8705 vs 8777 (-0.8%) | 17210 vs 17553 (-2.0%) | 18992 vs 26330 (-27.9%) | 33236 vs 35107 (-5.3%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 42.9 points at 94.7% of the default cost, 5.3% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 42.9 points at 94.7% of the default cost, 5.3% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 42.6 points at 54.1% of the default cost, 27.9% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 42.9 points at 94.7% of the default cost, 5.3% under the budget it was given.
- `avg_gated_lookup` at 1.00x: deviated from the default cell on family F0. Verification margin +11.0 points, sd 7.2, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 5.3% of the budget, 94.7% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_csqa_ouro_1_4b_base
# Table 1 -- csqa (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 61956 layer passes over 977 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 72.6 | +0.8 |
| default_cell | n/a | n/a | n/a | 73.0 (55%) | +0.4 |
| default_at_budget | n/a | n/a | n/a | 72.6 (100%) | +0.7 |
| lookup | 33.7 (100%) | 66.1 | 72.1 | 73.4 | +0.0 |
| equation | 32.9 (100%) | 61.5 | 71.6 | 72.3 | +1.1 |
| equation_n30 | 32.3 (100%) | 66.1 | 71.8 | 71.6 | +1.7 |
| equation_n100 | 32.9 (100%) | 61.5 | 71.8 | 72.3 | +1.1 |
| gated_equation | 32.9 (100%) | 61.5 | 71.8 | 73.4 (100%) | +0.0 |
| avg_lookup | 32.9 | 66.4 | 71.4 | 73.4 | +0.0 |
| avg_equation | 33.2 | 61.6 | 71.6 | 72.6 | +0.8 |
| avg_gated_lookup | 33.0 | 65.0 | 71.4 | 72.6 | +0.8 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 0, 73.4 points over 977 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 15464 vs 15489 (-0.2%) | 30822 vs 30978 (-0.5%) | 46221 vs 46467 (-0.5%) | 58628 vs 61956 (-5.4%) |
| avg_equation | 15481 vs 15489 (-0.1%) | 30977 vs 30978 (-0.0%) | 46519 vs 46467 (+0.1%) | 61954 vs 61956 (-0.0%) |
| avg_gated_lookup | 15484 vs 15489 (-0.0%) | 30459 vs 30978 (-1.7%) | 46221 vs 46467 (-0.5%) | 61954 vs 61956 (-0.0%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 73.4 points at 94.6% of the default cost, 5.4% under the budget it was given.
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin +1.4 points, sd 4.6, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 0.0% of the budget, 100.0% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_csqa_ouro_1_4b_think
# Table 1 -- csqa (ouro_1_4b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 133929 layer passes over 977 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 76.7 | +0.0 |
| default_cell | n/a | n/a | n/a | 76.7 | +0.0 |
| default_at_budget | n/a | 72.9 | 75.2 | 76.7 | +0.0 |
| lookup | 61.1 | 73.5 | 75.2 | 76.5 | +0.2 |
| equation | 61.1 | 73.9 | 75.2 | 76.7 | +0.0 |
| equation_n30 | 61.1 | 73.9 | 76.4 | 76.4 | +0.3 |
| equation_n100 | 61.1 | 73.9 | 75.2 | 76.7 | +0.0 |
| gated_equation | 61.1 | 72.9 | 75.2 | 76.7 | +0.0 |
| avg_lookup | 60.7 | 73.9 | 77.0 | 76.5 | +0.2 |
| avg_equation | 60.8 | 71.5 | 75.7 | 76.7 | +0.0 |
| avg_gated_lookup | 60.8 | 73.8 | 75.6 | 76.7 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 2048, 76.7 points over 977 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 33346 vs 33482 (-0.4%) | 66923 vs 66964 (-0.1%) | 98418 vs 100446 (-2.0%) | 104309 vs 133929 (-22.1%) |
| avg_equation | 33456 vs 33482 (-0.1%) | 66470 vs 66964 (-0.7%) | 99895 vs 100446 (-0.5%) | 111070 vs 133929 (-17.1%) |
| avg_gated_lookup | 33466 vs 33482 (-0.0%) | 66800 vs 66964 (-0.2%) | 98695 vs 100446 (-1.7%) | 119145 vs 133929 (-11.0%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 76.5 points at 77.9% of the default cost, 22.1% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 76.7 points at 82.9% of the default cost, 17.1% under the budget it was given.
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 11.0% of the budget, 89.0% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_csqa_ouro_2_6b_base
# Table 1 -- csqa (ouro_2_6b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 124188 layer passes over 977 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 80.3 | +1.6 |
| default_cell | n/a | n/a | n/a | 78.7 (55%) | +3.3 |
| default_at_budget | n/a | n/a | n/a | 81.1 (100%) | +0.8 |
| lookup | 36.8 (100%) | 75.5 | 81.2 | 82.0 | +0.0 |
| equation | 36.8 (100%) | 74.7 | 80.0 | 80.0 | +1.9 |
| equation_n30 | 36.8 (100%) | 74.7 | 80.2 | 80.0 | +1.9 |
| equation_n100 | 36.8 (100%) | 74.7 | 77.5 | 80.0 | +1.9 |
| gated_equation | 36.8 (100%) | 74.7 | 80.2 | 81.2 | +0.8 |
| avg_lookup | 40.3 | 76.0 | 81.2 | 82.0 | +0.0 |
| avg_equation | 40.3 | 74.6 | 79.6 | 80.3 | +1.6 |
| avg_gated_lookup | 40.2 | 76.0 | 81.2 | 82.0 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 0, 82.0 points over 977 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 31015 vs 31047 (-0.1%) | 61885 vs 62094 (-0.3%) | 93022 vs 93141 (-0.1%) | 117256 vs 124188 (-5.6%) |
| avg_equation | 31015 vs 31047 (-0.1%) | 62217 vs 62094 (+0.2%) | 93293 vs 93141 (+0.2%) | 124165 vs 124188 (-0.0%) |
| avg_gated_lookup | 30984 vs 31047 (-0.2%) | 61885 vs 62094 (-0.3%) | 93022 vs 93141 (-0.1%) | 117256 vs 124188 (-5.6%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 82.0 points at 94.4% of the default cost, 5.6% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 82.0 points at 94.4% of the default cost, 5.6% under the budget it was given.
- `avg_gated_lookup` at 1.00x: deviated from the default cell on family F0. Verification margin +4.1 points, sd 3.0, bar 0.50 sd (73 verification questions, the ids after the 171 that fit, out of 244 calibration); cost saving 5.6% of the budget, 94.4% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_csqa_ouro_2_6b_think
# Table 1 -- csqa (ouro_2_6b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 234088 layer passes over 977 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 80.9 | +0.0 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | 79.2 | 80.5 | +0.4 |
| lookup | 18.1 | 80.3 | 80.0 | 80.5 | +0.4 |
| equation | 20.2 | 76.7 | 76.7 | 80.5 | +0.4 |
| equation_n30 | 28.9 | 76.7 | 76.7 | 76.7 | +4.2 |
| equation_n100 | 20.2 | 76.7 | 79.4 | 80.5 | +0.4 |
| gated_equation | 20.2 | 76.7 | 79.2 | 80.5 | +0.4 |
| avg_lookup | 67.3 | 80.6 | 79.6 | 80.5 | +0.4 |
| avg_equation | 67.3 | 76.3 | 77.0 | 79.7 | +1.1 |
| avg_gated_lookup | 65.8 | 80.6 | 79.8 | 80.5 | +0.4 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 4096, 80.9 points over 977 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 57914 vs 58522 (-1.0%) | 115832 vs 117044 (-1.0%) | 176510 vs 175566 (+0.5%) | 229800 vs 234088 (-1.8%) |
| avg_equation | 57914 vs 58522 (-1.0%) | 116932 vs 117044 (-0.1%) | 173498 vs 175566 (-1.2%) | 231707 vs 234088 (-1.0%) |
| avg_gated_lookup | 56752 vs 58522 (-3.0%) | 115832 vs 117044 (-1.0%) | 167628 vs 175566 (-4.5%) | 229800 vs 234088 (-1.8%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 80.5 points at 98.2% of the default cost, 1.8% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 80.5 points at 98.2% of the default cost, 1.8% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_gsm8k_huginn_0125
# Table 1 -- gsm8k (huginn_0125), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 105638 layer passes over 1056 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 25.5 | +0.1 |
| default_cell | n/a | n/a | n/a | 25.6 (98%) | -0.1 |
| default_at_budget | n/a | n/a | 2.8 (24%) | 25.5 | +0.1 |
| lookup | 7.9 | 21.1 | 20.9 | 25.6 | +0.0 |
| equation | 8.1 | 21.0 | 20.8 | 25.5 | +0.1 |
| equation_n30 | 8.1 | 21.0 | 14.9 | 25.5 | +0.1 |
| equation_n100 | 8.1 | 21.0 | 20.8 | 25.5 | +0.1 |
| gated_equation | 8.1 | 21.0 | 20.8 | 25.5 | +0.1 |
| avg_lookup | 12.8 | 22.2 | 23.7 | 25.6 | +0.0 |
| avg_equation | 12.9 | 20.8 | 23.7 | 25.5 | +0.1 |
| avg_gated_lookup | 12.8 | 22.2 | 23.7 | 25.5 | +0.1 |

The ORACLE GAP is the best single evaluation cell (depth 32 at cap 256, 25.6 points over 1056 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3.

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 25134 vs 26410 (-4.8%) | 52601 vs 52819 (-0.4%) | 78966 vs 79229 (-0.3%) | 94848 vs 105638 (-10.2%) |
| avg_equation | 24959 vs 26410 (-5.5%) | 53520 vs 52819 (+1.3%) | 79458 vs 79229 (+0.3%) | 98118 vs 105638 (-7.1%) |
| avg_gated_lookup | 25134 vs 26410 (-4.8%) | 53401 vs 52819 (+1.1%) | 78966 vs 79229 (-0.3%) | 98118 vs 105638 (-7.1%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 25.6 points at 89.8% of the default cost, 10.2% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 25.5 points at 92.9% of the default cost, 7.1% under the budget it was given.
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 7.1% of the budget, 92.9% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_gsm8k_mcleish_llama32_r32
# Table 1 -- gsm8k (mcleish_llama32_r32), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 141339 layer passes over 1056 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 48.9 | +0.6 |
| default_cell | n/a | n/a | n/a | 52.4 (84%) | -2.9 |
| default_at_budget | n/a | n/a | 8.8 (6%) | 48.7 | +0.8 |
| lookup | 47.8 | 49.1 | 48.9 | 48.9 | +0.6 |
| equation | 47.8 | 49.4 | 49.4 | 49.4 | +0.0 |
| equation_n30 | 45.7 | 49.1 | 48.9 | 48.9 | +0.6 |
| equation_n100 | 47.5 | 49.1 | 48.9 | 48.9 | +0.6 |
| gated_equation | 47.8 | 49.4 | 48.9 | 48.9 | +0.6 |
| avg_lookup | 49.2 | 48.9 | 48.9 | 48.9 | +0.6 |
| avg_equation | 48.8 | 49.4 | 49.4 | 49.4 | +0.0 |
| avg_gated_lookup | 49.0 | 49.4 | 49.4 | 48.9 | +0.6 |

The ORACLE GAP is the best single evaluation cell (depth 8 at cap 256, 49.4 points over 1056 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2.

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 35393 vs 35335 (+0.2%) | 68960 vs 70670 (-2.4%) | 68960 vs 106005 (-34.9%) | 68960 vs 141339 (-51.2%) |
| avg_equation | 35115 vs 35335 (-0.6%) | 40159 vs 70670 (-43.2%) | 40159 vs 106005 (-62.1%) | 40159 vs 141339 (-71.6%) |
| avg_gated_lookup | 35022 vs 35335 (-0.9%) | 36071 vs 70670 (-49.0%) | 36071 vs 106005 (-66.0%) | 137429 vs 141339 (-2.8%) |
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 48.9 points at 48.8% of the default cost, 2.4% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 48.9 points at 48.8% of the default cost, 34.9% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 48.9 points at 48.8% of the default cost, 51.2% under the budget it was given.
- `avg_equation` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 49.4 points at 28.4% of the default cost, 43.2% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 49.4 points at 28.4% of the default cost, 62.1% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 49.4 points at 28.4% of the default cost, 71.6% under the budget it was given.
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 49.4 points at 25.5% of the default cost, 49.0% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 49.4 points at 25.5% of the default cost, 66.0% under the budget it was given.
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin -1.3 points, sd 3.4, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 2.8% of the budget, 97.2% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_gsm8k_ouro_1_4b_base
# Table 1 -- gsm8k (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 77105 layer passes over 1056 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 76.7 | +0.1 |
| default_cell | n/a | n/a | n/a | 81.6 (71%) | -4.8 |
| default_at_budget | n/a | n/a | n/a | 73.0 | +3.8 |
| lookup | 22.1 | 62.2 | 72.0 | 76.4 | +0.4 |
| equation | 22.2 | 62.2 | 72.2 | 76.4 | +0.4 |
| equation_n30 | 22.2 | 61.9 | 71.1 | 76.4 | +0.4 |
| equation_n100 | 22.2 | 62.2 | 72.2 | 76.2 | +0.6 |
| gated_equation | 22.2 | 62.2 | 72.2 | 76.4 | +0.4 |
| avg_lookup | 23.7 | 65.4 | 74.1 | 76.7 | +0.1 |
| avg_equation | 24.3 | 65.4 | 74.3 | 76.7 | +0.1 |
| avg_gated_lookup | 24.2 | 65.4 | 74.1 | 76.7 | +0.1 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 1024, 76.8 points over 1056 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 19482 vs 19276 (+1.1%) | 38596 vs 38552 (+0.1%) | 57997 vs 57829 (+0.3%) | 75002 vs 77105 (-2.7%) |
| avg_equation | 19615 vs 19276 (+1.8%) | 38596 vs 38552 (+0.1%) | 58078 vs 57829 (+0.4%) | 76310 vs 77105 (-1.0%) |
| avg_gated_lookup | 19794 vs 19276 (+2.7%) | 38596 vs 38552 (+0.1%) | 57997 vs 57829 (+0.3%) | 76310 vs 77105 (-1.0%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 76.7 points at 97.3% of the default cost, 2.7% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 76.7 points at 99.0% of the default cost, 1.0% under the budget it was given.
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 1.0% of the budget, 99.0% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_gsm8k_ouro_1_4b_think
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

## alloc_v5_gsm8k_ouro_2_6b_base
# Table 1 -- gsm8k (ouro_2_6b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 151176 layer passes over 1056 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 82.8 | +0.0 |
| default_cell | n/a | n/a | n/a | 88.2 (61%) | -5.5 |
| default_at_budget | n/a | n/a | n/a | 77.4 | +5.4 |
| lookup | 29.3 | 69.4 | 77.2 | 82.0 | +0.8 |
| equation | 29.3 | 69.4 | 77.2 | 82.0 | +0.8 |
| equation_n30 | 29.3 | 69.4 | 75.0 | 80.5 | +2.3 |
| equation_n100 | 29.3 | 69.4 | 77.2 | 82.0 | +0.8 |
| gated_equation | 29.3 | 69.1 | 77.2 | 82.0 | +0.8 |
| avg_lookup | 32.2 | 75.1 | 79.0 | 82.8 | +0.0 |
| avg_equation | 32.2 | 75.1 | 79.0 | 82.8 | +0.0 |
| avg_gated_lookup | 32.2 | 74.0 | 78.9 | 82.8 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 512, 82.8 points over 1056 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 38195 vs 37794 (+1.1%) | 76038 vs 75588 (+0.6%) | 113722 vs 113382 (+0.3%) | 148430 vs 151176 (-1.8%) |
| avg_equation | 38195 vs 37794 (+1.1%) | 76038 vs 75588 (+0.6%) | 113722 vs 113382 (+0.3%) | 148430 vs 151176 (-1.8%) |
| avg_gated_lookup | 38192 vs 37794 (+1.1%) | 76491 vs 75588 (+1.2%) | 114197 vs 113382 (+0.7%) | 150673 vs 151176 (-0.3%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 82.8 points at 98.2% of the default cost, 1.8% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 82.8 points at 98.2% of the default cost, 1.8% under the budget it was given.
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin -1.3 points, sd 1.2, bar 0.50 sd (79 verification questions, the ids after the 184 that fit, out of 263 calibration); cost saving 0.3% of the budget, 99.7% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_gsm8k_ouro_2_6b_think
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

## alloc_v5_hellaswag_huginn_0125
# Table 1 -- hellaswag (huginn_0125), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 116818 layer passes over 1700 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 34.0 | +5.6 |
| default_cell | n/a | n/a | n/a | 47.5 (34%) | -7.9 |
| default_at_budget | n/a | n/a | 59.0 (11%) | 34.7 (99%) | +4.9 |
| lookup | 24.2 | 38.2 | 38.7 | 39.6 | +0.0 |
| equation | 24.2 | 38.2 | 38.6 | 38.6 | +1.0 |
| equation_n30 | 25.3 | 38.6 | 38.7 | 39.6 | +0.0 |
| equation_n100 | 23.4 | 38.6 | 38.6 | 38.6 | +1.0 |
| gated_equation | 24.9 | 38.6 | 38.7 | 34.5 | +5.1 |
| avg_lookup | 32.9 | 38.8 | 39.2 | 39.6 | +0.0 |
| avg_equation | 32.9 | 38.6 | 38.6 | 38.6 | +1.0 |
| avg_gated_lookup | 32.9 | 38.8 | 39.2 | 39.6 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 32 at cap 0, 39.6 points over 1700 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0.

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 27478 vs 29204 (-5.9%) | 57752 vs 58409 (-1.1%) | 86653 vs 87613 (-1.1%) | 102451 vs 116818 (-12.3%) |
| avg_equation | 27478 vs 29204 (-5.9%) | 52778 vs 58409 (-9.6%) | 52778 vs 87613 (-39.8%) | 52778 vs 116818 (-54.8%) |
| avg_gated_lookup | 27478 vs 29204 (-5.9%) | 57752 vs 58409 (-1.1%) | 86653 vs 87613 (-1.1%) | 102451 vs 116818 (-12.3%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 39.6 points at 87.7% of the default cost, 12.3% under the budget it was given.
- `avg_equation` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 38.6 points at 45.2% of the default cost, 9.6% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 38.6 points at 45.2% of the default cost, 39.8% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 38.6 points at 45.2% of the default cost, 54.8% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 39.6 points at 87.7% of the default cost, 12.3% under the budget it was given.
- `avg_gated_lookup` at 1.00x: deviated from the default cell on family F0. Verification margin +2.2 points, sd 3.5, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 12.3% of the budget, 87.7% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_hellaswag_mcleish_llama32_r32
# Table 1 -- hellaswag (mcleish_llama32_r32), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 45837 layer passes over 1700 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 28.6 | +2.9 |
| default_cell | n/a | n/a | n/a | 33.9 (35%) | -2.4 |
| default_at_budget | n/a | n/a | 40.9 (15%) | 29.0 (99%) | +2.4 |
| lookup | 24.6 (99%) | 29.9 | 30.9 | 31.5 | +0.0 |
| equation | 24.6 (99%) | 29.9 | 30.8 | 28.8 | +2.6 |
| equation_n30 | 24.6 (99%) | 29.9 | 30.8 | 28.8 | +2.6 |
| equation_n100 | 24.6 (99%) | 29.9 | 30.9 | 31.5 | +0.0 |
| gated_equation | 24.6 (99%) | 29.9 | 30.7 | 31.6 (99%) | -0.2 |
| avg_lookup | 25.9 | 30.8 | 30.9 | 31.5 | +0.0 |
| avg_equation | 26.0 | 30.9 | 28.6 | 28.6 | +2.9 |
| avg_gated_lookup | 25.9 | 30.8 | 30.9 | 31.5 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 8 at cap 0, 31.5 points over 1700 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0, F2.

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 11427 vs 11459 (-0.3%) | 23043 vs 22918 (+0.5%) | 34109 vs 34378 (-0.8%) | 40123 vs 45837 (-12.5%) |
| avg_equation | 11400 vs 11459 (-0.5%) | 23046 vs 22918 (+0.6%) | 34410 vs 34378 (+0.1%) | 45758 vs 45837 (-0.2%) |
| avg_gated_lookup | 11440 vs 11459 (-0.2%) | 23043 vs 22918 (+0.5%) | 34109 vs 34378 (-0.8%) | 40123 vs 45837 (-12.5%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 31.5 points at 87.5% of the default cost, 12.5% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 31.5 points at 87.5% of the default cost, 12.5% under the budget it was given.
- `avg_gated_lookup` at 1.00x: deviated from the default cell on family F0. Verification margin +5.6 points, sd 4.0, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 12.5% of the budget, 87.5% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_hellaswag_ouro_1_4b_base
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

## alloc_v5_hellaswag_ouro_1_4b_think
# Table 1 -- hellaswag (ouro_1_4b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 145921 layer passes over 1700 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 74.8 | +2.9 |
| default_cell | n/a | n/a | n/a | 73.4 (44%) | +4.2 |
| default_at_budget | n/a | 68.6 (32%) | 72.4 | 74.8 | +2.9 |
| lookup | 37.9 | 76.6 | 77.6 | 77.6 | +0.0 |
| equation | 37.4 | 69.3 | 72.0 | 71.9 | +5.7 |
| equation_n30 | 36.4 | 69.3 | 72.0 | 74.8 | +2.9 |
| equation_n100 | 37.4 | 69.3 | 72.0 | 71.9 | +5.7 |
| gated_equation | 37.4 | 69.3 (32%) | 77.6 | 77.6 | +0.0 |
| avg_lookup | 56.3 | 77.5 | 77.6 | 77.6 | +0.0 |
| avg_equation | 56.7 | 75.0 | 71.9 | 71.9 | +5.7 |
| avg_gated_lookup | 54.9 | 77.2 | 76.6 | 77.6 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 0, 77.6 points over 1700 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 36074 vs 36480 (-1.1%) | 73178 vs 72960 (+0.3%) | 75221 vs 109441 (-31.3%) | 75221 vs 145921 (-48.5%) |
| avg_equation | 35956 vs 36480 (-1.4%) | 66902 vs 72960 (-8.3%) | 108830 vs 109441 (-0.6%) | 108830 vs 145921 (-25.4%) |
| avg_gated_lookup | 35939 vs 36480 (-1.5%) | 73202 vs 72960 (+0.3%) | 81365 vs 109441 (-25.7%) | 75221 vs 145921 (-48.5%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 77.6 points at 51.5% of the default cost, 31.3% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 77.6 points at 51.5% of the default cost, 48.5% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 71.9 points at 74.6% of the default cost, 25.4% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 76.6 points at 55.8% of the default cost, 25.7% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 77.6 points at 51.5% of the default cost, 48.5% under the budget it was given.
- `avg_gated_lookup` at 1.00x: deviated from the default cell on family F0. Verification margin +8.9 points, sd 4.1, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 48.5% of the budget, 51.5% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_hellaswag_ouro_2_6b_base
# Table 1 -- hellaswag (ouro_2_6b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 171164 layer passes over 1700 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 76.8 | +5.4 |
| default_cell | n/a | n/a | n/a | 74.6 (34%) | +7.5 |
| default_at_budget | n/a | n/a | 76.3 (16%) | 76.6 | +5.5 |
| lookup | 33.6 | 66.0 | 82.1 | 82.1 | +0.0 |
| equation | 33.6 | 58.2 | 74.9 | 76.2 | +5.9 |
| equation_n30 | 31.7 | 66.0 | 81.9 | 76.5 | +5.6 |
| equation_n100 | 33.6 | 58.2 | 74.9 | 76.5 | +5.6 |
| gated_equation | 33.6 | 58.2 | 74.9 | 82.1 | +0.0 |
| avg_lookup | 36.0 | 69.2 | 82.4 | 82.1 | +0.0 |
| avg_equation | 35.5 | 60.0 | 74.8 | 76.6 | +5.5 |
| avg_gated_lookup | 36.0 | 69.3 | 82.5 | 82.1 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 3 at cap 0, 82.1 points over 1700 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 41832 vs 42791 (-2.2%) | 85056 vs 85582 (-0.6%) | 128505 vs 128373 (+0.1%) | 147946 vs 171164 (-13.6%) |
| avg_equation | 41670 vs 42791 (-2.6%) | 84826 vs 85582 (-0.9%) | 127675 vs 128373 (-0.5%) | 158266 vs 171164 (-7.5%) |
| avg_gated_lookup | 41832 vs 42791 (-2.2%) | 85143 vs 85582 (-0.5%) | 128958 vs 128373 (+0.5%) | 147946 vs 171164 (-13.6%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 82.1 points at 86.4% of the default cost, 13.6% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 76.6 points at 92.5% of the default cost, 7.5% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 82.1 points at 86.4% of the default cost, 13.6% under the budget it was given.
- `avg_gated_lookup` at 1.00x: deviated from the default cell on family F0. Verification margin +2.2 points, sd 3.9, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 13.6% of the budget, 86.4% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_hellaswag_ouro_2_6b_think
# Table 1 -- hellaswag (ouro_2_6b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 280620 layer passes over 1700 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 81.2 | +0.9 |
| default_cell | n/a | n/a | n/a | 76.8 (34%) | +5.3 |
| default_at_budget | n/a | 74.6 (30%) | 81.2 | 81.4 | +0.7 |
| lookup | 39.9 | 80.4 | 81.3 | 81.2 | +0.8 |
| equation | 39.9 | 74.4 | 78.9 | 78.9 | +3.1 |
| equation_n30 | 39.9 | 74.4 | 73.9 | 81.2 | +0.9 |
| equation_n100 | 39.9 | 74.4 | 73.9 | 80.7 | +1.4 |
| gated_equation | 39.9 | 74.9 | 80.7 | 81.4 | +0.7 |
| avg_lookup | 63.1 | 81.4 | 81.2 | 81.2 | +0.8 |
| avg_equation | 63.2 | 73.6 | 78.9 | 78.9 | +3.1 |
| avg_gated_lookup | 62.8 | 79.1 | 79.1 | 81.2 | +0.9 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 64, 82.1 points over 1700 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 69126 vs 70155 (-1.5%) | 137722 vs 140310 (-1.8%) | 199558 vs 210465 (-5.2%) | 199558 vs 280620 (-28.9%) |
| avg_equation | 69009 vs 70155 (-1.6%) | 141100 vs 140310 (+0.6%) | 196012 vs 210465 (-6.9%) | 196012 vs 280620 (-30.2%) |
| avg_gated_lookup | 68656 vs 70155 (-2.1%) | 112832 vs 140310 (-19.6%) | 112832 vs 210465 (-46.4%) | 281530 vs 280620 (+0.3%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 81.2 points at 71.1% of the default cost, 5.2% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 81.2 points at 71.1% of the default cost, 28.9% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 78.9 points at 69.8% of the default cost, 6.9% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 78.9 points at 69.8% of the default cost, 30.2% under the budget it was given.
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 79.1 points at 40.2% of the default cost, 19.6% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 79.1 points at 40.2% of the default cost, 46.4% under the budget it was given.
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin -3.3 points, sd 3.7, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving -0.3% of the budget, 100.3% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_math500_huginn_0125
# Table 1 -- math500 (huginn_0125), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 224131 layer passes over 400 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 15.0 | +0.8 |
| default_cell | n/a | n/a | n/a | 17.1 (84%) | -1.3 |
| default_at_budget | n/a | n/a | 15.5 (98%) | 15.1 (99%) | +0.6 |
| lookup | 8.2 | 15.2 | 15.5 | 15.8 | +0.0 |
| equation | 7.2 | 13.5 | 15.5 | 15.0 | +0.8 |
| equation_n30 | 7.2 | 6.2 | 15.2 | 15.0 | +0.8 |
| equation_n100 | 7.2 | 13.5 | 15.5 | 15.0 | +0.8 |
| gated_equation | 7.2 | 6.2 | 13.5 | 13.5 | +2.2 |
| avg_lookup | 13.2 | 15.5 | 15.8 | 15.8 | +0.0 |
| avg_equation | 12.8 | 15.5 | 15.2 | 15.0 | +0.8 |
| avg_gated_lookup | 10.8 | 14.5 | 15.2 | 15.0 | +0.8 |

The ORACLE GAP is the best single evaluation cell (depth 16 at cap 256, 15.8 points over 400 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2.

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 56995 vs 56033 (+1.7%) | 111911 vs 112065 (-0.1%) | 155466 vs 168098 (-7.5%) | 155466 vs 224131 (-30.6%) |
| avg_equation | 57531 vs 56033 (+2.7%) | 112240 vs 112065 (+0.2%) | 156677 vs 168098 (-6.8%) | 221433 vs 224131 (-1.2%) |
| avg_gated_lookup | 57977 vs 56033 (+3.5%) | 114051 vs 112065 (+1.8%) | 146866 vs 168098 (-12.6%) | 221433 vs 224131 (-1.2%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 15.8 points at 69.4% of the default cost, 7.5% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 15.8 points at 69.4% of the default cost, 30.6% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 15.0 points at 98.8% of the default cost, 1.2% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 15.2 points at 65.5% of the default cost, 12.6% under the budget it was given.
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin -3.3 points, sd 3.4, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 1.2% of the budget, 98.8% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_math500_mcleish_llama32_r32
# Table 1 -- math500 (mcleish_llama32_r32), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 96379 layer passes over 400 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 30.2 | +1.8 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | 30.6 (99%) | 30.0 | +2.0 |
| lookup | 23.2 | 32.0 | 28.7 | 28.7 | +3.3 |
| equation | 26.2 | 30.8 | 30.8 | 30.8 | +1.2 |
| equation_n30 | 26.2 | 30.8 | 29.8 | 30.0 | +2.0 |
| equation_n100 | 26.2 | 30.8 | 30.8 | 30.8 | +1.2 |
| gated_equation | 26.2 | 30.8 | 30.0 | 30.0 | +2.0 |
| avg_lookup | 26.5 | 30.8 | 28.7 | 28.7 | +3.3 |
| avg_equation | 24.8 | 30.8 | 30.2 | 31.0 | +1.0 |
| avg_gated_lookup | 26.2 | 30.8 | 28.7 | 28.7 | +3.3 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 256, 32.0 points over 400 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F3.

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 24717 vs 24095 (+2.6%) | 49327 vs 48189 (+2.4%) | 62558 vs 72284 (-13.5%) | 62558 vs 96379 (-35.1%) |
| avg_equation | 24581 vs 24095 (+2.0%) | 47988 vs 48189 (-0.4%) | 69440 vs 72284 (-3.9%) | 95287 vs 96379 (-1.1%) |
| avg_gated_lookup | 23323 vs 24095 (-3.2%) | 49327 vs 48189 (+2.4%) | 62558 vs 72284 (-13.5%) | 62558 vs 96379 (-35.1%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 28.7 points at 64.9% of the default cost, 13.5% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 28.7 points at 64.9% of the default cost, 35.1% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 28.7 points at 64.9% of the default cost, 13.5% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 28.7 points at 64.9% of the default cost, 35.1% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_math500_ouro_1_4b_base
# Table 1 -- math500 (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 178329 layer passes over 400 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 63.5 | +2.5 |
| default_cell | n/a | n/a | n/a | 67.5 (92%) | -1.5 |
| default_at_budget | n/a | n/a | 56.3 (99%) | 63.9 (100%) | +2.1 |
| lookup | 24.1 (100%) | 64.8 | 65.8 | 65.5 | +0.5 |
| equation | 25.6 (100%) | 64.2 | 66.2 | 66.0 | +0.0 |
| equation_n30 | 25.6 (100%) | 64.2 | 66.0 | 66.0 | +0.0 |
| equation_n100 | 25.6 (100%) | 64.2 | 66.2 | 66.0 | +0.0 |
| gated_equation | 25.6 (100%) | 64.2 | 66.2 (100%) | 63.5 | +2.5 |
| avg_lookup | 30.2 | 66.2 | 65.5 | 65.5 | +0.5 |
| avg_equation | 29.5 | 64.5 | 66.0 | 66.0 | +0.0 |
| avg_gated_lookup | 29.2 | 66.2 | 65.5 | 63.5 | +2.5 |

The ORACLE GAP is the best single evaluation cell (depth 3 at cap 4096, 66.0 points over 400 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 43608 vs 44582 (-2.2%) | 88144 vs 89164 (-1.1%) | 109654 vs 133746 (-18.0%) | 109654 vs 178329 (-38.5%) |
| avg_equation | 44948 vs 44582 (+0.8%) | 89988 vs 89164 (+0.9%) | 132753 vs 133746 (-0.7%) | 132753 vs 178329 (-25.6%) |
| avg_gated_lookup | 42499 vs 44582 (-4.7%) | 87700 vs 89164 (-1.6%) | 109654 vs 133746 (-18.0%) | 167182 vs 178329 (-6.3%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 65.5 points at 61.5% of the default cost, 18.0% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 65.5 points at 61.5% of the default cost, 38.5% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 66.0 points at 74.4% of the default cost, 25.6% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 65.5 points at 61.5% of the default cost, 18.0% under the budget it was given.
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin -3.3 points, sd 10.1, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 6.3% of the budget, 93.7% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_math500_ouro_1_4b_think
# Table 1 -- math500 (ouro_1_4b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 278580 layer passes over 400 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 89.8 | +0.0 |
| default_cell | n/a | n/a | n/a | 92.2 (90%) | -2.5 |
| default_at_budget | n/a | 36.9 (99%) | 75.8 | 88.0 | +1.8 |
| lookup | 32.2 | 76.8 | 86.2 | 89.8 | +0.0 |
| equation | 32.2 | 76.8 | 85.5 | 89.8 | +0.0 |
| equation_n30 | 32.2 | 76.8 | 77.0 | 77.0 | +12.8 |
| equation_n100 | 32.2 | 76.8 | 85.5 | 89.8 | +0.0 |
| gated_equation | 32.2 | 73.5 | 86.8 | 87.8 | +2.0 |
| avg_lookup | 58.8 | 77.5 | 87.2 | 89.8 | +0.0 |
| avg_equation | 59.0 | 76.8 | 80.5 | 89.8 | +0.0 |
| avg_gated_lookup | 50.7 | 77.5 | 87.2 | 89.8 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 4096, 89.8 points over 400 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 72388 vs 69645 (+3.9%) | 135279 vs 139290 (-2.9%) | 210098 vs 208935 (+0.6%) | 270654 vs 278580 (-2.8%) |
| avg_equation | 71867 vs 69645 (+3.2%) | 139407 vs 139290 (+0.1%) | 212413 vs 208935 (+1.7%) | 270654 vs 278580 (-2.8%) |
| avg_gated_lookup | 68953 vs 69645 (-1.0%) | 133540 vs 139290 (-4.1%) | 210964 vs 208935 (+1.0%) | 270654 vs 278580 (-2.8%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 89.8 points at 97.2% of the default cost, 2.8% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 89.8 points at 97.2% of the default cost, 2.8% under the budget it was given.
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 2.8% of the budget, 97.2% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_math500_ouro_2_6b_base
# Table 1 -- math500 (ouro_2_6b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 338737 layer passes over 400 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 56.0 | +0.0 |
| default_cell | n/a | n/a | n/a | 56.6 (98%) | -0.6 |
| default_at_budget | n/a | n/a | 55.1 (98%) | 56.1 (100%) | -0.1 |
| lookup | 31.3 (100%) | 53.0 | 53.8 | 53.5 | +2.5 |
| equation | 34.8 (100%) | 53.0 | 52.5 | 55.8 | +0.3 |
| equation_n30 | 34.8 (100%) | 53.0 | 52.5 | 52.5 | +3.5 |
| equation_n100 | 34.8 (100%) | 53.0 | 52.5 | 55.8 | +0.3 |
| gated_equation | 34.8 (100%) | 53.0 | 53.8 | 56.2 | -0.2 |
| avg_lookup | 35.2 | 53.8 | 53.5 | 53.5 | +2.5 |
| avg_equation | 36.8 | 52.5 | 54.5 | 56.0 | +0.0 |
| avg_gated_lookup | 35.8 | 54.2 | 55.5 | 56.0 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 4096, 56.0 points over 400 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 83347 vs 84684 (-1.6%) | 170761 vs 169369 (+0.8%) | 181071 vs 254053 (-28.7%) | 181071 vs 338737 (-46.5%) |
| avg_equation | 85709 vs 84684 (+1.2%) | 167582 vs 169369 (-1.1%) | 258292 vs 254053 (+1.7%) | 290726 vs 338737 (-14.2%) |
| avg_gated_lookup | 84779 vs 84684 (+0.1%) | 170825 vs 169369 (+0.9%) | 237671 vs 254053 (-6.4%) | 290726 vs 338737 (-14.2%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 53.5 points at 53.5% of the default cost, 28.7% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 53.5 points at 53.5% of the default cost, 46.5% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 56.0 points at 85.8% of the default cost, 14.2% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 55.5 points at 70.2% of the default cost, 6.4% under the budget it was given.
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin -6.7 points, sd 4.6, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 14.2% of the budget, 85.8% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_math500_ouro_2_6b_think
# Table 1 -- math500 (ouro_2_6b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 563241 layer passes over 400 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 91.2 | +0.0 |
| default_cell | n/a | n/a | n/a | 92.8 (93%) | -1.5 |
| default_at_budget | n/a | 41.7 (99%) | 75.8 | 90.0 | +1.2 |
| lookup | 44.2 | 78.8 | 83.8 | 90.0 | +1.2 |
| equation | 44.2 | 78.8 | 87.8 | 91.5 | -0.2 |
| equation_n30 | 44.2 | 78.8 | 81.8 | 89.8 | +1.5 |
| equation_n100 | 44.2 | 78.8 | 87.8 | 91.5 | -0.2 |
| gated_equation | 44.2 | 71.8 | 89.0 | 90.2 | +1.0 |
| avg_lookup | 51.0 | 79.8 | 85.0 | 91.2 | +0.0 |
| avg_equation | 48.2 | 81.2 | 84.5 | 91.2 | +0.0 |
| avg_gated_lookup | 62.3 | 79.8 | 85.0 | 91.2 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 3 at cap 4096, 91.2 points over 400 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 134887 vs 140810 (-4.2%) | 282470 vs 281621 (+0.3%) | 438666 vs 422431 (+3.8%) | 537649 vs 563241 (-4.5%) |
| avg_equation | 143080 vs 140810 (+1.6%) | 279695 vs 281621 (-0.7%) | 431373 vs 422431 (+2.1%) | 537649 vs 563241 (-4.5%) |
| avg_gated_lookup | 146944 vs 140810 (+4.4%) | 284731 vs 281621 (+1.1%) | 438666 vs 422431 (+3.8%) | 537649 vs 563241 (-4.5%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 91.2 points at 95.5% of the default cost, 4.5% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 91.2 points at 95.5% of the default cost, 4.5% under the budget it was given.
- `avg_gated_lookup` at 1.00x: reverted to the default cell for every question. Verification margin +0.0 points, sd 0.0, bar 0.50 sd (30 verification questions, the ids after the 70 that fit, out of 100 calibration); cost saving 4.5% of the budget, 95.5% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_mmlu_huginn_0125
# Table 1 -- mmlu (huginn_0125), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 85913 layer passes over 1700 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 36.3 | +3.1 |
| default_cell | n/a | n/a | n/a | 42.6 (52%) | -3.2 |
| default_at_budget | n/a | n/a | 39.7 (70%) | 37.2 (91%) | +2.1 |
| lookup | 29.0 | 35.1 | 35.5 | 35.5 | +3.9 |
| equation | 29.2 | 34.9 | 35.2 | 35.3 | +4.1 |
| equation_n30 | 26.4 | 35.4 | 35.2 | 35.3 | +4.1 |
| equation_n100 | 26.4 | 34.9 | 35.2 | 35.3 | +4.1 |
| gated_equation | 29.6 | 34.9 | 36.2 | 35.3 | +4.1 |
| avg_lookup | 32.8 | 35.5 | 35.5 | 35.5 | +3.9 |
| avg_equation | 33.3 | 35.5 | 35.3 | 35.3 | +4.1 |
| avg_gated_lookup | 32.5 | 35.5 | 35.5 | 35.5 | +3.9 |

The ORACLE GAP is the best single evaluation cell (depth 16 at cap 0, 39.4 points over 1700 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3.

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 20954 vs 21478 (-2.4%) | 36235 vs 42956 (-15.6%) | 36235 vs 64435 (-43.8%) | 36235 vs 85913 (-57.8%) |
| avg_equation | 20676 vs 21478 (-3.7%) | 42993 vs 42956 (+0.1%) | 45699 vs 64435 (-29.1%) | 45699 vs 85913 (-46.8%) |
| avg_gated_lookup | 20205 vs 21478 (-5.9%) | 36235 vs 42956 (-15.6%) | 36235 vs 64435 (-43.8%) | 36235 vs 85913 (-57.8%) |
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 35.5 points at 42.2% of the default cost, 15.6% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 35.5 points at 42.2% of the default cost, 43.8% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 35.5 points at 42.2% of the default cost, 57.8% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 35.3 points at 53.2% of the default cost, 29.1% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 35.3 points at 53.2% of the default cost, 46.8% under the budget it was given.
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 35.5 points at 42.2% of the default cost, 15.6% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 35.5 points at 42.2% of the default cost, 43.8% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 35.5 points at 42.2% of the default cost, 57.8% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_mmlu_mcleish_llama32_r32
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

## alloc_v5_mmlu_ouro_1_4b_base
# Table 1 -- mmlu (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 58952 layer passes over 1700 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 68.4 | +0.0 |
| default_cell | n/a | n/a | n/a | 71.7 (79%) | -3.4 |
| default_at_budget | n/a | n/a | 74.3 (41%) | 70.5 (89%) | -2.1 |
| lookup | 40.3 (89%) | 59.2 | 65.6 | 66.8 | +1.6 |
| equation | 40.6 (89%) | 58.9 | 64.6 | 67.8 | +0.6 |
| equation_n30 | 40.6 (89%) | 58.9 | 64.9 | 67.8 | +0.6 |
| equation_n100 | 40.6 (89%) | 58.9 | 64.8 | 67.9 | +0.4 |
| gated_equation | 40.6 (89%) | 58.9 | 65.4 | 68.7 (89%) | -0.3 |
| avg_lookup | 43.6 | 61.4 | 66.4 | 67.4 | +1.0 |
| avg_equation | 42.9 | 61.6 | 65.5 | 68.4 | +0.0 |
| avg_gated_lookup | 44.5 | 61.1 | 66.6 | 67.4 | +1.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 128, 68.4 points over 1700 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 14821 vs 14738 (+0.6%) | 29297 vs 29476 (-0.6%) | 44279 vs 44214 (+0.1%) | 47957 vs 58952 (-18.7%) |
| avg_equation | 14756 vs 14738 (+0.1%) | 29502 vs 29476 (+0.1%) | 44472 vs 44214 (+0.6%) | 55207 vs 58952 (-6.4%) |
| avg_gated_lookup | 14675 vs 14738 (-0.4%) | 30152 vs 29476 (+2.3%) | 45275 vs 44214 (+2.4%) | 47957 vs 58952 (-18.7%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 67.4 points at 81.3% of the default cost, 18.7% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.4 points at 93.6% of the default cost, 6.4% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 67.4 points at 81.3% of the default cost, 18.7% under the budget it was given.
- `avg_gated_lookup` at 1.00x: deviated from the default cell on family F0. Verification margin +6.7 points, sd 4.6, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 18.7% of the budget, 81.3% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_mmlu_ouro_1_4b_think
# Table 1 -- mmlu (ouro_1_4b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 134380 layer passes over 1700 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 73.6 | +0.4 |
| default_cell | n/a | n/a | n/a | 75.6 (44%) | -1.6 |
| default_at_budget | n/a | 66.2 (94%) | 70.6 | 73.7 | +0.3 |
| lookup | 58.2 | 70.1 | 73.4 | 73.8 | +0.2 |
| equation | 55.4 | 71.5 | 73.6 | 73.7 | +0.3 |
| equation_n30 | 56.2 | 69.2 | 73.5 | 74.0 | +0.0 |
| equation_n100 | 55.0 | 71.5 | 73.5 | 73.7 | +0.3 |
| gated_equation | 56.2 | 65.8 | 71.1 | 73.7 | +0.3 |
| avg_lookup | 63.6 | 71.7 | 73.0 | 73.6 | +0.4 |
| avg_equation | 60.2 | 71.2 | 73.6 | 73.8 | +0.2 |
| avg_gated_lookup | 63.4 | 71.6 | 72.5 | 72.5 | +1.5 |

The ORACLE GAP is the best single evaluation cell (depth 3 at cap 4096, 74.0 points over 1700 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 33419 vs 33595 (-0.5%) | 66895 vs 67190 (-0.4%) | 100879 vs 100785 (+0.1%) | 118412 vs 134380 (-11.9%) |
| avg_equation | 32467 vs 33595 (-3.4%) | 66581 vs 67190 (-0.9%) | 99026 vs 100785 (-1.7%) | 134496 vs 134380 (+0.1%) |
| avg_gated_lookup | 33311 vs 33595 (-0.8%) | 68075 vs 67190 (+1.3%) | 76239 vs 100785 (-24.4%) | 76239 vs 134380 (-43.3%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 73.6 points at 88.1% of the default cost, 11.9% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 72.5 points at 56.7% of the default cost, 24.4% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 72.5 points at 56.7% of the default cost, 43.3% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_mmlu_ouro_2_6b_base
# Table 1 -- mmlu (ouro_2_6b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 119579 layer passes over 1700 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 74.7 | +0.1 |
| default_cell | n/a | n/a | 100.0 (0%) | 76.8 (82%) | -1.9 |
| default_at_budget | n/a | n/a | 79.2 (46%) | 76.4 (90%) | -1.6 |
| lookup | 54.2 (90%) | 66.3 | 73.1 | 74.0 | +0.8 |
| equation | 52.1 (90%) | 65.9 | 72.4 | 74.1 | +0.8 |
| equation_n30 | 54.2 (90%) | 66.5 | 72.4 | 74.1 | +0.8 |
| equation_n100 | 52.1 (90%) | 65.9 | 72.4 | 74.1 | +0.7 |
| gated_equation | 52.1 (90%) | 65.9 | 80.2 (46%) | 75.4 (90%) | -0.6 |
| avg_lookup | 56.5 | 69.4 | 73.8 | 74.5 | +0.4 |
| avg_equation | 52.0 | 68.3 | 73.6 | 74.7 | +0.1 |
| avg_gated_lookup | 57.2 | 69.4 | 73.8 | 74.5 | +0.4 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 128, 74.8 points over 1700 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 29156 vs 29895 (-2.5%) | 59413 vs 59790 (-0.6%) | 89604 vs 89684 (-0.1%) | 95913 vs 119579 (-19.8%) |
| avg_equation | 29551 vs 29895 (-1.1%) | 59243 vs 59790 (-0.9%) | 90336 vs 89684 (+0.7%) | 107798 vs 119579 (-9.9%) |
| avg_gated_lookup | 30268 vs 29895 (+1.2%) | 59575 vs 59790 (-0.4%) | 89634 vs 89684 (-0.1%) | 95913 vs 119579 (-19.8%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 74.5 points at 80.2% of the default cost, 19.8% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 74.7 points at 90.1% of the default cost, 9.9% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 74.5 points at 80.2% of the default cost, 19.8% under the budget it was given.
- `avg_gated_lookup` at 1.00x: deviated from the default cell on family F0. Verification margin +2.2 points, sd 4.2, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 19.8% of the budget, 80.2% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_mmlu_ouro_2_6b_think
# Table 1 -- mmlu (ouro_2_6b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 240640 layer passes over 1700 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 79.6 | +1.9 |
| default_cell | n/a | n/a | n/a | 82.6 (21%) | -1.0 |
| default_at_budget | n/a | 75.2 (89%) | 77.2 | 79.4 | +2.2 |
| lookup | 65.4 | 72.9 | 81.2 | 81.6 | +0.0 |
| equation | 45.5 | 74.8 | 81.3 | 81.6 | +0.0 |
| equation_n30 | 45.5 | 67.7 | 81.5 | 79.9 | +1.7 |
| equation_n100 | 45.5 | 67.7 | 81.5 | 81.6 | +0.0 |
| gated_equation | 46.2 | 75.5 (99%) | 81.1 | 79.5 | +2.1 |
| avg_lookup | 69.8 | 75.8 | 81.6 | 81.6 | +0.0 |
| avg_equation | 62.7 | 76.2 | 81.6 | 81.6 | +0.0 |
| avg_gated_lookup | 67.9 | 75.4 | 81.5 | 81.5 | +0.1 |

The ORACLE GAP is the best single evaluation cell (depth 3 at cap 4096, 81.6 points over 1700 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2, F3.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 60156 vs 60160 (-0.0%) | 116982 vs 120320 (-2.8%) | 177720 vs 180480 (-1.5%) | 177720 vs 240640 (-26.1%) |
| avg_equation | 58248 vs 60160 (-3.2%) | 120402 vs 120320 (+0.1%) | 177720 vs 180480 (-1.5%) | 177720 vs 240640 (-26.1%) |
| avg_gated_lookup | 61495 vs 60160 (+2.2%) | 115377 vs 120320 (-4.1%) | 164435 vs 180480 (-8.9%) | 164435 vs 240640 (-31.7%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 81.6 points at 73.9% of the default cost, 1.5% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 81.6 points at 73.9% of the default cost, 26.1% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 81.6 points at 73.9% of the default cost, 1.5% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 81.6 points at 73.9% of the default cost, 26.1% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 81.5 points at 68.3% of the default cost, 8.9% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 81.5 points at 68.3% of the default cost, 31.7% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_strategyqa_huginn_0125
# Table 1 -- strategyqa (huginn_0125), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 118487 layer passes over 1990 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 55.5 | +1.3 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 56.3 | 56.8 | 56.4 | +0.4 |
| lookup | 56.0 | 56.4 | 56.4 | 56.4 | +0.4 |
| equation | 56.0 | 56.0 | 56.2 | 56.2 | +0.6 |
| equation_n30 | 56.0 | 56.0 | 56.2 | 56.2 | +0.6 |
| equation_n100 | 56.0 | 56.0 | 56.2 | 56.2 | +0.6 |
| gated_equation | 56.0 | 56.0 | 56.8 | 56.4 | +0.4 |
| avg_lookup | 56.2 | 56.4 | 56.4 | 56.4 | +0.4 |
| avg_equation | 56.0 | 56.2 | 56.2 | 56.2 | +0.6 |
| avg_gated_lookup | 56.1 | 55.5 | 55.6 | 55.6 | +1.2 |

The ORACLE GAP is the best single evaluation cell (depth 32 at cap 1024, 56.8 points over 1990 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2.

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 29540 vs 29622 (-0.3%) | 30168 vs 59244 (-49.1%) | 30168 vs 88865 (-66.1%) | 30168 vs 118487 (-74.5%) |
| avg_equation | 28560 vs 29622 (-3.6%) | 55798 vs 59244 (-5.8%) | 72592 vs 88865 (-18.3%) | 72592 vs 118487 (-38.7%) |
| avg_gated_lookup | 29285 vs 29622 (-1.1%) | 59762 vs 59244 (+0.9%) | 62338 vs 88865 (-29.9%) | 62338 vs 118487 (-47.4%) |
- `avg_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 56.4 points at 25.5% of the default cost, 49.1% under the budget it was given.
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 56.4 points at 25.5% of the default cost, 66.1% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 56.4 points at 25.5% of the default cost, 74.5% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 56.2 points at 61.3% of the default cost, 18.3% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 56.2 points at 61.3% of the default cost, 38.7% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 55.6 points at 52.6% of the default cost, 29.9% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 55.6 points at 52.6% of the default cost, 47.4% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_strategyqa_mcleish_llama32_r32
# Table 1 -- strategyqa (mcleish_llama32_r32), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 59356 layer passes over 1990 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 49.7 | +2.6 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 50.7 | 50.3 | 50.3 | +2.0 |
| lookup | 51.5 | 49.4 | 50.4 | 50.4 | +1.9 |
| equation | 49.8 | 50.7 | 50.3 | 50.3 | +2.0 |
| equation_n30 | 49.8 | 50.7 | 50.3 | 50.3 | +2.0 |
| equation_n100 | 50.1 | 50.7 | 50.3 | 50.3 | +2.0 |
| gated_equation | 49.8 | 50.7 | 50.3 | 50.3 | +2.0 |
| avg_lookup | 50.5 | 50.9 | 50.4 | 50.4 | +1.9 |
| avg_equation | 50.3 | 50.9 | 50.2 | 49.6 | +2.7 |
| avg_gated_lookup | 50.8 | 49.4 | 49.4 | 49.4 | +2.9 |

The ORACLE GAP is the best single evaluation cell (depth 2 at cap 128, 52.3 points over 1990 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: none.

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 14745 vs 14839 (-0.6%) | 29150 vs 29678 (-1.8%) | 30617 vs 44517 (-31.2%) | 30617 vs 59356 (-48.4%) |
| avg_equation | 14789 vs 14839 (-0.3%) | 29150 vs 29678 (-1.8%) | 43529 vs 44517 (-2.2%) | 58596 vs 59356 (-1.3%) |
| avg_gated_lookup | 14540 vs 14839 (-2.0%) | 17901 vs 29678 (-39.7%) | 17901 vs 44517 (-59.8%) | 17901 vs 59356 (-69.8%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 50.4 points at 51.6% of the default cost, 31.2% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 50.4 points at 51.6% of the default cost, 48.4% under the budget it was given.
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 49.4 points at 30.2% of the default cost, 39.7% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 49.4 points at 30.2% of the default cost, 59.8% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 49.4 points at 30.2% of the default cost, 69.8% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_strategyqa_ouro_1_4b_base
# Table 1 -- strategyqa (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 59025 layer passes over 1990 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 66.5 | +1.9 |
| default_cell | n/a | n/a | n/a | 66.4 (100%) | +2.0 |
| default_at_budget | n/a | n/a | 66.8 | 66.5 | +1.9 |
| lookup | 55.5 | 64.4 | 68.1 | 68.1 | +0.3 |
| equation | 53.8 | 66.6 | 68.1 | 67.7 | +0.7 |
| equation_n30 | 53.8 | 52.7 | 52.0 | 52.0 | +16.4 |
| equation_n100 | 53.8 | 63.0 | 66.8 | 66.6 | +1.8 |
| gated_equation | 53.8 | 66.5 | 63.8 | 63.8 | +4.6 |
| avg_lookup | 61.2 | 68.0 | 68.1 | 68.1 | +0.3 |
| avg_equation | 55.1 | 67.0 | 68.0 | 67.7 | +0.7 |
| avg_gated_lookup | 61.2 | 67.8 | 68.1 | 63.8 | +4.6 |

The ORACLE GAP is the best single evaluation cell (depth 3 at cap 128, 68.4 points over 1990 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F0.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x yes.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 14326 vs 14756 (-2.9%) | 29264 vs 29513 (-0.8%) | 30423 vs 44269 (-31.3%) | 30423 vs 59025 (-48.5%) |
| avg_equation | 13178 vs 14756 (-10.7%) | 29244 vs 29513 (-0.9%) | 44303 vs 44269 (+0.1%) | 48331 vs 59025 (-18.1%) |
| avg_gated_lookup | 14326 vs 14756 (-2.9%) | 29613 vs 29513 (+0.3%) | 30423 vs 44269 (-31.3%) | 35861 vs 59025 (-39.2%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 68.1 points at 51.5% of the default cost, 31.3% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 68.1 points at 51.5% of the default cost, 48.5% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 67.7 points at 81.9% of the default cost, 18.1% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 68.1 points at 51.5% of the default cost, 31.3% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 63.8 points at 60.8% of the default cost, 39.2% under the budget it was given.
- `avg_gated_lookup` at 1.00x: deviated from the default cell on family F0. Verification margin +13.3 points, sd 5.8, bar 0.50 sd (90 verification questions, the ids after the 210 that fit, out of 300 calibration); cost saving 39.2% of the budget, 60.8% of the default cost.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_strategyqa_ouro_1_4b_think
# Table 1 -- strategyqa (ouro_1_4b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 108565 layer passes over 1990 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 72.4 | +0.2 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 69.7 | 72.2 | 72.6 | +0.0 |
| lookup | 61.0 | 69.7 | 71.0 | 71.0 | +1.6 |
| equation | 61.0 | 69.7 | 71.0 | 72.6 | +0.0 |
| equation_n30 | 61.0 | 67.5 | 72.2 | 72.6 | +0.0 |
| equation_n100 | 61.0 | 67.5 | 72.2 | 72.6 | +0.0 |
| gated_equation | 61.0 | 69.7 | 72.2 | 72.6 | +0.0 |
| avg_lookup | 63.3 | 69.6 | 71.0 | 71.0 | +1.6 |
| avg_equation | 63.0 | 70.9 | 70.6 | 72.3 | +0.3 |
| avg_gated_lookup | 63.4 | 68.4 | 71.0 | 71.0 | +1.6 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 2048, 72.6 points over 1990 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 27219 vs 27141 (+0.3%) | 53763 vs 54283 (-1.0%) | 75772 vs 81424 (-6.9%) | 75772 vs 108565 (-30.2%) |
| avg_equation | 26631 vs 27141 (-1.9%) | 53450 vs 54283 (-1.5%) | 80302 vs 81424 (-1.4%) | 108728 vs 108565 (+0.1%) |
| avg_gated_lookup | 26669 vs 27141 (-1.7%) | 53301 vs 54283 (-1.8%) | 75772 vs 81424 (-6.9%) | 75772 vs 108565 (-30.2%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 71.0 points at 69.8% of the default cost, 6.9% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 71.0 points at 69.8% of the default cost, 30.2% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 71.0 points at 69.8% of the default cost, 6.9% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 71.0 points at 69.8% of the default cost, 30.2% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_strategyqa_ouro_2_6b_base
# Table 1 -- strategyqa (ouro_2_6b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 98679 layer passes over 1990 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 74.8 | +0.3 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | 74.3 (100%) | 74.8 | +0.3 |
| lookup | 59.8 | 69.7 | 73.7 | 74.7 | +0.5 |
| equation | 59.7 | 69.9 | 73.8 | 74.9 | +0.3 |
| equation_n30 | 59.8 | 69.9 | 73.7 | 74.9 | +0.3 |
| equation_n100 | 59.7 | 69.9 | 73.8 | 74.9 | +0.3 |
| gated_equation | 59.7 | 69.9 | 73.8 | 74.8 | +0.3 |
| avg_lookup | 62.5 | 71.4 | 74.0 | 74.7 | +0.5 |
| avg_equation | 61.8 | 70.7 | 74.4 | 74.9 | +0.3 |
| avg_gated_lookup | 61.7 | 71.5 | 74.0 | 74.7 | +0.5 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 128, 75.1 points over 1990 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 23860 vs 24670 (-3.3%) | 49417 vs 49339 (+0.2%) | 73814 vs 74009 (-0.3%) | 81127 vs 98679 (-17.8%) |
| avg_equation | 22777 vs 24670 (-7.7%) | 47986 vs 49339 (-2.7%) | 73169 vs 74009 (-1.1%) | 96621 vs 98679 (-2.1%) |
| avg_gated_lookup | 22594 vs 24670 (-8.4%) | 49097 vs 49339 (-0.5%) | 73814 vs 74009 (-0.3%) | 81127 vs 98679 (-17.8%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 74.7 points at 82.2% of the default cost, 17.8% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 74.7 points at 82.2% of the default cost, 17.8% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_strategyqa_ouro_2_6b_think
# Table 1 -- strategyqa (ouro_2_6b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 194101 layer passes over 1990 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 77.8 | +1.3 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 74.6 | 78.0 | 77.9 | +1.2 |
| lookup | 59.7 | 77.5 | 78.6 | 78.6 | +0.5 |
| equation | 59.7 | 77.5 | 78.6 | 77.9 | +1.2 |
| equation_n30 | 59.7 | 77.5 | 78.6 | 77.9 | +1.2 |
| equation_n100 | 59.7 | 77.5 | 78.6 | 77.9 | +1.2 |
| gated_equation | 59.7 | 77.5 | 78.6 | 78.6 | +0.5 |
| avg_lookup | 67.5 | 76.9 | 78.6 | 78.6 | +0.5 |
| avg_equation | 66.8 | 77.8 | 78.5 | 77.9 | +1.2 |
| avg_gated_lookup | 67.5 | 76.9 | 79.1 | 79.1 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 3 at cap 512, 79.1 points over 1990 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 49083 vs 48525 (+1.2%) | 93847 vs 97050 (-3.3%) | 139280 vs 145576 (-4.3%) | 139280 vs 194101 (-28.2%) |
| avg_equation | 47391 vs 48525 (-2.3%) | 95065 vs 97050 (-2.0%) | 141962 vs 145576 (-2.5%) | 189443 vs 194101 (-2.4%) |
| avg_gated_lookup | 49083 vs 48525 (+1.2%) | 93847 vs 97050 (-3.3%) | 118132 vs 145576 (-18.9%) | 118132 vs 194101 (-39.1%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 78.6 points at 71.8% of the default cost, 4.3% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 78.6 points at 71.8% of the default cost, 28.2% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 77.9 points at 97.6% of the default cost, 2.4% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 79.1 points at 60.9% of the default cost, 18.9% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 79.1 points at 60.9% of the default cost, 39.1% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_svamp_huginn_0125
# Table 1 -- svamp (huginn_0125), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 84875 layer passes over 200 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 44.5 | +0.0 |
| default_cell | n/a | n/a | n/a | 58.8 (40%) | -14.2 |
| default_at_budget | n/a | n/a | n/a | 40.0 | +4.5 |
| lookup | 4.5 | 27.5 | 39.5 | 39.5 | +5.0 |
| equation | 3.5 | 28.0 | 39.5 | 41.0 | +3.5 |
| equation_n30 | 3.5 | 20.0 | 20.0 | 20.0 | +24.5 |
| equation_n100 | 3.5 | 28.0 | 39.5 | 41.0 | +3.5 |
| gated_equation | 3.5 | 21.0 | 39.5 | 41.5 | +3.0 |
| avg_lookup | 18.0 | 38.0 | 39.5 | 39.5 | +5.0 |
| avg_equation | 19.5 | 38.0 | 41.5 | 45.0 | -0.5 |
| avg_gated_lookup | 18.0 | 37.5 | 39.5 | 39.5 | +5.0 |

The ORACLE GAP is the best single evaluation cell (depth 32 at cap 128, 44.5 points over 200 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F3.

`default_cell` is the default operating point (depth 32 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 21280 vs 21219 (+0.3%) | 42712 vs 42438 (+0.6%) | 43791 vs 63657 (-31.2%) | 43791 vs 84875 (-48.4%) |
| avg_equation | 21562 vs 21219 (+1.6%) | 42728 vs 42438 (+0.7%) | 67841 vs 63657 (+6.6%) | 83838 vs 84875 (-1.2%) |
| avg_gated_lookup | 21267 vs 21219 (+0.2%) | 41755 vs 42438 (-1.6%) | 43791 vs 63657 (-31.2%) | 43791 vs 84875 (-48.4%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 39.5 points at 51.6% of the default cost, 31.2% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 39.5 points at 51.6% of the default cost, 48.4% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 39.5 points at 51.6% of the default cost, 31.2% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 39.5 points at 51.6% of the default cost, 48.4% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_svamp_mcleish_llama32_r32
# Table 1 -- svamp (mcleish_llama32_r32), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 32123 layer passes over 200 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 69.0 | +0.0 |
| default_cell | n/a | n/a | n/a | 77.2 (50%) | -8.2 |
| default_at_budget | n/a | n/a | n/a | 56.5 | +12.5 |
| lookup | 22.5 | 33.0 | 62.0 | 66.5 | +2.5 |
| equation | 24.0 | 39.0 | 63.0 | 67.0 | +2.0 |
| equation_n30 | 24.0 | 39.0 | 63.0 | 67.0 | +2.0 |
| equation_n100 | 24.0 | 39.0 | 63.0 | 67.0 | +2.0 |
| gated_equation | 24.0 | 39.0 | 63.0 | 57.0 | +12.0 |
| avg_lookup | 26.5 | 53.5 | 66.5 | 68.5 | +0.5 |
| avg_equation | 25.5 | 56.5 | 67.0 | 68.5 | +0.5 |
| avg_gated_lookup | 25.5 | 52.5 | 66.5 | 68.5 | +0.5 |

The ORACLE GAP is the best single evaluation cell (depth 8 at cap 128, 69.0 points over 200 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F3.

`default_cell` is the default operating point (depth 8 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 8144 vs 8031 (+1.4%) | 16543 vs 16062 (+3.0%) | 25213 vs 24092 (+4.7%) | 32048 vs 32123 (-0.2%) |
| avg_equation | 7994 vs 8031 (-0.5%) | 16737 vs 16062 (+4.2%) | 25471 vs 24092 (+5.7%) | 32062 vs 32123 (-0.2%) |
| avg_gated_lookup | 8260 vs 8031 (+2.9%) | 16437 vs 16062 (+2.3%) | 25213 vs 24092 (+4.7%) | 32048 vs 32123 (-0.2%) |

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_svamp_ouro_1_4b_base
# Table 1 -- svamp (ouro_1_4b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 65870 layer passes over 200 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 86.5 | +0.0 |
| default_cell | n/a | n/a | n/a | 92.4 (33%) | -5.9 |
| default_at_budget | n/a | n/a | n/a | 75.0 | +11.5 |
| lookup | 30.0 | 62.5 | 76.5 | 84.0 | +2.5 |
| equation | 33.5 | 62.5 | 77.0 | 86.5 | +0.0 |
| equation_n30 | 33.5 | 62.0 | 75.0 | 86.5 | +0.0 |
| equation_n100 | 33.5 | 62.5 | 77.0 | 86.5 | +0.0 |
| gated_equation | 33.5 | 62.5 | 77.0 | 85.5 | +1.0 |
| avg_lookup | 35.5 | 70.5 | 84.0 | 84.0 | +2.5 |
| avg_equation | 34.5 | 71.0 | 85.0 | 86.0 | +0.5 |
| avg_gated_lookup | 38.0 | 70.5 | 84.0 | 85.5 | +1.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 256, 86.5 points over 200 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 16356 vs 16467 (-0.7%) | 32711 vs 32935 (-0.7%) | 49213 vs 49402 (-0.4%) | 49643 vs 65870 (-24.6%) |
| avg_equation | 16379 vs 16467 (-0.5%) | 32782 vs 32935 (-0.5%) | 49282 vs 49402 (-0.2%) | 65770 vs 65870 (-0.2%) |
| avg_gated_lookup | 16467 vs 16467 (-0.0%) | 32711 vs 32935 (-0.7%) | 49213 vs 49402 (-0.4%) | 65277 vs 65870 (-0.9%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 84.0 points at 75.4% of the default cost, 24.6% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_svamp_ouro_1_4b_think
# Table 1 -- svamp (ouro_1_4b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 129897 layer passes over 200 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 89.5 | +0.5 |
| default_cell | n/a | n/a | n/a | 93.1 (50%) | -3.1 |
| default_at_budget | n/a | 59.5 (98%) | 88.5 | 89.5 | +0.5 |
| lookup | 47.5 | 87.0 | 87.5 | 87.5 | +2.5 |
| equation | 52.5 | 86.5 | 87.5 | 87.5 | +2.5 |
| equation_n30 | 52.5 | 86.5 | 87.5 | 87.5 | +2.5 |
| equation_n100 | 52.5 | 86.5 | 87.5 | 87.5 | +2.5 |
| gated_equation | 52.5 | 77.5 | 87.5 | 87.5 | +2.5 |
| avg_lookup | 61.5 | 88.0 | 87.5 | 87.5 | +2.5 |
| avg_equation | 64.0 | 87.0 | 87.5 | 87.5 | +2.5 |
| avg_gated_lookup | 64.0 | 87.0 | 87.0 | 87.0 | +3.0 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 2048, 90.0 points over 200 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 34920 vs 32474 (+7.5%) | 67981 vs 64949 (+4.7%) | 90826 vs 97423 (-6.8%) | 90826 vs 129897 (-30.1%) |
| avg_equation | 34470 vs 32474 (+6.1%) | 65774 vs 64949 (+1.3%) | 90826 vs 97423 (-6.8%) | 90826 vs 129897 (-30.1%) |
| avg_gated_lookup | 34470 vs 32474 (+6.1%) | 54122 vs 64949 (-16.7%) | 54122 vs 97423 (-44.4%) | 54122 vs 129897 (-58.3%) |
- `avg_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 87.5 points at 69.9% of the default cost, 6.8% under the budget it was given.
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 87.5 points at 69.9% of the default cost, 30.1% under the budget it was given.
- `avg_equation` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 87.5 points at 69.9% of the default cost, 6.8% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 87.5 points at 69.9% of the default cost, 30.1% under the budget it was given.
- `avg_gated_lookup` at 0.50x: the multiplier is 0, so the budget never binds. The row is the same 87.0 points at 41.7% of the default cost, 16.7% under the budget it was given.
- `avg_gated_lookup` at 0.75x: the multiplier is 0, so the budget never binds. The row is the same 87.0 points at 41.7% of the default cost, 44.4% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 87.0 points at 41.7% of the default cost, 58.3% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_svamp_ouro_2_6b_base
# Table 1 -- svamp (ouro_2_6b_base), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 131236 layer passes over 200 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 83.0 | +0.0 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | n/a | n/a | 72.0 | +11.0 |
| lookup | 40.0 | 68.0 | 76.0 | 82.5 | +0.5 |
| equation | 40.5 | 67.5 | 76.5 | 82.5 | +0.5 |
| equation_n30 | 40.5 | 68.5 | 76.5 | 83.5 | -0.5 |
| equation_n100 | 40.5 | 67.5 | 76.5 | 82.5 | +0.5 |
| gated_equation | 40.5 | 68.5 | 76.0 | 82.5 | +0.5 |
| avg_lookup | 47.0 | 79.5 | 82.5 | 82.5 | +0.5 |
| avg_equation | 37.0 | 80.0 | 83.0 | 82.5 | +0.5 |
| avg_gated_lookup | 41.0 | 79.5 | 82.5 | 82.5 | +0.5 |

The ORACLE GAP is the best single evaluation cell (depth 4 at cap 128, 83.0 points over 200 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F2.

`default_cell` is the default operating point (depth 4 at cap 4096) priced per prompt under expected accounting: the share in brackets is how often the allocator could buy the default's own operating point at that budget, and the accuracy above it is over those questions only, which are the cheaper -- and so the easier -- ones. Affordable ON AVERAGE over the questions: 0.25x no, 0.50x no, 0.75x no, 1.00x no.

`avg_lookup` and `avg_equation` hold the MEAN price over questions at or below the budget instead of capping every question, so the default cell for every question is one feasible policy and these rows are comparable with the `default` row itself. Realised mean price over the evaluation questions, against the budget the multiplier was fitted to:

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default |
|---|---|---|---|---|
| avg_lookup | 32852 vs 32809 (+0.1%) | 65206 vs 65618 (-0.6%) | 97963 vs 98427 (-0.5%) | 98646 vs 131236 (-24.8%) |
| avg_equation | 32554 vs 32809 (-0.8%) | 65209 vs 65618 (-0.6%) | 98721 vs 98427 (+0.3%) | 99958 vs 131236 (-23.8%) |
| avg_gated_lookup | 32688 vs 32809 (-0.4%) | 65038 vs 65618 (-0.9%) | 97793 vs 98427 (-0.6%) | 98646 vs 131236 (-24.8%) |
- `avg_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 82.5 points at 75.2% of the default cost, 24.8% under the budget it was given.
- `avg_equation` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 82.5 points at 76.2% of the default cost, 23.8% under the budget it was given.
- `avg_gated_lookup` at 1.00x: the multiplier is 0, so the budget never binds. The row is the same 82.5 points at 75.2% of the default cost, 24.8% under the budget it was given.

`not feasible` = the arm itself costs more than that budget, so it cannot be run there at all. `n/a` = the arm could run in principle but no question can afford any of its cells at that budget. A percentage in brackets is the share of questions that could afford the arm, and the mean above it is over those questions only.

## alloc_v5_svamp_ouro_2_6b_think
# Table 1 -- svamp (ouro_2_6b_think), expected accounting

Budget = a fraction of the DEFAULT COST, the mean realised layer-pass cost of the max depth at its natural stop, uncapped: 249394 layer passes over 200 questions (0.0% of them counted at the horizon). The budgets do not depend on the accounting; what each arm is CHARGED does.

| arm | 0.25 x default | 0.50 x default | 0.75 x default | 1.00 x default | oracle gap @1.00x |
|---|---|---|---|---|---|
| default | not feasible | not feasible | not feasible | 7.0 | +61.5 |
| default_cell | n/a | n/a | n/a | n/a | n/a |
| default_at_budget | n/a | 5.6 (45%) | 12.5 | 6.5 | +62.0 |
| lookup | 68.5 | 68.5 | 68.5 | 68.5 | +0.0 |
| equation | 68.5 | 68.5 | 68.5 | 68.5 | +0.0 |
| equation_n30 | 68.5 | 68.5 | 68.5 | 68.5 | +0.0 |
| equation_n100 | 68.5 | 68.5 | 68.5 | 68.5 | +0.0 |
| gated_equation | 68.5 | 68.5 | 68.5 | 68.5 | +0.0 |
| avg_lookup | 68.5 | 68.5 | 68.5 | 68.5 | +0.0 |
| avg_equation | 68.5 | 68.5 | 68.5 | 68.5 | +0.0 |
| avg_gated_lookup | 68.5 | 68.5 | 68.5 | 68.5 | +0.0 |

The ORACLE GAP is the best single evaluation cell (depth 1 at cap 1024, 68.5 points over 200 questions) minus each arm at 1.00x. It reads the EVALUATION labels, so it is a diagnostic and never a policy result: no allocator can pick that cell, because picking it needs the labels it is scored on. The gap is the price of calibration noise -- what the arm gives up by having to find the cell from the calibration questions. A negative gap means the arm beat every single cell by varying the cell per question.

Deviation families opened at some budget: F3.

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

