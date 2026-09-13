"""Freeze every prompt and row file into prod/tasks/data/ with a sha256, once.

  python -m prod.tasks.freeze --copy     # pure file copy from the spikes (laptop, no network)
  python -m prod.tasks.freeze --extend   # full-split rows where the spike file is a prefix
  python -m prod.tasks.freeze --verify   # re-hash data/ against data/hashes.json
  python -m prod.tasks.freeze --rehash   # rewrite hashes.json after a deliberate data change
  python -m prod.tasks.freeze --sources  # print data/sources.json (Hub repo + revision per set)

--copy takes, from the read-only spikes:
  prompt_gsm8k.txt     rebuilt from openai/gsm8k train rows 0-3 IF the dataset is cached, else
                       copied from s28_transfer_tasks/prompts/svamp.txt, which s28_download.py
                       wrote with S9a's own format string from exactly those rows (so it is the
                       S9a GSM8K 4-shot prefix, verbatim, and needs no network)
  prompt_math500.txt   the "prefix_text" field of s13_box_grid/artifacts/math500_prompt.json
  prompt_svamp.txt     s28_transfer_tasks/prompts/svamp.txt
  prompt_aqua.txt      s28_transfer_tasks/prompts/aqua.txt        (+ S28's "\\n\\n" separator rule)
  prompt_csqa.txt      s28_transfer_tasks/prompts/csqa.txt
  prompt_arc.txt       s28_transfer_tasks/prompts/arc.txt         (agent-written exemplars)
  prompt_bbh_*.txt     s26_bbh/prompts/*.txt with the canary line and "-----" dropped, which is
                       what s26_common.task_prompt does and what the BIG-Bench-Hard repo does
  rows_bbh_*.jsonl     s26_bbh/artifacts/bbh_*.jsonl (250 rows each: the full BBH task)
  rows_aqua.jsonl      s28_transfer_tasks/artifacts/data_aqua.jsonl (254 rows: the full split)
  rows_{svamp,csqa,arc}.jsonl  the 300-row spike files, replaced at --extend by the full split

--extend rebuilds SVAMP / CSQA / ARC at full N and GSM8K / MATH500 from their datasets, with
`shuffle(seed=20260908)` for the three S28 tasks (s28_download.py's own selection rule) and dataset
order for GSM8K, MATH500 and BBH, then ASSERTS the spike file is a byte-identical prefix.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from prod.common import DATA, SPLIT_SEED, load_json, save_json, sha256_file   # noqa: E402
from prod.tasks import TASKS, TASK_ORDER, prefix_keys, task_cfg             # noqa: E402

SPIKES = os.environ.get(
    "PROD_SPIKES",
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))), "spikes"))
S26 = os.path.join(SPIKES, "s26_bbh")
S28 = os.path.join(SPIKES, "s28_transfer_tasks")
S13 = os.path.join(SPIKES, "s13_box_grid")
LETTERS = "ABCDE"

# S28's HF coordinates, from s28_common.TASK_CFG, verbatim
HF = {"svamp": ("ChilleD/SVAMP", None, "test"),
      "aqua": ("deepmind/aqua_rat", "raw", "test"),
      "csqa": ("tau/commonsense_qa", None, "validation"),
      "arc": ("allenai/ai2_arc", "ARC-Challenge", "test")}


def _write_text(name, text):
    p = os.path.join(DATA, name)
    os.makedirs(DATA, exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    return p


def _write_rows(name, rws):
    p = os.path.join(DATA, name)
    os.makedirs(DATA, exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        for r in rws:
            f.write(json.dumps(r) + "\n")
    return p


def _read_rows(p):
    out = []
    with open(p, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


# ------------------------------------------------------------------ S28 row builders (verbatim)
def mc_input(question, labels, texts):
    """s28_download.mc_input, verbatim: the Wei et al. layout, lowercase option letters."""
    q = question.strip()
    opts = " ".join("(%s) %s" % (labels[i].lower(), texts[i].strip()) for i in range(len(labels)))
    return q + " Answer Choices: " + opts


def rows_svamp(d):
    out = []
    for i in range(len(d)):
        r = d[i]
        body = str(r.get("Body", r.get("body", ""))).strip()
        q = str(r.get("Question", r.get("question", ""))).strip()
        ans = r.get("Answer", r.get("answer"))
        try:
            f = float(ans)
            gold = str(int(f)) if abs(f - int(f)) < 1e-9 else repr(f)
        except Exception:                                     # noqa: BLE001
            gold = str(ans).strip()
        out.append({"input": (body + " " + q).strip(), "target": gold,
                    "options": [], "gold_text": ""})
    return out


def rows_aqua(d):
    out = []
    for i in range(len(d)):
        r = d[i]
        labels, texts = [], []
        for j, o in enumerate(list(r["options"])):
            o = str(o)
            if ")" in o[:3]:
                lab, txt = o.split(")", 1)
            else:
                lab, txt = LETTERS[j], o
            labels.append(lab.strip().upper())
            texts.append(txt.strip())
        gold = str(r["correct"]).strip().upper()
        gt = texts[labels.index(gold)] if gold in labels else ""
        out.append({"input": mc_input(r["question"], labels, texts), "target": gold,
                    "options": labels, "gold_text": gt})
    return out


def rows_choices(d, qkey="question"):
    out = []
    for i in range(len(d)):
        r = d[i]
        ch = r["choices"]
        labels = [str(x).strip().upper() for x in ch["label"]]
        texts = [str(x).strip() for x in ch["text"]]
        if not all(l in LETTERS for l in labels):
            m = {l: LETTERS[j] for j, l in enumerate(labels)}
            labels = [m[l] for l in labels]
        else:
            m = {l: l for l in labels}
        gold = m.get(str(r["answerKey"]).strip().upper(), str(r["answerKey"]).strip().upper())
        gt = texts[labels.index(gold)] if gold in labels else ""
        out.append({"input": mc_input(r[qkey], labels, texts), "target": gold,
                    "options": labels, "gold_text": gt})
    return out


# ------------------------------------------------------------------ copy
def do_copy():
    rep = {"mode": "copy", "notes": [], "files": {}}

    # --- GSM8K 4-shot prefix. s28_download.py wrote it from openai/gsm8k train rows 0-3 with S9a's
    # own format string, so prompts/svamp.txt IS the S9a GSM8K prefix; it is copied for both tasks.
    gsm_prefix = open(os.path.join(S28, "prompts", "svamp.txt"), encoding="utf-8").read()
    if not gsm_prefix.endswith("\n\n"):
        gsm_prefix = gsm_prefix.rstrip("\n") + "\n\n"
    _write_text("prompt_gsm8k.txt", gsm_prefix)
    _write_text("prompt_svamp.txt", gsm_prefix)
    rep["notes"].append("prompt_gsm8k.txt == prompt_svamp.txt == the S9a 4-shot GSM8K prefix "
                        "(s28_transfer_tasks/prompts/svamp.txt, written by s28_download.py from "
                        "openai/gsm8k train rows 0-3 with s9a_common's format string)")

    # --- MATH500 prefix, frozen (S13's math_shots() reads a dataset neither machine caches)
    mp = json.load(open(os.path.join(S13, "artifacts", "math500_prompt.json"), encoding="utf-8"))
    pref = mp["prefix_text"]
    if not pref.endswith("\n\n"):
        pref = pref.rstrip("\n") + "\n\n"
    _write_text("prompt_math500.txt", pref)
    rep["math500_shots_meta"] = mp.get("shots_meta")
    rep["math500_prefix_tokens_s13"] = mp.get("prefix_tokens")
    rep["notes"].append("prompt_math500.txt is the frozen prefix_text of "
                        "s13_box_grid/artifacts/math500_prompt.json (shots_meta %r); S13's "
                        "math_shots() would fall back to a different source offline"
                        % (mp.get("shots_meta"),))

    # --- S28 letter tasks. s28_common.task_prompt rstrips newlines then appends cfg["sep"];
    # the separator is applied by build_prompts, so the stored file is the rstripped exemplar block.
    for t in ("aqua", "csqa", "arc"):
        raw = open(os.path.join(S28, "prompts", "%s.txt" % t), encoding="utf-8").read()
        _write_text("prompt_%s.txt" % t, raw.rstrip("\n"))

    # --- BBH prompts: s26_common.task_prompt drops the canary line and the "-----" separator
    for name, cfg in TASKS.items():
        if "bbh_sub" not in cfg:
            continue
        raw = open(os.path.join(S26, "prompts", "%s.txt" % cfg["bbh_sub"]),
                   encoding="utf-8").read()
        _write_text("prompt_%s.txt" % name, "\n".join(raw.split("\n")[2:]).rstrip("\n"))
        _write_rows("rows_%s.jsonl" % name,
                    _read_rows(os.path.join(S26, "artifacts", "bbh_%s.jsonl" % cfg["bbh_sub"])))

    # --- S28 rows: AQuA is already the full split; the other three are 300-row prefixes
    for t in ("aqua", "svamp", "csqa", "arc"):
        rws = _read_rows(os.path.join(S28, "artifacts", "data_%s.jsonl" % t))
        _write_rows("rows_%s.jsonl" % t, rws)
        rep["files"]["rows_%s.jsonl" % t] = {"n": len(rws),
                                            "full": len(rws) >= TASKS[t]["n_full"]}

    _write_text("README_prompts.md", PROMPT_README)
    write_hashes(rep)
    return rep


def do_extend():
    """Rebuild the tasks whose spike file is a prefix of the full split. Needs the datasets cached
    (HF_HUB_OFFLINE=1 is honoured); never downloads a model and never uses a token."""
    rep = {"mode": "extend", "prefix_checks": {}, "files": {}, "notes": [], "errors": {}}
    from datasets import load_dataset

    only = [x.split("=", 1)[1].split(",") for x in sys.argv if x.startswith("--only=")]
    only = only[0] if only else None

    def wanted(t):
        return only is None or t in only

    if wanted("gsm8k"):
      try:
        # GSM8K test, dataset order (s9a/s13/s32 all use the dataset order)
        d = load_dataset("openai/gsm8k", "main", split="test")
        rws = [{"idx": i, "src_idx": i, "input": d[i]["question"],
                "target": d[i]["answer"].split("####")[-1].strip().replace(",", "")
                .replace("$", ""), "options": [], "gold_text": ""} for i in range(len(d))]
        _write_rows("rows_gsm8k.jsonl", rws)
        rep["files"]["rows_gsm8k.jsonl"] = {"n": len(rws)}
      except Exception as e:                                     # noqa: BLE001
        rep["errors"]["gsm8k"] = repr(e)[:300]

    if wanted("math500"):
      try:
        # MATH500 test, dataset order (s13/s32)
        d = load_dataset("HuggingFaceH4/MATH-500", split="test")
        rws = [{"idx": i, "src_idx": i, "input": d[i]["problem"], "target": d[i]["answer"],
                "options": [], "gold_text": "", "solution": d[i]["solution"],
                "subject": d[i].get("subject"), "level": d[i].get("level")}
               for i in range(len(d))]
        _write_rows("rows_math500.jsonl", rws)
        rep["files"]["rows_math500.jsonl"] = {"n": len(rws)}
      except Exception as e:                                     # noqa: BLE001
        rep["errors"]["math500"] = repr(e)[:300]

    # SVAMP / CSQA / ARC: shuffle(seed=20260908) over the FULL split, then assert the spike file
    # (300 rows) is a byte-identical prefix. AQuA is already full at 254.
    for t in ("svamp", "csqa", "arc"):
      if not wanted(t):
        continue
      try:
        repo, cfg, split = HF[t]
        d = load_dataset(repo, cfg, split=split) if cfg else load_dataset(repo, split=split)
        n_split = len(d)
        d = d.shuffle(seed=SPLIT_SEED)
        if t == "svamp":
            rws = rows_svamp(d)
        else:
            rws = rows_choices(d)
        for i, r in enumerate(rws):
            r["idx"] = i
            r["src_idx"] = i
        # the prefix reference is the frozen copy in data/ (written by --copy from the spike file),
        # so --extend needs no access to work/spikes and runs on the GPU host as well
        ref = os.path.join(DATA, "rows_%s.jsonl" % t)
        if not os.path.exists(ref):
            ref = os.path.join(S28, "artifacts", "data_%s.jsonl" % t)
        old = _read_rows(ref)
        if len(old) > len(rws):
            old = old[:len(rws)]
        rep["prefix_reference"] = rep.get("prefix_reference", {})
        rep["prefix_reference"][t] = ref
        same = all(rws[i]["input"] == old[i]["input"] and str(rws[i]["target"]) ==
                   str(old[i]["target"]) for i in range(len(old)))
        rep["prefix_checks"][t] = {"n_spike": len(old), "n_full": len(rws), "n_split": n_split,
                                   "spike_is_prefix": bool(same)}
        if not same:
            first = next(i for i in range(len(old)) if rws[i]["input"] != old[i]["input"]
                         or str(rws[i]["target"]) != str(old[i]["target"]))
            rep["prefix_checks"][t]["first_mismatch_row"] = first
            rep["notes"].append("%s: shuffle(seed=%d) does NOT reproduce the spike prefix "
                                "(first mismatch at row %d); rows_%s.jsonl NOT replaced"
                                % (t, SPLIT_SEED, first, t))
            continue
        _write_rows("rows_%s.jsonl" % t, rws)
        rep["files"]["rows_%s.jsonl" % t] = {"n": len(rws)}
      except Exception as e:                                     # noqa: BLE001
        rep["errors"][t] = repr(e)[:300]

    # AQuA: the spike file is the whole split already; confirm the count
    aqua = _read_rows(os.path.join(DATA, "rows_aqua.jsonl"))
    rep["prefix_checks"]["aqua"] = {"n_spike": len(aqua), "n_full": len(aqua),
                                    "spike_is_prefix": True}
    write_hashes(rep)
    return rep


def sources():
    """data/sources.json: the Hub repo, config, split and revision each PP3 row file was built
    from, plus the exemplar provenance of each prompt file (decision 3)."""
    return load_json(os.path.join(DATA, "sources.json"), {})


SOURCES = sources()


def write_hashes(rep=None):
    h = {}
    for fn in sorted(os.listdir(DATA)):
        # model_revisions.json is install OUTPUT (prod/install_models.py), not frozen data: it is
        # rewritten on every install and must not make `--verify` fail.
        if fn in ("hashes.json", "freeze_report.json", "model_revisions.json"):
            continue
        p = os.path.join(DATA, fn)
        if os.path.isfile(p):
            h[fn] = {"sha256": sha256_file(p), "bytes": os.path.getsize(p)}
            if fn.startswith("rows_"):
                h[fn]["rows"] = sum(1 for _ in open(p, encoding="utf-8"))
            src = SOURCES.get(fn) or SOURCES.get(fn.replace("rows_", "").replace(".jsonl", ""))
            if src:
                # PP3 decision 3: the Hub repo and REVISION each row file was built from travel
                # with the hash, so a frozen file can be rebuilt from its source exactly.
                h[fn]["hub"] = {k: src.get(k) for k in ("repo", "config", "split", "revision")}
    save_json(os.path.join(DATA, "hashes.json"), h)
    if rep is not None:
        rep["hashes"] = h
    return h


def do_verify():
    stored = load_json(os.path.join(DATA, "hashes.json"), {})
    bad = {}
    for fn, rec in stored.items():
        p = os.path.join(DATA, fn)
        if not os.path.exists(p):
            bad[fn] = "missing"
        elif sha256_file(p) != rec["sha256"]:
            bad[fn] = "sha256 changed"
    missing_tasks, missing_prompts = [], []
    for t in TASK_ORDER:
        if not os.path.exists(os.path.join(DATA, task_cfg(t)["rows_file"])):
            missing_tasks.append(t)
            continue
        # PP3: pooled BBH and MMLU name an exemplar file PER ROW (`prefix_key`); a task with
        # per_row_prefix has no single prompt_file and every key its rows name must exist.
        for key in prefix_keys(t):
            if key is None:
                missing_prompts.append("%s: no prompt file" % t)
            elif not os.path.exists(os.path.join(DATA, key if key.endswith(".txt")
                                                 else "prompt_%s.txt" % key)):
                missing_prompts.append("%s: prompt_%s.txt" % (t, key))
    short = {}
    for t in TASK_ORDER:
        p = os.path.join(DATA, task_cfg(t)["rows_file"])
        if os.path.exists(p):
            n = sum(1 for _ in open(p, encoding="utf-8"))
            if n < task_cfg(t)["n_full"]:
                short[t] = {"have": n, "want": task_cfg(t)["n_full"]}
    src = sources()
    no_source = [t for t in ("strategyqa", "bbh", "mmlu", "hellaswag") if t not in src]
    return {"mode": "verify", "n_files": len(stored), "mismatches": bad,
            "tasks_missing_files": missing_tasks, "prompt_files_missing": missing_prompts,
            "tasks_short_of_full_N": short, "sources_recorded": sorted(src.keys()),
            "sources_missing": no_source,
            "ok": not bad and not missing_tasks and not missing_prompts and not short
            and not no_source}


PROMPT_README = """# Provenance of every file in prod/tasks/data/

