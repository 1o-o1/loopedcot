"""Build token IDs, supervision masks, and independent padded blocks from task prompts and candidate answer chains."""
import hashlib, json, os, re, subprocess, sys, time
from collections import Counter, defaultdict
from contextlib import contextmanager

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG = os.path.join(HERE, "config.yaml")
# The weight tables stage 0 (theory_weights.py) reads off the base model's production grid. They
# ship with the package and are pinned by content in config.yaml, exactly like the pool.
THEORY_WEIGHTS = os.path.join(HERE, "data", "theory_weights.json")

# The shared evaluation harness ships with the package (s32_common, s28_common, s13_shots,
# s3_patch), so exemplar bytes and task protocols are identical and every stage imports it by bare
# name from this directory.
RUN_ROOT_ENV = "S36_RUN_ROOT"
if HERE not in sys.path:
    sys.path.insert(0, HERE)
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")
os.environ.setdefault("HF_HUB_OFFLINE", "1")

DEV = "cuda"
TARGET_KINDS = ("DIRECT", "CHAIN", "CHAIN_PLUS", "FALLBACK")
KIND_OF_FORMAT = {"numeric_hash": "numeric", "math_boxed": "math", "letter_paren": "letter"}


# ================================================================= config
class Config(dict):
    """Map configuration fields to task formats, token block lengths, budget variants, and loop-depth distributions."""

    def horizon(self, src):
        """Return the natural-stop horizon in tokens for one chains source, or the shared default."""
        h = self["chains"].get(src)
        if h and "horizon" in h:
            return int(h["horizon"])
        return int(self["chains_horizon"])

    def block_len_for(self, n_tokens):
        """Return the smallest block-length bucket that holds a visit of n_tokens, or None when none does."""
        for L in self.block_lens:
            if int(n_tokens) <= L:
                return L
        return None

    def micro(self, L):
        """Return the blocks per micro-batch of one block-length bucket."""
        return int(self["micro_by_block_len"][int(L)])

    def accum(self, L):
        """Return the micro-batches per optimiser step of one bucket, so every window is the same number of blocks."""
        return int(self["effective_batch_blocks"]) // self.micro(L)

    def budget_grid_for(self, src):
        """Return the token budgets one source draws T from, with None for the no-limit draw."""
        by_src = self.get("budget_grid_by_source") or {}
        return list(by_src.get(src, self["budget_grid"]))

    def eval_task(self, src):
        """Return the evaluation task whose prompt and parser a chains source borrows."""
        return self["chains"][src]["eval_task"]

    def fmt(self, src):
        """Return the answer format name of a chains source."""
        return self["chains"][src]["format"]

    def kind(self, src):
        """Return the answer kind (numeric, math or letter) of a chains source."""
        return KIND_OF_FORMAT[self.fmt(src)]

    def variant(self, name):
        """Return one variant's target rule, budget-line flag and fallback flag."""
        if name not in self["variants"]:
            raise KeyError("unknown variant %r; config has %s" % (name, sorted(self["variants"])))
        return self["variants"][name]

    @property
    def sources(self):
        """Return the chains source names, in config order."""
        return list(self["chains"])

    @property
    def budget_grid(self):
        """Return the default training budgets in tokens, with None for the no-limit draw."""
        return list(self["budget_grid"])

    @property
    def block_lens(self):
        """Return the block-length buckets in tokens, ascending."""
        return sorted(int(L) for L in self["block_lens"])

    @property
    def depths(self):
        """Return the loop depths that can be sampled, ascending."""
        return sorted(int(d) for d in self["depth_probabilities"])


SUPPORTED = {"budget_line_position": "after_question_before_answer_prefix",
             "schedule": "cosine", "loss": "ce_sum_over_window_supervised", "protocol": "v2"}

# `draw` says where a visit's T comes from, `depth` where its block depth comes from. A variant with
# no `depth` field keeps the pairing the two original draws had: theory -> the theory depth table,
# anything else -> the flat `depth_probabilities` mix.
DRAW_VALUES = ("theory", "uniform", "none_only")
DEPTH_VALUES = ("theory", "config")          # plus "fixed:<d>", a depth held at one value
RULE_VALUES = ("longest_fitting", "shortest_fitting")
EVAL_ROWS_VALUES = ("production", "s32")     # which question rows a grid evaluates


def check_variants(c):
    """Refuse a variant field no stage implements, naming the variant, the field and the values."""
    depths = sorted(int(k) for k in c["depth_probabilities"])
    for name, v in (c.get("variants") or {}).items():
        rule = str(v.get("rule"))
        if rule not in RULE_VALUES:
            raise ValueError("variant %r has rule=%r; implemented rules are %s"
                             % (name, rule, list(RULE_VALUES)))
        draw = str(v.get("draw", "theory"))
        if draw not in DRAW_VALUES:
            raise ValueError("variant %r has draw=%r; implemented draws are %s"
                             % (name, draw, list(DRAW_VALUES)))
        if v.get("depth") is None:
            continue
        d = str(v["depth"])
        if d.startswith("fixed:"):
            tail = d.split(":", 1)[1]
            if not tail.isdigit() or int(tail) not in depths:
                raise ValueError("variant %r has depth=%r; a fixed depth must be one of %s"
                                 % (name, d, depths))
        elif d not in DEPTH_VALUES:
            raise ValueError("variant %r has depth=%r; implemented depths are %s plus fixed:<d>"
                             % (name, d, list(DEPTH_VALUES)))


def load_config(path=None, sources=None):
    """Return parsed YAML configuration, optionally restricted to a comma-separated list of source tasks; lengths and budgets are tokens."""
    import yaml
    with open(path or DEFAULT_CONFIG, encoding="utf-8") as f:
        c = Config(yaml.safe_load(f))
    c["depth_probabilities"] = {int(k): float(v) for k, v in c["depth_probabilities"].items()}
    c["micro_by_block_len"] = {int(k): int(v) for k, v in c["micro_by_block_len"].items()}
    # every switch the stages can honour has exactly one implemented value; refuse the others
    # rather than silently running a recipe the config does not describe
    for key, only in SUPPORTED.items():
        assert str(c[key]) == only, "config %s=%r; only %r is implemented" % (key, c[key], only)
    assert bool(c["eos_strip"]), "the parsers always strip the end-of-text string; eos_strip=false is not implemented"
    er = str(c.get("eval_rows", "production"))
    if er not in EVAL_ROWS_VALUES:
        raise ValueError("config eval_rows=%r; implemented values are %s"
                         % (er, list(EVAL_ROWS_VALUES)))
    c["eval_rows"] = er
    check_variants(c)
    # one micro width per bucket, and one window size for every bucket: an accumulation window that
    # was 32 blocks in one bucket and 24 in another would weight the buckets differently
    nb = int(c["effective_batch_blocks"])
    for L in c.block_lens:
        m = c["micro_by_block_len"].get(L)
        assert m, "block length %d has no micro_by_block_len entry" % L
        assert nb % m == 0, ("effective_batch_blocks %d is not a whole number of micro-batches of "
                             "%d blocks (block length %d)" % (nb, m, L))
    for src, h in c["chains"].items():
        top = max(t for t in c.budget_grid_for(src) if t is not None)
        assert top <= c.horizon(src), ("source %s draws budgets up to %d but its chains only run to %d; "
                                       "the top budget would never bind" % (src, top, c.horizon(src)))
    if sources:
        keep = [s.strip() for s in sources.split(",") if s.strip()]
        missing = [s for s in keep if s not in c["chains"]]
        assert not missing, "unknown source(s) %s" % missing
        c["chains"] = {k: v for k, v in c["chains"].items() if k in keep}
    return c


