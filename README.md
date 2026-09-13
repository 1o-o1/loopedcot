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

Plan on the login node, giving the GPU memory since no GPU is visible there (96 for a 96 GB device):

```bash
$PROD_PYTHON -m prod.launcher --plan --gpus=8 --workers-per-gpu=2 --device-gb=96 --placement-horizon=1024
```

Run inside one allocation (edit `--gres`, `--time`, partition and account in the file; `--gpus`
inside it follows the allocation):

```bash
sbatch slurm/run.sbatch
$PROD_PYTHON -m prod.launcher --status   # from the login node, any time
```

When the time limit ends the job, `sbatch slurm/run.sbatch` again: the queue re-queues what was
running and every job resumes from its checkpoint. Do not submit a second one while the first is
alive. Inside the allocation the launcher maps its slots onto the GPUs Slurm made visible.

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

Analysis (`prod.score`, `prod.analyze`) reads the cells files; see the module docstrings.

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
`--placement-horizon=1024` (typical trace lengths) and one worker per GPU; a long tail that still
overflows is caught by the decoder, which halves the batch and retries, and exits non-zero if a row
still fails (the job is then re-queued by the next `--run`).

The forced-continuation block ("Wait" injection to 4096 on GSM8K and MATH500, Ouro only) is OFF by
default (`forced_block.enabled: false` in `prod/config.yaml`). To run it later: set it to `true` and
plan a new queue with `--root=<new dir>`.

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
prompt-inclusive and prompt-free, with FLOPs alongside. The calibration split is 100 items per dataset
by seed 20260908 (BBH stratified by subtask); policies are chosen on calibration rows and scored on the
rest.
