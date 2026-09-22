# Budget-conditioned anytime training

One reviewable package: chains, targets, gates, training, evaluation grid, analysis, config,
prompts and tests for teaching Ouro-1.4B to answer under a stated token budget. It imports only the
shared evaluation harness, which ships inside this directory; nothing is imported from another
experiment directory, and anything reused was copied with its source named at the point of use.

## What the recipe teaches

Every training example is one **visit**: a prompt, a budget line, and a target the model must
produce under that budget. The budget `T` is drawn from **that source's own grid** --
{0, 16, 32, 64, 128, 256, 512, 1024, no limit} for GSM8K, CSQA and AQuA, and
{0, 16, 32, 64, 128, 256, 512, 1024, 2048, no limit} for MATH -- under **that source's own weights**
(see *Where the theory enters the objective*), and four target kinds cover it.

**Why the grid reaches the task's own horizon.** The base model's chains are not one length. On the
hard tasks they run to thousands of tokens: Ouro-1.4B base gains 7 points on MATH500 between a 512
cap and a 4096 cap, and the production grids this recipe is compared against run the natural stop out
to 4096 with caps {0, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096}. A recipe that generated chains only to 512
and capped its grid at 512 would teach a length prior, and its grid at horizon 512 could not be
placed beside those base grids in Table 1. So the horizon for chain generation is per source (GSM8K, CSQA and
AQuA 1024, MATH 2048), the top budget of each source equals its horizon, and the no-limit target is
the **full** chain.

| kind | when | what it is | what it teaches |
|---|---|---|---|
| `DIRECT` | `T = 0` | the forced suffix, the answer, EOS; only the answer and EOS supervised | answer immediately when there is no room to think |
| `CHAIN` | `T > 0`, some chain fits | the **longest** correct chain that fits `T`, plus EOS | use the whole budget you were given, and stop |
| `CHAIN` / `CHAIN_PLUS` | `T = none` | the selected correct chain; a `fullplus_p` share (0.20) also gets suffix + answer | reason to the end when nothing is capped |
| `FALLBACK` | `T > 0`, nothing fits | the standard chain cut at `T`, then suffix + answer; only the answer and EOS supervised | commit to an answer from a truncated chain |

**Which questions enter the mixture.** A question is used only when at least one of its two chains
was correct **and finished on its own**. A question the base model never solved supplies no target at
all, not even a `DIRECT` one: that is a stated decision, not an oversight, and it keeps the mixture
inside the region where the model can already reach the answer.

A chain that ran into its horizon is not a correct chain whatever its text parses to -- it is an
unfinished chain, and supervising it would teach the model to stop where chain generation stopped. Those
are dropped from the kept pool and counted per source in `chains_meta_<src>_<tag>.json` as
`n_hit_horizon` and `n_correct_but_unfinished`. At the 512 horizon of the first draft that share was
0.00 on GSM8K and 0.03 on MATH; at 1024 and 2048 it is smaller still, and what was cut off before is
now a usable long chain.

The fallback cuts the kept (correct, trimmed) standard chain when there is one, and the raw standard
chain otherwise. A raw chain that already finishes inside `T` is **not** used: supervising the gold
answer straight after a complete but rejected chain would teach the model to assert an answer its own
reasoning did not reach, so those visits get the read-out alone.

Both candidate chains come from the **base** checkpoint at k=4: chain **A** under the harness's
standard few-shot prompt (the prompt used at evaluation), chain **B** under a short-exemplar prompt
that never appears at evaluation (`prompts/`, four exemplars per source, short answers by
construction). A chain is a candidate only if its own answer equals gold, and it is trimmed to end
at the task's answer sentence.

**Longest, not shortest.** A pilot that picked the *shortest* correct chain that fits made every
budget at or above 32 on GSM8K a 23-token target: the model wrote 33 tokens whatever the budget and
inherited the short chains' 79 percent yield, losing 11.0 points at `Budget: 512` and 4.0 at 128
against the untargeted reference. Picking the longest fitting chain repairs the large-budget end
while keeping the small-budget gain (+24.7 at 32 on GSM8K).

**Why a line at all.** The cap has to be *stated*, not implied by where generation is cut, or the
model cannot allocate. The line is one sentence after the question and before the answer prefix:

    ...Question: <q>
    Budget: 128 tokens.
    Answer:

The exemplar block above it is the harness's, byte for byte, and carries no budget line. The line is
never a loss target. Gate V1 proves that deleting it recovers the harness's untagged prompt exactly,
so a cell from this recipe is comparable with a reference cell.

