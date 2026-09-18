"""S28 shared helpers. Built from work/spikes/s26_bbh/scripts/s26_common.py (the harness the brief
tells us to extend) and work/spikes/s9_grid/s9a/scripts/s9a_common.py (the 4-shot GSM8K prompt and
the numeric parse), both read-only. Nothing in S26 / S9a / S13 / S3 is edited.

Differences from s26_common.py, and only these:
  - Spark paths, BATCH_CAP 32 and RESERVE_GB 2.0 (121 GB unified memory instead of an 8 GB laptop)
  - a per-task configuration table (prompt file, question layout, forced suffix, stop strings,
    own-answer marker, answer kind) in place of the BBH-only constants
  - the numeric parse (svamp) is s9a_common's, verbatim; the letter parse is s26_common's with the
    character class widened to lowercase (the Wei et al. exemplars write "(a)") and the yes/no
    branch dropped
  - `first_pos`, the decode-and-bisect used for the two new reach fields
The model loading, the static cache, the batch sizing, the natural stop (`make_find_cut`), the
decode loop and the checkpoint helpers are copied unchanged.
"""
import json, os, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")
import torch

BASE_REPO = "ByteDance/Ouro-1.4B"
THINK_REPO = "ByteDance/Ouro-1.4B-Thinking"
# The exemplar blocks are package content: they ship beside this file and are pinned by sha256, so
# every run builds the same prompt bytes. Everything a run reads or writes is under its run root.
PROMPTS = os.path.join(HERE, "prompts")
ROOT = ART = LOGS = None


def set_run_root(root):
    """Point ROOT, ART and LOGS at the run root the stages pass with --root."""
    global ROOT, ART, LOGS
    ROOT = os.path.abspath(os.path.expanduser(str(root)))
    ART = os.path.join(ROOT, "artifacts")
    LOGS = os.path.join(ROOT, "logs")
    return ROOT


set_run_root(os.environ.get("S36_RUN_ROOT") or os.getcwd())
DEV = "cuda"
MEM_FRACTION = float(os.environ.get("S28_MEM_FRACTION", "0.85"))
BUDGETS = [0, 16, 32, 64, 128, 256, 512]
KS = [1, 2, 3, 4]
MAXB = 512          # generation horizon = the largest budget
NANS = 8            # forced answer tokens (the brief)
BATCH_CAP = int(os.environ.get("S28_BATCH_CAP", "32"))
SEED = 20260908     # the fixed seed for "first N by a fixed seed"

TASKS = ["svamp", "aqua", "csqa", "arc"]
REQUIRED_TASKS = ["svamp", "aqua", "csqa"]
CHANCE = {"svamp": 0.0, "aqua": 0.2, "csqa": 0.2, "arc": 0.25}

# ------------------------------------------------------------------ per-task configuration
# `q_prefix` / `a_prefix` / `sep` reproduce each prompt's own layout exactly:
#   svamp  -> S9a's GSM8K prompt, whose prefix already ends with "\n\n"
#   others -> the Wei et al. 2022 CoT layout, "Q: ... \nA: ..." separated by a blank line
TASK_CFG = {
    "svamp": {"kind": "numeric", "hf": "ChilleD/SVAMP", "config": None, "split": "test",
              "n": 300, "sep": "", "q_prefix": "Question: ", "a_prefix": "\nAnswer:",
              # base: " Final Answer:" and not S9a's "\nFinal Answer:". With the newline the base
              # model answers " The final answer is \boxed{" and the 8 answer tokens run out
              # before the number (20-problem smoke: forced parse rate 0.70 against 1.00, acc
              # 0.60 against 0.90). The thinking suffix stays S9a's, which measured a parse rate
              # of 1.00 against 0.95 for the alternative. Both are recorded in smoke.json.
              "suffix": " Final Answer:", "suffix_think": "\n\nFinal Answer:",
              "suffix_alt": "\nFinal Answer:",
              "stops": ["\n\nQuestion:", "Final Answer:"], "own_marker": "####"},
    "aqua": {"kind": "letter", "hf": "deepmind/aqua_rat", "config": "raw", "split": "test",
             "n": None, "sep": "\n\n", "q_prefix": "Q: ", "a_prefix": "\nA:",
             "suffix": "\nThe answer is", "suffix_think": "\nThe answer is",
             "suffix_alt": " The answer is",
             "stops": ["\n\nQ:", "\nQ:"], "own_marker": "The answer is"},
    "csqa": {"kind": "letter", "hf": "tau/commonsense_qa", "config": None, "split": "validation",
             "n": 300, "sep": "\n\n", "q_prefix": "Q: ", "a_prefix": "\nA:",
             "suffix": "\nSo the answer is", "suffix_think": "\nSo the answer is",
             "suffix_alt": " So the answer is",
             "stops": ["\n\nQ:", "\nQ:"], "own_marker": "So the answer is"},
    "arc": {"kind": "letter", "hf": "allenai/ai2_arc", "config": "ARC-Challenge", "split": "test",
            "n": 300, "sep": "\n\n", "q_prefix": "Q: ", "a_prefix": "\nA:",
            "suffix": "\nSo the answer is", "suffix_think": "\nSo the answer is",
            "suffix_alt": " So the answer is",
            "stops": ["\n\nQ:", "\nQ:"], "own_marker": "So the answer is"},
}


