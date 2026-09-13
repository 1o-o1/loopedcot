"""Cost accounting, four ways (the compute reporting rule of record, 2026-09-05).

  python -m prod.cost --models=all [--P=800 --T=512] [--old] [--out=FILE]
  python -m prod.cost --cells=DIR --model=... --task=...     # per-cell, from the stored rows

1. LAYER-TOKEN PASSES, the primary unit within a family:
     Ouro    k * L * (P + T + R)
     raven   (prelude + k * core + coda) * (P + T + R)
   prompt-inclusive and prompt-free, both stored per row by generate.py.

2. FLOPs by the T5 formula (PLAN.md line 952, verbatim):
     FLOPs per question = 2 * N_nonembed * k * (P + T + R)
                        + k * [attention quadratic term over FULL-ATTENTION layers only]
                        + 2 * V * d * (T + R)                  (output head once per generated token)
   with the quadratic term the MEAN OVER PROBLEMS of (P + T)^2, not the square of the mean; suffix
   and answer tokens counted as generated; prefill and decode stored separately.
   The four defects this corrects, from KB09-09 section 1 (S27): attention not multiplied by k for a
   looped model, dense attention assumed for hybrid models, the square of the mean length, suffix
   tokens excluded. `--old` also prints S27's original formula so G4 can show the old-vs-new table.

3. WALL CLOCK on one fixed GPU for one fixed cell per model: `generate.py` records
   `generate_seconds` and `tokens_per_s` per pass; `wall_clock_table` collects them.

4. KV MEMORY per token: k * L layer-KVs for Ouro, passes_per_token(k) step slots for raven;
   `adapter.kv_bytes_per_token(k)` is the single definition and `cost.py` only reports it.
"""
import argparse
import os

import numpy as np

from .common import load_json, save_json

# ------------------------------------------------------------------ model shapes
# Read from each checkpoint's config so nothing is typed twice. `n_full_attention_layers` matters
# only for the dense references (Gemma 4 sliding window, Qwen3.5 hybrid layers); the three looped
# families run full attention in every layer.
LOOPED = {
    "ouro_1_4b_base": {"repo": "ByteDance/Ouro-1.4B", "family": "ouro"},
    "ouro_1_4b_think": {"repo": "ByteDance/Ouro-1.4B-Thinking", "family": "ouro"},
    "ouro_2_6b_base": {"repo": "ByteDance/Ouro-2.6B", "family": "ouro"},
    "ouro_2_6b_think": {"repo": "ByteDance/Ouro-2.6B-Thinking", "family": "ouro"},
    "huginn_0125": {"repo": "tomg-group-umd/huginn-0125", "family": "raven"},
    "mcleish_llama32_r32": {"repo": "smcleish/Recurrent-Llama-3.2-train-recurrence-32",
                            "family": "raven"},
}