**Why one visit per block, and why five block lengths.** Earlier runs concatenated every visit of a
depth into one stream and reshaped it into 512-token blocks, with no attention mask between visits.
With 573-754 token few-shot prompts, 92 percent of visits were split: the whole prompt sat in the
same block for 1 percent of supervised tokens, and 14 percent saw no prompt token at all. The model
was trained almost never with the exemplars that evaluation always gives it. Here a block holds
exactly one visit, the loss covers that visit only, and padding is mask 0. The forward is causal, so
no supervised position can attend to the padding and no attention mask is needed.

A 2048-token MATH chain does not fit a 1024-token block, and padding every visit to 3072 would spend
two thirds of the forward on padding. So the block length is a **bucket**: the visit goes in the
smallest of {1024, 1536, 2048, 2560, 3072} that holds it, right-padded, one visit per block. A visit
longer than 3072 is **dropped and counted** (`dropped_draws.longer_than_longest_block`), never
truncated: truncating would delete the answer supervision at exactly the large budgets this recipe
repairs. The manifest reports `padding_share_by_block_len`, so the bucket set is judged on measured
padding rather than on a guess, and `blocks_dropped_as_remainder_by_len` with
`buckets_with_no_window` name any bucket too thin to fill one accumulation window.

## The objective

For a block at depth `d`, with `H = hidden_states_list[d-1]` (the model norms these before
returning them, so this is the inference read-out) and the supervised mask `m`:

    loss(window) = sum over the micro-batches of the window, over positions i with m[i+1] = 1,
                   of  CE( lm_head(H)[i] , x[i+1] )      /      sum of m[i+1] over the same window

A CE **sum** divided by the accumulation window's own supervised-token count, so no example's
per-token weight depends on its length. Prompt, budget line, forced suffix and padding are all mask
0, and none of them enters any token or layer-pass count. The schedule keeps whole micro-batches and
whole windows, so a few blocks never train: the manifest reports `supervised_tokens_drawn` and
`supervised_tokens_scheduled` separately, with the block count it dropped as a remainder. Depth is
set per block through
`total_ut_steps`, drawn from **that block's source's depth weights** (below), and restored after every forward;
a micro-batch is homogeneous in depth **and** in block length, and so is a whole accumulation
window, because the micro width is per bucket. Only LoRA trains (rank 16, alpha 32, on the seven
projections of all 24 layers, all read from `config.yaml`); base, norms, embeddings, `lm_head` and
the exit gate are frozen.

**The window is 32 blocks in every bucket.** `micro_by_block_len` is {1024: 4, 1536: 2, 2048: 2,
2560: 2, 3072: 1} and the accumulation count is `effective_batch_blocks / micro`, so 8, 16, 16, 16 and
32. The optimiser step is the same 32 blocks and the same gradient wherever it comes from; only the
number of blocks resident in one forward changes. `train.py` steps over windows, not over a fixed
stride, and refuses a schedule whose window is not 32 blocks or mixes two block lengths.

## Where the theory enters the objective

The paper's mechanism is not only what the analysis measures; it is what the training distribution is
built out of. Stage 0, `train/theory_weights.py`, reads the **base model's own production grid** --
the `cells_ouro_1_4b_base_<task>_natural_k{1,2,3,4}.jsonl` files this recipe's grid is placed beside
in Table 1 -- and writes two tables per source into `train/data/theory_weights.json`. The
**calibration split only**: the evaluation half of the base grid never enters a training weight.

Both tables rest on one label-free definition, copied into the stage rather than imported from
`alloc`, so it cannot drift: a question is **settled** at cap `T` when its forced read-out at `T`
and at every cap after it equals the last cap's read-out and parses. The first settled cap is the
question's **settle cap**; a read-out that never stops moving settles nowhere. From that, per depth
`k`: `G_k(T)` is the settled share, `c_k(j)` the accuracy of the questions that settle at `j`,
`l_k(T)` the accuracy **at** `T` of the questions not settled by `T`, and `c_k(>T)` the accuracy
those same questions reach at the last cap.

**The budget weights, in words.** A cap is worth training at in proportion to the accuracy the base
model *leaves on the table* by stopping there: the share of questions that have not yet made up
their minds at `T`, times how much more of them are right once they are allowed to finish. Averaged
over depths, clipped at zero, then mixed half and half with the uniform draw so no budget of the
grid is starved; the no-limit entry takes the uniform share outright, having no cap to leave
anything at.

    w(T)  proportional to  mean over k of  clip( (1 - G_k(T)) * (c_k(>T) - l_k(T)) , 0 )
    w = 0.5 * uniform + 0.5 * normalised(w),   w(no limit) = uniform