def paths(root):
    """Return named output-directory paths under the supplied run root, expanding the user home directory."""
    root = os.path.expanduser(root)
    # the harness modules keep their own ART/ADAPTERS/LOGS/... constants; publish the run root so
    # they resolve under it, whether they are imported before this call or after it
    os.environ[RUN_ROOT_ENV] = root
    _h = sys.modules.get("s32_common")
    if _h is not None and hasattr(_h, "set_run_root"):
        _h.set_run_root(root)
    d = {k: os.path.join(root, k) for k in ("artifacts", "data", "gates", "logs", "adapters",
                                            "train_logs", "prompts")}
    d["root"] = root
    return d


def ensure_dirs(P):
    """Create every output directory of a run root except the root entry itself."""
    for k, v in P.items():
        if k != "root":
            os.makedirs(v, exist_ok=True)


def data_dir(P, variant):
    """Return (and create) the block/schedule directory of one variant; variants never share stage-2 files."""
    d = os.path.join(P["data"], str(variant))
    os.makedirs(d, exist_ok=True)
    return d


def variant_key(cfg, variant, seed=None):
    """Return the name stage 2's files are keyed by: the variant, plus the seed when it is not the
    config's own. Two seeds of one variant are two different draws, so they must not share one
    data directory or one manifest; the config's seed keeps today's paths exactly."""
    if seed is None or int(seed) == int(cfg["seed"]):
        return str(variant)
    return "%s_seed%d" % (variant, int(seed))


def manifest_path(P, key):
    """Return the target manifest of one variant key (variant, or variant_seed<n>)."""
    return os.path.join(P["artifacts"], "target_manifest_%s.json" % key)


def blocks_fingerprint(arrays):
    """Return a hex digest over every block length, id array and mask, so a trainer can tell one variant's data from another's."""
    h = hashlib.sha256()
    for L, a in sorted(arrays.items()):
        h.update(b"L%d:" % int(L))
        h.update(np.ascontiguousarray(a["blocks"], dtype=np.int32).tobytes())
        h.update(np.ascontiguousarray(a["mask"], dtype=np.int8).tobytes())
    return h.hexdigest()


def lora_settings(cfg):
    """Return the adapter shape as plain numbers: rank, alpha, dropout and the projection names."""
    lo = cfg["lora"]
    return {"r": int(lo["r"]), "alpha": int(lo["alpha"]), "dropout": float(lo["dropout"]),
            "targets": list(lo["targets"])}


def short_prompt_path(P, cfg, src):
    """Return the short-exemplar prompt file for one source: the run root's copy if present, else the packaged one."""
    name = str(cfg["prompt_file_pattern"]) % src
    at_root = os.path.join(P["prompts"], name)
    if os.path.exists(at_root):
        return at_root
    return os.path.join(HERE, "prompts", name)


@contextmanager
def execution_depth(base, depth):
    """Temporarily set model/config loop counts to depth (loops), restoring them on every exit."""
    objects = (base.model, base.config)
    old = [obj.total_ut_steps for obj in objects]
    try:
        for obj in objects:
            obj.total_ut_steps = int(depth)
        yield
    finally:
        for obj, value in zip(objects, old):
            obj.total_ut_steps = value


def generation_waves(limit, first=128):
    """Return the ascending decode checkpoints up to a token limit: doubling widths, then the limit itself, so a long horizon is not one blind pass."""
    limit = int(limit)
    if limit <= 0:
        return []
    out, w = [], int(first)
    while w < limit:
        out.append(w)
        w *= 2
    out.append(limit)
    return out


def budget_key(T):
    """Return a canonical JSON/resume key for a token cap or no-limit sentinel."""
    return "none" if T is None or str(T).lower() in ("none", "null") else str(int(T))


def count_by_budget(values):
    """Return a plain dict counting token caps under their canonical keys, so every artifact spells no-limit the same way."""
    out = Counter(budget_key(v) for v in values)
    return dict(out)


# ================================================================= misc helpers
def jdump(obj, path):
    """Write obj as indented JSON to path through a temporary file, so a reader never sees half a file."""
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)
    os.replace(tmp, path)


def jload(path, default=None):
    """Return the JSON at path, or default when the file does not exist."""
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def norm_q(s):
    """Return a question reduced to lowercase alphanumerics and single spaces, for pool membership tests."""
    return re.sub(r"[^a-z0-9]+", " ", str(s).lower()).strip()


def require_root(root, stage):
    """Return the run root or refuse to start; --root has no default, so two runs can never land in one directory because nobody typed it."""
    if not root:
        raise SystemExit("%s: --root=<run root> is required and has no default, for example "
                         "--root=$PROD_ART/s36" % stage)
    return root