def ouro_nonembed_from_config(cfg):
    """s27_flops.py's Ouro branch, verbatim: non-embedding parameters from config arithmetic (no
    GPU, no state dict). Per layer: q, k, v, o projections + 3 * d * ffn + 2 * d (the two norms)."""
    d, L, ff = cfg.hidden_size, cfg.num_hidden_layers, cfg.intermediate_size
    hd = getattr(cfg, "head_dim", d // cfg.num_attention_heads)
    nq, nkv = cfg.num_attention_heads, cfg.num_key_value_heads
    per_layer = (d * nq * hd + 2 * d * nkv * hd + nq * hd * d) + 3 * d * ff + 2 * d
    return int(L * per_layer + d), int(per_layer)


def raven_shapes(cfg):
    """Huginn / McLeish: the recurrent block is executed k times, the prelude and coda once, so the
    parameter count that multiplies by k is the CORE block's, not the whole model's."""
    d, ff = cfg.n_embd, cfg.intermediate_size
    nq, nkv = cfg.num_attention_heads, cfg.num_key_value_heads
    hd = d // nq
    # SandwichBlock: attention (q,k,v,o) + GatedMLP (fc -> 2 * intermediate, proj) + 4 norms
    per_layer = (d * nq * hd + 2 * d * nkv * hd + nq * hd * d) + (d * 2 * ff + ff * d) + 4 * d
    return {"per_layer": int(per_layer),
            "prelude": int(cfg.n_layers_in_prelude), "core": int(cfg.n_layers_in_recurrent_block),
            "coda": int(cfg.n_layers_in_coda), "d_model": int(d),
            "vocab_size": int(cfg.vocab_size), "n_heads": int(nq), "n_kv_heads": int(nkv),
            "head_dim": int(hd)}


def model_shapes(name):
    from transformers import AutoConfig
    spec = LOOPED[name]
    cfg = AutoConfig.from_pretrained(spec["repo"], trust_remote_code=True)
    if spec["family"] == "ouro":
        nonembed, per_layer = ouro_nonembed_from_config(cfg)
        return {"model": name, "repo": spec["repo"], "family": "ouro",
                "n_layers": int(cfg.num_hidden_layers), "d_model": int(cfg.hidden_size),
                "vocab_size": int(cfg.vocab_size), "intermediate_size": int(cfg.intermediate_size),
                "n_heads": int(cfg.num_attention_heads),
                "n_kv_heads": int(cfg.num_key_value_heads),
                "head_dim": int(getattr(cfg, "head_dim",
                                        cfg.hidden_size // cfg.num_attention_heads)),
                "n_nonembed": nonembed, "per_layer_params": per_layer,
                "n_nonembed_per_loop": nonembed,          # every layer is inside the loop
                "n_full_attention_layers": int(cfg.num_hidden_layers),
                "layers_per_loop": int(cfg.num_hidden_layers), "layers_fixed": 0}
    sh = raven_shapes(cfg)
    total_layers = sh["prelude"] + sh["core"] + sh["coda"]
    return {"model": name, "repo": spec["repo"], "family": "raven",
            "n_layers": total_layers, "d_model": sh["d_model"], "vocab_size": sh["vocab_size"],
            "intermediate_size": int(cfg.intermediate_size), "n_heads": sh["n_heads"],
            "n_kv_heads": sh["n_kv_heads"], "head_dim": sh["head_dim"],
            "per_layer_params": sh["per_layer"],
            "n_nonembed": int(total_layers * sh["per_layer"]),
            "n_nonembed_per_loop": int(sh["core"] * sh["per_layer"]),
            "n_nonembed_fixed": int((sh["prelude"] + sh["coda"]) * sh["per_layer"]),
            "n_full_attention_layers": total_layers,
            "layers_per_loop": sh["core"], "layers_fixed": sh["prelude"] + sh["coda"],
            "mean_recurrence": int(getattr(cfg, "mean_recurrence", 0))}


# ------------------------------------------------------------------ layer-token passes
def layer_passes(sh, k, n_tokens):
    """The primary unit. Ouro: k * L * tokens. raven: (prelude + k * core + coda) * tokens."""
    return int((sh["layers_fixed"] + int(k) * sh["layers_per_loop"]) * int(n_tokens))


def kv_bytes_per_token(sh, k, itemsize=2):
    """2 (K, V) * kv heads * head_dim * itemsize * (layer passes per token)."""
    ppt = sh["layers_fixed"] + int(k) * sh["layers_per_loop"]
    return int(2 * sh["n_kv_heads"] * sh["head_dim"] * itemsize * ppt)


# ------------------------------------------------------------------ FLOPs, T5
def flops_t5(sh, k, P, T, R=0.0, sq_lengths=None, attn_layers=None, split=False):
    """PLAN.md T5, verbatim.

    P  prompt tokens, T generated trace tokens, R suffix + answer tokens (counted as generated).
    sq_lengths: the MEAN OVER PROBLEMS of (P + T)^2. When None it falls back to (P + T)^2, which is
                the square of the mean -- one of the four defects T5 fixes -- and the return value is
                flagged `mean_of_squares: False`.
    attn_layers: the number of FULL-ATTENTION layers the quadratic term runs over; defaults to the
                model's own count (all layers for the three looped families).
    """
    S = float(P) + float(T) + float(R)
    gen = float(T) + float(R)
    La = sh["n_full_attention_layers"] if attn_layers is None else int(attn_layers)
    # matmul term: the fixed layers once, the loop layers k times
    mm = 2.0 * (sh.get("n_nonembed_fixed", 0) + int(k) * sh["n_nonembed_per_loop"]) * S
    sq = (float(P) + float(T)) ** 2 if sq_lengths is None else float(sq_lengths)
    # the quadratic term carries k because a looped model re-runs attention on every loop; the
    # fixed layers carry it once.
    attn_loop = 4.0 * (La - sh["layers_fixed"]) * sh["d_model"] * sq / 2.0 * int(k)
    attn_fixed = 4.0 * sh["layers_fixed"] * sh["d_model"] * sq / 2.0
    head = 2.0 * sh["vocab_size"] * sh["d_model"] * gen
    out = {"flops": mm + attn_loop + attn_fixed + head, "matmul": mm,
           "attention": attn_loop + attn_fixed, "output_head": head,
           "mean_of_squares": sq_lengths is not None, "k": int(k), "P": float(P), "T": float(T),
           "R": float(R), "attn_layers": La}
    if split:
        # prefill = the prompt pass; decode = every generated token's pass
        out["flops_prefill"] = (2.0 * (sh.get("n_nonembed_fixed", 0)
                                       + int(k) * sh["n_nonembed_per_loop"]) * float(P)
                                + attn_loop + attn_fixed)
        out["flops_decode"] = out["flops"] - out["flops_prefill"]
    return out


def flops_s27_old(n_nonembed, n_layers, d_model, P, T, k=1, attn_layers=None,
                  attn_scaled_by_k=False):
    """s27_common.flops_per_problem, VERBATIM, kept only so G4 can print the old-vs-new table.

        2 * N_nonembed * k * S + 4 * L * d_model * S^2 / 2,  S = P + T
    """
    S = float(P) + float(T)
    L = n_layers if attn_layers is None else attn_layers
    if attn_scaled_by_k:
        L = L * k
    return 2.0 * n_nonembed * k * S + 4.0 * L * d_model * S * S / 2.0


# ------------------------------------------------------------------ per-cell costs from rows
def cell_costs(cells, sh, caps=None):
    """Per (k, B) cost of a measured grid, using each problem's own P, T and reserve.

    Returns layer passes (prompt-inclusive and prompt-free), FLOPs with the mean of squared lengths,
    and KV bytes per token, all averaged over the problems of the grid.
    """
    ks, Bs = cells.ks, (caps or cells.Bs)
    bi = {b: i for i, b in enumerate(cells.Bs)}
    out = {"ks": ks, "Bs": list(Bs), "layer_passes": [], "layer_passes_promptfree": [],
           "flops": [], "flops_prefill": [], "flops_decode": [], "kv_bytes_per_token": []}
    for a, k in enumerate(ks):
        rowlp, rowpf, rowfl, rowpre, rowdec = [], [], [], [], []
        for b in Bs:
            j = bi[b]
            P = cells.ptok
            R = cells.reserve
            T = np.nan_to_num(cells.ncut[a, j], nan=0.0)
            rowlp.append(float(np.nanmean(cells.passes[a, j])))
            rowpf.append(float(np.nanmean(cells.passes_pf[a, j])))
            sq = float(np.nanmean((P + T) ** 2))
            f = flops_t5(sh, k, float(np.nanmean(P)), float(np.nanmean(T)),
                         float(np.nanmean(R)), sq_lengths=sq, split=True)
            rowfl.append(f["flops"])
            rowpre.append(f["flops_prefill"])
            rowdec.append(f["flops_decode"])
        out["layer_passes"].append(rowlp)
        out["layer_passes_promptfree"].append(rowpf)
        out["flops"].append(rowfl)
        out["flops_prefill"].append(rowpre)
        out["flops_decode"].append(rowdec)
        out["kv_bytes_per_token"].append(kv_bytes_per_token(sh, k))
    return out


def wall_clock_table(art_dir):
    """Collect `tokens_per_s` and `generate_seconds` from every run meta in `art_dir`.

    The compute rule asks for wall clock on ONE FIXED GPU for ONE FIXED CELL per model; the fixed
    cell of record is (k = the model's trained depth, cap 512) on GSM8K natural stop, and the table
    marks which rows are that cell.
    """
    import glob
    out = []
    for p in sorted(glob.glob(os.path.join(art_dir, "meta_*.json"))):
        m = load_json(p, {})
        for key, pas in (m.get("passes") or {}).items():
            out.append({"file": os.path.basename(p), "model": m.get("model"),
                        "task": m.get("task"), "k": m.get("k"), "protocol": m.get("protocol"),
                        "pass": key, "device": (m.get("env") or {}).get("device"),
                        "generated_tokens": pas.get("generated_tokens"),
                        "generate_seconds": pas.get("generate_seconds"),
                        "tokens_per_s": pas.get("tokens_per_s"),
                        "peak_gb": m.get("peak_gb"),
                        "reference_cell": bool(m.get("task") == "gsm8k"
                                               and m.get("protocol") == "natural")})
    return out


# ------------------------------------------------------------------ CLI
def main(argv=None):
    p = argparse.ArgumentParser(prog="prod.cost")
    p.add_argument("--models", default="all")
    p.add_argument("--P", type=float, default=800.0)
    p.add_argument("--T", type=float, default=512.0)
    p.add_argument("--R", type=float, default=0.0)
    p.add_argument("--ks", default="1,2,3,4")
    p.add_argument("--old", action="store_true", help="also print S27's original formula")
    p.add_argument("--wall-clock-from", dest="wall_from", default=None)
    p.add_argument("--out", default=None)
    a = p.parse_args(argv)
    names = list(LOOPED) if a.models == "all" else a.models.split(",")
    ks = [int(x) for x in a.ks.split(",")]
    out = {"formula": ("T5: 2 (N_fixed + k N_core) (P+T+R) + k * 4 L_core d (mean of (P+T)^2)/2 "
                       "+ 4 L_fixed d (mean of (P+T)^2)/2 + 2 V d (T+R)"),
           "reference_point": {"P": a.P, "T": a.T, "R": a.R}, "models": {}}
    for n in names:
        try:
            sh = model_shapes(n)
        except Exception as e:                             # noqa: BLE001
            out["models"][n] = {"error": repr(e)}
            continue
        rec = dict(sh)
        for k in ks:
            if k > 4 and sh["family"] == "ouro":
                continue
            f = flops_t5(sh, k, a.P, a.T, a.R, sq_lengths=None, split=True)
            rec["k%d" % k] = {"layer_passes": layer_passes(sh, k, a.P + a.T + a.R),
                              "layer_passes_promptfree": layer_passes(sh, k, a.T + a.R),
                              "kv_bytes_per_token": kv_bytes_per_token(sh, k),
                              "flops_t5": f["flops"], "flops_prefill": f["flops_prefill"],
                              "flops_decode": f["flops_decode"]}
            if a.old:
                rec["k%d" % k]["flops_s27_old"] = flops_s27_old(
                    sh["n_nonembed"], sh["n_layers"], sh["d_model"], a.P, a.T, k=k)
        out["models"][n] = rec
        print("%-22s L=%-3d d=%-5d N_nonembed=%.3e  k=%s FLOPs %s"
              % (n, sh["n_layers"], sh["d_model"], sh["n_nonembed"], ks,
                 ["%.3e" % rec["k%d" % k]["flops_t5"] for k in ks if "k%d" % k in rec]))
    if a.wall_from:
        out["wall_clock"] = wall_clock_table(a.wall_from)
    dest = a.out or os.path.join(os.environ.get("PROD_ART", "."), "cost_table.json")
    save_json(dest, out)
    print("wrote", dest)
    return out


if __name__ == "__main__":
    main()
