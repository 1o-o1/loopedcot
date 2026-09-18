# The allocator

Pick, per question and per compute budget, how many loop passes to run and how many tokens of chain
to allow before forcing the answer out. CPU, numpy only, no imports from any other directory.

## Frozen defaults (2026-09-18)

Both rulings come off the 60-pair run under `work/analysis_2026-09-18`: `equation_v6` (one fold)
against `equation_v6_folds2` (two folds), expected accounting, 1.0x of the default cost.

**1. Two folds are the default** (`policy.GATE_FOLDS = 2`). A deviation has to be earned in both
directions of the calibration split: fit on half A and verify on half B, then fit on B and verify on
A, and deviate only when both verified margins clear `c_gate * sd`. At 1.0x it removed every FALSE
deviation -- one that loses to its own fallback on the evaluation questions -- for both gated arms:

| arm | deviations | false at two folds | mean gain @1.0x | cost saving @1.0x |
|---|---|---|---|---|
| `avg_gated_lookup` | 31 -> 22 | 0 | 1.22 -> 1.45 | 42% -> 35% |
| `avg_gated_equation_resolved` | 34 -> 25 | 0 | 0.95 -> 1.13 | 42% -> 35% |

Nine deviations fell in each arm and the mean gain went UP, because what fell did not repay. The
saving is smaller for the same reason: a withheld deviation runs the dearer fallback.
`--gate-folds 1` is the one-direction gate, kept for comparison.

**2. The ranking of record is `equation_resolved`**, the settle-time-resolved commitment identity
(`policy.RANKING_OF_RECORD`). It is statistically indistinguishable from the lookup on 58 of the 60
pairs, and it is the one the mechanism justifies: the lookup is a table of measured cell means with
no account of WHEN a question commits, so it can only repeat what the calibration labels happened to
say. So `avg_gated_equation_resolved` leads the CLI's arm list and Table 1 and `avg_gated_lookup`
comes second, as the label-only baseline the resolved arm is read against; every other arm is still
available (`policy.AVG_ARMS`).

Every `results.json` header carries both: `ranking_of_record` and `gate_folds`.

## The three stages

1. **Measure.** Run the model over a grid of **cells** `(k, T)`: `k` loop passes per token, `T`
   tokens of chain before a forced read-out. Each cell gives each question a label, a read-out, a
   price.
2. **Calibrate.** On held-out *calibration* questions, put the cells in one total order. Two orders
   are built, and they agree within noise.
3. **Allocate.** For each *evaluation* question and budget, run the first cell of that order the
   question can afford, against **normal operation**: deepest depth, largest affordable cap.

## Cost

The price of a cell for question `i`, in layer-token passes:

    cost(k, T, i) = (L_fixed + k * L) * (P_i + T + R_i)
    prompt-free   = (L_fixed + k * L) * (T + R_i)

`L` is the layers inside one loop pass, `L_fixed` the layers paid once per token whatever `k` is,
`P_i` the prompt length. The layer counts differ by family and nothing guesses them: a fully
recurrent stack has `L = layers, L_fixed = 0` (24 and 48 for the two sizes here); a fixed prelude
and coda around a recurrent core gives `L = core, L_fixed = prelude + coda` (2/4/2 -> 4 and 4;
4/6/4 -> 6 and 8). Pin them with `--layers-per-loop` and `--fixed-layers`, or point `--model-config`
at a production config file to read that model's `layers` or `prelude`/`core`/`coda` keys. Any
checkpoint but the 24-layer fully recurrent one is refused rather than priced at a default.

`R_i` is the **reserve**: the tokens paid for after the chain, whatever the model actually writes.

    R_i = suffix tokens + the task's answer budget     numeric 8 (12 on GSM8K), maths 32,
                                                       letter 8, yes/no 8, free-form 48

