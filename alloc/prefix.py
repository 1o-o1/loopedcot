"""Prefix-cached pricing: the third accounting of a grid.

The few-shot exemplar block in front of a question is byte-identical for every question that shares
it, so a server holding a prefix cache computes it once and every query after the first pays only
for its own prompt tokens. That is a third price for the same cells, beside the two the package
already has:

    prompt-free      (L_fixed + k L)(E_cal[min(len_k,T)] + R_i)
    PREFIX-CACHED    (L_fixed + k L)(P_i - S_i + E_cal[min(len_k,T)] + R_i)
    prompt-inclusive (L_fixed + k L)(P_i + E_cal[min(len_k,T)] + R_i)

`S_i` is the longest common TOKEN prefix among the questions that carry question `i`'s exemplar
block, measured by rebuilding the prompts with the package's own builder and tokenising them with
the checkpoint's own pinned tokenizer. A cache is keyed on the text it holds, not on the task slot,
so the block and not the task is the unit: a task whose questions all share one block gets one
value, and a pooled task (BBH's ten subtasks, MMLU's four subjects) gets one value per subtask.

`with_prefix_cached` returns a COPY of the grid with the two prompt-token arrays reduced, so the
prompt-inclusive price of that copy IS the prefix-cached price of the original, and the default cost
-- and therefore every budget X = f * default_cost -- re-anchors under the same accounting. The
one-off cost of FILLING the cache (one entry per block and depth) is not inside these prices.

Only `numpy` is imported at module level. The prompt builder and the frozen task rows live outside
this directory and are imported inside the two functions that need them, so the rest of the package
keeps its numpy-only import surface.
"""
import copy
import glob
import json
import os

import numpy as np


def common_prefix_len(seqs):
    """The length of the longest common token prefix of a list of token-id lists."""
    if not seqs:
        return 0
    m = min(len(s) for s in seqs)
    first = seqs[0]
    for j in range(m):
        v = first[j]
        for s in seqs:
            if s[j] != v:
                return j
    return m


def run_prompt_settings(cells_dir, checkpoint, task, protocol="natural"):
    """The prompt shape the RUN recorded, read from its own meta files beside the cells.

    Nothing here is assumed: `add_special_tokens` and `chat_template` are the two arguments the
    generation pass handed the prompt builder and the encode, and `tag_loops` / `tag_tokens` say
    whether a control line was spliced between the exemplars and the question -- a prompt the
    builder alone would not rebuild, so such a grid is refused rather than mismeasured. Every depth
    file of the pair must agree, or this raises.
    """
    pat = os.path.join(cells_dir, "meta_%s_%s_%s_k*.json" % (checkpoint, task, protocol))
    got = sorted(glob.glob(pat))
    if not got:
        raise FileNotFoundError(
            "no run meta files for %s/%s (%s) under %s: the prefix cannot be measured without the "
            "prompt settings the run used" % (checkpoint, task, protocol, cells_dir))
    seen = set()
    for p in got:
        with open(p, encoding="utf-8") as fh:
            m = json.load(fh)
        mm = m.get("model_meta") or {}
        seen.add((bool(m.get("add_special_tokens")), bool(mm.get("chat_template")),
                  bool(m.get("tag_loops")), bool(m.get("tag_tokens")),
                  bool((m.get("config") or {}).get("think_tag_is_stop", True))))
    if len(seen) != 1:
        raise ValueError("%s/%s: the run meta files disagree on the prompt settings: %s"
                         % (checkpoint, task, sorted(seen)))
    ast, chat, tag_loops, tag_tokens, tstop = seen.pop()
    if tag_loops or tag_tokens:
        raise ValueError("%s/%s: the run spliced a control line into the prompt (tag_loops=%s, "
                         "tag_tokens=%s), which the prompt builder alone does not rebuild"
                         % (checkpoint, task, tag_loops, tag_tokens))
    return {"add_special_tokens": ast, "chat_template": chat, "think_tag_is_stop": tstop,
            "meta_files": [os.path.basename(p) for p in got]}


def tokenizer_for(checkpoint):
    """The checkpoint's own tokenizer at the revision that was installed, from the local cache.

    The revision is pinned, so the tokenisation is the one the grid was generated under and the
    rebuilt token counts can be checked against the stored `n_prompt_tokens`. Nothing is downloaded.
    """
    from transformers import AutoTokenizer
    from prod import config as prod_config
    path = os.path.join(os.path.dirname(os.path.abspath(prod_config.__file__)),
                        "tasks", "data", "model_revisions.json")
    with open(path, encoding="utf-8") as fh:
        spec = (json.load(fh).get("models") or {}).get(checkpoint)
    if not spec:
        raise KeyError("%s has no installed revision in %s" % (checkpoint, path))
    tok = AutoTokenizer.from_pretrained(spec["repo"], revision=spec.get("revision"),
                                        trust_remote_code=bool(spec.get("trust_remote_code")),
                                        local_files_only=True)
    return tok, {"repo": spec["repo"], "revision": spec.get("revision"),
                 "tokenizer_class": type(tok).__name__}


