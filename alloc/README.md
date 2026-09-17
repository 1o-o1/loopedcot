# The allocator

Pick, per question and per compute budget, how many loop passes to run and how many tokens of chain
to allow before forcing the answer out. CPU, numpy only, no imports from any other directory.

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

## The two rankings

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
No evaluation label reaches either ranking; both ranking functions reject non-calibration positions.

## The gate

At a given budget the allocator's pick can be worse than normal operation. The gate keeps normal
unless the predicted margin clears its own uncertainty:

    run the pick  iff  A_hat(pick) - A_hat(normal) > c_gate * s
    s = the standard deviation of that same margin across resamples of the calibration questions

Those resamples are the same draws the calibration bootstrap uses to re-rank the cells, so gate
noise and order noise come from one plan. `c_gate = 0` demands only a strictly positive margin.
**`c_gate = 0.5` is the frozen default**: swept over `{0, 0.5, 1, 1.5, 2}` on seven tasks under
"maximise mean gain over normal subject to a worst-case per-budget loss no worse than -1 point".
`c = 0` breaks the constraint; `0.5` satisfies it at the highest mean gain and wins every
leave-one-task-out fold. `evaluate.gate_selection` reruns the sweep, splitting the calibration
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

**`--n-select 50 --n-verify 30` is the frozen default**, swept over `{50/50, 100/20, 50/30}` on the
ten S33 spike grids (five tasks, two checkpoints) at 1.0x of the default cost. `100/20` cannot run
there at all -- every one of those grids has exactly 100 calibration ids -- and `50/50` closes the
one true deviation in the set, MATH500 A0 at depth 3, worth +3.3 points for a 21.5 percent saving.
`50/30` keeps it, opens no deviation that loses beyond its own interval, and spends 8.6 percent
under budget against the old gate's 8.1 at the same mean accuracy.

`--gate-mode whole` restores the old rule, one set fitting and measuring, so the two can be read
side by side. It is the only way to reproduce the pre-repair numbers.

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
    python -m unittest discover -s tests -t tests            # 143 tests, CPU, seconds

    python -m alloc.cli --cells DIR --task gsm8k --checkpoint NAME \
                        --model-config PATH | --layers-per-loop N [--fixed-layers M] \
                        [--reference NAME] [--c-gate 0.5] [--n-labels 30] \
                        [--gate-mode split|whole] [--one-se] [--n-select 50] [--n-verify 30] \
                        [--accounting cap|realised|expected|all] [--avg-budget] \
                        [--ks 1,2,4,8] [--caps 0,64,512,4096] --out OUTDIR

`--cells` is any directory of cell jsonl files; two file-name shapes and two row shapes need no
flag. Names: `cells_<model>_<task>_<protocol>_k<K>[_s<I>of<N>].jsonl`, where a depth may be split
over shards and every shard is read and unioned, and the older `cells_<task>_<model>_k<K>.jsonl`;
names marked a dry run or a smoke test are ignored. Rows: keyed by `idx`, or with a leading
`{"_header": ...}` line plus `row_idx`, `kind` and `subtask`. A line that is not JSON is counted and
warned about, never dropped in silence. One case needs a flag: a reference file of raw
multiple-choice rows with no split or parsed read-out (`--reference-bbh-base`).
`--avg-budget` adds the `avg_lookup` and `avg_equation` rows to every Table 1 written.
Outputs: `cards.json` (per checkpoint — `G`, `c`, `l`, `A_hat`, the measured surface, the
reconstruction error and its noise floor, both rankings, the calibration and predicted accuracies,
every cell's median price and expected length); `results.json` (five arms with both gain means, both
bootstrap intervals, the worst budget and the per-budget record; the two contrasts; the
non-inferiority verdict at the top three `B*` budgets with a 2-point margin; the default cost;
Table 1, and one Table 1 per accounting under `--accounting all`); `table1.md` and one
`table1_<accounting>.md` per accounting run. The gains and the contrasts are priced under one
accounting, the first of the list, so `all` tabulates three and prices the rest under `cap`.

## File map

| file | holds |
|---|---|
| `alloc/cells.py` | both file-name and row shapes, labels, the read-out parse, the reserve, the grid assertions, model geometry, the calibration expected-length table |
| `alloc/mechanism.py` | arrival, `G`, `c`, `l`, `A_hat`, the reconstruction error and noise floor |
| `alloc/policy.py` | the three prices, the 16 budgets, `B*`/`B_low`, both rankings, affordability, normal operation, the gate, the one-standard-error rule, the paired margin SD, the average-budget multiplier |
| `alloc/evaluate.py` | gain over normal, contrasts, non-inferiority, default cost, Table 1, the calibration split, the gate sweep |
| `tests/` | a planted optimum, both file-name and row shapes, a 6x10 grid out to cap 4096, the gate, the pairing assertion, the three accountings and the default cell at 1.0x, a planted tie the average budget must spend elsewhere, a planted winner's curse the split gate must close and a planted cap-0 optimum it must keep, a reproduction test against frozen real numbers |

Rerunning the real grids reproduces 26 frozen numbers to **0.05 points** (tolerance 0.1): headline
and pooled gain over normal on six tasks under lookup and five under equation at 30 labels, plus
four contrasts. Those grids are 4 by 7; the wider grid is exercised synthetically for now.