The reserve is deliberately *not* read off the row: some cell files store the **realised** read-out
length in that field (3 to 5 tokens) and others store the **reserve** (12 or 32), so reading it
would price two checkpoints of one task differently and split their feasibility and their pairing.
The realised count is kept as `answer_tokens_realised` and never enters a price.

### The three accountings

`--accounting` picks how a cell is charged. The reserve and the layer counts are the same in all
three; only the chain length differs.

| accounting | what cell `(k, T)` costs question `i` | known before generating |
|---|---|---|
| `cap` | `(L_fixed + k L)(P_i + T + R_i)` | yes |
| `expected` | `(L_fixed + k L)(P_i + E_cal[min(len_k, T)] + R_i)` | yes |
| `realised` | that question's own measured layer passes at that cell | no |

`E_cal[min(len_k, T)]` is the mean, over the **calibration** questions, of the length they generated
at depth `k` cut at `T`. The largest cap (or an explicit negative "no cap") stands for natural stop,
so the last column of that table is the mean natural length. The evaluation question's own length
never prices it: it is not known when the cell is chosen, and using it would price a cell with the
answer it is buying.

**Which comparison each supports.** Under a *hard per-prompt cap* the allocator is read against
`default_at_budget`, normal operation under the same cap, because a budget set at the **mean** cost
of a run cannot buy that run for the questions priced above the mean, whatever the accounting.
Under an *average budget* it is read against the uncapped `default` row, and there `expected` is the
accounting that makes the two commensurable: `cap` charges a natural-stop cell for a cap it never
writes, so the default's own operating point is unaffordable at its own cost (0 percent of
questions at 1.0x on both real tasks, against 71 and 76 percent under `expected`, and affordable on
average). `realised` is an audit price only -- it needs the generation it is pricing, so no
allocator can decide with it -- and it is kept to bound what perfect length foresight would buy.

**Budgets** are 16 log-spaced points from the cheapest to the dearest cell, both priced at the
median prompt. The endpoints are exactly those two prices; the float slack lives in the
affordability test (`policy.affordable`), inclusive to a relative `1e-9`. Two named ranges: `B*` =
budgets where the deepest depth fits at cap 64; `B_low` = where it does not but the shallowest does.

The **default cost** is a statistic, not a formula: the mean realised layer-pass cost of the deepest
depth run to its natural stop. A question that never stops inside the largest cap is counted at that
cap, not skipped, and its share is reported.

The depth and cap sets are whatever the rows hold, so a grid running to cap 4096 and depth 32 loads
whole. `--ks` and `--caps` narrow that to a subset; a depth or cap the rows lack is an error.

## The three rankings

**lookup** ranks cells by accuracy on the calibration questions. Ties go to the lower price at the
median prompt, then the lower depth and cap, so the order is deterministic; a cell with no
calibration observation sorts last.

**equation** ranks cells by a predicted accuracy built from one label-free curve and two labelled
numbers per depth:

    G_k(T)     share of calibration questions ARRIVED at (k, T)   -- read-outs only, no labels
    c_k        accuracy of the arrived (question, cap) cells at k -- labels
    l_k        accuracy of the not-yet-arrived cells at k         -- labels
    A_hat(k,T) = G_k(T) * c_k + (1 - G_k(T)) * l_k

A question has **arrived** at cap `T` at depth `k` when the forced read-out at every cap from `T` up
to the largest loaded cap equals the read-out at that largest cap. No gold label and no
answer-string search, so `G` costs no labels; a read-out that does not parse never equals anything
and so never arrives. (Prefix Consistency, Lanham arXiv 2307.13702 — the one external source here.)

`c_k` and `l_k` are the only labelled inputs and come from the first `n_labels` calibration
questions in id order, so labels can be traded against accuracy. `l_k` falls back to `c_k` at a
depth where every cell has arrived and the `(1 - G)` term is zero anyway. The card reports how well
`A_hat` reconstructs the measured surface next to a **noise floor**: the error a perfect surface
would still show, since the measured accuracy is itself a mean of `n_labels` coin flips.
No evaluation label reaches any ranking; every ranking function rejects non-calibration positions.

