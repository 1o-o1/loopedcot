# loopedcot

Accuracy of looped language models over loop count and chain-of-thought length. The package generates,
scores and analyses the full accuracy surface for six checkpoints (Ouro-1.4B and Ouro-2.6B, base and
Thinking; Huginn-0125; McLeish Recurrent-Llama-3.2) on ten reasoning datasets, and evaluates a
calibrated allocator against each checkpoint's default operation at matched compute.

## 1. Setup (once, needs internet, about 38 GB of downloads)

```bash
git clone https://github.com/1o-o1/loopedcot.git && cd loopedcot
./setup_env.sh
```

`setup_env.sh` creates `.venv/` (torch comes from the machine's own install and must be a CUDA build),
installs the pinned packages from `requirements.txt` (transformers 4.56.2 is required: the Ouro remote
code fails below it), downloads the six checkpoints at pinned revisions into `hf/` (public repos, no
token), and verifies the data hashes. It ends with `environment ready`. If it stops earlier, the last
lines say which step failed.

Every later shell starts with:

```bash
cd loopedcot && source env.sh
```

`env.sh` puts the model cache offline (`HF_HUB_OFFLINE=1`) and sets `PROD_ART=artifacts/`,
`PROD_LOGS=logs/` and `PROD_PYTHON=.venv/bin/python`.

## 2. GPU check (one job, a few minutes)

```bash
$PROD_PYTHON -m prod.generate --model=ouro_1_4b_base --task=gsm8k --k=4 --n=20
```

It ends with a `DONE ... peak <GB> GB` line. The 20 problems it writes are part of the real job and
are skipped by the full run later. Read the peak: if it is under a third of the GPU's memory, run the
queue with `--workers-per-gpu=2` below, otherwise use `--workers-per-gpu=1`.

## 3. Plan and run

```bash
$PROD_PYTHON -m prod.launcher --plan --gpus=8 --workers-per-gpu=2
```

Prints `queued 262 jobs ...`. If it also prints an `unplaceable` list, stop: those jobs do not fit
the GPU by the memory estimate (see section 6). With nothing unplaceable:

```bash
setsid nohup $PROD_PYTHON -m prod.launcher --run --gpus=8 --workers-per-gpu=2 > $PROD_LOGS/launcher.log 2>&1 < /dev/null &
$PROD_PYTHON -m prod.launcher --status
```

`--status` prints the counts in `todo / claimed / done / failed` and the log of every failure. Run it
any time. `--gpus=8` means CUDA devices 0 to 7; `--gpu-ids=0,1,2` selects specific ones.

**If anything is interrupted** (a worker dies, the node reboots, you stop it), run the same `--run`
command again. It moves stranded claims back to the queue and every job resumes from its own
per-problem checkpoint; no row is generated twice. A `--run` on an existing queue never re-plans it.
Never start a second launcher on a live queue without `--no-requeue`.

## 3b. The same under Slurm

Setup (section 1) runs on the login node, which has internet; the model cache it fills is read
offline by the jobs. The GPU check is one submission:

```bash
sbatch slurm/gpu_check.sbatch          # then read logs/slurm-check-<jobid>.out for the DONE line
```

Plan either as a one-GPU job (`sbatch slurm/plan.sbatch`) or on the login node, giving the GPU memory
since no GPU is visible there (96 for a 96 GB device):

```bash
$PROD_PYTHON -m prod.launcher --plan --gpus=8 --workers-per-gpu=2 --device-gb=96 --placement-horizon=2048
```

The five `slurm/*.sbatch` files are templates (`plan`, `run`, `gpu_check`, `alloc` for the allocator on every
finished grid on CPU, `live` for the live allocator check on one GPU). Copy each to `<name>.slurm` at the repository root,
put your partition, account, mail and environment lines there, and submit those: `*.slurm` and
`slurm_script.sh` are git-ignored, so `git pull` never touches them. The install record
(`artifacts/model_install.json`) is local too; the pins file in `prod/tasks/data/` is only read.

Run inside one allocation (edit `--gres`, `--time`, partition and account in the file; `--gpus`
inside it follows the allocation):

```bash
sbatch slurm/run.sbatch
$PROD_PYTHON -m prod.launcher --status   # from the login node, any time
```

When the time limit ends the job, `sbatch slurm/run.sbatch` again: the queue re-queues what was
running and every job resumes from its checkpoint. Inside the allocation the launcher maps its
slots onto the GPUs Slurm made visible.

**More than one node on the same queue** is fine: claims are atomic renames, and every claim records
the Slurm job that holds it. A launcher that starts (or restarts) re-queues only claims whose Slurm
job is no longer in `squeue`, so a second `sbatch slurm/run.sbatch` on another node simply takes
the next jobs. Both nodes write into the same `artifacts/` (a shared home is required).

## 4. Completeness and cleanup

```bash
$PROD_PYTHON -m prod.manifest --check --cells=$PROD_ART --manifest=$PROD_ART/manifest.json
$PROD_PYTHON -m prod.cleanup --cells=$PROD_ART --manifest=$PROD_ART/manifest.json          # dry run
$PROD_PYTHON -m prod.cleanup --cells=$PROD_ART --manifest=$PROD_ART/manifest.json --apply
```

Cleanup strips the long text fields from completed jobs and removes their trace checkpoints; with
`--manifest` a job counts as complete only when its row count matches the manifest.

## 5. Results

All under `artifacts/`:

| file | what |
|---|---|
| `cells_<model>_<task>_natural_k<k>.jsonl` | one row per (problem, cap): `pred`, `correct`, `trace_answer`, `trace_correct`, `correct_v2`, `natural_stop`, `n_cut`, costs, `batch_width`, `split`. The first line is a `_header` row holding the effective config and its sha256. |
| `meta_<model>_<task>_natural_k<k>.json` | the job record: rows written and expected, timings, `peak_gb`, accuracy by cap. |
| `trace_<...>.jsonl` | per-problem generation checkpoint (resume state only). |
| `manifest.json` | the run list the queue was planned from. |
| `launcher_plan.json`, `launcher_status.json`, `queue/` | the queue and its state. |

## 5b. Analysis

Every command reads the cells files of one (checkpoint, dataset, protocol) grid, shards included, and
writes under `artifacts/`. `--protocol=forced` selects the forced-continuation grid.

```bash
source env.sh
$PROD_PYTHON -m prod.score --cells=$PROD_ART --model=ouro_1_4b_think --task=math500                     # k x cap table, parse rates, commitment mechanism (G, c, l)
$PROD_PYTHON -m prod.analyze.figures --cells=$PROD_ART --model=ouro_1_4b_think --task=math500           # heatmap, frontier, card, arrival, gain figures
$PROD_PYTHON -m prod.analyze.figures --cells=$PROD_ART --model=ouro_1_4b_think --task=math500 --protocol=forced
$PROD_PYTHON -m prod.analyze.cards --cells=$PROD_ART --model=ouro_1_4b_think --tasks=gsm8k,math500,aqua  # per-checkpoint card over several datasets
$PROD_PYTHON -m prod.live_check --model=ouro_1_4b_base --task=gsm8k --cells=$PROD_ART --alloc-dir=$PROD_ART/alloc_v5_gsm8k_ouro_1_4b_base --budget-fraction=0.5 --no-generate   # the allocator's pick per prompt, read from alloc's results.json
$PROD_PYTHON -m prod.analyze.table1 --cells=$PROD_ART --models=ouro_1_4b_base,ouro_1_4b_think,ouro_2_6b_base,ouro_2_6b_think --tasks=gsm8k,math500,svamp,aqua,csqa,arc,strategyqa,bbh,mmlu,hellaswag --accounting=both   # Table 1: default vs allocator at 25/50/100% of the default cost
$PROD_PYTHON -m alloc.cli --cells $PROD_ART --task <task> --checkpoint <model> --model-config prod/config.yaml --accounting all --avg-budget --promptfree --boot 2000 --out $PROD_ART/alloc_v6_<task>_<model>   # the allocator (v6): arm of record avg_gated_equation_resolved, the label-only baseline avg_gated_lookup, the per-prompt rules, every accounting
$PROD_PYTHON -m alloc.cli --cells $PROD_ART --task <task> --checkpoint <model> --model-config prod/config.yaml --accounting all --avg-budget --promptfree --boot 2000 --protocol natural2 --out $PROD_ART/alloc_v6n2_<task>_<model>   # the same on the think-tag continuation grid (natural2h for the horizon extension)
$PROD_PYTHON -m prod.live_check --model=<model> --task=<task> --cells=$PROD_ART --alloc-dir=$PROD_ART/alloc_v6_<task>_<model> --budget-fraction=0.5 --arm avg_gated_equation_resolved   # live check of the arm of record at alloc's own picks; --arm avg_gated_lookup, equation_resolved, lookup read the same way
```

`prod.score` prints the accuracy table and writes `score_<model>_<task>_<protocol>.json`; the figures
go to `artifacts/figures/`; `table1` writes `artifacts/table1.md` and `.json` (per prompt the budget is a
fraction of the cap cost of the default's own uncapped cell, so the 100 percent row reproduces the uncapped
baseline; realised spend is reported beside every row; `--trained=<model>` adds the trained checkpoint's row).
`alloc.cli` (package `alloc/`, its README explains the method) writes: `cards.json` (the checkpoint's calibration
card: per-cell accuracy and price, the two rankings, the label-free commitment curve); `results.json` (per budget, every
arm's paired accuracy, gain and bootstrap intervals, under the accounting the gains are priced in; `table1` is priced under
the first accounting of `--accounting`, named by `table1_accounting`, and `table1_by_accounting.expected` is the
expected-accounting table; `picks` holds every arm's per-prompt pick per accounting and budget, with the calibration ids
they were fitted on); `table1_cap.md` (arms
charged the whole cap they commit to); `table1_expected.md` (arms charged the mean chain length the calibration prompts
realised at that cell, the decision-time price the average-budget arms are fitted under); `table1_realised.md` (arms
charged what their rows actually generated, an audit price). The arm of record is `avg_gated_equation_resolved`: cells
ranked by the commitment identity resolved by settle time (`equation_resolved`), the average budget held over the
prompts, and every deviation from the default verified by a two-fold gate on the calibration questions;
`avg_gated_lookup` is the label-only baseline, the same policy ranked by calibration accuracy alone. `--protocol
natural2|natural2h` runs the allocator on the continuation grid of the same pair instead of the natural-stop grid
(default `natural`; only the files carrying that protocol segment are read). `prod.live_check --alloc-dir <alloc
output> --arm <arm>` reads that arm's picks for the budget fraction out of alloc's `results.json` (it refuses to run
without them, or if the cells' split is not the one alloc calibrated on), regenerates every evaluation prompt at its
recorded cell and prints n, live accuracy, grid accuracy at the same picks, live minus grid in points, and the mean
realised price against the budget; the arms are `avg_gated_equation_resolved`, `avg_gated_lookup`,
`equation_resolved` and `lookup` (default), all read the same way, and `--preflight` runs one throwaway generation
first so a broken environment fails before the picks are spent.
The calibration split grows with the dataset, min(300, 20 percent of N) with a floor of 100, promoted from the
evaluation split in seeded order (round-robin over subtasks on BBH; `--n-cal` overrides), and the gate fits on 70
percent of it and verifies every deviation from the default on the rest, with the verified margin, its sd and the cost
saving printed under Table 1 for each gated deviation. The gate tests the structured deviation families
first, smallest first (F0 the deepest depth at cap 0, F1 the deepest depth at any cap, F2 one depth shallower, then F3
the free set), and Table 1's oracle-gap column is the best single evaluation cell minus each arm at 1.0x, a diagnostic
of calibration noise that no arm reads.

## 6. What the queue is

262 jobs, one per (checkpoint, dataset, loop count), all at full N, natural stop at horizon 4096, caps
{0, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096}. Order: Ouro-1.4B base and Thinking on all ten
datasets, then Ouro-2.6B base and Thinking, then McLeish, then Huginn. Estimated 185 GPU-hours at an
assumed 4x speed-up over the GB10 where the rates were measured; the GPU check in section 2 is what
replaces that assumption.

Batch width is pinned at 16 and stored per row. Three (checkpoint, depth) pairs do not fit a 141 GB GPU
at width 16 and horizon 4096 by the memory estimate, so `prod/config.yaml` overrides them: Ouro-2.6B at
k=3,4 width 8, Huginn k=16 width 8, Huginn k=32 width 4. With those, nothing is unplaceable on a 141 GB
device. The estimate is a worst case (every row of a batch at 4096 tokens); on GPUs under about 80 GB it
refuses most jobs while the measured peak of a 16-row Ouro-1.4B k=4 job is 13 GB. There, plan with
`--placement-horizon=2048` (a k=3/4 job then shares a card only with a k=1/2 job; measured peaks of
long-chain jobs reach 50 GB) and two workers per GPU; a long tail that still
overflows is caught by the decoder, which halves the batch and retries, and exits non-zero if a row
still fails (the job is then re-queued by the next `--run`).

The forced-continuation block ("Wait" injection to 4096 on GSM8K and MATH500, Ouro only) is OFF by
default (`forced_block.enabled: false` in `prod/config.yaml`). To run it later: set it to `true` and
plan a new queue with `--root=<new dir>`.

### Continuing a stored chain instead of regenerating it

Every natural-stop job writes `chains_<model>_<task>_k<k>.jsonl`, one row per problem holding the
chain up to its own stop, and the cluster has all 262 of them. `prod.generate --continue-chains=<mode>`
replays those ids as the prefix and carries the greedy decoding on, so a chain that stopped too early
costs its continuation rather than a whole regeneration. Two modes:

| mode | rows it continues | selection field | where it stops |
|---|---|---|---|
| `think_tag` | the chain ended at the closing think tag | `stop_marker == "</think>"` in the OLD cells rows (the chains file records the stop position, not which marker made it) | the tag is put back and decoding runs on to the task's stop strings, the tokenizer eos, or the horizon |
| `horizon` | the chain reached the old horizon | `natural_stop` in the chains file: missing or >= the old horizon | the new `--horizon` |

The cuts and forced read-outs are recomputed at **every** cap in `--caps` for the continued rows. A cap
at or below a continued row's old stop is **copied** from the old cells row, not regenerated: the cut is
`min(stop, B) = B` under both stop rules and the first `B` ids are the same ids, so the read-out is
identical and stays bit-comparable to the published grid, which a regeneration at a different batch
composition would not be. Rows the mode did not select are copied at every cap (a cap the old grid never
had is served by the copied row with the same cut). Output goes to a new grid under `--protocol-tag`
(`natural2` for think_tag, `natural2h` for horizon, so both can exist for one cell); the source cells
file and the chains sidecar are only ever read, and `prod.cleanup` never deletes a chains file.

```bash
source env.sh
# C1, think_tag: for MODEL in ouro_1_4b_think ouro_2_6b_think; for TASK in the ten; for K in 1 2 3 4
$PROD_PYTHON -m prod.generate --model=$MODEL --task=$TASK --k=$K --protocol=natural \
  --continue-chains=think_tag --protocol-tag=natural2 --out=$PROD_ART \
  --horizon=4096 --caps=0,16,32,64,128,256,512,1024,2048,4096 --no-extra-caps --old-horizon=4096
# C2, horizon to 8192: the same two checkpoints on the ten tasks, plus mcleish_llama32_r32 on
# math500 and strategyqa (K in 1 2 4 8 there); 8192 must be IN --caps or the new tail is never scored
$PROD_PYTHON -m prod.generate --model=$MODEL --task=$TASK --k=$K --protocol=natural \
  --continue-chains=horizon --protocol-tag=natural2h --out=$PROD_ART \
  --horizon=8192 --caps=0,16,32,64,128,256,512,1024,2048,4096,8192 --no-extra-caps --old-horizon=4096
```

Pass no `--batch-width` and the per-(model, k) table in `config.yaml` applies (16, or 8 for Ouro-2.6B
at k=3,4). A C2 job's KV cache is twice a natural-stop job's, since its horizon is.

Cost, from the cells and meta files of the 88 jobs concerned (rates are each job's own measured
tokens/s; two jobs finished in a resumed process that generated nothing and take the median of their
(model, k)):

| | rows | continuation candidates | continuation tokens | GPU-hours | full regeneration |
|---|---|---|---|---|---|
| C1 think_tag, 80 jobs (2 Thinking checkpoints x 10 tasks x k1-4) | 107,944 | 89,163 (82.6%) | 14.6 M at 150/row + 126,586 read-out groups | **59** | 408 |
| C2 horizon to 8192, 88 jobs (the same 80, plus McLeish on math500 and strategyqa) | 119,104 | 22,215 (18.7%): 18,777 Ouro, 3,438 McLeish | 91 M at 4096/row | **145** (289 if the chain prefill is charged at the decode rate) | 510 |

The hours are cluster hours, not GB10 hours: they are priced off the rates these jobs actually ran at.
The continuation prefill (one forward pass over the stored chain per row) is free in the lower figure
and charged at the full decode rate in the upper one; the truth is near the lower end.

## 7. Layout

- `prod/config.yaml`, `prod/config.py`: every knob (models and loop sets, per-job batch widths, caps, horizon, datasets, calibration seed, workers per GPU). Command-line flags override the file.
- `prod/tasks/`: dataset loaders, prompts, suffixes, parsers, the calibration split; `data/` holds the rows and prompt files with their hashes and provenance (`data/README_prompts.md`, `data/sources.json`).
- `prod/models/`: one adapter per family (`ouro.py`; `raven.py` for Huginn and McLeish, with batched left-padded decoding).
- `prod/generate.py`: one job. Natural stop to the horizon, cut at every cap, one forced read-out per distinct cut, both parses, per-problem resume.
- `prod/score.py`, `prod/cost.py`: protocol-v2 labels and commitment arrival; layer passes, FLOPs, KV bytes.
- `prod/manifest.py`, `prod/launcher.py`: the job list with priorities; a claim-file queue over GPUs with memory-aware placement, re-queue and resume.
- `prod/live_check.py`: the allocation rule end to end on one dataset, against its offline value.
- `prod/analyze/`: cards, surface tests, the allocator with paired and calibration-draw bootstraps, figures.
- `prod/cleanup.py`, `prod/install_models.py`, `prod/checks.py`, `prod/rescore.py` (rebuilds labels from the stored read-out text; dry run by default).
- `tests/`: CPU unit tests (`python tests/test_parsers_pp3.py`, `tests/test_config_yaml.py`, `tests/test_launcher_placement.py`).

## 8. Protocol in one paragraph

Greedy decoding, bf16, batch width pinned per job and stored per row. Each problem is generated once
per loop count to its natural stop (horizon 4096); every cap is a cut of that chain followed by the
read-out suffix. A cell's label is the model's own answer if it was written and parses within the cut,
else the forced read-out (protocol v2). Costs are layer passes k x L x (prompt + generated + read-out),
prompt-inclusive and prompt-free, with FLOPs alongside. 100 items per dataset are held out at generation time
by seed 20260908 (BBH stratified by subtask); at analysis time `alloc` calibrates on min(300, 20 percent of N)
questions, floor 100, taken as the first ids of that seeded order, and the evaluation split shrinks by the
same count (MATH500, SVAMP and AQuA stay at 100). Policies are chosen on the calibration questions and
scored on the rest.

## 9. Training recipe (S36)

`train/` is the budget-conditioned anytime training package: it self-distils Ouro-1.4B on its own
correct chains and teaches one looped adapter to answer at any token budget and any loop count k in
{1, 2, 3, 4}. LoRA r16 alpha 32 on the seven projections, base frozen. Chains are generated from the
base model at k=4 on the TRAIN splits of GSM8K, MATH, CSQA and AQuA (natural stop, per-source
horizons 1024, MATH 2048; a chain that hits its horizon is discarded), and each training example is
the task's evaluation exemplar block byte-identical, the question, one line `Budget: T tokens.` or
`Budget: no limit.`, and the answer prefix; the target is the longest correct chain that fits T,
ending in the answer sentence then EOS, with cross-entropy on the chain, answer and EOS only, read
from `lm_head` on the sampled depth's hidden state and divided by the window's supervised-token
count. The theory sets the training distribution: per source, T and the block depth are drawn from
`train/data/theory_weights.json`, each table half uniform and half the base model's own production
grid (the accuracy left unrealised at that cap, and the allocator's depth usage with the deepest
depth floored at 0.20), the file sha-pinned in `train/config.yaml` and the realised draws checked by
gate V10. Variants: `budget_longest` (the recipe) and `uniform_longest` (the same targets under a uniform
T and a flat depth mix). The reference is this repository's own `ouro_1_4b_base` production grid.

```bash
R=$PROD_ART/s36
$PROD_PYTHON -m train.chains gsm8k --prompt=standard --root=$R    # x4 sources x {standard,short}
$PROD_PYTHON -m train.targets --variant=budget_longest --root=$R
$PROD_PYTHON -m train.gates --cpu --variant=budget_longest --root=$R   # V1 V2 V3-CONTEXT V9 V10
$PROD_PYTHON -m train.gates --v4 --variant=budget_longest --no-wait --root=$R
$PROD_PYTHON -m train.train s36_budget_longest --variant=budget_longest --no-wait --root=$R
$PROD_PYTHON -m train.run_grid s36_budget_longest gsm8k --variant=budget_longest --k=4 --no-wait --root=$R   # writes cells_gsm8k_s36_budget_longest_full_k4.jsonl (production rows and split; --eval-rows=s32 for the 300+100 subset)
$PROD_PYTHON -m train.analysis --name=s36_budget_longest_full --ref=ouro_1_4b_base --ref-dir=$PROD_ART --root=$R
```

`train.analysis` loads its reference as `<ref-dir>/cells_<task>_<ref>_k<k>.jsonl`, so the
production grids, which are named `artifacts/cells_ouro_1_4b_base_<task>_natural_k<k>.jsonl`,
have to be reachable under that spelling before the last line runs.

Under Slurm the same six stages are `slurm/chains_s36.sbatch` (array 0-7, one source and one prompt
each), `slurm/variant_s36.sbatch` (array 0-1, targets then gates then training for one variant) and
`slurm/grids_s36.sbatch` (array 0-7, one variant and one task each, with the analysis command in its
header). `--root` is required and has no default. Everything else -- the target rule, the gates, the
two grid files, the measured compute -- is in `train/README.md`.