def nvsmi():
    try:
        return subprocess.run(
            ["nvidia-smi", "--query-gpu=memory.used,memory.total", "--format=csv,noheader"],
            capture_output=True, text=True, timeout=60).stdout.strip()
    except Exception as e:
        return "nvidia-smi failed: %r" % (e,)


def gpu_procs():
    try:
        return subprocess.run(
            ["nvidia-smi", "--query-compute-apps=pid,process_name,used_memory",
             "--format=csv,noheader"], capture_output=True, text=True,
            timeout=60).stdout.strip().replace("\n", " | ")
    except Exception as e:
        return "nvidia-smi failed: %r" % (e,)


# ------------------------------------------------------------------ model (S26 verbatim)
def load_model(repo=BASE_REPO):
    torch.cuda.set_per_process_memory_fraction(MEM_FRACTION)
    from transformers import AutoTokenizer, AutoModelForCausalLM
    tok = AutoTokenizer.from_pretrained(repo, trust_remote_code=True)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    m = AutoModelForCausalLM.from_pretrained(
        repo, dtype=torch.bfloat16, trust_remote_code=True,
        attn_implementation="sdpa").to(DEV).eval()
    return tok, m


def set_steps(model, k):
    model.model.total_ut_steps = int(k)
    assert int(model.model.total_ut_steps) == int(k)


def cache_class(model):
    return getattr(sys.modules[type(model).__module__], "UniversalTransformerCache")


def make_static_cache_cls(model):
    """S9d/S13's preallocated UniversalTransformerCache, verbatim."""
    UTC = cache_class(model)

    class StaticUTCache(UTC):
        def __init__(self, n_entries, batch, max_len, n_kv_heads, head_dim, dtype, device):
            self.key_cache, self.value_cache, self.layers = [], [], []
            self._seen_tokens = 0
            self.max_cache_size = n_entries
            self.lens = [0] * n_entries
            self.max_len = max_len
            for _ in range(n_entries):
                self.key_cache.append(torch.empty(batch, n_kv_heads, max_len, head_dim,
                                                  dtype=dtype, device=device))
                self.value_cache.append(torch.empty(batch, n_kv_heads, max_len, head_dim,
                                                    dtype=dtype, device=device))

        def update(self, key_states, value_states, layer_idx, cache_kwargs=None):
            n = key_states.shape[2]
            s = self.lens[layer_idx]
            if s + n > self.max_len:
                raise RuntimeError("StaticUTCache overflow: %d + %d > %d" % (s, n, self.max_len))
            self.key_cache[layer_idx][:, :, s:s + n, :] = key_states
            self.value_cache[layer_idx][:, :, s:s + n, :] = value_states
            self.lens[layer_idx] = s + n
            self._seen_tokens = s + n
            return (self.key_cache[layer_idx][:, :, :s + n, :],
                    self.value_cache[layer_idx][:, :, :s + n, :])

        def get_seq_length(self, layer_idx=0):
            if layer_idx is None:
                layer_idx = 0
            if layer_idx < 0 or layer_idx >= len(self.lens):
                return 0
            return self.lens[layer_idx]

        def get_usable_length(self, new_seq_length, layer_idx=0):
            return self.get_seq_length(layer_idx)

        def clear(self):
            self.lens = [0] * len(self.lens)
            self._seen_tokens = 0

    return StaticUTCache


