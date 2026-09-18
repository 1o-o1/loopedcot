"""S32 shared helpers. Built on S28's harness, which ships beside this file as s28_common.py and
is imported read-only; nothing in it is edited.

What is reused verbatim by import: load_model, set_steps, static cache, batch sizing, decode,
strip_tail, make_find_cut, the numeric and letter parses, ans_eq, the jsonl checkpoint helpers,
and the SVAMP/AQuA/CSQA task table and prompt files.

What is new here and only here:
  - the five S32 arms (A0 plus the four factorial arms) and LoRA adapter loading
  - the control-line tag ("Loops: k." / "Loops: k. Tokens: T.") inserted between the few-shot
    prompt and the question
  - the GSM8K task (S9a prompt/stop/parse, 12 answer tokens) and the MATH500 task (S13
    prompt/stop/parse, 32 answer tokens) added to S28's table
  - protocol v2 scoring (own answer if it parses inside the cut, else the forced read-out)
"""
import json, os, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:                   # s28_common, s13_shots and s3_patch ship beside this file
    sys.path.insert(0, HERE)
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")
os.environ.setdefault("HF_HUB_OFFLINE", "1")

import torch
import s28_common as S28

# Every directory a run reads or writes hangs off the run root the stages pass with --root.
# targets.paths() publishes it as S36_RUN_ROOT and calls set_run_root() on this module if it is
# already imported, so the two always agree; without it the working directory stands in.
ROOT = ART = DATA = ADAPTERS = LOGS = TRAIN_LOGS = None


def set_run_root(root):
    """Point ROOT, ART, DATA, ADAPTERS, LOGS and TRAIN_LOGS at one run root, here and in S28."""
    global ROOT, ART, DATA, ADAPTERS, LOGS, TRAIN_LOGS
    ROOT = os.path.abspath(os.path.expanduser(str(root)))
    ART = os.path.join(ROOT, "artifacts")
    DATA = os.path.join(ROOT, "data")
    ADAPTERS = os.path.join(ROOT, "adapters")
    LOGS = os.path.join(ROOT, "logs")
    TRAIN_LOGS = os.path.join(ROOT, "train_logs")
    S28.set_run_root(ROOT)
    return ROOT


set_run_root(os.environ.get("S36_RUN_ROOT") or os.getcwd())
BASE_REPO = "ByteDance/Ouro-1.4B"
DEV = "cuda"
MEM_FRACTION = float(os.environ.get("S32_MEM_FRACTION", "0.85"))
BATCH_CAP = int(os.environ.get("S32_BATCH_CAP", "32"))
BUDGETS = [0, 16, 32, 64, 128, 256, 512]
CAPS = [16, 32, 64, 128, 256, 512]
KS = [1, 2, 3, 4]
MAXB = 512
SEED = 20260910
S28_SEED = 20260908
LORA_TARGETS = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
LORA_R, LORA_ALPHA, LORA_DROPOUT = 16, 32, 0.0

ARMS = ["A0", "F00", "F01", "F10", "F11"]
ARM_CFG = {                       # (execution-depth policy in training, tagged?)
    "A0":  {"trained": False, "tagged": False, "mixed": None},
    "F00": {"trained": True,  "tagged": False, "mixed": False},
    "F01": {"trained": True,  "tagged": True,  "mixed": False},
    "F10": {"trained": True,  "tagged": False, "mixed": True},
    "F11": {"trained": True,  "tagged": True,  "mixed": True},
}

# ------------------------------------------------------------------ tasks
# S28's three tasks are taken from its table unchanged. GSM8K and MATH500 are added with their
# own harnesses' constants: GSM8K = S9a (12 answer tokens), MATH500 = S13 (32 answer tokens).
NANS = {"gsm8k": 12, "math500": 32, "svamp": 8, "aqua": 8, "csqa": 8}
EVAL_N = {"gsm8k": 300, "math500": 300, "svamp": 300, "csqa": 300, "aqua": 154}
CAL_N = {"gsm8k": 100, "math500": 100, "svamp": 100, "csqa": 100, "aqua": 100}
TASK_ORDER = ["gsm8k", "math500", "svamp", "csqa", "aqua"]
CHANCE = {"gsm8k": 0.0, "math500": 0.0, "svamp": 0.0, "aqua": 0.2, "csqa": 0.2}