**equation_resolved** is the same identity RESOLVED BY SETTLE TIME. A question's settle cap
`s_k(n)` is the FIRST cap it has arrived at -- the arrival Boolean is a suffix in the cap, so that
cap is well defined -- and a question that never stops moving, or whose last read-out does not
parse, settles `never`, encoded beyond the last cap and never at it. Then

    P_k(s=j)   share of calibration questions whose settle cap is j   -- read-outs only, no labels
    c_k(j)     accuracy of the questions that settled at cap j        -- labels, read at the last cap
    l_k(T)     accuracy at cap T of the questions not settled by T    -- labels
    A_res(k,T) = sum_{j<=T} P_k(s=j) c_k(j) + P_k(s>T) l_k(T)

`c_k(j)` is well defined because a question settled at `j` carries the same read-out, and so the
same label, at every cap from `j` on. The two terms partition the same questions, so `A_res`
reproduces the calibration surface exactly once every settle cap is estimated from its own labels.

Why it exists: the pooled surface is `G c_k + (1 - G) l_k` with one `c_k` per depth, so wherever
`c_k > l_k` it RISES with `T` and can never rank the first cap first. On the class sets the first
answer is the good one -- first-answer accuracy beats the later settlers' by about 20 points and
nearly half the questions settle at cap 0 -- and the best evaluation cell is a cap-0 cell on 14 of
the 60 production grids. The pooled surface finds a cap-0 optimum on 1 of them, the resolved one on
8. Per-cell evaluation RMSE at 100 labels falls from 4.95 to 4.59 points; at 30 labels it RISES to
8.28 against 7.30, because one `c` per settle cap is many more numbers than one per depth and 30
labels cannot fill them.

**Sparse settle caps.** A settle cap holding fewer than `mechanism.MIN_SETTLE_LABELS` (8) labelled
calibration questions takes its bin's pooled `c` instead of its own; bins are
`0 / 16-32 / 64-128 / 256-512 / 1024-4096` (`mechanism.SETTLE_BINS`), and a bin that is itself short
falls back to the depth's pooled `c` -- the number the pooled identity carries. A cap the table does
not cover pools by octave pair and can never join a table bin. Every fallback is counted
(`c_source`, `n_caps_own`, `n_caps_binned`, `n_caps_pooled`, and the `_with_mass` counts, which say
how many fallbacks a cap with calibration mass behind it actually used).

`equation_resolved` is usable everywhere `equation` is: the hard per-prompt cap
(`equation_resolved`, `gated_equation_resolved`), the average budget (`avg_equation_resolved`,
`avg_gated_equation_resolved`), and the measured split gate with the deviation families. `n_labels`
takes the same subset the pooled version takes, the first `n_labels` calibration ids in id order.
It is the RANKING OF RECORD (see Frozen defaults), with `lookup` as the label-only baseline.

## The gate

At a given budget the allocator's pick can be worse than normal operation. The gate keeps normal
unless the MEASURED margin clears its own uncertainty:

    run the pick  iff  mean_ver[ acc(pick) - acc(normal) ] > c_gate * s
    s = the paired bootstrap SD of that same difference over the verification questions

The margin is the two cells' own labels on the verification questions, differenced question by
question, and never the surface's prediction of it. `A_hat` ranks the cells; only the labels can
say whether the cell it ranked first is better. Where the equation's assumption fails -- a task
whose early read-out is committed and wrong, so the depth's committed mean is dragged up by the one
cell that is accurate at the horizon -- the predicted margin has the wrong sign, and a gate reading
it opens on a deviation that loses points. `c_gate = 0` demands only a strictly positive margin.
**`c_gate = 0.5` is the frozen default**: swept over `{0, 0.5, 1, 1.5, 2}` on seven tasks under
"maximise mean gain over normal subject to a worst-case per-budget loss no worse than -1 point".
`c = 0` breaks the constraint; `0.5` satisfies it at the highest mean gain and wins every
leave-one-task-out fold. It is re-confirmed against `1.0` in the twenty-grid sweep below, where at
the frozen split the two carry the same deviations and the same cost saving and `0.5` gains +0.83
points at 1.0x against `1.0`'s +0.80. `evaluate.gate_selection` reruns the sweep, splitting the calibration
questions in two so no evaluation label picks the constant. `--one-se` replaces the constant with a
whole standard error, the conventional conservative reading.

