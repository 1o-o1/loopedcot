#!/bin/bash
# Chain-continuation runs (prod.generate --continue-chains): one Slurm job per (model, task, depth), one GPU
# each, ALL submitted at once so the scheduler fills every free GPU on every node. Run from anywhere:
#   bash slurm/continue_chains.sh run     # everything: probe the nodes, then (re)submit whatever is not done, avoiding bad nodes
#   bash slurm/continue_chains.sh probe   # one 5-minute job per GPU node: can torch initialise CUDA there? waits for the
#                                         # verdicts and writes logs/bad_nodes.txt; every later submission excludes those nodes
#   bash slurm/continue_chains.sh c1      # think-tag continuation: 2 Thinking checkpoints x 10 tasks x depths 1-4 = 80 jobs
#   bash slurm/continue_chains.sh c2      # horizon 4096 -> 8192 on the ten (model, task, depth) below; a Thinking job
#                                         # waits for its c1 job (afterok) and continues from the natural2 cells
#   bash slurm/continue_chains.sh retry   # resubmit every c1 and c2 job that is not RC=0 and not running/pending; a node
#                                         # whose job died at CUDA start is added to logs/bad_nodes.txt and excluded
#   bash slurm/continue_chains.sh c2more  # the four extra k=2 Thinking jobs, only once c2 is done and GPUs are idle
#   bash slurm/continue_chains.sh c2all   # every remaining cell with 2 percent or more chains at the 4096 horizon (73 jobs, includes c2more)
#   bash slurm/continue_chains.sh status  # finished / failed counts, and the last 30 log lines of every failed job
#   bash slurm/continue_chains.sh report  # per c2 job: rows continued, share stopped before 8192, accuracy at caps 4096 and 8192
# Every job log starts with the node, CUDA_VISIBLE_DEVICES and nvidia-smi -L, and ends with RC=<exit code of
# prod.generate>; the batch job exits with that code, so an afterok dependency really waits for success.
# Outputs: cells_<model>_<task>_natural2_k<K>.jsonl (c1) and cells_<model>_<task>_natural2h_k<K>.jsonl (c2).
# Knobs (export before running): TIME_C1 (24:00:00) TIME_C2 (48:00:00) MEM (64gb) CPUS (8) SBATCH_EXTRA HITLIST
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
source "$ROOT/env.sh"
mkdir -p logs
MODE="${1:-}"
TIME_C1="${TIME_C1:-24:00:00}"; TIME_C2="${TIME_C2:-48:00:00}"; MEM="${MEM:-64gb}"; CPUS="${CPUS:-8}"
EXTRA="${SBATCH_EXTRA:-}"
CAPS_C1="0,16,32,64,128,256,512,1024,2048,4096"
CAPS_C2="0,16,32,64,128,256,512,1024,2048,4096,8192"
C1_MODELS="ouro_1_4b_think ouro_2_6b_think"
TASKS="gsm8k math500 svamp aqua csqa arc strategyqa bbh mmlu hellaswag"
# The horizon-extension set (model:task:depth): the deepest depths of the two tasks whose chains run into the
# 4096 horizon most (MATH500, AQuA) on the Thinking checkpoints, and McLeish's deepest depth on MATH500 and
# StrategyQA. The full >= 5% horizon-hit list is 83 jobs and was cut to these ten on 2026-09-17.
HITLIST="${HITLIST:-ouro_1_4b_think:math500:4 ouro_1_4b_think:math500:3 ouro_1_4b_think:aqua:4 ouro_1_4b_think:aqua:3 ouro_2_6b_think:math500:4 ouro_2_6b_think:math500:3 ouro_2_6b_think:aqua:4 ouro_2_6b_think:aqua:3 mcleish_llama32_r32:math500:8 mcleish_llama32_r32:strategyqa:8}"
HITLIST_MORE="ouro_1_4b_think:math500:2 ouro_1_4b_think:aqua:2 ouro_2_6b_think:math500:2 ouro_2_6b_think:aqua:2"
# Every remaining (model, task, depth) whose 4096-horizon chains hit the horizon on 2 percent or more of
# the questions (counted on the natural2 grids for the Thinking models and the natural grids for McLeish,
# 2026-09-20), heaviest first: the shallow depths, where the Thinking models run long. 73 jobs.
HITLIST_ALL="ouro_1_4b_think:aqua:1 ouro_1_4b_think:strategyqa:1 ouro_1_4b_think:bbh:1 ouro_1_4b_think:math500:1 ouro_1_4b_think:csqa:1 mcleish_llama32_r32:strategyqa:1 mcleish_llama32_r32:hellaswag:1 ouro_2_6b_think:math500:1 ouro_1_4b_think:hellaswag:1 ouro_2_6b_think:bbh:1 mcleish_llama32_r32:math500:1 ouro_2_6b_think:aqua:1 ouro_1_4b_think:gsm8k:1 mcleish_llama32_r32:mmlu:1 ouro_2_6b_think:strategyqa:1 ouro_1_4b_think:arc:1 ouro_1_4b_think:svamp:1 mcleish_llama32_r32:aqua:1 ouro_1_4b_think:aqua:2 ouro_1_4b_think:math500:2 mcleish_llama32_r32:bbh:1 ouro_1_4b_think:mmlu:1 mcleish_llama32_r32:math500:2 ouro_1_4b_think:bbh:2 ouro_2_6b_think:math500:2 ouro_2_6b_think:hellaswag:1 ouro_2_6b_think:csqa:1 mcleish_llama32_r32:strategyqa:2 ouro_2_6b_think:svamp:1 ouro_2_6b_think:mmlu:1 mcleish_llama32_r32:gsm8k:1 ouro_2_6b_think:gsm8k:1 ouro_2_6b_think:aqua:2 mcleish_llama32_r32:hellaswag:2 mcleish_llama32_r32:strategyqa:4 mcleish_llama32_r32:bbh:2 mcleish_llama32_r32:math500:4 ouro_1_4b_think:mmlu:2 ouro_1_4b_think:hellaswag:2 ouro_1_4b_think:csqa:2 ouro_1_4b_think:strategyqa:2 ouro_2_6b_think:bbh:2 mcleish_llama32_r32:aqua:2 mcleish_llama32_r32:mmlu:2 ouro_1_4b_think:svamp:2 ouro_1_4b_think:gsm8k:2 ouro_2_6b_think:arc:1 ouro_2_6b_think:svamp:2 mcleish_llama32_r32:svamp:1 ouro_2_6b_think:hellaswag:2 mcleish_llama32_r32:gsm8k:2 ouro_1_4b_think:arc:2 ouro_2_6b_think:mmlu:2 ouro_2_6b_think:csqa:2 ouro_2_6b_think:strategyqa:2 ouro_2_6b_think:bbh:3 ouro_1_4b_think:gsm8k:3 mcleish_llama32_r32:aqua:4 ouro_2_6b_think:mmlu:4 ouro_2_6b_think:hellaswag:3 ouro_2_6b_think:csqa:3 ouro_2_6b_think:bbh:4 ouro_1_4b_think:gsm8k:4 ouro_2_6b_think:mmlu:3 ouro_2_6b_think:hellaswag:4 mcleish_llama32_r32:hellaswag:4 ouro_2_6b_think:gsm8k:2 ouro_2_6b_think:csqa:4 mcleish_llama32_r32:aqua:8 ouro_1_4b_think:arc:3 ouro_2_6b_think:strategyqa:4 ouro_1_4b_think:arc:4 ouro_2_6b_think:strategyqa:3"