def file_sha256(path):
    """Return the hex sha256 of a file, read in one-megabyte chunks."""
    h = hashlib.sha256()
    with open(os.path.expanduser(path), "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def check_pool(cfg):
    """Return the pool file's sha256 after checking it against the config pin; a pool whose bytes
    changed invalidates the V9 screening argument, so the stage stops instead of running on it."""
    path = os.path.expanduser(cfg["pool_jsonl"])
    pinned = str(cfg["pool_sha256"]).strip().lower()
    got = file_sha256(path)
    if got != pinned:
        raise SystemExit(
            "pool_sha256 mismatch for %s\n  config pins %s\n  file is     %s\n"
            "The screened pool is read-only. Re-pin only after a deliberate re-screen: run\n"
            "  sha256sum %s\n"
            "and paste the digest into config.yaml as pool_sha256." % (path, pinned, got, path))
    return got


def check_theory_weights(cfg, path=None):
    """Return the theory-weights file's sha256 after checking it against the config pin.

    The budget and depth tables ARE the objective: a file whose bytes changed is a different
    training distribution, and a run that quietly picked it up could not be compared with the one
    the paper describes. So the stage stops, the same way `check_pool` stops on an edited pool.
    """
    p = os.path.expanduser(path or THEORY_WEIGHTS)
    pinned = str(cfg["theory_weights_sha256"]).strip().lower()
    if not os.path.exists(p):
        raise SystemExit(
            "MISSING %s\nThe budget and depth weights are stage 0 of the recipe. Run\n"
            "  python train/theory_weights.py --cells-dir=<dir of the base grids>\n"
            "and pin the digest it prints in config.yaml as theory_weights_sha256." % p)
    got = file_sha256(p)
    if got != pinned:
        raise SystemExit(
            "theory_weights_sha256 mismatch for %s\n  config pins %s\n  file is     %s\n"
            "The weight tables are the training objective. Re-pin only after deliberately "
            "recomputing them: run\n  python train/theory_weights.py --cells-dir=<dir>\n"
            "and paste the digest into config.yaml as theory_weights_sha256." % (p, pinned, got))
    return got


def load_theory_weights(cfg, path=None):
    """Return (the pinned weight tables, their sha256), checked against the config and the sources.

    Every source of the mixture must have a table, and its budget table must name exactly the caps
    that source's grid draws: a weight read at a cap the grid never measured, or a cap with no
    weight, would be a silently different draw.
    """
    sha = check_theory_weights(cfg, path)
    tw = jload(os.path.expanduser(path or THEORY_WEIGHTS))
    for src in cfg.sources:
        s = (tw.get("sources") or {}).get(src)
        if not s:
            raise SystemExit("%s has no weight table in %s" % (src, path or THEORY_WEIGHTS))
        want = [budget_key(t) for t in cfg.budget_grid_for(src)]
        if sorted(s["budget_weights"]) != sorted(want):
            raise SystemExit("%s budget weights cover %s; the source's grid is %s"
                             % (src, sorted(s["budget_weights"]), sorted(want)))
        missing = [d for d in cfg.depths if str(d) not in s["depth_weights"]]
        if missing:
            raise SystemExit("%s has no depth weight for depth(s) %s" % (src, missing))
    return tw, sha


def draw_rule(cfg, variant):
    """Return where one variant draws T from: theory, uniform, or none_only (T is always no-limit)."""
    return str(cfg.variant(variant).get("draw", "theory"))


def depth_source(cfg, variant):
    """Return where one variant draws the block depth from: theory, config, or fixed:<d>.

    A variant that does not say keeps the pairing the two original draws had, so the theory
    variants read the depth table and the others take the flat `depth_probabilities` mix.
    """
    d = cfg.variant(variant).get("depth")
    if d:
        return str(d)
    return "theory" if draw_rule(cfg, variant) == "theory" else "config"


def uses_theory(cfg, variant):
    """Return whether one variant draws T and the block depth from the theory tables or from the flat mix."""
    return draw_rule(cfg, variant) == "theory"


def budget_draw(cfg, tw, variant, src):
    """Return one source's budget grid and the probability of each entry, in grid order.

    A theory variant reads the table; `uniform_longest` draws every entry of the grid with equal
    probability, which is what every variant did before the weights existed; a `none_only` baseline
    draws the no-limit entry every time, so its grid is that one entry.
    """
    draw = draw_rule(cfg, variant)
    grid = cfg.budget_grid_for(src)
    if draw == "none_only":
        return [None], np.array([1.0])
    if draw != "theory":
        return grid, np.full(len(grid), 1.0 / len(grid))
    w = tw["sources"][src]["budget_weights"]
    p = np.array([float(w[budget_key(t)]) for t in grid], float)
    assert p.min() > 0 and abs(p.sum() - 1.0) < 1e-6, (src, p.sum())
    return grid, p / p.sum()


def depth_draw(cfg, tw, variant, src):
    """Return the block depths and the probability of each, for one source and variant.

    A theory depth reads that source's depth table; `config` takes the fixed `depth_probabilities`
    mix, the same for every source; `fixed:<d>` holds every block at one depth, so its list is that
    one depth.
    """
    which = depth_source(cfg, variant)
    if which.startswith("fixed:"):
        return [int(which.split(":", 1)[1])], np.array([1.0])
    depths = cfg.depths
    if which == "config":
        p = np.array([float(cfg["depth_probabilities"][d]) for d in depths], float)
    else:
        w = tw["sources"][src]["depth_weights"]
        p = np.array([float(w[str(d)]) for d in depths], float)
    assert p.min() > 0, (src, p)
    return depths, p / p.sum()


def intended_weights(cfg, tw, variant, srcs):
    """Return the budget and depth weight tables one variant intends to draw with, per source."""
    T, D = {}, {}
    for src in srcs:
        grid, p = budget_draw(cfg, tw, variant, src)
        T[src] = {budget_key(t): float(pi) for t, pi in zip(grid, p)}
        depths, q = depth_draw(cfg, tw, variant, src)
        D[src] = {str(int(d)): float(qi) for d, qi in zip(depths, q)}
    return {"budget": T, "depth": D}


def histogram(counts):
    """Return a count table as shares of its own total; an empty table is an empty histogram."""
    total = sum(int(v) for v in counts.values())
    if total <= 0:
        return {}
    return {str(k): int(v) / total for k, v in counts.items()}


def weight_deviation(intended, realised):
    """Return the largest absolute gap between an intended weight table and a realised histogram.

    Keys the histogram never saw count as zero, so a weight the draw missed entirely is a gap of
    its whole weight rather than an absent comparison.
    """
    keys = set(intended) | set(realised)
    return max([abs(float(intended.get(k, 0.0)) - float(realised.get(k, 0.0))) for k in keys]
               or [0.0])


def draw_allowance(p, n, tol=0.05, sd_mult=3.0):
    """Return how far one weight's realised share may sit from `p` on a manifest of n visits.

    The realised share is a multinomial draw of n visits from the intended weights, so a correct
    draw still misses each weight by about sqrt(p(1-p)/n). The bound is the stated `tol` or
    `sd_mult` of that sampling error, whichever is larger: on the full manifest (tens of thousands
    of visits) the sampling term is well under 0.05, so the 0.05 is what binds and is what is
    checked; on a smoke of a few hundred visits the sampling term binds instead, which is the only
    honest bound there.
    """
    p = float(p)
    se = float(np.sqrt(max(p * (1.0 - p), 0.0) / max(1, int(n))))
    return max(float(tol), float(sd_mult) * se)


def v10_draw_weights(man, tol=0.05, sd_mult=3.0):
    """Return the V10 record: every source's realised T and depth histogram against its intended weights.

    The manifest carries both sides -- the table stage 0 wrote and the histogram the draw realised
    -- so the gate compares the objective on disk with the objective on paper, per source and per
    weight. Dropped draws are the only mechanism that can move the two apart at large n, and they
    are counted per T in the same manifest.
    """
    rec = {"tol": float(tol), "sd_mult": float(sd_mult), "variant": man.get("variant"),
           "draw": man.get("draw_rule"),
           "theory_weights_sha256": man.get("theory_weights_sha256"), "by_source": {},
           "worst": 0.0, "ok": True}
    want = man.get("draw_weights_intended") or {}
    counts = {"budget": man.get("visits_by_src_T") or {},
              "depth": man.get("visits_by_src_depth") or {}}
    for what in ("budget", "depth"):
        for src, intended in sorted((want.get(what) or {}).items()):
            ct = {str(k): int(v) for k, v in (counts[what].get(src) or {}).items()}
            n = sum(ct.values())
            realised = histogram(ct)
            worst_key, worst_dev, worst_allow, ok = None, 0.0, float(tol), True
            for k in sorted(set(intended) | set(realised)):
                dev = abs(float(intended.get(k, 0.0)) - float(realised.get(k, 0.0)))
                allow = draw_allowance(intended.get(k, 0.0), n, tol, sd_mult)
                if dev > allow:
                    ok = False
                if dev > worst_dev:
                    worst_key, worst_dev, worst_allow = k, dev, allow
            rec["by_source"]["%s_%s" % (what, src)] = {
                "n_visits": int(n), "max_abs_dev": worst_dev, "worst_key": worst_key,
                "allowance_at_worst_key": worst_allow, "sampling_bound_binds": worst_allow > tol,
                "within_tol": bool(ok), "intended": intended, "realised": realised}
            rec["worst"] = max(rec["worst"], worst_dev)
            rec["ok"] = rec["ok"] and ok
    rec["ok"] = bool(rec["ok"] and rec["by_source"])
    return rec


def share_caps(cfg, srcs):
    """Return the source and format share caps for one mixture. A cap below one over its bucket
    count can never be met, because some bucket must always hold at least that share; such a cap
    is reported inactive and not enforced. Every active cap leaves at least one bucket under it,
    so enforcing it from the first token cannot starve the draw loop."""
    fmts = sorted({cfg.fmt(s) for s in srcs})

    def one(cap, n):
        return {"cap": float(cap), "active": bool(n > 0 and float(cap) * n >= 1.0 - 1e-9),
                "draws_refused": 0, "realised": {}}

    src = one(cfg["source_max_share"], len(srcs))
    src["n_sources"] = len(srcs)
    fmt = one(cfg["format_max_share"], len(fmts))
    fmt["n_formats"] = len(fmts)
    return {"source": src, "format": fmt, "applied_from_supervised_token": 0}


# Wait for other GPU jobs before loading work to avoid overlapping allocations.
SLURM_JOB_VARS = ("SLURM_JOB_ID", "SLURM_JOBID")


def should_wait_for_gpu(argv, env=None):
    """Return whether a GPU stage should wait for an idle GPU. A Slurm job already owns its GPU
    and must never wait; --no-wait never waits; otherwise wait only when --wait asks for it or
    CLUSTER=0 marks the shared unmanaged box."""
    env = os.environ if env is None else env
    flags = {a.lstrip("-").partition("=")[0] for a in argv}
    if "no-wait" in flags:
        return False
    if any(env.get(v) for v in SLURM_JOB_VARS):
        return False
    if "wait" in flags:
        return True
    return str(env.get("CLUSTER", "")) == "0"
def gpu_apps():
    """Return one line per process holding GPU memory (pid, name, MiB), or the error text."""
    try:
        return subprocess.run(
            ["nvidia-smi", "--query-compute-apps=pid,process_name,used_memory",
             "--format=csv,noheader"], capture_output=True, text=True, timeout=60).stdout.strip()
    except Exception as e:
        return "nvidia-smi failed: %r" % (e,)


def wait_for_gpu(log_path, poll_s=600, max_wait_h=48.0):
    """Wait until no other process holds GPU memory; return elapsed seconds and poll count, with timeout specified in hours."""
    me = os.getpid()
    t0 = time.time()
    logf = open(log_path, "a", encoding="utf-8")
    n = 0
    while True:
        apps = gpu_apps()
        pids = []
        for line in apps.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                pid = int(line.split(",")[0].strip())
            except Exception:
                continue
            if pid != me:
                pids.append(pid)
        logf.write(json.dumps({"poll": n, "waited_s": round(time.time() - t0, 1),
                               "other_gpu_pids": pids, "nvidia_smi_apps": apps,
                               "ts": time.strftime("%Y-%m-%dT%H:%M:%S")}) + "\n")
        logf.flush()
        os.fsync(logf.fileno())
        if not pids:
            print("[gpu] free after %.0fs (%d polls)" % (time.time() - t0, n), flush=True)
            logf.close()
            return {"waited_s": round(time.time() - t0, 1), "polls": n}
        print("[gpu] busy: %s -- waiting %ds" % (pids, poll_s), flush=True)
        if time.time() - t0 > max_wait_h * 3600:
            logf.close()
            raise RuntimeError("waited %.1f h for the GPU" % max_wait_h)
        time.sleep(poll_s)
        n += 1


# ================================================================= the prompt backend
# Cache harness exemplar text; tests can inject a lightweight prompt backend.
_BACKEND = None
_PREFIX_CACHE = {}


def set_prompt_backend(few_shot_prefix_fn, task_bits_fn):
    """Install exemplar-prefix and task-metadata callables for prompt building, clearing cached prefixes."""
    global _BACKEND
    _PREFIX_CACHE.clear()
    _BACKEND = (few_shot_prefix_fn, task_bits_fn)


def reset_prompt_backend():
    """Drop the injected prompt backend and the cached exemplar prefixes."""
    global _BACKEND
    _PREFIX_CACHE.clear()
    _BACKEND = None


def _backend():
    global _BACKEND
    if _BACKEND is None:
        import s32_common
        _BACKEND = (s32_common.few_shot_prefix, s32_common.task_bits)
    return _BACKEND


def few_shot_prefix(tok, eval_task):
    """Return the task's exemplar block as text, cached per task; it carries no budget line."""
    if eval_task not in _PREFIX_CACHE:
        _PREFIX_CACHE[eval_task] = _backend()[0](tok, eval_task)
    return _PREFIX_CACHE[eval_task]


def task_bits(eval_task):
    """Return question/answer prefixes, read-out suffix, stop strings, answer marker, and answer kind for an evaluation task."""
    return _backend()[1](eval_task)


def exemplar_fingerprints(tok, cfg, tasks=None):
    """Return {evaluation task: sha256 of its exemplar block}, for the given tasks or every configured source, so a later stage can prove it used the same exemplars."""
    want = list(tasks) if tasks else [cfg.eval_task(src) for src in cfg.sources]
    return {t: hashlib.sha256(few_shot_prefix(tok, t).encode("utf-8")).hexdigest()
            for t in dict.fromkeys(want)}


def check_exemplars(tok, cfg, recorded, tasks=None):
    """Refuse an exemplar block whose bytes no longer match the digest recorded when the targets were built; only the given tasks are checked."""
    now = exemplar_fingerprints(tok, cfg, tasks)
    for task, want in (recorded or {}).items():
        if task in now:
            assert now[task] == want, ("exemplar block for %s changed since the targets were "
                                       "built (%s != %s)" % (task, now[task], want))


def math_shot_source():
    """Return the metadata of the MATH exemplar shots (dataset name, config, excluded indices), or None when the helper is unavailable."""
    try:
        from s13_shots import math_shots
        return math_shots(4)[1]
    except Exception:
        return None


def check_exemplar_source(meta):
    """Refuse MATH exemplars drawn from the evaluation split; meta is the dict math_shots returns."""
    if not meta:
        return
    assert not meta.get("excluded_test_idx"), (
        "MATH exemplars were taken from evaluation rows %s" % meta["excluded_test_idx"])
    assert "test" not in str(meta.get("source", "")).lower(), (
        "MATH exemplars came from %r, an evaluation split" % meta.get("source"))


# ================================================================= the budget line and the prompt
def budget_line(cfg, T, with_line=True):
    """Return the control line for token cap T or None (no limit); with_line=False returns an empty string."""
    if not with_line:
        return ""
    if T is None:
        return str(cfg["budget_line_no_limit"])
    return str(cfg["budget_line_with_limit"]) % int(T)


def eval_prompt(cfg, tok, eval_task, question, T, with_line=True):
    """Return exemplar block + question + optional token-budget line + answer prefix, using the same bytes in training and evaluation."""
    qp, ap = task_bits(eval_task)[0], task_bits(eval_task)[1]
    return (few_shot_prefix(tok, eval_task) + qp + question
            + budget_line(cfg, T, with_line) + ap)


def answer_text(cfg, src, gold):
    """Return the task-formatted gold answer text to append after the read-out suffix; the output is text, not token IDs."""
    if cfg.kind(src) == "letter":
        return " (%s)." % str(gold).strip().strip("()").lower()
    return " %s" % str(gold).strip()


# ================================================================= the fixed parser
# Strip EOS before parsing and treat empty read-outs as missing answers.
EOS_STR = "<|endoftext|>"


def strip_eos_text(t):
    """Return the text before the first end-of-text string, or None when the input is None."""
    if t is None:
        return None
    i = t.find(EOS_STR)
    return t if i < 0 else t[:i]


def parse_forced_fixed(text, eval_task, options=None):
    """Return the answer read out of a forced read-out, or None; the input is decoded text with EOS stripped first."""
    import s28_common as S28
    import s32_common as S32
    t = strip_eos_text(text)
    if t is None:
        return None
    if eval_task in ("math500", "math"):
        b = S32.last_boxed(t)
        if b is not None:
            return b
        if "Final Answer:" in t:
            t = t.rsplit("Final Answer:", 1)[1]
        for line in t.split("\n"):
            line = line.strip().strip("$").strip()
            if line:
                return line
        return None
    if eval_task in ("gsm8k", "svamp"):
        return S28.parse_final_answer(t)
    return S28.parse_letter(t, options)


def parse_own_fixed(cut_text, eval_task, options=None):
    """Return the answer the model wrote inside its own cut chain, or None when it never finished one."""
    import s28_common as S28
    import s32_common as S32
    t = strip_eos_text(cut_text)
    if not t:
        return None
    if eval_task in ("math500", "math"):
        return S32.last_boxed(t)
    if eval_task in ("gsm8k", "svamp"):
        return S28.trace_own_number(t)
    return S28.parse_own(t, eval_task, options)


def ans_eq_fixed(pred, gold, eval_task):
    """Return whether a parsed answer equals gold under the task's own comparison."""
    import s28_common as S28
    import s32_common as S32
    if pred is None:
        return False
    if eval_task in ("math500", "math"):
        return bool(S32.math_eq(pred, gold))
    if eval_task in ("gsm8k", "svamp"):
        return bool(S28.num_eq(pred, gold))
    return bool(S28.ans_eq(pred, gold, eval_task))


# ================================================================= target construction
def chain_ids(tok, prompt, chain):
    """Return prompt IDs and continuation IDs by tokenizing prompt+chain in context; reject a changed prompt token boundary."""
    p_ids = tok(prompt, add_special_tokens=False)["input_ids"]
    f_ids = tok(prompt + chain, add_special_tokens=False)["input_ids"]
    assert f_ids[:len(p_ids)] == p_ids, "prompt tokenisation not stable under concatenation"
    return p_ids, f_ids[len(p_ids):]


def answer_sentence_end(text, eval_task):
    """Return the exclusive character offset of a complete task answer, or None if absent."""
    text = strip_eos_text(text)
    if not text:
        return None
    if eval_task in ("math", "math500"):
        matches = list(re.finditer(r"\\boxed\s*\{", text))
        if not matches:
            return None
        start = matches[-1].end()
        depth = 1
        for j in range(start, len(text)):
            if text[j] == "{" and (j == 0 or text[j - 1] != "\\"):
                depth += 1
            elif text[j] == "}" and (j == 0 or text[j - 1] != "\\"):
                depth -= 1
                if depth == 0:
                    return j + 1 if text[start:j].strip() else None
        return None
    marker = "####" if eval_task in ("gsm8k", "svamp") else task_bits(eval_task)[4]
    if marker not in text:
        return None
    start = text.rfind(marker) + len(marker)
    pattern = (r"\s*\$?\s*[+-]?(?:\d[\d,]*(?:\.\d+)?|\.\d+)"
               if eval_task in ("gsm8k", "svamp") else r"\s*(?:\([A-Za-z]\)|[A-Za-z]\b)\.?")
    match = re.match(pattern, text[start:])
    return start + match.end() if match else None


def trim_answer_sentence(text, eval_task):
    """Return candidate text through its complete answer, excluding EOS and trailing continuations."""
    if text is None:
        return None
    text = strip_eos_text(text)
    end = answer_sentence_end(text, eval_task)
    return text[:end] if end is not None else text


def select_chain(cands, rule):
    """Return the longest/shortest fitting (token count,name,chain) candidate, preferring A on ties, or None for no candidates."""
    if not cands:
        return None
    if rule == "longest_fitting":
        return max(cands, key=lambda c: (c[0], c[1] == "A"))
    if rule == "shortest_fitting":
        return min(cands, key=lambda c: (c[0], c[1] != "A"))
    raise ValueError("unknown target rule %r" % (rule,))


def build_target(cfg, tok, variant, src, question, gold, T, chain_A, chain_B, fullplus=False,
                 fallback_chain_A=None):
    """Return token IDs, binary loss mask, and token-count metadata for a budget/variant; supervise chain, answer, EOS, or answer/EOS only for fallback. None IDs indicate a dropped visit."""
    A = cfg.variant(variant)
    et = cfg.eval_task(src)
    chain_A = trim_answer_sentence(chain_A, et)
    chain_B = trim_answer_sentence(chain_B, et)
    with_line = bool(A["budget_line"])
    sfx = task_bits(et)[2]
    prompt = eval_prompt(cfg, tok, et, question, T, with_line)
    p_ids = tok(prompt, add_special_tokens=False)["input_ids"]
    _, s_ids = chain_ids(tok, prompt, sfx)
    _, a_ids = chain_ids(tok, prompt + sfx, answer_text(cfg, src, gold))
    EOS = tok.eos_token_id
    bl = budget_line(cfg, T, with_line)
    info = {"T": T, "variant": variant, "n_prompt": len(p_ids), "n_suffix": len(s_ids),
            "n_answer": len(a_ids), "fullplus": bool(fullplus), "kind": None, "chain_used": None,
            "n_chain": 0, "budget_line": bl,
            "budget_line_tokens": (len(tok(bl, add_special_tokens=False)["input_ids"]) if bl
                                   else 0),
            "dropped": None}
    ids, msk = list(p_ids), [0] * len(p_ids)

    def append_readout():
        context = tok.decode(ids, clean_up_tokenization_spaces=False)
        assert tok(context, add_special_tokens=False)["input_ids"] == ids, "cut does not round-trip"
        # evaluation appends the suffix as its own standalone tokens, so training must too, or
        # the model meets a different token sequence at the read-out than the one it was taught
        suffix_ids = tok(sfx, add_special_tokens=False)["input_ids"]
        _, answer_ids = chain_ids(tok, context + sfx, answer_text(cfg, src, gold))
        ids.extend(suffix_ids + answer_ids + [EOS])
        msk.extend([0] * len(suffix_ids) + [1] * (len(answer_ids) + 1))
        info.update(n_suffix=len(suffix_ids), n_answer=len(answer_ids))

    if T is not None and int(T) < 0:
        raise ValueError("T must be a nonnegative token cap or None")
    if T == 0:
        append_readout()
        info["kind"] = "DIRECT"
    elif T is None:
        candidates = [(len(chain_ids(tok, prompt, ch)[1]), name, ch)
                      for name, ch in (("A", chain_A), ("B", chain_B)) if ch is not None]
        pick = select_chain(candidates, A["rule"])
        if pick is None:
            info["dropped"] = "no_correct_chain"
            return None, None, info
        _, name, ch = pick
        _p, c_ids = chain_ids(tok, prompt, ch)
        ids += c_ids
        msk += [1] * len(c_ids)
        if fullplus:
            append_readout()
        else:
            ids += [EOS]
            msk += [1]
        info.update({"kind": "CHAIN_PLUS" if fullplus else "CHAIN", "chain_used": name,
                     "n_chain": len(c_ids)})
    else:
        cands = []
        for name, ch in (("A", chain_A), ("B", chain_B)):
            if ch is None:
                continue
            _p, c = chain_ids(tok, prompt, ch)
            if len(c) <= T:
                cands.append((len(c), name, c))
        pick = select_chain(cands, A["rule"])
        if pick is not None:
            n, name, c = pick
            ids += c + [EOS]
            msk += [1] * (len(c) + 1)
            info.update({"kind": "CHAIN", "chain_used": name, "n_chain": n})
        elif not A["fallback"]:
            info["dropped"] = "no_fitting_chain_and_no_fallback"
            return None, None, info
        else:
            # the kept (correct, trimmed) standard chain if there is one, else the raw standard
            # chain, which may be wrong
            ch = chain_A if chain_A is not None else fallback_chain_A
            if ch is None:
                info["dropped"] = "no_correct_chain"
                return None, None, info
            _p, c = chain_ids(tok, prompt, ch)
            if len(c) <= int(T):
                # the only chain available already finishes inside the budget and was rejected;
                # supervising gold after a complete wrong chain would teach the wrong lesson, so
                # read the answer out straight away instead
                append_readout()
                info.update({"kind": "FALLBACK", "chain_used": "readout_only", "n_chain": 0})
            else:
                cut = c[:int(T)]
                ids += cut
                msk += [0] * len(cut)
                append_readout()
                info.update({"kind": "FALLBACK", "chain_used": "A_cut", "n_chain": len(cut),
                             "cut_chain": "kept" if chain_A is not None else "raw"})
    assert len(ids) == len(msk)
    info["n_supervised"] = int(sum(msk))
    info["n_tokens"] = len(ids)
    return ids, msk, info


# ================================================================= packing
def pack_one_visit_per_block(visits, pad_id):
    """Return arrays and spans from visits, one visit per right-padded block; masks exclude padding and lengths count content tokens."""
    by_L = defaultdict(list)
    for vi, v in enumerate(visits):
        by_L[int(v["block_len"])].append(vi)
    arrays, spans = {}, []
    for L, idxs in sorted(by_L.items()):
        n = len(idxs)
        blk = np.full((n, L), pad_id, dtype=np.int32)
        msk = np.zeros((n, L), dtype=np.int8)
        lengths = np.zeros(n, dtype=np.int32)
        dep = np.zeros(n, dtype=np.int8)
        vid = np.zeros(n, dtype=np.int32)
        for b, vi in enumerate(idxs):
            v = visits[vi]
            m = len(v["ids"])
            assert m <= L, "visit %d is %d tokens, block length %d" % (vi, m, L)
            blk[b, :m] = np.asarray(v["ids"], dtype=np.int32)
            msk[b, :m] = np.asarray(v["mask"], dtype=np.int8)
            lengths[b] = m
            dep[b] = int(v["depth"])
            vid[b] = vi
            spans.append({"L": L, "block": b, "start": 0, "end": m, "visit": vi, "v_start": 0,
                          "visit_prompt_len": int(v["n_prompt"]), "visit_len": m,
                          "ids_sha256": ids_digest(v["ids"])})
        arrays[L] = {"blocks": blk, "mask": msk, "depth": dep, "visit": vid, "length": lengths}
    return arrays, spans


def ids_digest(ids):
    """Return a sha256 over a token-id sequence, so a gate can prove a block still holds its visit."""
    return hashlib.sha256(np.asarray(ids, dtype=np.int32).tobytes()).hexdigest()


def legacy_pack(visits, seq, pad_id=0):
    """Return concatenated fixed-token blocks and visit spans for a negative context test; training must use independent visit blocks."""
    ids_s, msk_s, owner = [], [], []
    for vi, v in enumerate(visits):
        ids_s.extend(v["ids"])
        msk_s.extend(v["mask"])
        owner.extend([(vi, j) for j in range(len(v["ids"]))])
    nb = len(ids_s) // seq
    blk = np.asarray(ids_s[:nb * seq], dtype=np.int32).reshape(nb, seq)
    msk = np.asarray(msk_s[:nb * seq], dtype=np.int8).reshape(nb, seq)
    spans, cur = [], None
    for pos in range(nb * seq):
        b, off = divmod(pos, seq)
        vi, voff = owner[pos]
        if cur is not None and cur["block"] == b and cur["visit"] == vi:
            cur["end"] = off + 1
            continue
        cur = {"L": seq, "block": b, "start": off, "end": off + 1, "visit": vi, "v_start": voff,
               "visit_prompt_len": int(visits[vi]["n_prompt"]), "visit_len": len(visits[vi]["ids"])}
        spans.append(cur)
    arrays = {seq: {"blocks": blk, "mask": msk,
                    "depth": np.ones(nb, dtype=np.int8),
                    "visit": np.full(nb, -1, dtype=np.int32)}}
    return arrays, spans


# ================================================================= the schedule
def build_schedule(cfg, arrays, rng):
    """Return shuffled micro-batches homogeneous in depth AND block length, grouped into equal-block windows by a window index, and the optimizer-step count; supervised counts exclude padding."""
    windows = []
    for L, A in sorted(arrays.items()):
        micro_n, accum = cfg.micro(L), cfg.accum(L)
        pool = []
        for d in cfg.depths:
            idx = [int(i) for i in np.where(A["depth"] == d)[0]]
            rng.shuffle(idx)
            for j in range(len(idx) // micro_n):
                sel = idx[j * micro_n:(j + 1) * micro_n]
                mb = {"depth": int(d), "seq_len": int(L), "blocks": sel,
                      "supervised": int(A["mask"][sel][:, 1:].sum())}
                if mb["supervised"] > 0:
                    pool.append(mb)
        rng.shuffle(pool)
        # a window never mixes block lengths: its accumulation count is the bucket's own
        for j in range(len(pool) // accum):
            windows.append(pool[j * accum:(j + 1) * accum])
    rng.shuffle(windows)
    sched = []
    for w, window in enumerate(windows):
        for mb in window:
            sched.append(dict(mb, window=w))
    return sched, len(windows)


def windows_from_schedule(sched):
    """Return the schedule grouped into accumulation windows, in order; a micro-batch with no window index becomes its own window, which check_micro then refuses as an undersized step."""
    out = []
    for mb in sched:
        w = int(mb.get("window", len(out)))
        while len(out) <= w:
            out.append([])
        out[w].append(mb)
    return [w for w in out if w]


# ================================================================= V3-CONTEXT
def v3_context(arrays, spans, max_report=20, pad_id=None):
    """Return boundary and supervision diagnostics from block arrays and spans; reject any split or cross-visit context, any block whose ids no longer match its visit, and any padding that is not pad_id."""
    n_sup = 0
    fails = Counter()
    owners = Counter((s["L"], s["block"]) for s in spans)
    visits = Counter(s["visit"] for s in spans)
    for L, A in arrays.items():
        for block in range(len(A["blocks"])):
            if owners[(L, block)] != 1:
                fails["block_span_count"] += 1
    if any(count != 1 for count in visits.values()):
        fails["visit_span_count"] += sum(count != 1 for count in visits.values())
    detail = []
    for s in spans:
        A = arrays[s["L"]]
        if not 0 <= s["start"] < s["end"] <= s["L"]:
            fails["invalid_span_bounds"] += 1
        if A["mask"][s["block"], s["end"]:].any():
            fails["supervised_padding"] += 1
        if "ids_sha256" in s and ids_digest(
                A["blocks"][s["block"], s["start"]:s["end"]]) != s["ids_sha256"]:
            fails["block_ids_changed"] += 1
        if pad_id is not None and not np.all(A["blocks"][s["block"], s["end"]:] == pad_id):
            fails["padding_not_pad_id"] += 1
        m = A["mask"][s["block"], s["start"]:s["end"]]
        pos = np.where(m == 1)[0]
        n_sup += int(pos.size)
        j0 = int(pos.min()) + s["start"] if pos.size else s["end"]
        bad = []
        if s["v_start"] != 0:
            bad.append("prompt_split_or_absent")
        if s["start"] != 0:
            bad.append("cross_visit_context")
        if pos.size and s["start"] + s["visit_prompt_len"] > j0:
            bad.append("prompt_not_before_token")
        if s["end"] - s["start"] != s.get("visit_len", s["end"] - s["start"]):
            bad.append("visit_split")
        for b in bad:
            fails[b] += max(1, int(pos.size))
        if bad and len(detail) < max_report:
            detail.append({"block": int(s["block"]), "L": int(s["L"]), "visit": int(s["visit"]),
                           "v_start": int(s["v_start"]), "start": int(s["start"]),
                           "prompt_len": int(s["visit_prompt_len"]),
                           "first_supervised": j0, "reasons": bad})
    n_bad = sum(1 for s in spans
                if (s["v_start"] != 0 or s["start"] != 0
                    or s["end"] - s["start"] != s.get("visit_len", s["end"] - s["start"])))
    return {"n_spans": len(spans), "n_supervised_tokens": n_sup,
            "n_failing_spans": int(n_bad), "failures_by_reason": dict(fails),
            "ok": bool(n_bad == 0 and not fails), "detail": detail}


# ================================================================= records
def load_records(cfg, P, n_records=None):
    """Return pool records with correct A/B candidates and raw standard fallback chains, plus the chain-stage counts, optionally limited by record count."""
    check_pool(cfg)
    pool = defaultdict(dict)
    with open(os.path.expanduser(cfg["pool_jsonl"]), encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            if r.get("src") in cfg["chains"]:
                pool[r["src"]][int(r["pool_i"])] = r
    records, stats = [], {}
    for src in cfg.sources:
        got = {}
        for tag, key in (("A", "chain_A"), ("B", "chain_B")):
            p = os.path.join(P["artifacts"], "chains_%s_%s_k%d.jsonl"
                             % (src, tag, int(cfg["k_chains"])))
            if not os.path.exists(p):
                raise SystemExit("MISSING chains file %s" % p)
            n_tot = n_kept = 0
            with open(p, encoding="utf-8") as f:
                for line in f:
                    h = json.loads(line)
                    n_tot += 1
                    if h["kept"]:
                        n_kept += 1
                    record = got.setdefault(int(h["pool_i"]), {})
                    record[key] = h["chain"] if h["kept"] else None
                    if tag == "A":
                        record["fallback_chain_A"] = h["chain"]
            stats["%s_%s" % (src, tag)] = {"n": n_tot, "n_kept": n_kept,
                                           "kept_frac": n_kept / max(1, n_tot)}
        for pi, ch in sorted(got.items()):
            a = pool[src].get(pi)
            if a is None:
                continue
            if ch.get("chain_A") is None and ch.get("chain_B") is None:
                continue
            records.append({"src": src, "pool_i": pi, "question": a["question"],
                            "gold": a["gold"], "options": a.get("options"),
                            "chain_A": ch.get("chain_A"), "chain_B": ch.get("chain_B"),
                            "fallback_chain_A": ch.get("fallback_chain_A")})
            if n_records and len(records) >= n_records:
                break
    return records, stats


# ================================================================= stage 2 main
def main(argv):
    """Draw visits until the supervised-token budget is met, pack one visit per block, and write the variant's blocks, schedule, spans and manifest; returns a process exit code."""
    cfg_path, root, variant = DEFAULT_CONFIG, None, None
    budget, seed, n_records, sources = None, None, None, None
    for a in argv:
        k, _, v = a.lstrip("-").partition("=")
        if k == "config":
            cfg_path = v
        elif k == "root":
            root = v
        elif k == "variant":
            variant = v
        elif k == "sources":
            sources = v
        elif k == "budget":
            budget = int(v)
        elif k == "seed":
            seed = int(v)
        elif k == "n-records":
            n_records = int(v)
    require_root(root, "targets.py")
    cfg = load_config(cfg_path, sources)
    variant = variant or cfg["default_variant"]
    A = cfg.variant(variant)
    budget = budget if budget is not None else int(cfg["supervised_token_budget"])
    seed = seed if seed is not None else int(cfg["seed"])
    KEY = variant_key(cfg, variant, seed)
    P = paths(root)
    ensure_dirs(P)
    rng = np.random.default_rng(seed)

    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(cfg["base_repo"], trust_remote_code=True)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    pad_id = tok.pad_token_id

    records, chains_stats = load_records(cfg, P, n_records=n_records)
    print("[targets] variant=%s %d records; chains kept %s"
          % (variant, len(records), {k: round(v["kept_frac"], 3)
                                     for k, v in chains_stats.items()}), flush=True)
    by_src = defaultdict(list)
    for i, r in enumerate(records):
        by_src[r["src"]].append(i)
    srcs = [s for s in cfg.sources if by_src[s]]
    assert srcs, "no source has any record"

    # The objective's two draws come from the theory tables, per source: T from the budget weights
    # and the block depth from the depth weights. `uniform_longest` is the ablation that keeps the
    # old uniform T and the fixed depth mix; the tables are still loaded and recorded, so the two
    # variants differ only in what they draw with.
    tw, tw_sha = load_theory_weights(cfg)
    T_GRID_BY_SRC, T_P_BY_SRC, D_BY_SRC, D_P_BY_SRC = {}, {}, {}, {}
    depths = cfg.depths
    for s in srcs:
        T_GRID_BY_SRC[s], T_P_BY_SRC[s] = budget_draw(cfg, tw, variant, s)
        D_BY_SRC[s], D_P_BY_SRC[s] = depth_draw(cfg, tw, variant, s)
    want = intended_weights(cfg, tw, variant, srcs)
    print("[targets] draw=%s; T weights %s"
          % (draw_rule(cfg, variant),
             {s: {k: round(v, 4) for k, v in want["budget"][s].items()} for s in srcs}),
          flush=True)
    print("[targets] depth weights %s"
          % {s: {k: round(v, 4) for k, v in want["depth"][s].items()} for s in srcs}, flush=True)

    caps = share_caps(cfg, srcs)
    print("[targets] share caps: source %.4f %s, format %.4f %s"
          % (caps["source"]["cap"], "active" if caps["source"]["active"] else "INACTIVE (no "
             "mixture of %d sources could meet it)" % caps["source"]["n_sources"],
             caps["format"]["cap"], "active" if caps["format"]["active"] else "INACTIVE (no "
             "mixture of %d formats could meet it)" % caps["format"]["n_formats"]), flush=True)
    sup_by_src, sup_by_fmt = Counter(), Counter()
    sup_total, tries = 0, 0
    visits, kind_ct = [], Counter()
    sup_by_T, sup_by_kind = Counter(), Counter()
    fb_by_src_T, n_by_src_T = defaultdict(Counter), defaultdict(Counter)
    n_by_src_depth = defaultdict(Counter)
    dropped = Counter()
    dropped_by_T = defaultdict(Counter)
    MAXTRIES = 400000
    while sup_total < budget and tries < MAXTRIES:
        tries += 1
        src = srcs[int(rng.integers(0, len(srcs)))]
        # balance: refuse a source or a format already over its share. The caps apply from the
        # first supervised token; a threshold would leave them inert for every smoke or pilot
        # budget below it, which is exactly where an unbalanced mixture is easiest to ship.
        if caps["source"]["active"] and \
                sup_by_src[src] / max(1, sup_total) > caps["source"]["cap"]:
            caps["source"]["draws_refused"] += 1
            continue
        if caps["format"]["active"] and \
                sup_by_fmt[cfg.fmt(src)] / max(1, sup_total) > caps["format"]["cap"]:
            caps["format"]["draws_refused"] += 1
            continue
        r = records[by_src[src][int(rng.integers(0, len(by_src[src])))]]
        grid = T_GRID_BY_SRC[src]                  # T is drawn over THIS source's grid, with THIS
        T = grid[int(rng.choice(len(grid), p=T_P_BY_SRC[src]))]      # source's weights
        ds = D_BY_SRC[src]                         # one entry when the variant fixes the depth
        depth = int(ds[int(rng.choice(len(ds), p=D_P_BY_SRC[src]))])
        fullplus = bool(T is None and rng.random() < float(cfg["fullplus_p"]))
        try:
            ids, msk, info = build_target(cfg, tok, variant, src, r["question"], r["gold"], T,
                                          r["chain_A"], r["chain_B"], fullplus=fullplus,
                                          fallback_chain_A=r.get("fallback_chain_A"))
        except AssertionError:
            dropped["unstable_tokenisation"] += 1
            continue
        if ids is None:
            dropped[info["dropped"]] += 1
            dropped_by_T[budget_key(T)][info["dropped"]] += 1
            continue
        L = cfg.block_len_for(len(ids))            # the smallest bucket that holds this visit
        if L is None:
            # a visit longer than the largest bucket is DROPPED, never truncated. Truncating would
            # delete the answer supervision at exactly the large budgets this recipe repairs.
            dropped["longer_than_longest_block"] += 1
            dropped_by_T[budget_key(T)]["longer_than_longest_block"] += 1
            continue
        ns = int(info["n_supervised"])
        if ns <= 0:
            dropped["no_supervised_token"] += 1
            continue
        sup_total += ns
        sup_by_src[src] += ns
        sup_by_fmt[cfg.fmt(src)] += ns
        sup_by_T[budget_key(T)] += ns
        sup_by_kind[info["kind"]] += ns
        kind_ct[info["kind"]] += 1
        n_by_src_T[src][budget_key(T)] += 1
        n_by_src_depth[src][str(depth)] += 1
        if info["kind"] == "FALLBACK":
            fb_by_src_T[src][budget_key(T)] += 1
        visits.append({"record": r["pool_i"], "src": src, "T": T, "depth": depth, "ids": ids,
                       "mask": msk, "kind": info["kind"], "chain_used": info["chain_used"],
                       "n_chain": info["n_chain"], "n_prompt": info["n_prompt"],
                       "n_supervised": ns, "n_tokens": len(ids), "block_len": L,
                       "budget_line_tokens": info["budget_line_tokens"]})

    for name, counter in (("source", sup_by_src), ("format", sup_by_fmt)):
        caps[name]["realised"] = {k: counter[k] / max(1, sup_total) for k in counter}
        caps[name]["max_realised"] = max(list(caps[name]["realised"].values()) or [0.0])
        caps[name]["within_cap"] = bool(not caps[name]["active"]
                                        or caps[name]["max_realised"] <= caps[name]["cap"] + 0.05)
    fallback_share = kind_ct["FALLBACK"] / max(1, len(visits))
    drop_share = sum(dropped.values()) / max(1, tries)
    print("[targets] %d visits, %d supervised tokens, fallback %.4f, dropped %.4f of draws"
          % (len(visits), sup_total, fallback_share, drop_share), flush=True)

    arrays, spans = pack_one_visit_per_block(visits, pad_id)
    v3 = v3_context(arrays, spans, pad_id=pad_id)
    assert v3["ok"], v3
    sched, n_opt = build_schedule(cfg, arrays, rng)
    # build_schedule keeps whole micro-batches and whole windows, so some blocks never train
    sup_scheduled = int(sum(int(m["supervised"]) for m in sched))
    pad_by_L = {str(L): round(1.0 - float(a["length"].sum()) / max(1, int(a["blocks"].size)), 5)
                for L, a in sorted(arrays.items())}
    n_blocks = int(sum(int(a["blocks"].shape[0]) for a in arrays.values()))
    n_used = int(sum(len(m["blocks"]) for m in sched))
    used_by_L = Counter()
    for m in sched:
        used_by_L[int(m["seq_len"])] += len(m["blocks"])
    # a bucket needs micro x accum blocks to fill one window, so a thin bucket can lose all of them
    drop_by_L = {str(L): int(a["blocks"].shape[0]) - int(used_by_L[L])
                 for L, a in sorted(arrays.items())}

    # one directory per variant, and per seed when the seed is not the config's: the trainer must
    # never pick up another variant's blocks, nor another seed's draw of the same variant
    DATA = data_dir(P, KEY)
    for L, Aa in arrays.items():
        np.save(os.path.join(DATA, "blocks_%d.npy" % L), Aa["blocks"])
        np.save(os.path.join(DATA, "mask_%d.npy" % L), Aa["mask"])
        np.save(os.path.join(DATA, "length_%d.npy" % L), Aa["length"])
        np.save(os.path.join(DATA, "bdepth_%d.npy" % L), Aa["depth"])
        np.save(os.path.join(DATA, "bvisit_%d.npy" % L), Aa["visit"])
    json.dump(sched, open(os.path.join(DATA, "schedule.json"), "w"))
    with open(os.path.join(DATA, "spans.jsonl"), "w", encoding="utf-8") as f:
        for s in spans:
            f.write(json.dumps(s) + "\n")
    with open(os.path.join(DATA, "visits.jsonl"), "w", encoding="utf-8") as f:
        for v in visits:
            row = {k: v[k] for k in ("record", "src", "T", "depth", "kind", "chain_used",
                                     "n_chain", "n_prompt", "n_supervised", "n_tokens",
                                     "block_len", "budget_line_tokens")}
            row["budget"] = budget_key(v["T"])
            f.write(json.dumps(row) + "\n")

    tok_total = int(sum(int(a["blocks"].size) for a in arrays.values()))
    man = {
        "variant": variant, "variant_key": KEY, "variant_config": A, "seed": seed,
        "supervised_token_budget": budget,
        "data_dir": DATA, "blocks_sha256": blocks_fingerprint(arrays), "pad_id": int(pad_id),
        "exemplar_sha256": exemplar_fingerprints(tok, cfg),
        "supervised_tokens_scheduled": sup_scheduled,
        "blocks_dropped_as_remainder": n_blocks - n_used,
        "micro_by_block_len": {str(L): cfg.micro(L) for L in sorted(arrays)},
        "accum_by_block_len": {str(L): cfg.accum(L) for L in sorted(arrays)},
        "effective_batch_blocks": int(cfg["effective_batch_blocks"]),
        "lora": lora_settings(cfg),
        "supervised_tokens_drawn": sup_total, "n_visits": len(visits),
        "n_records": len(records), "chains": chains_stats,
        "one_visit_per_block": True,
        "packing": "one visit per block, smallest fitting bucket, right-padded, pad mask 0",
        "block_lens": cfg.block_lens,
        "chains_horizon_by_source": {s: cfg.horizon(s) for s in cfg.sources},
        "budget_grid_by_source": {s: [budget_key(t) for t in cfg.budget_grid_for(s)]
                                  for s in cfg.sources},
        "blocks_by_len": {str(L): int(a["blocks"].shape[0]) for L, a in sorted(arrays.items())},
        "visits_by_block_len": {str(L): int(sum(1 for v in visits if v["block_len"] == L))
                                for L in sorted(arrays)},
        "blocks_used_by_len": {str(L): int(used_by_L[L]) for L in sorted(arrays)},
        "blocks_dropped_as_remainder_by_len": drop_by_L,
        "buckets_with_no_window": [str(L) for L in sorted(arrays) if not used_by_L[L]],
        "tokens_in_blocks": sum(v["n_tokens"] for v in visits),
        "padded_tokens_in_blocks": tok_total,
        "padding_share": round(1.0 - sum(v["n_tokens"] for v in visits) / max(1, tok_total), 5),
        "padding_share_by_block_len": pad_by_L,
        "visits_by_T": count_by_budget(v["T"] for v in visits),
        "supervised_by_T": dict(sup_by_T),
        "visits_by_kind": dict(kind_ct), "supervised_by_kind": dict(sup_by_kind),
        "fallback_share_overall": fallback_share,
        "fallback_share_by_src_T": {s: {t: fb_by_src_T[s][t] / max(1, n_by_src_T[s][t])
                                        for t in n_by_src_T[s]} for s in n_by_src_T},
        "visits_by_src_T": {s: dict(n_by_src_T[s]) for s in n_by_src_T},
        "visits_by_src_depth": {s: dict(n_by_src_depth[s]) for s in n_by_src_depth},
        # the objective's two draws: what the theory asked for, and what the draw realised. V10
        # compares them; they can only differ through drops, which are counted above.
        "draw_rule": draw_rule(cfg, variant), "depth_rule": depth_source(cfg, variant),
        "theory_weights_json": THEORY_WEIGHTS, "theory_weights_sha256": tw_sha,
        "theory_weights_formulas": tw.get("formulas"),
        "draw_weights_intended": want,
        "draw_histogram_realised": {"budget": {s: histogram(n_by_src_T[s]) for s in n_by_src_T},
                                    "depth": {s: histogram(n_by_src_depth[s])
                                              for s in n_by_src_depth}},
        "supervised_share_by_source": {s: sup_by_src[s] / max(1, sup_total) for s in sup_by_src},
        "supervised_share_by_format": {f: sup_by_fmt[f] / max(1, sup_total) for f in sup_by_fmt},
        "share_caps": caps, "pool_jsonl": cfg["pool_jsonl"], "pool_sha256": check_pool(cfg),
        "chain_used": dict(Counter(v["chain_used"] for v in visits)),
        "dropped_draws": dict(dropped), "dropped_by_T": {t: dict(d) for t, d in
                                                         dropped_by_T.items()},
        "drop_share_of_draws": round(drop_share, 5),
        "drop_share_over_warn": bool(drop_share > float(cfg["drop_share_warn"])),
        "supervised_in_blocks": int(sum(int(a["mask"].sum()) for a in arrays.values())),
        "supervised_density": float(sum(int(a["mask"].sum()) for a in arrays.values()))
                              / max(1, tok_total),
        "micro_batches": len(sched), "optimiser_steps": n_opt,
        "supervised_tokens_per_opt_step": round(sup_scheduled / max(1, n_opt), 1),
        "depth_fraction_realised": {str(d): float(np.mean([v["depth"] == d for v in visits]))
                                    for d in depths},
        "v3_context": v3, "draw_tries": tries}
    man["v10_draw_weights"] = v10_draw_weights(man)
    jdump(man, manifest_path(P, KEY))
    print(json.dumps({k: man[k] for k in ("variant", "supervised_tokens_drawn", "n_visits",
                                          "blocks_by_len", "optimiser_steps",
                                          "supervised_tokens_per_opt_step",
                                          "supervised_density", "padding_share",
                                          "padding_share_by_block_len",
                                          "fallback_share_overall", "drop_share_of_draws",
                                          "supervised_share_by_source", "visits_by_kind")},
                     indent=2), flush=True)
    if fallback_share >= float(cfg["fallback_ceiling"]):
        print("STOP: fallback share %.4f reaches the %.2f limit -- ask before training"
              % (fallback_share, float(cfg["fallback_ceiling"])), flush=True)
        return 2
    print("TARGETS OK", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