### Where the margin is measured

`s` above cannot be read on the data that chose the cell. The pick is the argmax over the whole
grid of one set of calibration labels; the maximum of many noisy estimates sits above the truth by
roughly the noise spread times how many cells were in the running, so a margin read on those same
labels is optimistic by that bias and `c_gate = 0.5` sd does not cover it. That is the winner's
curse, and it is what opened the gate on cells that then lost 2 to 5 points while saving 30 to 55
percent of the cost.

**`--gate-mode split` is the default.** The calibration questions are cut IN ID ORDER: the first
`--n-select` fit the ranking and the multiplier, the next `--n-verify` measure the margin of what
was fitted and take no part in choosing it. The margin is the paired accuracy difference over those
verification questions, its SD a paired bootstrap of 2000 resamples of them, and the selection half
is bootstrapped in its turn to report how often a refit still clears the same bar. Both halves'
sizes travel with every gated row. A calibration split shorter than the sum is used entire, keeping
the requested proportion, and the row says `gate_split_truncated`.

**`--n-select 70 --n-verify 30` is the frozen default**, re-swept under the measured rule over
`{50/50, 50/30, 70/30}` x `c_gate {0.5, 1.0}` on **twenty grids**: the ten Ouro-1.4B base
production grids at horizon 4096 (ten tasks, 100 calibration and 300 evaluation questions each) and
the ten S33 spike grids (five tasks, two checkpoints). Both gated arms, expected accounting, 1.0x
of the default cost. The objective, in order: no deviation that loses to its own fallback beyond
the paired evaluation interval, then the largest mean gain at 1.0x, then the largest mean cost
saving.

| setting | deviations | false | gain @1.0x | saving @1.0x | worst row |
|---|---|---|---|---|---|
| 50/50, c 0.5 | 19 | 0 | +0.56 | 12.77% | -10.0 |
| 50/50, c 1.0 | 16 | 0 | +0.67 | 10.35% | -10.0 |
| 50/30, c 0.5 | 22 | **1** | +0.64 | 12.64% | -10.0 |
| 50/30, c 1.0 | 19 | **1** | +0.73 | 11.41% | -10.0 |
| **70/30, c 0.5** | 17 | 0 | **+0.83** | 11.10% | -2.0 |
| 70/30, c 1.0 | 17 | 0 | +0.80 | 11.10% | -2.0 |

The one false deviation, at 50/30 under both bars, is HellaSwag: ids 50-79 read +6.7 points for the
depth-3 deviation against an SD of 6.5, and it then loses 5.7 points over 300 evaluation questions.
Moving the cut to 70 changes both halves -- a policy fitted on 70 questions, verified on ids 70-99
-- and that pair measures +0.0, so the gate reverts. `50/50` saves more but gains less, and saving
is the third criterion. The verdict does not move with the bootstrap seed.

What 70/30 gives up: the gate now reverts every S33 grid at 1.0x, including MATH500 A0's depth-3
deviation, which the whole-set gate keeps on a +8.0 point margin and ids 50-79 backed at +16.7.
Ids 70-99 measure the same policy at -10.0. A margin that swings 27 points between two halves of
one calibration set is not a margin thirty questions can settle, and the conservative reading is
the one that carries no losing deviation.

