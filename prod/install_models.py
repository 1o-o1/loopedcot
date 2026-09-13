"""Fetch the six checkpoints from the Hugging Face Hub and pin their revisions (Brief PP3, dec. 3).

  python -m prod.install_models                 # resolve, download, pin, write model_revisions.json
  python -m prod.install_models --resolve-only  # resolve and write the pins, download nothing
  python -m prod.install_models --verify        # re-check the pinned revisions against the cache
  python -m prod.install_models --models=ouro_1_4b_base,huginn_0125

This replaces every step that transferred a cache from the Spark. All six repos are PUBLIC and no
token is used or accepted: `HF_TOKEN` and friends are cleared for the duration of the call, so an
install can never silently depend on someone's credentials.

  ByteDance/Ouro-1.4B                                   trust_remote_code at LOAD time
  ByteDance/Ouro-1.4B-Thinking                          trust_remote_code at LOAD time
  ByteDance/Ouro-2.6B                                   trust_remote_code at LOAD time
  ByteDance/Ouro-2.6B-Thinking                          trust_remote_code at LOAD time
  tomg-group-umd/huginn-0125
  smcleish/Recurrent-Llama-3.2-train-recurrence-32

`trust_remote_code` is a flag on `from_pretrained`, not on the download: the Ouro modelling files are
ordinary files in the repo and `snapshot_download` brings them in with everything else, so the
install itself executes no repository code.

What is written to `prod/tasks/data/model_revisions.json`:
  {"resolved_at": ..., "transformers_pin": "4.56.2",
   "models": {"<name>": {"repo", "revision", "params", "dtype", "bytes", "n_files",
                         "shapes": {kv_heads, head_dim, layers|prelude/core/coda, entries, params},
                         "local_dir", "verified"}}}
`prod/config.py:shapes_for` prefers this file over its static table, so the launcher's memory
estimate is derived from the checkpoints that are actually installed.

After this runs, the run itself is offline: `HF_HUB_OFFLINE=1` (prod/common.py sets it by default).
"""
import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prod import config as cfgmod                                    # noqa: E402
from prod.common import DATA, save_json, load_json                   # noqa: E402

REVISIONS_FILE = os.path.join(DATA, "model_revisions.json")
TRANSFORMERS_PIN = "4.56.2"
TRUST_REMOTE_CODE = {"ouro_1_4b_base", "ouro_1_4b_think", "ouro_2_6b_base", "ouro_2_6b_think"}

#: never fetch the optimiser states or the duplicate formats; the load path wants safetensors.
IGNORE = ["*.pt", "*.bin", "*.msgpack", "*.h5", "*.onnx", "optimizer*", "*.pth"]


def _no_token_env():
    """Clear every token variable for this process (the brief: no token, all repos public)."""
    for v in ("HF_TOKEN", "HUGGING_FACE_HUB_TOKEN", "HUGGINGFACEHUB_API_TOKEN"):
        os.environ.pop(v, None)
    os.environ["HF_HUB_OFFLINE"] = "0"          # the install is the ONE online step


def resolve(models=None):
    """The revision sha, parameter count and dtype of each repo, from the Hub."""
    from huggingface_hub import HfApi
    api = HfApi()
    out = {}
    for name in (models or cfgmod.MODEL_ORDER):
        spec = cfgmod.MODEL_SHAPES[name]
        info = api.model_info(spec["repo"], token=False)
        st = getattr(info, "safetensors", None)
        params = int(st.total) if st and st.total else int(spec["params"])
        dtypes = dict(st.parameters) if st and st.parameters else {}
        out[name] = {"repo": spec["repo"], "revision": info.sha, "params": params,
                     "stored_dtypes": dtypes,
                     "trust_remote_code": name in TRUST_REMOTE_CODE,
                     "shapes": {k: v for k, v in spec.items() if k != "repo"}}
        out[name]["shapes"]["params"] = params
        print("  %-22s %s  rev %s  %.2fB params %s"
              % (name, spec["repo"], info.sha[:12], params / 1e9,
                 ",".join(dtypes) or "?"), flush=True)
    return out


def download(entry, name):
    from huggingface_hub import snapshot_download
    t0 = time.time()
    d = snapshot_download(entry["repo"], revision=entry["revision"], token=False,
                          ignore_patterns=IGNORE)
    nb, nf = 0, 0
    for base, _dirs, files in os.walk(d):
        for fn in files:
            try:
                nb += os.path.getsize(os.path.join(base, fn))
            except OSError:
                continue
            nf += 1
    # snapshot_download(revision=<sha>) does NOT write refs/main, and `from_pretrained(repo)` under
    # HF_HUB_OFFLINE=1 resolves the revision "main" through exactly that file -- so a pinned-only
    # install downloads 2.7 GB and then fails to load offline ("couldn't connect ... and couldn't
    # find them in the cached files"). Found on the laptop, 2026-09-13. Pointing refs/main at the
    # pin is the honest local meaning of a pinned install: on this machine, main IS the pin.
    refs = os.path.join(os.path.dirname(os.path.dirname(d)), "refs")
    try:
        os.makedirs(refs, exist_ok=True)
        with open(os.path.join(refs, "main"), "w", encoding="utf-8") as f:
            f.write(entry["revision"])
        entry["refs_main_written"] = True
    except OSError as e:                                      # noqa: BLE001
        entry["refs_main_written"] = "failed: %r" % (e,)
    entry.update({"local_dir": d, "bytes": nb, "n_files": nf,
                  "download_seconds": round(time.time() - t0, 1)})
    print("  %-22s %.2f GB in %d files -> %s [%.0fs]"
          % (name, nb / 1024 ** 3, nf, d, entry["download_seconds"]), flush=True)
    return entry