def static_cache_factory(model, k):
    cls = make_static_cache_cls(model)
    cfg = model.config
    nkv, hd = cfg.num_key_value_heads, cfg.head_dim
    dtype = next(model.parameters()).dtype
    dev = next(model.parameters()).device

    def factory(batch, max_len):
        return cls(cfg.num_hidden_layers * int(k), batch, max_len, nkv, hd, dtype, dev)
    return factory


def bytes_per_row_token(k):
    """2(K,V) * 16 kv heads * 128 head_dim * 2 (bf16) * 24 layers * k steps."""
    return 196608 * int(k)


RESERVE_GB = float(os.environ.get("S28_RESERVE_GB", "2.0"))


def row_token_ceiling(k, reserve_gb=RESERVE_GB):
    """Largest (batch row x token) KV allocation we may make right now, MEASURED. S26 verbatim
    except for the fallback constants, which are the Spark's."""
    free, total = torch.cuda.mem_get_info()
    ours = torch.cuda.memory_reserved()
    cap_left = MEM_FRACTION * total - ours
    avail = min(float(free), max(0.0, cap_left)) - reserve_gb * 1024 ** 3
    return max(256, int(avail / bytes_per_row_token(k)))


def batch_for(k, max_seq, cap=BATCH_CAP):
    """(batch, unclamped estimate)."""
    try:
        est = int(row_token_ceiling(k) / max(1, max_seq))
    except Exception:
        est = cap
    return max(1, min(cap, est)), est


def token_pieces(tok, vocab_size):
    return tok.batch_decode([[i] for i in range(vocab_size)], clean_up_tokenization_spaces=False)


# ------------------------------------------------------------------ data
def task_rows(task, lo=0, hi=None):
    """Rows of artifacts/data_<task>.jsonl: {idx, input, target, options, gold_text}."""
    p = os.path.join(ART, "data_%s.jsonl" % task)
    rows = [json.loads(l) for l in open(p, encoding="utf-8")]
    hi = len(rows) if hi is None else min(hi, len(rows))
    return rows[lo:hi]


def task_prompt(task):
    """The exemplar block, verbatim. No canary header in these files, so no lines are dropped."""
    return open(os.path.join(PROMPTS, "%s.txt" % task), encoding="utf-8").read().rstrip("\n")


def build_prompts(tok, model_name, task, rows, suffix_text=None):
    cfg = TASK_CFG[task]
    tp = task_prompt(task)
    if task == "svamp":
        tp = tp + "\n\n"        # S9a's prefix ends with a blank line; rstrip above removed it
    head = tp + cfg["sep"] + cfg["q_prefix"]
    if model_name == "base":
        stext = cfg["suffix"] if suffix_text is None else suffix_text
        prompts = [head + r["input"] + cfg["a_prefix"] for r in rows]
        suffix_ids = tok(stext, add_special_tokens=False)["input_ids"]
        stop_strings = list(cfg["stops"])
        eos_ids = [tok.eos_token_id]
        extra = {"prefix_tokens": len(tok(tp, add_special_tokens=False)["input_ids"])}
    else:
        stext = cfg["suffix_think"] if suffix_text is None else suffix_text
        user = [head + r["input"] for r in rows]
        prompts = [tok.apply_chat_template([{"role": "user", "content": u}], tokenize=False,
                                           add_generation_prompt=True, enable_thinking=True)
                   for u in user]
        end_think = tok.convert_tokens_to_ids("</think>")
        suffix_ids = [end_think] + tok(stext, add_special_tokens=False)["input_ids"]
        stop_strings = None
        eos_ids = [tok.eos_token_id, end_think]
        extra = {"end_think_id": end_think}
    extra["suffix_text"] = stext
    return prompts, suffix_ids, stop_strings, eos_ids, extra


# ------------------------------------------------------------------ natural stop (S26 verbatim)
def make_find_cut(tok, model_name, stop_strings, eos_ids):
    def find_cut_base(ids):
        full = tok.decode(ids, clean_up_tokenization_spaces=False)
        hits = [full.find(m) for m in stop_strings]
        hits = [h for h in hits if h >= 0]
        eosp = None
        for j, v in enumerate(ids):
            if v in eos_ids:
                eosp = j
                break
        if not hits:
            return (len(ids), None) if eosp is None else (eosp, "eos")
        pos = min(hits)
        lo, hi = 0, len(ids)
        while lo < hi:
            mid = (lo + hi) // 2
            if len(tok.decode(ids[:mid], clean_up_tokenization_spaces=False)) > pos:
                hi = mid
            else:
                lo = mid + 1
        c = max(0, lo - 1)
        if eosp is not None and eosp < c:
            return eosp, "eos"
        return c, full[pos:pos + 16]

    def find_cut_think(ids):
        for j, v in enumerate(ids):
            if v in eos_ids:
                return j, tok.decode([v])
        return len(ids), None

    return find_cut_base if model_name == "base" else find_cut_think