`--gate-mode whole` restores the old rule, so the two can be read side by side: one set fits and
measures, and what it reads is the PREDICTED margin `A_hat(pick) - A_hat(normal)` against the SD of
that margin across calibration resamples -- the same draws the calibration bootstrap uses to
re-rank the cells, so gate noise and order noise come from one plan. It is the only way to
reproduce the pre-repair numbers.

**What the verification half has to be big enough for.** The margin is a measurement, so its error
bar is the sampling error of `n_verify` questions and nothing else: thirty binary questions give
about 5 to 7 points of SD, and `c_gate = 0.5` asks for half of one. That is the live constraint on
this gate, and it is why the sweep above is read on twenty grids rather than on any single task's
verdict. A larger verification half costs selection questions, which is the trade `50/50` loses on.

### Two folds

Two folds are the DEFAULT (`policy.GATE_FOLDS`, frozen 2026-09-18; see Frozen defaults above for
what the second fold bought). The deviation has to be earned in BOTH directions of the split: fit the
ranking, the multiplier and the reference on the selection half and verify on the verification half,
then fit on the verification half and verify on the selection half, and take the deviation only when
both verified margins clear `c_gate * sd`. **Nothing about one fold moves:** the arm that RUNS is
always the fold-1 policy, so a second fold can only withhold a deviation, never add or change one.
Every gated row carries `gate_folds`, with each further fold's own margin and SD beside the first's
(`gate_fold_detail`, and `folds` inside each family decision), so a withheld deviation says which
half refused it. `--gate-folds 1` is the one-direction gate, kept for comparison.

Why it exists: a thirty-question verification half can read a margin the evaluation questions do not
repay. StrategyQA's F0 deviation verified +13.3 +/- 5.5 and then lost 2.7 points over 1,990
evaluation questions. One fold cannot tell that from a real edge; two folds ask the other half of
the calibration set the same question. `--gate-mode whole` has one set that both fits and measures,
so it has no second fold: the default there is one fold, and asking for two is refused rather than
ignored (`policy.resolve_gate_folds`).

The second fold can also move WHICH family opens. On the planted true cap-0 grid in the tests F0
clears fold 1 at +12.0 +/- 8.7 and measures 0.0 on the mirror half, so it is withheld and F2 -- one
depth shallower, still at cap 0, +20.0 and +16.0 -- runs instead. The deviation is not lost, it is
the one both halves paid for.

## The average budget

Every arm above obeys a **hard per-prompt cap**: each question must be priced at or below `X`. The
uncapped default obeys no such cap -- it runs the deepest depth to its natural stop and spends the
*mean* cost of doing so -- so at `X` set to that mean cost a capped arm can buy the default's own
cell only for the questions priced under the mean (71 percent on GSM8K, 76 on MATH500 under
`expected`), and it trails the default row (GSM8K lookup 76.7 against 79.7).

The like-for-like constraint is an **average** one: choose a cell per question so that the MEAN
price over questions is at most `X`. "The default cell for every question" is then one feasible
policy, so the allocator has a floor it can be read against, and it clears the floor by taking a
cheaper cell wherever the ranking scores it the same and spending the saving where depth is worth
buying.

`avg_lookup` and `avg_equation` implement that with one Lagrangian multiplier. For `lambda >= 0`
question `i` takes the cell maximising

    score(k, T) - lambda * price_i(k, T)

where `score` is the ranking's own per-cell value: calibration accuracy for lookup, `A_hat` for
equation. A tie goes to the lower price, then the lower depth and cap. The spend falls as `lambda`
rises, so the multiplier wanted is the SMALLEST one whose mean price fits `X` -- the largest
feasible spend -- and bisection finds it on the **calibration** questions, between `lambda = 0` and
a multiplier at which price decides alone. That multiplier is then applied unchanged to the
evaluation questions, so their mean price is a *measurement*, not a constraint imposed on them: it
can land over `X` when the questions either side of the threshold split differently in the two
halves, and every row reports it beside `X` with an `over_budget` flag above 2 percent. The prices
must be known before generating, so the arms need `cap` or `expected` accounting and are left out
under `realised`.