| source | 0 | 16 | 32 | 64 | 128 | 256 | 512 | 1024 | 2048 | no limit |
|---|---|---|---|---|---|---|---|---|---|---|
| `gsm8k` | 0.166 | 0.178 | 0.169 | 0.132 | 0.073 | 0.059 | 0.056 | 0.056 | -- | 0.111 |
| `math` | 0.129 | 0.133 | 0.128 | 0.130 | 0.121 | 0.097 | 0.061 | 0.052 | 0.050 | 0.100 |
| `csqa` | 0.278 | 0.100 | 0.233 | 0.056 | 0.056 | 0.056 | 0.056 | 0.056 | -- | 0.111 |
| `aqua` | 0.172 | 0.187 | 0.165 | 0.129 | 0.062 | 0.057 | 0.059 | 0.057 | -- | 0.111 |

Read them for plausibility. On the three short tasks the weight collapses onto 0 to 64 and every cap
from 256 up sits exactly on the floor, `0.5 / 9 = 0.056`: by 256 tokens those questions have
settled, so stopping later buys nothing and the draw only keeps the floor's worth of them. MATH,
whose chains run to thousands of tokens, stays nearly flat out to 128 and only then falls. CSQA's
0.278 at cap 0 and its dip at 16 are real and not a bug: it is five-way multiple choice, so a forced
read-out at 0 is often accidentally right, moves away, and comes back -- which is exactly the
non-monotone unrealised accuracy the settle-time definition is there to capture.

**The depth weights, in words.** A depth is worth training at in proportion to how often an
allocator would actually buy it. The allocator is the average-budget **lookup** arm: it scores each
(depth, cap) cell by its calibration accuracy and, at a compute budget `X`, buys the cells that
maximise score minus a multiple of price, with the multiplier set so the mean price over prompts is
at most `X`. It is run at 16 log-spaced budgets from the cheapest cell of the median-prompt cost
matrix to the cost of the default operating point (deepest depth at natural stop), and every depth's
share is pooled over that whole ladder. Prices are layer-token passes,
`(L_fixed + kL)(P + E_cal[min(len_k, T)] + R)` with `L = 24`, `L_fixed = 0` and
`R = suffix + answer allowance` (12 on GSM8K, 32 on MATH, 8 elsewhere). The pooled usage is then
turned into a draw by **the same mixture rule as the budget weights**, and only after that is the
**deepest** depth raised to a hard floor of 0.20, with the shallower depths rescaled to what is left:

    usage(k)  proportional to  the allocator's pooled share of k over the 16 budgets
    w = 0.5 * uniform + 0.5 * normalised(usage),   then  w(k_max) >= 0.20,  w(k < k_max) scaled to 0.80

| source | k=1 | k=2 | k=3 | k=4 | allocator usage | cheapest cell | default cost |
|---|---|---|---|---|---|---|---|
| `gsm8k` | 0.312 | 0.334 | 0.125 | 0.228 | 0.37, 0.42, 0.00, 0.21 | 15,696 | 74,524 |
| `math` | 0.306 | 0.238 | 0.256 | 0.200 | 0.42, 0.27, 0.31, 0.00 | 24,012 | 166,113 |
| `csqa` | 0.279 | 0.290 | 0.231 | 0.200 | 0.31, 0.33, 0.21, 0.15 | 14,604 | 61,919 |
| `aqua` | 0.255 | 0.253 | 0.292 | 0.200 | 0.31, 0.30, 0.39, 0.00 | 15,264 | 84,208 |

The allocator buys k=4 almost nowhere on the ladder -- most of the range from the cheapest cell to
the default cost is spent below the default's own price, where shallow depths win on price -- and on
three of the four sources its usage of one depth is exactly zero. The uniform half of the mixture is
what keeps those depths trained: every depth holds at least `0.5 / 4 = 0.125` of its source's
blocks, the same floor the budget draw gets, rather than a separately chosen per-depth constant.

**k=4 is then floored at 0.20 on top of that.** The deepest depth is the checkpoint's released
default and the cell Table 1 checks at 1.0x, where the claim is non-inferiority of the trained k=4
natural stop against the base model's. A mixture that trained k=4 at 0.125 while the allocator
ignores it would put that row on the least-trained depth of the four, so the floor binds on `math`,
`aqua` and -- by a thousandth -- `csqa`, and the shallower depths keep their proportions to each
other inside the remaining 0.80. `gsm8k` clears it on its own at 0.228. The allocator-usage column is
in the manifest and in the JSON, so both the mixture and the floor are visible rather than implied.