def prompt_token_ids(cells, tokenizer, chat_template=False, add_special_tokens=False,
                     think_tag_is_stop=True):
    """Rebuild and tokenise every prompt of a grid; return (token ids, block key) per question.

    The order is `cells.idx`, so the two lists line up with every per-question array on the grid.
    The prompts come from the package's own builder over the frozen task rows, which is what makes
    the rebuilt count comparable with the stored `n_prompt_tokens`.
    """
    from prod.tasks import build_prompts, rows as task_rows
    all_rows = {int(r["idx"]): r for r in task_rows(cells.task)}
    rws = [all_rows[int(i)] for i in cells.idx]
    prompts, _suffix, _stops, _eos, _extra = build_prompts(
        tokenizer, cells.task, rws, chat_template=bool(chat_template),
        think_tag_is_stop=bool(think_tag_is_stop))
    enc = [tokenizer(p, add_special_tokens=bool(add_special_tokens))["input_ids"] for p in prompts]
    keys = [(r.get("prefix_key") or "default") for r in rws]
    return enc, keys


def shared_prefix(cells, tokenizer, chat_template=False, add_special_tokens=False,
                  think_tag_is_stop=True):
    """Return S per question: the shared prefix of the block that question's prompt carries.

    Questions sharing an exemplar block share a cache entry, so they share one value; a grid whose
    questions all carry one block gets one value repeated. The result is capped at each prompt's own
    length, which only binds if a block were longer than a prompt that carries it.
    """
    enc, keys = prompt_token_ids(cells, tokenizer, chat_template=chat_template,
                                 add_special_tokens=add_special_tokens,
                                 think_tag_is_stop=think_tag_is_stop)
    if len(enc) != len(cells.idx):
        raise ValueError("%s/%s: rebuilt %d prompts for %d questions"
                         % (cells.name, cells.task, len(enc), len(cells.idx)))
    by_key = {}
    for i, k in enumerate(keys):
        by_key.setdefault(k, []).append(enc[i])
    per_key = {k: common_prefix_len(v) for k, v in by_key.items()}
    return np.array([min(per_key[k], len(enc[i])) for i, k in enumerate(keys)], float)


def with_prefix_cached(cells, shared):
    """A COPY of `cells` priced as if the shared prefix were already in the server's cache.

    Two arrays are replaced and nothing else is touched:
      ptok   -> ptok - S          the only prompt-token array a pricing function reads
                                  (policy.Cost, under `cap` and `expected` alike)
      passes -> passes - w_k S    the realised prompt-inclusive layer passes, read by
                                  evaluate.default_cost, so the default cost and every budget
                                  X = f * default_cost re-anchor under this same accounting.
    `passes_pf` is the prompt-free field and is left alone, so a prefix-cached grid must be priced
    prompt-inclusive: that is what the price above says. The original object is not modified.

    `shared` is one number for the whole grid or one per QUESTION in the order of `cells.idx`; the
    per-question form broadcasts along the prompt axis. The copy carries it as
    `prefix_shared_tokens`.
    """
    s = np.asarray(shared, float)
    if s.ndim == 0:
        s = np.full(len(cells.idx), float(s))
    if s.shape != (len(cells.idx),):
        raise ValueError("%s/%s: the shared prefix must be a scalar or one value per question "
                         "(%d), got %s" % (cells.name, cells.task, len(cells.idx), s.shape))
    if np.nanmin(s) < 0:
        raise ValueError("the shared prefix must not be negative: min %g" % float(np.nanmin(s)))
    out = copy.copy(cells)
    out.ptok = np.asarray(cells.ptok, float) - s
    if np.nanmin(out.ptok) < 0:
        raise ValueError("%s/%s: the shared prefix exceeds a prompt's own length (worst %g tokens)"
                         % (cells.name, cells.task, float(np.nanmin(out.ptok))))
    w = np.array([cells.L_fixed + int(k) * cells.L for k in cells.ks], float).reshape(-1, 1, 1)
    out.passes = np.asarray(cells.passes, float) - w * s.reshape(1, 1, -1)
    out.prefix_shared_tokens = s
    return out