GSM8K_STOPS = ["\n\nQuestion:", "Final Answer:"]        # S9a verbatim
MATH_STOPS = ["\n\nProblem:", "Final Answer:"]          # S13 verbatim


def nvsmi():
    return S28.nvsmi()


def gpu_procs():
    return S28.gpu_procs()


# ------------------------------------------------------------------ data
def _harness_rows(task):
    """The evaluation harness's frozen rows of `task` (prod/tasks/data/rows_<task>.jsonl, dataset
    order, sha-pinned in hashes.json) in this module's row shape, or None outside the checkout.
    They are the rows every production grid was generated on, and they need no network."""
    path = os.path.join(os.path.dirname(HERE), "prod", "tasks", "data", "rows_%s.jsonl" % task)
    if not os.path.exists(path):
        return None
    out = []
    for line in open(path, encoding="utf-8"):
        r = json.loads(line)
        row = {"idx": int(r["idx"]), "input": r["input"], "target": r["target"],
               "options": None, "gold_text": None}
        if "solution" in r:
            row["solution"] = r["solution"]
        out.append(row)
    return out


def gsm8k_rows(split, lo=0, hi=None):
    """S9a's loader, verbatim semantics: openai/gsm8k main, dataset order (the harness's frozen
    test rows when the package sits inside the checkout, the Hub otherwise)."""
    if split == "test":
        rows = _harness_rows("gsm8k")
        if rows is not None:
            hi = len(rows) if hi is None else min(hi, len(rows))
            return rows[lo:hi]
    from datasets import load_dataset
    d = load_dataset("openai/gsm8k", "main", split=split)
    hi = len(d) if hi is None else min(hi, len(d))
    return [{"idx": i, "input": d[i]["question"],
             "target": d[i]["answer"].split("####")[-1].strip().replace(",", "").replace("$", ""),
             "options": None, "gold_text": None} for i in range(lo, hi)]


def math500_rows(lo=0, hi=None):
    """S13's loader, verbatim semantics: HuggingFaceH4/MATH-500 test, dataset order (the
    harness's frozen rows inside the checkout, the Hub otherwise)."""
    rows = _harness_rows("math500")
    if rows is not None:
        hi = len(rows) if hi is None else min(hi, len(rows))
        return rows[lo:hi]
    from datasets import load_dataset
    d = load_dataset("HuggingFaceH4/MATH-500", split="test")
    hi = len(d) if hi is None else min(hi, len(d))
    return [{"idx": i, "input": d[i]["problem"], "target": d[i]["answer"],
             "options": None, "gold_text": None, "solution": d[i]["solution"]}
            for i in range(lo, hi)]


def task_rows(task, lo=0, hi=None):
    if task == "gsm8k":
        return gsm8k_rows("test", lo, hi)
    if task == "math500":
        return math500_rows(lo, hi)
    # S28's three tasks come from artifacts/data32_<task>.jsonl, which s32_data.py builds from
    # S28's own shuffle(seed=20260908) and asserts is byte-identical to S28's file on the
    # evaluation half, extended with the calibration rows S28 never wrote.
    p = os.path.join(ART, "data32_%s.jsonl" % task)
    if not os.path.exists(p):
        # the row sets ship with the package (train/data/, copied from the S32 spike); a run
        # root may carry its own copy, which wins
        p = os.path.join(HERE, "data", "data32_%s.jsonl" % task)
    rows = [json.loads(l) for l in open(p, encoding="utf-8")]
    hi = len(rows) if hi is None else min(hi, len(rows))
    return rows[lo:hi]


def split_rows(task):
    """(evaluation rows, calibration rows). The evaluation half is each harness's own N; the
    calibration half is the next CAL_N rows in the same order (S28's rule, AQuA 154/100)."""
    n_e, n_c = EVAL_N[task], CAL_N[task]
    rows = task_rows(task, 0, n_e + n_c)
    return rows[:n_e], rows[n_e:n_e + n_c]


