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
questions in two so no evaluation label picks the constant.

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

**Table 1** reports each arm at 0.25, 0.50 and 1.00 of the default cost. The `default` arm *is* the
deepest depth at natural stop, so it costs the whole default cost and cannot be bought below 1.00:
those cells read `not feasible`, never the unbudgeted accuracy repeated.

## Running it

    cd work/spikes/s35_allocator
    python -m unittest discover -s tests -t tests            # 60 tests, CPU, seconds

    python -m alloc.cli --cells DIR --task gsm8k --checkpoint NAME \
                        --model-config PATH | --layers-per-loop N [--fixed-layers M] \
                        [--reference NAME] [--c-gate 0.5] [--n-labels 30] \
                        [--ks 1,2,4,8] [--caps 0,64,512,4096] --out OUTDIR

`--cells` is any directory of cell jsonl files; two file-name shapes and two row shapes need no
flag. Names: `cells_<model>_<task>_<protocol>_k<K>[_s<I>of<N>].jsonl`, where a depth may be split
over shards and every shard is read and unioned, and the older `cells_<task>_<model>_k<K>.jsonl`;
names marked a dry run or a smoke test are ignored. Rows: keyed by `idx`, or with a leading
`{"_header": ...}` line plus `row_idx`, `kind` and `subtask`. A line that is not JSON is counted and
warned about, never dropped in silence. One case needs a flag: a reference file of raw
multiple-choice rows with no split or parsed read-out (`--reference-bbh-base`).
Outputs: `cards.json` (per checkpoint — `G`, `c`, `l`, `A_hat`, the measured surface, the
reconstruction error and its noise floor, both rankings, the calibration and predicted accuracies,
every cell's median price); `results.json` (five arms with both gain means, both bootstrap
intervals, the worst budget and the per-budget record; the two contrasts; the non-inferiority
verdict at the top three `B*` budgets with a 2-point margin; the default cost; Table 1); `table1.md`.

## File map

| file | holds |
|---|---|
| `alloc/cells.py` | both file-name and row shapes, labels, the read-out parse, the reserve, the grid assertions, model geometry |
| `alloc/mechanism.py` | arrival, `G`, `c`, `l`, `A_hat`, the reconstruction error and noise floor |
| `alloc/policy.py` | prices, the 16 budgets, `B*`/`B_low`, both rankings, affordability, normal operation, the gate |
| `alloc/evaluate.py` | gain over normal, contrasts, non-inferiority, default cost, Table 1, the gate sweep |
| `tests/` | a planted optimum, both file-name and row shapes, a 6x10 grid out to cap 4096, the gate, the pairing assertion, a reproduction test against frozen real numbers |

Rerunning the real grids reproduces 26 frozen numbers to **0.05 points** (tolerance 0.1): headline
and pooled gain over normal on six tasks under lookup and five under equation at 30 labels, plus
four contrasts. Those grids are 4 by 7; the wider grid is exercised synthetically for now.