width_for() {  # the batch width for 8192-token sequences: half the width the 4096 grid used for this model/depth
  case "$1:$2" in
    ouro_2_6b_think:3|ouro_2_6b_think:4|ouro_2_6b_base:3|ouro_2_6b_base:4) echo 4 ;;   # 4096 override is 8
    huginn_0125:16) echo 4 ;; huginn_0125:32) echo 2 ;;                                 # 4096 overrides 8 and 4
    *) echo 8 ;;                                                                         # config batch_width 16
  esac
}

ok_log()   { [ -f "logs/$1.out" ] && grep -q "^RC=0" "logs/$1.out"; }

# Nodes to avoid: every node whose probe failed, plus every node where a c1/c2 job died at CUDA start
# (the two signatures seen on 2026-09-17). Kept in logs/bad_nodes.txt; submit() excludes them.
collect_bad_nodes() {
  { [ -f logs/bad_nodes.txt ] && cat logs/bad_nodes.txt
    for f in logs/probe_*.out; do [ -f "$f" ] || continue; grep -q "^RC=" "$f" && ! grep -q "^RC=0" "$f" && { n=${f#logs/probe_}; echo "${n%.out}"; }; done
    for f in logs/c1_*.out logs/c2_*.out; do [ -f "$f" ] || continue; case "$f" in *.prev.out) continue ;; esac
      grep -q "CUDA unknown error\|No devices were found" "$f" && grep -m1 "^node=" "$f" | sed "s/^node=\([^ ]*\).*/\1/"; done
  } | grep -v "^$" | sort -u > logs/bad_nodes.tmp && mv -f logs/bad_nodes.tmp logs/bad_nodes.txt
}
exclude_arg() { [ -s logs/bad_nodes.txt ] && echo "--exclude=$(paste -sd, logs/bad_nodes.txt)"; }
in_queue() { squeue -u "$USER" -h -n "$1" -o %j | grep -qx "$1"; }

submit() {  # submit <name> <time> <dependency or ""> <command...>; prints the job id
  local name="$1" time="$2" dep="$3"; shift 3
  [ -f "logs/${name}.out" ] && mv -f "logs/${name}.out" "logs/${name}.prev.out"
  sbatch --parsable $EXTRA $(exclude_arg) ${dep:+--dependency=afterok:$dep} --job-name="$name" --gres=gpu:1 \
    --cpus-per-task="$CPUS" --mem="$MEM" --time="$time" --output="logs/${name}.out" \
    --wrap="echo node=\$(hostname) CUDA_VISIBLE_DEVICES=\${CUDA_VISIBLE_DEVICES:-unset}; nvidia-smi -L; cd '$ROOT' && $* ; rc=\$?; echo RC=\$rc; exit \$rc"
}

c1_cmd() { echo "$PROD_PYTHON -m prod.generate --model=$1 --task=$2 --k=$3 --protocol=natural --out=$PROD_ART --continue-chains=think_tag --protocol-tag=natural2 --horizon=4096 --old-horizon=4096 --caps=$CAPS_C1 --no-extra-caps --no-think-tag-is-stop"; }
c2_cmd() {  # c2_cmd <model> <task> <k>
  local src=""
  [[ "$1" == ouro_* ]] && src="--continue-from-cells=$PROD_ART/cells_${1}_${2}_natural2_k${3}.jsonl"
  echo "$PROD_PYTHON -m prod.generate --model=$1 --task=$2 --k=$3 --protocol=natural --out=$PROD_ART --continue-chains=horizon --protocol-tag=natural2h --horizon=8192 --old-horizon=4096 --caps=$CAPS_C2 --no-extra-caps --batch-width=$(width_for "$1" "$3") $src"
}

record_c1() {  # record_c1 <model> <task> <k> <jobid>: replace the pair's line in logs/c1_jobs.txt
  touch logs/c1_jobs.txt
  awk -v m="$1" -v t="$2" -v k="$3" '!($1==m && $2==t && $3==k)' logs/c1_jobs.txt > logs/c1_jobs.tmp
  echo "$1 $2 $3 $4" >> logs/c1_jobs.tmp; mv -f logs/c1_jobs.tmp logs/c1_jobs.txt
}

submit_c1_pair() {  # skips a pair already RC=0 or in the queue
  local name="c1_${2}_${1}_k${3}"
  ok_log "$name" && { echo "  done   $name"; return 1; }
  in_queue "$name" && { echo "  queued $name"; return 1; }
  local jid; jid=$(submit "$name" "$TIME_C1" "" "$(c1_cmd "$1" "$2" "$3")")
  record_c1 "$1" "$2" "$3" "$jid"; echo "  sent   $name ($jid)"
}

submit_c2_pair() {  # a Thinking pair waits for its c1 job unless that job is already RC=0
  local name="c2_${2}_${1}_k${3}" dep=""
  ok_log "$name" && { echo "  done   $name"; return 1; }
  in_queue "$name" && { echo "  queued $name"; return 1; }
  if [[ "$1" == ouro_* ]] && ! ok_log "c1_${2}_${1}_k${3}"; then
    dep=$(awk -v m="$1" -v t="$2" -v k="$3" '$1==m && $2==t && $3==k {print $4}' logs/c1_jobs.txt 2>/dev/null)
    [ -n "$dep" ] || { echo "  skip   $name: its c1 job is neither done nor recorded (run c1 or retry first)"; return 1; }
  fi
  local jid; jid=$(submit "$name" "$TIME_C2" "$dep" "$(c2_cmd "$1" "$2" "$3")")
  echo "  sent   $name ($jid)${dep:+ after c1 job $dep}"
}

do_retry() {  # (re)submit every c1 and c2 job that is neither RC=0 nor in the queue, avoiding the bad nodes
  collect_bad_nodes; echo "excluded nodes: $(paste -sd, logs/bad_nodes.txt 2>/dev/null)"
  # c2 jobs still waiting on a c1 job that failed can never start (afterok): cancel them, resubmit below
  for j in $(squeue -u "$USER" -h -o "%i %j %r" | awk '$2 ~ /^c2_/ && $3 ~ /Dependency/ {print $1}'); do scancel "$j"; done
  for M in $C1_MODELS; do for T in $TASKS; do for K in 1 2 3 4; do submit_c1_pair "$M" "$T" "$K"; done; done; done | grep -v "  done\|  queued"
  submit_c2_list "$HITLIST" | grep -v "  done\|  queued"
}

submit_c2_list() { local n=0 M T K; for item in $1; do IFS=: read -r M T K <<< "$item"; submit_c2_pair "$M" "$T" "$K" && n=$((n + 1)); done; echo "c2: $n jobs submitted"; }

case "$MODE" in
  probe|run)
    # GPU nodes that are up (down/drained ones are left alone, a probe there would only pend)
    nodes=$(sinfo -h -N -o "%N %G %T" | awk '$2 ~ /gpu/ && $3 !~ /down|drain|drng|fail|maint|unk/ {print $1}' | sort -u)
    rm -f logs/probe_*.out
    for n in $nodes; do
      sbatch --parsable $EXTRA --nodelist="$n" --job-name="probe_$n" --gres=gpu:1 --cpus-per-task=2 --mem=8gb --time=00:05:00 --output="logs/probe_$n.out" \
        --wrap="hostname; echo CUDA_VISIBLE_DEVICES=\${CUDA_VISIBLE_DEVICES:-unset}; nvidia-smi -L; nvidia-smi --query-gpu=name,compute_mode,memory.used,driver_version --format=csv; $PROD_PYTHON -c 'import torch; torch.cuda.init(); print(\"device_count\", torch.cuda.device_count(), torch.cuda.get_device_name(0), torch.version.cuda)'; rc=\$?; echo RC=\$rc; exit \$rc" > /dev/null
    done
    total=$(echo $nodes | wc -w); echo "probing $total nodes: $(echo $nodes | tr '\n' ' ')"
    for i in $(seq 1 40); do   # up to ~13 minutes; a probe that gets no GPU in that time counts as unknown, not bad
      fin=$(grep -l "^RC=" logs/probe_*.out 2>/dev/null | wc -l); [ "$fin" -ge "$total" ] && break; sleep 20
    done
    for f in logs/probe_*.out; do [ -f "$f" ] || continue; n=${f#logs/probe_}; n=${n%.out}
      if grep -q "^RC=0" "$f"; then echo "  ok      $n: $(grep -m1 device_count "$f")"
      elif grep -q "^RC=" "$f"; then echo "  BAD     $n: $(grep -m1 -i "error\|No devices" "$f" | cut -c1-110)"
      else echo "  unknown $n (probe did not run in time; not excluded)"; fi; done
    for j in $(squeue -u "$USER" -h -o "%i %j" | awk '$2 ~ /^probe_/ {print $1}'); do scancel "$j"; done
    collect_bad_nodes; echo "excluded nodes: $(paste -sd, logs/bad_nodes.txt 2>/dev/null)"
    [ "$MODE" = probe ] && exit 0
    do_retry ;;
  c1)
    for M in $C1_MODELS; do for T in $TASKS; do for K in 1 2 3 4; do submit_c1_pair "$M" "$T" "$K"; done; done; done
    echo "c1 job ids in logs/c1_jobs.txt" ;;
  c2)      submit_c2_list "$HITLIST" ;;
  c2more)  submit_c2_list "$HITLIST_MORE" ;;
  c2all)   submit_c2_list "$HITLIST_ALL" ;;
  retry)   do_retry ;;
  status)
    for stage in c1 c2; do
      all=$(ls logs/${stage}_*.out 2>/dev/null | grep -vc prev); ok=$(grep -l "^RC=0" logs/${stage}_*.out 2>/dev/null | grep -vc prev)
      done_any=$(grep -l "^RC=" logs/${stage}_*.out 2>/dev/null | grep -vc prev)
      echo "$stage: $all started, $done_any finished, $ok ok, $((done_any - ok)) failed, $((all - done_any)) running"
    done
    echo "queued/running: $(squeue -u "$USER" -h | wc -l) (never-startable, dependency on a failed job: $(squeue -u "$USER" -h -o %r | grep -c DependencyNever))"
    for f in logs/c1_*.out logs/c2_*.out; do
      [ -f "$f" ] || continue; case "$f" in *.prev.out) continue ;; esac
      grep -q "^RC=" "$f" && ! grep -q "^RC=0" "$f" && { echo "== FAILED $f ($(grep -m1 '^node=' "$f"))"; tail -30 "$f"; }
    done ;;
  report)
    $PROD_PYTHON - "$PROD_ART" <<'EOF'