# ------------------------------------------------------------------ few-shot prefix per task
def _harness_prefix(task):
    """The evaluation harness's own exemplar block for `task`, or None outside the checkout.

    prod/tasks/data/prompt_<task>.txt is the frozen, sha-pinned block every production grid was
    generated with (prod.tasks.prompt_prefix plus the task's separator). Reading it is what
    "byte-identical to evaluation" means, and it needs no network: the rebuilds below fetch
    openai/gsm8k and MATH-500 from the Hub, which a compute node in offline mode cannot.
    """
    repo = os.path.dirname(HERE)
    if repo not in sys.path:
        sys.path.insert(0, repo)
    try:
        from prod import tasks as PT
        return PT.prompt_prefix(task, None) + PT.task_cfg(task)["sep"]
    except Exception:                      # noqa: BLE001 -- not inside the loopedcot checkout
        return None


def few_shot_prefix(tok, task):
    """The task's exemplar block, ending exactly where the tag line is inserted: the evaluation
    harness's frozen file when the package sits inside the checkout, else the S9a/S13/S28 rebuild
    (byte-identical for csqa and aqua, checked; the frozen gsm8k and math500 files are those
    rebuilds' output, frozen)."""
    blk = _harness_prefix(task)
    if blk is not None:
        return blk
    if task == "gsm8k":                       # S9a / S13 verbatim
        from datasets import load_dataset
        d = load_dataset("openai/gsm8k", "main", split="train")
        return "".join("Question: %s\nAnswer: %s\n\n" % (d[i]["question"], d[i]["answer"])
                       for i in range(4))
    if task == "math500":                     # S13's math_shots, verbatim
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
        from s13_shots import math_shots      # a verbatim copy of S13's helper, see that file
        shots, meta = math_shots(4)
        return "".join("Problem: %s\nSolution: %s\nFinal Answer: %s\n\n" % (s["p"], s["s"], s["a"])
                       for s in shots)
    tp = S28.task_prompt(task)
    if task == "svamp":
        return tp + "\n\n"
    return tp + S28.TASK_CFG[task]["sep"]


def task_bits(task):
    """(question prefix, answer prefix, forced suffix text, stop strings, own marker, kind)."""
    if task == "gsm8k":
        return ("Question: ", "\nAnswer:", "\nFinal Answer:", list(GSM8K_STOPS), "####", "numeric")
    if task == "math500":
        return ("Problem: ", "\nSolution:", "\nFinal Answer:", list(MATH_STOPS), "\\boxed", "math")
    c = S28.TASK_CFG[task]
    return (c["q_prefix"], c["a_prefix"], c["suffix"], list(c["stops"]), c["own_marker"], c["kind"])


# ------------------------------------------------------------------ the tag line
def tag_line(arm, k, T=None):
    """The one control line inserted between the few-shot prompt and the question.

    A0 has no line at all. Untagged arms carry only the depth. Tagged arms carry depth and cap;
    the cap value of the B=0 cell is 0, which never appears in the training pool (recorded)."""
    if arm == "A0":
        return ""
    if ARM_CFG[arm]["tagged"] and T is not None:
        return "Loops: %d. Tokens: %d.\n" % (int(k), int(T))
    return "Loops: %d.\n" % int(k)


def build_prompts(tok, task, rows, arm, k, T=None, tag_override=None):
    qp, ap, suffix_text, stops, marker, kind = task_bits(task)
    prefix = few_shot_prefix(tok, task)
    tl = tag_line(arm, k, T) if tag_override is None else tag_override
    prompts = [prefix + tl + qp + r["input"] + ap for r in rows]
    suffix_ids = tok(suffix_text, add_special_tokens=False)["input_ids"]
    extra = {"prefix_tokens": len(tok(prefix, add_special_tokens=False)["input_ids"]),
             "tag_line": tl,
             "tag_line_tokens": len(tok(tl, add_special_tokens=False)["input_ids"]) if tl else 0,
             "suffix_text": suffix_text}
    return prompts, suffix_ids, stops, [tok.eos_token_id], extra