**The tables are pinned by content.** `config.yaml` carries `theory_weights_sha256`, and stage 2
stops unless `train/data/theory_weights.json` hashes to it -- the same rule as the pool, for the same
reason: the two tables *are* the objective, and a run that silently picked up different ones could
not be compared with the one described here. After deliberately recomputing them, re-pin with the
digest stage 0 prints. Gate **V10** then checks the other direction: that the histogram the draw
actually realised, per source, sits within 0.05 of the table it was supposed to draw from.

## Ablations: one flag

`--variant` selects the target rule. Everything else is identical, so a variant difference is a target
difference. Each variant keeps its own blocks, spans and schedule under `data/<variant>/`, and the trainer
refuses blocks whose manifest names another variant or whose content hash does not match.

| variant | rule | budget line | fallback | draw |
|---|---|---|---|---|
| `budget_longest` | longest correct chain that fits `T` | yes | yes | theory |
| `budget_shortest` | shortest correct chain that fits `T` | yes | yes | theory |
| `nobudget` | same as `budget_longest` | **no line, train or eval** | yes | theory |
| `nocut` | longest that fits | yes | **no**, those visits are dropped | theory |
| `uniform_longest` | same as `budget_longest` | yes | yes | **uniform** |
| `plain_sft` | longest correct chain, nothing to fit | **no line** | **no**, never reached | **none_only**, depth fixed at 4 |
| `plain_sft_mix` | longest correct chain, nothing to fit | **no line** | **no**, never reached | **none_only**, theory depth mix |

`uniform_longest` is the ablation that prices the theory weights themselves: the same target rule and
the same line, drawing `T` uniformly over the source's grid and the depth from the flat
`depth_probabilities` mix, which is what every variant did before the weights existed. **It is not
scheduled** -- it is there so a reviewer asking "what do the weights buy?" can be answered by one
flag rather than by a rebuild, and it runs only if the two variants of record leave time.

**The plan of record runs them in order, not in parallel.** `budget_longest` and the base-model
reference grid go first, because those two are what Table 1 needs; `nobudget` second, because it
prices the budget line itself and is the one ablation a reviewer will ask for; `budget_shortest`,
`nocut` and `uniform_longest` only if time remains. Each variant is about 15 h of idle Spark time (train
plus grid), so the order is the schedule.

## Runs beyond the two scheduled variants

**Full-size evaluation.** `eval_rows: production`, the default, evaluates every row of
`prod/tasks/data/rows_<task>.jsonl` (GSM8K 1319, MATH500 500, CSQA 1221, AQuA 254), labelled `cal`
or `eval` by the harness's own `prod.tasks.split_labels`, so rows and split are the base grids' own.
Its files carry the label `<name>_full` (`cells_<task>_<name>_full_k<k>.jsonl`, the budget file and
the meta likewise) and `analysis.py --name=<name>_full` reads them, so a full-N grid never lands on
the 300+100 files `eval_rows: s32` writes. `run_grid.py --eval-rows=production|s32` beats the config.

**Any variant, any seed.** `VARIANTS="a b c"` is the list both launchers index into (index i takes
variant i, or variant i/4 and task i%4 in `grids_s36.sbatch`), and `EVAL_ROWS` reaches the grid.
`SEED=<n>` other than `config.yaml`'s seed names the run `s36_<variant>_seed<n>` and keys stage 2's
directory and manifest `<variant>_seed<n>`; the default seed keeps today's names and paths.

**Baselines without the objective.** `plain_sft` draws `T = none` on every visit at a fixed depth 4:
the base model's own full correct chain, no budget line, no cut, nothing for the fallback to do --
ordinary self-distillation, the control for the whole objective. `plain_sft_mix` is that target with
the depth mix `budget_longest` draws from, separating the depth sampling from the budget conditioning.

## Files