Written by `prod/tasks/freeze.py`. Nothing here is authored by the production package; each file is
copied from the spike that measured it, and `hashes.json` records the sha256 of each one.

| file | source | note |
|---|---|---|
| prompt_gsm8k.txt | s28_transfer_tasks/prompts/svamp.txt | the S9a 4-shot GSM8K prefix, written by s28_download.py from openai/gsm8k train rows 0-3 with s9a_common's own format string |
| prompt_svamp.txt | same file | S28 uses the GSM8K prefix for SVAMP by design |
| prompt_math500.txt | s13_box_grid/artifacts/math500_prompt.json ("prefix_text") | frozen because S13's math_shots() reads EleutherAI/hendrycks_math (config algebra), which is not cached on either machine and would silently fall back to a different source |
| prompt_aqua.txt, prompt_csqa.txt | s28_transfer_tasks/prompts/*.txt | Wei et al. 2022 CoT exemplars |
| prompt_arc.txt | s28_transfer_tasks/prompts/arc.txt | THREE AGENT-WRITTEN exemplars in the BBH style (not from a published prompt set); labelled as such wherever ARC numbers appear |
| prompt_bbh_*.txt | s26_bbh/prompts/*.txt | the official BIG-Bench-Hard cot prompt with the canary line and the "-----" separator dropped, which is what the BBH repo's own evaluation does |
| rows_bbh_*.jsonl | s26_bbh/artifacts/bbh_*.jsonl | 250 rows = the whole BBH task |
| rows_aqua.jsonl | s28_transfer_tasks/artifacts/data_aqua.jsonl | 254 rows = the whole test split |
| rows_svamp.jsonl, rows_csqa.jsonl, rows_arc.jsonl | s28 spike file (300 rows), replaced at `--extend` by the full split | built by `load_dataset(...).shuffle(seed=20260908)`, s28_download.py's own selection rule, with the spike file asserted to be a byte-identical prefix |
| rows_gsm8k.jsonl, rows_math500.jsonl | datasets, dataset order | written at `--extend` |
"""


if __name__ == "__main__":
    what = [a for a in sys.argv[1:] if a.startswith("--")] or ["--verify"]
    out = {}
    if "--rehash" in what:
        out["rehash"] = {"files": len(write_hashes())}
    if "--sources" in what:
        out["sources"] = sources()
    if "--copy" in what:
        out["copy"] = do_copy()
    if "--extend" in what:
        out["extend"] = do_extend()
    if "--verify" in what or True:
        out["verify"] = do_verify()
    save_json(os.path.join(DATA, "freeze_report.json"), out)
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "hashes"}
                      for k, v in out.items()}, indent=2, default=str))
    if not out["verify"].get("ok"):
        sys.exit(1)