Gain over normal is not defined for these arms -- normal operation is a per-prompt-cap policy and
the two are not priced the same way -- so each row carries two paired differences instead: against
the uncapped `default` row and against `default_at_budget`.

**`avg_gated_lookup`** fits the same policy and then has to earn the deviation. Under the default
split gate the ranking and the multiplier are fitted on the SELECTION half alone; where the default
cell fits the budget on average, the policy is then run on the VERIFICATION half and its paired
accuracy margin over the default cell there decides, against `c_gate` times a paired bootstrap SD
of that same margin. Otherwise the default cell runs for every prompt. It is the same rule as the
per-prompt gate (`policy.gate_passes`), measured between two whole policies on held-out labels. On
GSM8K A0 at 1.0x the cheaper cell is 10 points BEHIND the default cell on questions that did not
choose it, so the arm reverts and lands on the default row (79.7); on MATH500 A0 depth 3 is 16.7
points ahead against a 7.0-point SD, so the policy stands and keeps the 59.7 it bought. Under
`--gate-mode whole` the same two rows read +8.0 and -0.0 against calibration SDs of 4.6 and 1.3,
which is the biased reading the split replaces.

**Underspending is the claim, not a defect.** Where the multiplier reaches 0 the budget never
binds: the arm buys its best-scoring cell outright and spends less than it was given. Each row
carries `cost_saving_pct` against its own budget and `pct_of_default_cost`, and the markdown says
it in one line -- GSM8K `avg_equation` is the same 73.7 points at 74.2 percent of the default
cost.

## v5: the calibration size, the deviation families, the oracle gap

Two changes and one column, all aimed at the distance between the allocator and the best cell the
evaluation questions actually have. **The calibration size is now a function of N**:
`n_cal = max(100, min(300, floor(0.2 N)))`, and the split of record draws calibration as the first
`n_cal` of one seeded permutation, so a larger size keeps every id the smaller one had and takes
the extra ids off the front of the evaluation split, which shrinks by exactly as many
(`cells.promote_calibration`, `--n-cal` to override); the gate's cut is then 70/30 OF that size
rather than a fixed 70 and 30, which at the frozen 100 is the frozen 70 and 30 and nothing about
these grids moves. **The structured deviation families** replace the free set as what the gate is
allowed to deviate to, tested in order, smallest first, the first whose verification margin clears
the bar winning: `F0` the deepest depth at cap 0, `F1` the deepest depth at any cap, `F2` one depth
shallower at any cap, `F3` the free set, which is v4 exactly and is the last resort, so a family
can only add a deviation the structured test earned and never take one away. Fewer cells in the
running means less of a winner's curse for the bar to cover, and both gated arms record which
family opened. **The oracle gap** is the third: the best single cell on the EVALUATION questions
minus each arm at 1.0x, one column of Table 1 and one field per row of `results.json`. It reads
the evaluation labels, so it is a diagnostic -- the price of calibration noise, what the arm gives
up by having to find the cell from the calibration half instead of being told it -- and never a
policy result; no arm consumes it, and a negative gap means an arm beat every single cell by
varying the cell per question.

**What is frozen.** The size rule and the 70/30 proportion. At N = 400 the rule sits on its floor
and returns the 100 v4 used, so the twenty grids here do not move by it; the emulation is where it
pays, promoting evaluation ids in seeded order to n_cal 150 and 200 (the evaluation split shrinking
to 250 and 200). Over the ten production grids the mean gain at 1.0x runs +0.07, +0.41, +0.25 under
v4's gate and +0.12, +0.73, +0.77 under v5's, with no false deviation at any size, and HellaSwag's
genuine cap-0 optimum -- worth +5.6 and +7.5 points, and the one grid where the gap closes to zero
-- is recovered only at 150 and 200. The families **are frozen on** (ruling 2026-09-18: the production grids at horizon 4096 are the setting of record, and there they win at every calibration size; `--no-families` restores the free set). They carry no false
deviation either, but over the twenty grids at n_cal 100 the mean gain at 1.0x falls +0.67 to +0.62
and the oracle gap rises 2.03 to 2.08, and the condition was that the gain rise. The split is not
even: on the ten production grids they win at every size and cut the gap (2.11 to 2.06, 2.32 to
1.94, 2.55 to 1.95); on the ten S33 spike grids they lose, +1.26 to +1.11, and those rows are the
larger numbers. The families are on by default; `--no-families` turns them off.