# ------------------------------------------------------------------ model
def load_base():
    torch.cuda.set_per_process_memory_fraction(MEM_FRACTION)
    from transformers import AutoTokenizer, AutoModelForCausalLM
    tok = AutoTokenizer.from_pretrained(BASE_REPO, trust_remote_code=True)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    m = AutoModelForCausalLM.from_pretrained(
        BASE_REPO, dtype=torch.bfloat16, trust_remote_code=True,
        attn_implementation="sdpa").to(DEV).eval()
    return tok, m


def load_arm(arm):
    """A0 is the stock checkpoint. The four arms are the stock checkpoint with their LoRA adapter
    merged in (merge_and_unload keeps the decode path byte-identical to A0's)."""
    tok, m = load_base()
    if arm == "A0":
        return tok, m, {"merged": False}
    from peft import PeftModel
    path = os.path.join(ADAPTERS, arm)
    pm = PeftModel.from_pretrained(m, path, is_trainable=False)
    m = pm.merge_and_unload()
    m = m.to(DEV).eval()
    return tok, m, {"merged": True, "adapter": path}


def lora_config(r=LORA_R, alpha=LORA_ALPHA, dropout=LORA_DROPOUT):
    from peft import LoraConfig
    return LoraConfig(r=r, lora_alpha=alpha, lora_dropout=dropout, bias="none",
                      task_type="CAUSAL_LM", target_modules=list(LORA_TARGETS))


def set_steps(model, k):
    S28.set_steps(model, k)


# ------------------------------------------------------------------ parsing
RE_BOXED = re.compile(r"\\boxed\s*{")


def last_boxed(s):
    """S13's last-\\boxed extraction (brace matched), verbatim behaviour."""
    if s is None:
        return None
    ms = list(RE_BOXED.finditer(s))
    if not ms:
        return None
    i = ms[-1].end()
    depth, out = 1, []
    while i < len(s) and depth:
        c = s[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                break
        out.append(c)
        i += 1
    return "".join(out).strip() or None


def norm_math(a):
    if a is None:
        return None
    a = str(a).strip().strip("$").replace(" ", "").replace("\\!", "").replace("\\,", "")
    a = a.replace("\\left", "").replace("\\right", "").replace("dfrac", "frac").rstrip(".")
    return a


def math_eq(pred, gold):
    """math_verify when importable, S13's string-normalised fallback otherwise."""
    if pred is None:
        return False
    try:
        from math_verify import parse as mv_parse, verify as mv_verify
        return bool(mv_verify(mv_parse("$%s$" % gold), mv_parse("$%s$" % pred)))
    except Exception:
        return norm_math(pred) == norm_math(gold)


def parse_forced(text, task, options=None):
    if task == "math500":
        if text is None:
            return None
        b = last_boxed(text)
        if b is not None:
            return b
        t = text.split("\n")[0].strip()
        return t or None
    if task == "gsm8k":
        return S28.parse_final_answer(text) if text is not None else None
    return S28.parse_answer(text, task, options)


def parse_own(cut_text, task, options=None):
    if task == "math500":
        return last_boxed(cut_text)
    if task == "gsm8k":
        return S28.trace_own_number(cut_text) if cut_text else None
    return S28.parse_own(cut_text, task, options)


def ans_eq(pred, gold, task):
    if pred is None:
        return False
    if task == "math500":
        return bool(math_eq(pred, gold))
    if task == "gsm8k":
        return bool(S28.num_eq(pred, gold))
    return bool(S28.ans_eq(pred, gold, task))


def score_v2(row):
    """Protocol v2 (D1): the model's own answer if it parses inside the cut, else the forced
    read-out. Computed from stored fields only."""
    if row.get("trace_answer") is not None:
        return bool(row["trace_correct"])
    return bool(row["correct"])


# ------------------------------------------------------------------ re-exports used by the runner
load_ckpt = S28.load_ckpt
Appender = S28.Appender
decode = S28.decode
strip_tail = S28.strip_tail
leftpad = S28.leftpad
make_find_cut = S28.make_find_cut
static_cache_factory = S28.static_cache_factory
batch_for = S28.batch_for
token_pieces = S28.token_pieces