| file | what it is |
|---|---|
| `train/config.yaml` | every knob, one line of comment each. The single source of the recipe's numbers; a value no stage implements is refused at load. |
| `train/theory_weights.py` | stage 0, CPU, run once. The two definitions copied from the paper's mechanism, and the budget and depth tables they imply, read off the base model's production grid. |
| `train/data/theory_weights.json` | those tables, plus the formulas, the per-source commitment surfaces and the sha256 of every grid file they were read from. Pinned in `config.yaml`. |
| `train/chains.py` | stage 1, GPU. Chains A and B from the base checkpoint at k=4, correct-only, resumable per pool question. |
| `train/targets.py` | stage 2, CPU, **and the shared library**: config, prompt builder, budget line, target rule, one-visit-per-block packer, span table, `target_manifest_<variant>.json`. |
| `train/gates.py` | stage 3. V1 parity, V2 masks, V3-CONTEXT (+ its negative control), V9 contamination on CPU; V4 preflight on GPU. Any failure stops. |
| `train/train.py` | stage 4, GPU. The loop above, an atomic checkpoint every 100 steps, `train_config_<variant>.json` with realised tokens and layer passes. |
| `train/run_grid.py` | stage 5, GPU. The no-limit pass at horizon 4096 cut at the ten standard caps, written in the base grids' cells format; one budgeted pass per stated budget with its own line and hard stop, in `cells_budget_*.jsonl`. |
| `train/analysis.py` | stage 6, CPU. F1-F5 against a reference variant, paired bootstraps; the grid comes from `config.yaml`. |
| `train/s32_common.py`, `train/s28_common.py`, `train/s13_shots.py`, `train/s3_patch.py` | the shared evaluation harness, copied in so the package runs from a checkout: model loading, the static cache, batch sizing, the natural stop, decoding, the exemplar blocks and the parsers. Every directory they write hangs off the run root (`S36_RUN_ROOT`, published by `targets.paths()`); the exemplar blocks stay package-relative, in `prompts/`. |
| `prompts/` | the short-exemplar blocks used only when the chains are generated, and the standard exemplar block per task, with their provenance in `prompts/README.txt`. |
| `tests/` | CPU tests on synthetic data: the rule, the masks token by token, the packing, the line, the variants, variant keying, resume, and V3-CONTEXT failing on a split stream. |

## The gates

- **V1 parity** - the training and evaluation prompts are the same function call; with the line
  deleted the prompt equals the harness's untagged prompt byte for byte, and the line appears
  exactly once, immediately before the answer prefix.
- **V2 masks** - prompt, budget line, forced suffix and padding unsupervised; chain, answer and one
  EOS supervised. Checked token by token on 20 visits and array-wide for padding.
- **V3-CONTEXT** - for every supervised token, its block holds the whole prompt of its visit, before
  it, with no other visit's tokens in front of it. The gate re-reads the block's token ids against
  the digest recorded for that visit and checks that every position past the visit is the pad id, so
  a swapped or edited block fails too. Then the same visits are repacked the old way and the gate
  must **fail**, or passing proves nothing. None of V1, V2 or V4 looks at the context a supervised
  token sees.
- **V4 preflight** - a packed micro-batch at its own depth equals the same blocks forwarded one at
  a time, compared in float32 within 1e-3 of the logit scale (bf16 kernels differ by batch shape
  on most GPUs, so bit-identity is a property of the card, not of the packing; a mask leak is
  order 1), and a different depth gives a different answer.
- **V10 draw weights** - the realised `T` and depth histograms, per source, sit within 0.05 of the
  weights `theory_weights.json` intended. The manifest carries both sides, so this is a check of the
  objective on disk against the objective on paper; the only way they can part is a dropped draw,
  which the same manifest counts per `T` and per source. The one drop a variant makes by its own
  rule, `fallback: false` dropping every visit whose `T` no chain fits (nocut), is added back to the
  realised `T` histogram before the comparison; every other drop reason counts against it. Below a few thousand visits the multinomial sampling error
  of the histogram is larger than 0.05, so the bound there is three of its own standard errors
  instead, reported per table as `sampling_bound_binds`.
- **V9 contamination** - every chain's question is a pool question, and the pool was screened
  against every evaluation set. The gate also pins the exemplar block per task by sha256 (the grid
  refuses to run against a different one) and refuses MATH exemplars drawn from the evaluation split,
  which the shot helper will silently do when no training split is reachable.

## The evaluation grid

Two protocols, two files, one run of `run_grid.py`.

| file | what is in it | who reads it |
|---|---|---|
| `cells_<task>_<name>_k<k>.jsonl` | the **no-limit pass**: one generation per question to horizon 4096, scored at the caps of record {0, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096}, one row per (question, cap), `budget` = `none` | `alloc` and Table 1, beside the base grids; `alloc.cells.cell_paths` already matches this name |
| `cells_budget_<task>_<name>_k<k>.jsonl` | the **budgeted passes**: one generation per stated budget {0, 32, 128, 512, 2048}, each with its own `Budget:` line and a hard stop at that budget | `analysis.py` (F1-F5) |