## Gain, contrast, Table 1

**Gain over normal** is averaged over the budgets where normal operation is affordable for at least
90 percent of questions. `gain_mean_pts`, the headline, gives every qualifying budget equal weight;
`pooled_gain_mean_pts` averages over every feasible (question, budget) pair instead, so a budget
more questions can afford weighs more. Both carry a paired bootstrap that resamples question indices
*once* and reuses them at every budget, leaving infeasible entries as NaN in their own slot. A
second bootstrap resamples the calibration questions and re-ranks per draw: selection noise.

**Contrast** of two checkpoints is the paired difference between their policies. The second grid is
the reference: its median prompt, its cost function and its cost matrix fix the budget grid and the
ranges, so both are read at one fixed set of budgets whichever is cheaper. Complete case over the
range (a question missing at any budget leaves every budget), and identical evaluation ids are
asserted before anything is compared.

**Table 1** reports each arm at 0.25, 0.50, 0.75 and 1.00 of the default cost. The budgets are the same
under every accounting, because the default cost is a measured statistic and not a price; what
changes is what each arm is charged. The `default` arm *is* the deepest depth at natural stop, so it
costs the whole default cost and cannot be bought below 1.00: those cells read `not feasible`, never
the unbudgeted accuracy repeated. The `default_cell` arm is that same operating point priced per
question as a cell of the grid, with the share of questions that could buy it and whether it fits
the budget on average; its accuracy is over the affordable questions only, which are the cheaper and
so the easier ones. Every arm also carries `vs_default`, its paired difference from the `default`
row with a bootstrap interval over questions.

## Running it

    cd work/spikes/s35_allocator
    python -m unittest discover -s tests -t tests            # 280 tests, CPU, a minute

    python -m alloc.cli --cells DIR --task gsm8k --checkpoint NAME \
                        --model-config PATH | --layers-per-loop N [--fixed-layers M] \
                        [--reference NAME] [--c-gate 0.5] [--n-labels 30] \
                        [--gate-mode split|whole] [--one-se] [--n-select 70] [--n-verify 30] \
                        [--gate-folds 1|2] [--n-cal 150] [--no-families] \
                        [--accounting cap|realised|expected|all] [--avg-budget] \
                        [--ks 1,2,4,8] [--caps 0,64,512,4096] \
                        [--cache-dir DIR | --no-cache] --out OUTDIR