def shapes_from_config(entry):
    """Re-derive the memory-estimate shapes from the DOWNLOADED config.json, not from the table."""
    p = os.path.join(entry.get("local_dir") or "", "config.json")
    if not os.path.exists(p):
        return entry["shapes"]
    c = load_json(p, {})
    s = dict(entry["shapes"])
    if "num_hidden_layers" in c:                      # Ouro
        s.update({"kv_heads": int(c.get("num_key_value_heads", s["kv_heads"])),
                  "head_dim": int(c.get("head_dim") or
                                  c["hidden_size"] // c["num_attention_heads"]),
                  "layers": int(c["num_hidden_layers"]), "entries": "ouro"})
    elif "n_layers_in_recurrent_block" in c:          # raven (Huginn, McLeish)
        s.update({"kv_heads": int(c.get("num_key_value_heads", s["kv_heads"])),
                  "head_dim": int(c.get("head_dim") or c["n_embd"] // c["n_heads"]),
                  "prelude": int(c["n_layers_in_prelude"]),
                  "core": int(c["n_layers_in_recurrent_block"]),
                  "coda": int(c["n_layers_in_coda"]), "entries": "raven"})
    s["dtype_bytes"] = 2                               # every adapter loads in bf16
    return s


def verify(doc):
    """Re-resolve each pin and re-check that the local snapshot is there."""
    from huggingface_hub import HfApi
    api = HfApi()
    ok, notes = True, {}
    for name, e in doc["models"].items():
        try:
            live = api.model_info(e["repo"], token=False).sha
        except Exception as ex:                       # noqa: BLE001
            notes[name] = "hub unreachable: %r" % (ex,)
            live = None
        present = bool(e.get("local_dir")) and os.path.exists(
            os.path.join(e["local_dir"], "config.json"))
        e["verified"] = bool(present and (live is None or live == e["revision"]))
        if live and live != e["revision"]:
            notes[name] = ("the repo has MOVED since the pin: %s -> %s (the pin is what the run "
                           "uses; re-install deliberately if you want the new one)"
                           % (e["revision"][:12], live[:12]))
        if not present:
            notes[name] = notes.get(name, "") + " local snapshot missing"
        ok = ok and e["verified"]
    doc["verify_ok"] = ok
    doc["verify_notes"] = notes
    return doc


def main(argv=None):
    p = argparse.ArgumentParser(prog="prod.install_models")
    p.add_argument("--models", default=None)
    p.add_argument("--resolve-only", dest="resolve_only", action="store_true")
    p.add_argument("--verify", action="store_true")
    p.add_argument("--out", default=REVISIONS_FILE)
    a = p.parse_args(argv)
    models = [x.strip() for x in a.models.split(",")] if a.models else None

    if a.verify:
        doc = load_json(a.out, {})
        if not doc:
            raise SystemExit("no pins at %s; run `python -m prod.install_models` first" % a.out)
        _no_token_env()
        doc = verify(doc)
        save_json(a.out, doc)
        print(json.dumps({"verify_ok": doc["verify_ok"], "notes": doc["verify_notes"]}, indent=2))
        return doc

    _no_token_env()
    print("[install] resolving revisions from the Hub (public repos, no token)", flush=True)
    ent = resolve(models)
    if not a.resolve_only:
        print("[install] downloading at the pinned revisions", flush=True)
        for name, e in ent.items():
            download(e, name)
            e["shapes"] = shapes_from_config(e)
    doc = load_json(a.out, {"models": {}})
    doc.setdefault("models", {}).update(ent)
    doc.update({"resolved_at": time.strftime("%FT%T"), "transformers_pin": TRANSFORMERS_PIN,
                "source": "huggingface hub, public, no token",
                "offline_after_install": True})
    doc = verify(doc) if not a.resolve_only else doc
    save_json(a.out, doc)
    print("[install] wrote %s (%d models, verify_ok=%s)"
          % (a.out, len(doc["models"]), doc.get("verify_ok")), flush=True)
    os.environ["HF_HUB_OFFLINE"] = "1"
    return doc


if __name__ == "__main__":
    main()