# ------------------------------------------------------------------ parsing
# numeric: s9a_common.py, verbatim
RE_INT = re.compile(r"-?\d[\d,]*(?:\.\d+)?")


def parse_final_answer(text):
    if "Final Answer:" in text:
        tail = text.rsplit("Final Answer:", 1)[1]
    else:
        tail = text
    tail = tail.split("\n")[0] if "\n" in tail else tail
    m = RE_INT.findall(tail.replace("$", ""))
    if not m:
        m = RE_INT.findall(text.replace("$", ""))
        if not m:
            return None
    v = m[-1].replace(",", "")
    if v.endswith("."):
        v = v[:-1]
    return v


def num_eq(a, b):
    if a is None:
        return False
    try:
        return abs(float(a) - float(b)) < 1e-6
    except Exception:
        return a == b


def trace_own_number(cut_text):
    """s9a_common.trace_own_answer, verbatim: first number after the LAST '####'."""
    if "####" not in cut_text:
        return None
    m = RE_INT.findall(cut_text.rsplit("####", 1)[1].replace("$", ""))
    return m[0].replace(",", "") if m else None


# letter: s26_common.py with the class widened to lowercase (the exemplars write "(a)")
RE_PAREN = re.compile(r"\(([A-Ea-e])\)")
RE_BARE = re.compile(r"^[^A-Za-z0-9]*([A-Ea-e])\b")


def parse_letter(text, options=None):
    if text is None:
        return None
    m = RE_PAREN.search(text)
    if m:
        return "(%s)" % m.group(1).upper()
    m = RE_BARE.match(text)
    if m and (not options or m.group(1).upper() in options):
        return "(%s)" % m.group(1).upper()
    return None


def parse_answer(text, task, options=None):
    """The forced parse. `text` is the decoded forced-answer continuation (8 tokens)."""
    if TASK_CFG[task]["kind"] == "numeric":
        return parse_final_answer(text) if text is not None else None
    return parse_letter(text, options)


def parse_own(cut_text, task, options=None):
    """The model's own answer inside the cut trace: what follows the LAST own marker."""
    if not cut_text:
        return None
    mk = TASK_CFG[task]["own_marker"]
    if mk not in cut_text:
        return None
    if TASK_CFG[task]["kind"] == "numeric":
        return trace_own_number(cut_text)
    tail = cut_text.rsplit(mk, 1)[1].split("\n")[0]
    return parse_letter(tail, options)


def ans_eq(pred, gold, task):
    if pred is None:
        return False
    if TASK_CFG[task]["kind"] == "numeric":
        return bool(num_eq(pred, gold))
    # gold is a bare letter in data_<task>.jsonl, the parses return "(X)": compare unwrapped
    return pred.strip().upper().strip("()") == gold.strip().upper().strip("()")


# ------------------------------------------------------------------ reach positions (NEW)
def _num_patterns(gold):
    """Digit/decimal-point boundaries so '50' does not match inside '150' or '3.507'."""
    g = str(gold).strip()
    pats = [g]
    try:
        f = float(g)
        if abs(f - int(f)) < 1e-9:
            pats.append("{:,}".format(int(f)))     # comma-formatted variant
            pats.append(str(int(f)))
    except Exception:
        pass
    out = []
    for p in dict.fromkeys(pats):
        out.append(re.compile(r"(?<![\d.])" + re.escape(p) + r"(?![\d.])"))
    return out


def reach_patterns(task, ans, options=None):
    """Regexes whose first complete occurrence defines the reach position of `ans`."""
    if ans is None:
        return []
    if TASK_CFG[task]["kind"] == "numeric":
        return _num_patterns(ans)
    L = str(ans).strip().strip("()").upper()
    if not L:
        return []
    return [re.compile(r"\(" + L + r"\)", re.IGNORECASE)]


def text_patterns(s):
    if not s:
        return []
    s = str(s).strip()
    if len(s) < 2:
        return []
    return [re.compile(re.escape(s), re.IGNORECASE)]