`--cells` is any directory of cell jsonl files; two file-name shapes and two row shapes need no
flag. Names: `cells_<model>_<task>_<protocol>_k<K>[_s<I>of<N>].jsonl`, where a depth may be split
over shards and every shard is read and unioned, and the older `cells_<task>_<model>_k<K>.jsonl`;
names marked a dry run or a smoke test are ignored. Rows: keyed by `idx`, or with a leading
`{"_header": ...}` line plus `row_idx`, `kind` and `subtask`. A line that is not JSON is counted and
warned about, never dropped in silence. One case needs a flag: a reference file of raw
multiple-choice rows with no split or parsed read-out (`--reference-bbh-base`).
Each cells file is parsed once and kept as a compressed numpy archive
(`<name>.jsonl.alloc-cache.npz`) beside it, keyed by its size, mtime and header line, so a
regenerated grid invalidates its own entry and a second pass over the same grids reads arrays
instead of JSON. `--cache-dir` puts the archives somewhere else; `--no-cache` reads and writes none.
The three routes give identical numbers -- the cache only changes the wall time -- and `results.json`
records which was used under `read`.
`--avg-budget` adds the five average-budget rows -- `avg_gated_equation_resolved` (the arm of record), `avg_gated_lookup` (the label-only baseline), then `avg_lookup`, `avg_equation`, `avg_equation_resolved` -- to every Table 1 written, in that order, and a second table of their realised mean price against the budget each was fitted to.
Outputs: `cards.json` (per checkpoint — `G`, `c`, `l`, `A_hat`, the measured surface, the
reconstruction error and its noise floor, every ranking, the calibration and predicted
accuracies, every cell's median price and expected length; and the resolved identity: the
settle-time distribution per depth, `P_k(s=j)`, `c_k(j)`, `l_k(T)`, which source each `c` came from,
`A_res`, and both surfaces' RMSE against the measured one on the calibration AND the evaluation
questions beside each split's noise floor); `results.json` (seven arms with both gain means, both
bootstrap intervals, the worst budget and the per-budget record; the two contrasts; the
non-inferiority verdict at the top three `B*` budgets with a 2-point margin; the default cost;
Table 1 with the oracle gap of every arm, and one Table 1 per accounting under `--accounting all`;
the resolved calibration size and the promotion record under `n_cal_rule`); `table1.md` and one
`table1_<accounting>.md` per accounting run. The gains and the contrasts are priced under one
accounting, the first of the list, so `all` tabulates three and prices the rest under `cap`.

## File map

| file | holds |
|---|---|
| `alloc/cells.py` | both file-name and row shapes, labels, the read-out parse, the reserve, the grid assertions, model geometry, the calibration expected-length table, the calibration-size rule and the seeded promotion of evaluation ids into it |
| `alloc/mechanism.py` | arrival, `G`, `c`, `l`, `A_hat`, the reconstruction error and noise floor; settle time, its distribution, the sparse-cap bins, `P_k(s=j)`, `c_k(j)`, `l_k(T)` and `A_res` |
| `alloc/policy.py` | the three prices, the 16 budgets, `B*`/`B_low`, all three rankings, affordability, normal operation, both gates (`MeasuredGate`, the default, and its folds; `Gate`, the predicted one `whole` keeps), the one-standard-error rule, the paired margin SD, the average-budget multiplier, the 70/30 proportion and the four deviation families |
| `alloc/evaluate.py` | gain over normal, contrasts, non-inferiority, default cost, Table 1, the calibration split, the gate sweep, the family tests, the oracle gap, each arm against its own fallback |
| `tests/` | a planted first-answer-is-best grid the pooled identity must misrank and the resolved one must lead with cap 0, the resolved identity reproducing its own calibration surface exactly, the sparse-cap fallbacks, the four resolved arms in Table 1 and in its picks, the card's four RMSEs, the two-fold gate withholding a deviation one fold keeps, and a reproduction of compute.py's resolved evaluation RMSE on a production grid to 0.05; a planted optimum, both file-name and row shapes, a 6x10 grid out to cap 4096, the gate, the pairing assertion, the three accountings and the default cell at 1.0x, a planted tie the average budget must spend elsewhere, a planted winner's curse the split gate must close, a planted cap-0 optimum it must keep and a planted wrong-signed surface where the predicted margin opens the gate and the measured one reverts, a reproduction test against frozen real numbers, and the v5 file: the size rule, the promotion, the proportional split, the four families on a true cap-0 plant and on a losing one, the oracle gap, the fallback interval, the frozen defaults |

Rerunning the real grids reproduces 26 frozen numbers to **0.05 points** (tolerance 0.1): headline
and pooled gain over normal on six tasks under lookup and five under equation at 30 labels, plus
four contrasts. Those grids are 4 by 7; the wider grid is exercised synthetically for now.