They are separate files because they are separate protocols: both write a row at cap 512, and a
loader that keys on (depth, cap, question) -- which `alloc` does -- would silently overwrite one with
the other. The budgeted file's name matches no `alloc` pattern, so that cannot happen by accident.

Every row carries the fields the base grids carry (`row_idx`, `k`, `B`, `split`, `n_cut`,
`natural_stop`, `n_prompt_tokens`, `n_suffix_tokens`, `n_answer_tokens`, `layer_passes`,
`layer_passes_promptfree`, `correct_v2`, ...) plus two this recipe adds: **`stop_reason`**
(`natural` when the chain stopped itself, `budget` when the stated cap cut it, `horizon` when the
4096-token horizon did) and **`chain_tail`**, the last 200 characters of the cut chain, so a row that
stopped badly can be read without regenerating it.

`analysis.py` reads the cap set **off the rows**, not from the config, and pairs only caps both grids
measured: a reference that ran to 512 is still comparable, at 512. F1 (own answer inside the cap) and
F5 (CSQA/AQuA at 0 and 32) are unchanged; F2 takes the no-limit median at the largest cap the grid
holds; F3 checks non-inferiority at the **top budget of the grid, 2048, and at the no-limit run cut
at 2048**; F4's commitment runs over the shared caps and still reports `G128`.

## Running it

    source env.sh ; PY=$PROD_PYTHON ; R=$PROD_ART/s36   # run from the repository root
    $PY train/theory_weights.py --cells-dir=$PROD_ART   # stage 0, once; re-pin the digest
    $PY train/chains.py gsm8k --root=$R --prompt=standard   # and --prompt=short, for each source
    $PY train/targets.py --root=$R --variant=budget_longest
    $PY train/gates.py --cpu --root=$R --variant=budget_longest
    $PY train/gates.py --v4  --root=$R --variant=budget_longest
    $PY train/train.py s36_budget_longest --root=$R --variant=budget_longest
    $PY train/run_grid.py s36_budget_longest gsm8k --root=$R --variant=budget_longest --k=4
    $PY train/run_grid.py A0 gsm8k --root=$R --variant=budget_longest --k=4   # the base reference, same protocol
    $PY train/analysis.py --root=$R --name=s36_budget_longest --ref=s33

**`--root` is required and has no default.** Every stage refuses to start without it, so two runs
can never write into one directory because nobody typed the flag.

**CSQA and AQuA rows come from the run root.** `run_grid.py` takes its question rows from the shared
harness's `split_rows`, which reads `<run root>/artifacts/data32_<task>.jsonl` for CSQA and AQuA;
GSM8K and MATH500 are loaded straight from their Hugging Face datasets. Those two files have to be
in the run root before stage 5 runs on those tasks.

**Stage 0 needs no run root and no GPU.** It reads the base grids and writes into the package, not
into a run; `--cells-dir` names the directory holding them, and `S36_CELLS_DIR` answers for it.

**The pool is pinned.** `config.yaml` carries `pool_sha256`, and stage 2 and gate V9 stop unless the
file at `pool_jsonl` hashes to it: V9's screening argument is about those exact questions. After a
deliberate re-screen, re-pin with `sha256sum <pool_jsonl>` and paste the digest into `config.yaml`.

**Waiting for the GPU.** `gates.py --v4`, `chains.py`, `train.py` and `run_grid.py` can wait for an
idle GPU. The V4 preflight waits only when `--wait` asks for it or `CLUSTER=0` marks the shared
unmanaged box, never under Slurm, and never with `--no-wait`.

`--prompt=short` reads `<run root>/prompts/prompts_short_<src>.txt` when that file exists and falls
back to the copy shipped in `prompts/`. Useful flags: `--sources=gsm8k,math` restricts the chains
table, `--max-steps=N` bounds training, `--budgets=0,32,none` overrides the grid, `--n=N` bounds the
problem count. The CPU tests run anywhere: `python -m pytest tests -q`.

## Compute, measured on the Spark (GB10, 121 GB unified)

Every rate below is measured; every hour is a rate times a count, and the counts that are estimates
are named as such. Contended means the smoke shared the card with two other jobs; **idle** divides by
the **3.3** contention factor the same smoke measured on training (149.2 vs 45.2 s/step).