def first_pos(tok, ids, patterns):
    """Smallest token count t such that decode(ids[:t]) already CONTAINS one of `patterns`.

    Decode the trace once, take the earliest match END (so the whole string is present), then
    bisect on the decoded length -- the same decode-and-bisect `find_cut` uses. None if no match.
    """
    if not patterns or not ids:
        return None
    full = tok.decode(ids, clean_up_tokenization_spaces=False)
    end = None
    for p in patterns:
        m = p.search(full)
        if m is not None:
            end = m.end() if end is None else min(end, m.end())
    if end is None:
        return None
    lo, hi = 0, len(ids)
    while lo < hi:
        mid = (lo + hi) // 2
        if len(tok.decode(ids[:mid], clean_up_tokenization_spaces=False)) >= end:
            hi = mid
        else:
            lo = mid + 1
    return int(lo)


# ------------------------------------------------------------------ decode (S26 verbatim)
def leftpad(seqs, pad, dev):
    L = max(len(s) for s in seqs)
    ids = torch.full((len(seqs), L), pad, dtype=torch.long)
    att = torch.zeros((len(seqs), L), dtype=torch.long)
    for r, s in enumerate(seqs):
        ids[r, L - len(s):] = torch.tensor(s, dtype=torch.long)
        att[r, L - len(s):] = 1
    return ids.to(dev), att.to(dev), L


@torch.no_grad()
def decode(model, tok, seqs, n_new, pad, cache_factory, k, eos_ids, pieces,
           stop_strings=None):
    """Greedy decode over the patched UniversalTransformerCache. S26 verbatim."""
    dev = next(model.parameters()).device
    B = len(seqs)
    ids, attn, L = leftpad(seqs, pad, dev)
    cache = cache_factory(B, L + n_new)
    pos = (attn.cumsum(-1) - 1).clamp(min=0)
    cp = torch.arange(L, device=dev)
    out = model(input_ids=ids, attention_mask=attn, position_ids=pos, past_key_values=cache,
                use_cache=True, cache_position=cp, logits_to_keep=1)
    cur = out.logits[:, -1, :].float().argmax(-1)
    del out

    gen = [[] for _ in range(B)]
    tails = [""] * B
    fin = [False] * B
    eset = set(eos_ids or [])
    t0 = time.time()
    t = 0
    while t < n_new:
        nxt = cur.tolist()
        feed = [pad] * B
        for b in range(B):
            if fin[b]:
                continue
            x = nxt[b]
            gen[b].append(x)
            feed[b] = x
            if x in eset:
                fin[b] = True
                continue
            if stop_strings:
                tails[b] = (tails[b] + pieces[x])[-64:]
                if any(s in tails[b] for s in stop_strings):
                    fin[b] = True
        t += 1
        if t >= n_new or all(fin):
            break
        cur_in = torch.tensor(feed, dtype=torch.long, device=dev).unsqueeze(1)
        attn = torch.cat([attn, torch.ones((B, 1), dtype=attn.dtype, device=dev)], 1)
        o = model(input_ids=cur_in, attention_mask=attn,
                  position_ids=attn.sum(-1, keepdim=True) - 1,
                  past_key_values=cache, use_cache=True,
                  cache_position=torch.tensor([L + t - 1], device=dev), logits_to_keep=1)
        cur = o.logits[:, -1, :].float().argmax(-1)
        del o
    dt = time.time() - t0
    del cache, ids, attn, cur
    torch.cuda.empty_cache()
    return gen, dt


def strip_tail(ids_out, eos_ids):
    """S9a verbatim: keep the eos token, drop everything after it."""
    out = []
    for t in ids_out:
        cut = len(t)
        for j, v in enumerate(t):
            if v in eos_ids:
                cut = j + 1
                break
        out.append(t[:cut])
    return out


# ------------------------------------------------------------------ jsonl checkpoints (verbatim)
def load_ckpt(path, keyfn):
    done = {}
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                except Exception:
                    continue  # truncated last line after a kill
                done[keyfn(r)] = r
    return done


class Appender(object):
    def __init__(self, path):
        self.path = path
        self.f = open(path, "a", encoding="utf-8")

    def write(self, row):
        self.f.write(json.dumps(row) + "\n")
        self.f.flush()
        os.fsync(self.f.fileno())

    def close(self):
        self.f.close()