import glob, json, os, re, sys
art = sys.argv[1]
OLD, NEW = 4096, 8192
def stops(path, cap):
    """{row_idx: natural_stop} read off the rows at one cap (natural_stop is per problem)."""
    out = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            if r.get("_header") or int(r["B"]) != cap:
                continue
            out[int(r.get("row_idx", r.get("idx")))] = r.get("natural_stop")
    return out
print("%-22s %-11s %2s %6s %8s %8s %8s %8s" % ("model", "task", "k", "cont.", "<8192", "acc4096", "acc8192", "d_pts"))
for mp in sorted(glob.glob(os.path.join(art, "meta_*_natural2h_k*.json"))):
    m = re.match(r"meta_(.+?)_(gsm8k|math500|svamp|aqua|csqa|arc|strategyqa|bbh|mmlu|hellaswag)_natural2h_k(\d+)\.json", os.path.basename(mp))
    if not m:
        continue
    model, task, k = m.group(1), m.group(2), int(m.group(3))
    meta = json.load(open(mp))
    cont = meta.get("continue") or {}
    n_cont = cont.get("n_selected")
    cells = mp.replace("meta_", "cells_").replace(".json", ".jsonl")
    src = cont.get("source_cells") or ""
    share = float("nan")
    if os.path.exists(cells) and os.path.exists(src):
        old = stops(src, OLD)
        new = stops(cells, NEW)
        hit = [i for i, s in old.items() if s is None or int(s) >= OLD]
        if hit:
            share = sum(1 for i in hit if new.get(i) is not None and int(new[i]) < NEW) / len(hit)
            n_cont = n_cont or len(hit)
    bb = meta.get("by_budget") or {}
    a4 = (bb.get(str(OLD)) or {}).get("acc_v2"); a8 = (bb.get(str(NEW)) or {}).get("acc_v2")
    f = lambda v: ("%8.1f" % (100 * v)) if isinstance(v, (int, float)) else "%8s" % "-"
    d = ("%+8.1f" % (100 * (a8 - a4))) if isinstance(a4, (int, float)) and isinstance(a8, (int, float)) else "%8s" % "-"
    print("%-22s %-11s %2d %6s %8s %s %s %s" % (model, task, k, n_cont if n_cont is not None else "-",
          ("%7.1f%%" % (100 * share)) if share == share else "-", f(a4), f(a8), d))
EOF
    ;;
  *)
    echo "usage: bash slurm/continue_chains.sh run|probe|c1|c2|retry|c2more|c2all|status|report"; exit 1 ;;
esac