| measured rate | value |
|---|---|
| train, micro 4 x accum 8 = 32 blocks, mixed 1024/1280 blocks | **149.2 s/step contended**, 45.2 s/step idle |
| train, 32 blocks of 1024 only / 1280 only (idle) | 38.9 s / 59.8 s per step |
| supervised density, one visit per block | **0.055** of padded tokens; padding share 0.329 at fixed 1024/1280 |
| supervised tokens per optimiser step (GSM8K+MATH smoke) | 2,033-2,142, i.e. **63.5 per visit** |
| chains, 100 questions, k=4, contended | GSM8K 415 s standard / 158 s short; MATH 995 s / 336 s |
| chain lengths at the old 512 horizon | GSM8K mean 72.6, max 159, **0.00 hit the horizon**; MATH mean 194, p90 340, **0.03 hit it** |
| grid, natural-stop decode rate, Ouro-1.4B base | 69.4 tok/s at k=4, 128.1 at k=2, 201.9 at k=1 |
| production record: `ouro_1_4b_base` natural grids, horizon 4096 | **43.2 GPU-h for 40 jobs** at full N (280 tokens per problem, the four S36 tasks at k=4 are 3.7 h of it) |

| smoke stage, measured (100-200 pool questions per source) | measured |
|---|---|
| targets + all CPU gates | 4 s + 3 s |
| V4 preflight (GPU) | 38 s, max abs diff 0.0 in bf16 on the GB10; the gate now compares in float32 against a 1e-3 relative bar |
| grid, 6 problems, k=4, budgets {0, 32, none} | 64 s, peak 19.9 GB, 54 cells, no field missing |
| train, 512-packing reference run, 1,136 steps, 18.61M tokens | 19,180 s, 970.4 tok/s, peak 48.3 GB |
| the packing factor of one visit per block | supervised density 0.0821 dense -> **0.0551** padded: **1.49x**, not the 2x estimated |

**Per-bucket step time.** Cost per block is modelled as `L (1 + L/6144)` -- the Ouro-1.4B split
between the 12d^2 linear term and the 4Ld attention term at d=2048, where the two are equal at
L = 3d = 6144 -- calibrated to the 45.2 s/step mixed measurement. The window is 32 blocks in every
bucket, so the step time is the per-block cost times 32:

| bucket | micro x accum | s/step idle | s/step contended |
|---|---|---|---|
| 1024 | 4 x 8 | **39** (measured 38.9) | 130 |
| 1536 | 2 x 16 | 63 | 208 |
| 2048 | 2 x 16 | 90 | 296 |
| 2560 | 2 x 16 | 119 | 393 |
| 3072 | 1 x 32 | 152 | 500 |

The model reproduces the measured 1024 point by construction and under-predicts the measured 1280
point by 15 percent (51 s against 59.8), so read the long buckets as a floor, not a ceiling.

**Chains, at the new per-source horizons.** Two prompts per source over the N of record (GSM8K
3,000, MATH 1,360, CSQA 1,500, AQuA 1,500). GSM8K, CSQA and AQuA cost nothing extra for the raise:
no GSM8K chain reached even 512. MATH pays for the 3 percent that did, now running to at most 2048,
at the 20.4 tok/s aggregate the smoke measured.

| source | basis | contended | idle |
|---|---|---|---|
| GSM8K | measured 4.15 + 1.58 s/question | 4.8 h | 1.4 h |
| MATH | measured 9.95 + 3.36 s/question, plus 0.4 h for the horizon tail | 5.4 h | 1.6 h |
| CSQA | **estimated**, GSM8K scaled by prompt+chain tokens (x0.91) | 2.2 h | 0.7 h |
| AQuA | **estimated**, GSM8K scaled (x1.00) | 2.4 h | 0.7 h |
| total, once for all variants | | **14.8 h** | **4.5 h** |

Raising the horizon is 0.4 h of that 14.8 h. The cost of the change is three percent of chain generation.

**Training, per variant, at 1.2M supervised tokens.** Two estimated counts drive it, both replaceable by
the stage-2 manifest before the run starts (`supervised_tokens_per_opt_step`, `visits_by_block_len`):

- supervised tokens per visit, **estimated 46.5** for the four-source mixture, from the measured
  63.5 of the GSM8K+MATH smoke and the measured chain lengths per task (GSM8K 48, MATH 118, CSQA 18,
  AQuA 41 per visit), with MATH held to its one-third share cap. That is **1,488 per 32-block step**
  and **about 800 steps** for 1.2M supervised tokens.
- the bucket mix, **estimated** from prompt length plus measured chain length: 1024 **0.94**, 1536
  0.06, 2048 and above under 0.01. Mean 41 s/step idle.

| per variant | idle | contended |
|---|---|---|
| train, about 800 steps | **9.1 h** | 30 h |
| the same plan under the old 512 recipe | 10.4 h (830 steps at 45.2 s) | 34 h |

Training is **cheaper**, not dearer, than the 512 recipe on the same four sources: the longer chains
put more supervised tokens in each visit, and bucketing stops the MATH blocks being padded to 1280.
The **7.4 h per variant** figure was 590 steps on a GSM8K+MATH-only mixture and is superseded.

**The grid, per variant, at horizon 4096.** Priced the way the production record is priced: tokens per
problem over the measured natural-stop rate, at 300 questions per (task, depth).

| pass | tokens per problem |
|---|---|
| no-limit, horizon 4096, 10 caps | mean natural stop (220, the production basis) + 6 read-outs = 292 |
| budgeted {0, 32, 128, 512, 2048} | 0 + 32 + 128 + 200 + 220 generated + 5 read-outs = 640 |
| total | **932**, against 680 for the 512 grid |

| per variant | hours |
|---|---|
| four tasks at k=4 | 4.5 h (1.12 h each; the 512 grid was 0.82 h each) |
| MATH500 at k=2, CSQA and AQuA at k=1 (F4, F5) | 1.4 h |
| **grid total per variant** | **5.9 h**, and the same again for the base reference |

That cross-checks against the production record: 3.7 h buys the four tasks at k=4 at full N (3,294
questions) and 280 tokens each, and 1,200 questions at 932 tokens each is 4.5 h at the same rate.

**Memory at the 4096 horizon, on the grid side.** Ouro-1.4B at k=4 holds 786 KB of KV per token, so
one row at the horizon is 3.2 GB and a width-16 batch would be 51 GB before the prompt. `run_grid.py`
sizes every batch with the harness's `batch_for` and halves it on an OOM, so it adapts; the
production queue met the same wall and pinned the width to 8 for its 4096-horizon jobs. The 69.4
tok/s rate above was measured at width 16, so a narrower width makes the grid hours below a floor.

**The largest uncertainty is the mean natural stop at 4096.** The 220-token figure is the production
estimator's, measured at a 512 horizon, and MATH500's 7-point gain between 512 and 4096 says the true
mean is longer on the hard tasks. At a 600-token mean the no-limit and 2048 passes both grow and the
grid is **2.4 h per (task, k)**, i.e. 12 h per variant rather than 6. The first grid job on the cluster
reports `passes.none.natural_stop_mean` and `natural_stop_max`; re-price from it before queueing the
rest.

**The plan of record, end to end, on an idle Spark.** Chains 4.5 h once, then `budget_longest`
train 9.1 h + grid 5.9 h, and the base reference grid 5.9 h: **about 26 h to the first
Table-1-comparable result**. `nobudget` adds 15 h; `budget_shortest` and `nocut` 15 h each. Contended
throughout it is roughly 57 h to the same point.

**Memory is the binding constraint, not time.** A first smoke at micro 8 x accum 4 peaked at
**101.3 GB** of the Spark's 121 GB, so the config ships micro 4 for the two short buckets: the same
32-block window, half the blocks resident per forward.

**What micro 4 actually measured.** A 20-step smoke run at micro 4 x accum 8 on 1024/1280 blocks
peaked at **58.4 GB**, but that number is censored: the process ran under a 59.3 GB allocator cap and
**15 of 20** steps took the OOM split path, halving the chunk for that window and restoring the full
width afterwards. The peak is therefore what the cap allowed, not what the configuration wants, and
the true uncapped peak is higher. **Budget 70 GB per variant** and do not place a second job beside it;
the 9.1 h per variant figure assumes an **uncontended** GPU, against the 3.3x the same smoke measured
while sharing the card.

**The bucket memory note, and the one number to watch.** The resident forward is `micro x block_len`
positions, so the shipped table keeps that product at or under 6,144: 4 x 1536, 2 x 2560, 1 x 3072.
The 58.4 GB censored peak was measured at 4 x 1280 = 5,120, so **the 1536 bucket is 20 percent above
anything that has been run** -- if a window of 1536 blocks OOMs (the log prints `[OOM] step N split
1 -> 2`), set `micro_by_block_len: {1536: 2}` and the accumulation follows automatically. The 2048
and 2560 buckets already ship at micro 2 and 3072 at micro 1 for the same reason. At micro 1 there is
nothing left to split, so an OOM there raises instead of retrying, by design.
