"""Train adapters from independent blocks using selected loop-depth hidden states and token-normalized cross entropy."""
import gc, json, math, os, shutil, sys, tempfile, time, traceback
from contextlib import contextmanager

import numpy as np
import torch
import torch.nn.functional as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import targets as G

INITIAL_SPLIT = 1          # micro-batches run whole; an OOM halves them for that window only


def lora_config(cfg):
    """Return the peft adapter config named by config.yaml: rank, alpha, dropout and projections."""
    from peft import LoraConfig
    lo = G.lora_settings(cfg)
    return LoraConfig(r=lo["r"], lora_alpha=lo["alpha"], lora_dropout=lo["dropout"],
                      bias="none", task_type="CAUSAL_LM", target_modules=lo["targets"])


def check_data_matches_arm(arrays, manifest, arm):
    """Refuse blocks another arm produced: the manifest must name this arm and fingerprint these arrays."""
    assert manifest.get("arm") == arm, ("blocks were built for arm %r, not %r"
                                        % (manifest.get("arm"), arm))
    want, got = manifest.get("blocks_sha256"), G.blocks_fingerprint(arrays)
    assert want == got, "blocks do not match the manifest fingerprint (%s != %s)" % (got, want)


def micro_from_schedule(sched):
    """Return the blocks per micro-batch the schedule on disk was built with, per block length."""
    widths = {}
    for mb in sched:
        L = int(mb["seq_len"])
        got = widths.setdefault(L, len(mb["blocks"]))
        assert got == len(mb["blocks"]), ("schedule mixes micro-batch widths %d and %d at block "
                                          "length %d" % (got, len(mb["blocks"]), L))
    return widths


def check_micro(sched, cfg):
    """Refuse a config whose per-bucket micro width or window size disagrees with the schedule on disk."""
    for L, got in sorted(micro_from_schedule(sched).items()):
        want = cfg.micro(L)
        assert got == want, ("schedule has %d blocks per micro-batch at block length %d, config "
                             "says %d; rebuild the targets or fix the config" % (got, L, want))
    nb = int(cfg["effective_batch_blocks"])
    for w, window in enumerate(G.windows_from_schedule(sched)):
        lens = {int(mb["seq_len"]) for mb in window}
        assert len(lens) == 1, "window %d mixes block lengths %s" % (w, sorted(lens))
        blocks = sum(len(mb["blocks"]) for mb in window)
        assert blocks == nb, ("window %d holds %d blocks, config says %d per optimiser step"
                              % (w, blocks, nb))


@contextmanager
def atomic_checkpoint(path):
    """Yield a staging directory that replaces path only once the body returns, so an interrupted save leaves the previous checkpoint intact."""
    parent = os.path.dirname(os.path.abspath(path)) or "."
    os.makedirs(parent, exist_ok=True)
    staging = tempfile.mkdtemp(prefix=".ckpt_", dir=parent)
    try:
        yield staging
    except BaseException:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    previous = path + ".old"
    shutil.rmtree(previous, ignore_errors=True)
    if os.path.exists(path):
        os.replace(path, previous)
    os.replace(staging, path)
    shutil.rmtree(previous, ignore_errors=True)


def block_ce_sum(base, x, mask, depth):
    """Return summed next-token CE and supervised-token count for independent padded blocks."""
    with G.execution_depth(base, depth):
        _out, hidden, _gate = base.model(input_ids=x, use_cache=False)
        logits = base.lm_head(hidden[depth - 1])
    selected = mask[:, 1:].reshape(-1).bool()
    targets = x[:, 1:].reshape(-1)[selected]
    scores = logits[:, :-1].reshape(-1, logits.shape[-1])[selected].float()
    return F.cross_entropy(scores, targets, reduction="sum"), int(selected.sum())


def main(argv):
    """Train one arm's adapter over its own blocks and write train_config_<arm>.json with realised supervised tokens, content tokens and layer passes; returns a process exit code."""
    NAME = argv[0] if argv and not argv[0].startswith("-") else "s36"
    cfg_path, root, arm = G.DEFAULT_CONFIG, None, None
    ckpt_every, wait, max_steps = None, True, None
    for a in argv:
        k, _, v = a.lstrip("-").partition("=")
        if k == "config":
            cfg_path = v
        elif k == "root":
            root = v
        elif k == "arm":
            arm = v
        elif k == "ckpt-every":
            ckpt_every = int(v)
        elif k == "max-steps":
            max_steps = int(v)
        elif k == "no-wait":
            wait = False
    G.require_root(root, "train.py")
    cfg = G.load_config(cfg_path)
    arm = arm or cfg["default_arm"]
    ckpt_every = ckpt_every if ckpt_every is not None else int(cfg["ckpt_every"])
    P = G.paths(root)
    G.ensure_dirs(P)
    T0 = time.time()
    waited = (G.wait_for_gpu(os.path.join(P["logs"], "gpu_wait.log")) if wait
              else {"waited_s": 0})

    # ---------------------------------------------------------------- data
    DATA = G.data_dir(P, arm)
    arrays = {}
    for name in sorted(os.listdir(DATA)):
        if name.startswith("blocks_") and name.endswith(".npy"):
            L = int(name[len("blocks_"):-len(".npy")])
            arrays[L] = {"blocks": np.load(os.path.join(DATA, name)),
                         "mask": np.load(os.path.join(DATA, "mask_%d.npy" % L)),
                         "length": np.load(os.path.join(DATA, "length_%d.npy" % L)),
                         "depth": np.load(os.path.join(DATA, "bdepth_%d.npy" % L))}
    assert arrays, "no blocks_<L>.npy in %s -- run targets.py --arm=%s first" % (DATA, arm)
    man = G.jload(os.path.join(P["artifacts"], "target_manifest_%s.json" % arm), {}) or {}
    check_data_matches_arm(arrays, man, arm)
    with open(os.path.join(DATA, "spans.jsonl"), encoding="utf-8") as f:
        spans = [json.loads(line) for line in f if line.strip()]
    assert G.v3_context(arrays, spans, pad_id=man.get("pad_id"))["ok"], "invalid block boundaries"
    for span in spans:              # the saved content length is the block minus its padding
        assert int(arrays[span["L"]]["length"][span["block"]]) == int(span["end"]), span
    sched = json.load(open(os.path.join(DATA, "schedule.json"), encoding="utf-8"))
    check_micro(sched, cfg)
    windows = G.windows_from_schedule(sched)      # one optimiser step per window, one block length
    n_micro = len(sched)
    n_opt = len(windows)
    if max_steps:
        n_opt = min(n_opt, max_steps)
    warmup = max(1, int(round(float(cfg["warmup_frac"]) * n_opt)))
    for mb in sched:
        L = int(mb["seq_len"])
        assert len({int(arrays[L]["depth"][b]) for b in mb["blocks"]}) == 1, mb
        assert int(arrays[L]["depth"][mb["blocks"][0]]) == int(mb["depth"]), mb
    print("name=%s arm=%s blocks=%s micro_batches=%d micro=%s n_opt=%d warmup=%d"
          % (NAME, arm, {L: int(a["blocks"].shape[0]) for L, a in arrays.items()}, n_micro,
             {L: cfg.micro(L) for L in sorted(arrays)}, n_opt, warmup), flush=True)

    torch.manual_seed(int(cfg["seed"]))
    np.random.seed(int(cfg["seed"]))
    from s32_common import load_base
    tok, model = load_base()
    model.config.use_cache = False
    from peft import get_peft_model
    pmodel = get_peft_model(model, lora_config(cfg))
    base = pmodel.base_model.model
    trainable = []
    for n_, p in pmodel.named_parameters():
        if p.requires_grad:
            assert "lora_" in n_, n_
            p.data = p.data.float()
            trainable.append((n_, p))
    assert not any(("early_exit_gate" in n or "lm_head" in n or "embed_tokens" in n
                    or ".norm" in n) for n, _ in trainable), "froze the wrong thing"
    n_train = sum(p.numel() for _, p in trainable)
    opt = torch.optim.AdamW([p for _, p in trainable], lr=float(cfg["lr"]),
                            betas=tuple(cfg["betas"]), weight_decay=float(cfg["weight_decay"]))
    print("trainable %d params in %d tensors" % (n_train, len(trainable)), flush=True)

    CKPT = os.path.join(P["adapters"], "%s_ckpt" % NAME)
    start = 0
    st = {}
    if os.path.exists(os.path.join(CKPT, "state.json")):
        st = G.jload(os.path.join(CKPT, "state.json")) or {}
        if st.get("name") == NAME:
            assert st.get("arm", arm) == arm, ("checkpoint %s was trained on arm %r, not %r"
                                               % (CKPT, st.get("arm"), arm))
            from peft import set_peft_model_state_dict
            from safetensors.torch import load_file
            weights = load_file(os.path.join(CKPT, "adapter", "adapter_model.safetensors"))
            assert weights, "checkpoint adapter has no tensors"
            missing = set_peft_model_state_dict(pmodel, weights)
            opt.load_state_dict(torch.load(os.path.join(CKPT, "opt.pt"), map_location=G.DEV))
            start = int(st["opt_step"])
            # the plan the earlier run followed decides the schedule, or the cosine would restart
            n_opt = int(st.get("n_opt", n_opt))
            warmup = int(st.get("warmup", warmup))
            print("resumed at optimiser step %d of %d (unexpected keys %s)"
                  % (start, n_opt, getattr(missing, "unexpected_keys", None)), flush=True)

    LR = float(cfg["lr"])
    assert str(cfg["schedule"]) == "cosine", cfg["schedule"]

    def lr_at(step):
        """Return the learning rate at one optimiser step: linear warmup, then cosine decay to zero."""
        if step < warmup:
            return LR * (step + 1) / warmup
        prog = (step - warmup) / max(1, n_opt - warmup)
        return LR * 0.5 * (1.0 + math.cos(math.pi * min(1.0, prog)))

    META = os.path.join(P["artifacts"], "train_config_%s.json" % arm)
    meta = G.jload(META, {}) or {}
    meta.update({
        "name": NAME, "arm": arm, "arm_config": cfg.arm(arm), "seed": int(cfg["seed"]),
        "blocks_by_len": {str(L): int(a["blocks"].shape[0]) for L, a in arrays.items()},
        "one_visit_per_block": True,
        "packing": "one visit per block, right-padded, pad mask 0, causal forward, no attention mask",
        "tokens_in_blocks": man.get("tokens_in_blocks"),
        "padding_share": man.get("padding_share"),
        "supervised_token_budget": int(cfg["supervised_token_budget"]),
        "supervised_tokens_drawn": man.get("supervised_tokens_drawn"),
        "supervised_tokens_scheduled": man.get("supervised_tokens_scheduled"),
        "blocks_dropped_as_remainder": man.get("blocks_dropped_as_remainder"),
        "supervised_tokens_planned": int(sum(int(m["supervised"]) for w in windows[:n_opt]
                                            for m in w)),
        "supervised_density": man.get("supervised_density"),
        "visits_by_T": man.get("visits_by_T"), "visits_by_kind": man.get("visits_by_kind"),
        "fallback_share_overall": man.get("fallback_share_overall"),
        "supervised_share_by_source": man.get("supervised_share_by_source"),
        "supervised_share_by_format": man.get("supervised_share_by_format"),
        "micro_by_block_len": {str(L): cfg.micro(L) for L in sorted(arrays)},
        "accum_by_block_len": {str(L): cfg.accum(L) for L in sorted(arrays)},
        "effective_batch_blocks": int(cfg["effective_batch_blocks"]),
        "padding_share_by_block_len": man.get("padding_share_by_block_len"),
        "harvest_horizon_by_source": man.get("harvest_horizon_by_source"),
        "n_micro_batches": n_micro, "n_opt_steps": n_opt,
        "warmup_steps": warmup, "lr": LR, "weight_decay": float(cfg["weight_decay"]),
        "betas": list(cfg["betas"]), "grad_clip": float(cfg["grad_clip"]),
        "lora": G.lora_settings(cfg), "n_trainable_params": int(n_train),
        "loss": str(cfg["loss"]),
        "loss_detail": ("CE SUM from lm_head(hidden_states_list[d-1]) on the masked target "
                        "tokens, divided by the accumulation window's own supervised-token "
                        "total; padding is mask 0 and never enters the sum"),
        "lr_schedule": str(cfg["schedule"]),
        "blocks_sha256": man.get("blocks_sha256"), "data_dir": DATA,
        "gradient_checkpointing": False,
        "depth_probabilities": {str(k): v for k, v in cfg["depth_probabilities"].items()},
        "budget_grid_by_source": man.get("budget_grid_by_source"),
        "block_lens": cfg.block_lens,
        "control_line": (cfg["budget_line_with_limit"] + " | " + cfg["budget_line_no_limit"]
                         + "  (never supervised)") if cfg.arm(arm)["budget_line"] else "none",
        "gpu_wait": waited, "errors": {}})
    G.jdump(meta, META)

    LOGF = open(os.path.join(P["train_logs"], "%s.jsonl" % NAME), "a", encoding="utf-8")
    NL = int(cfg["n_layers"])
    CLIP = float(cfg["grad_clip"])
    state = {"sup": int(st.get("supervised_tokens", 0)),
             "real": int(st.get("padded_tokens", st.get("real_tokens", 0))),
             "content": int(st.get("content_tokens", 0)),
             "lp": int(st.get("layer_passes_fwd", 0)), "ce": 0.0}
    losses = list(st.get("losses", []))
    step = start
    t_train = time.time()
    try:
        while step < n_opt:
            t_step = time.time()
            opt.zero_grad(set_to_none=True)
            for g in opt.param_groups:
                g["lr"] = lr_at(step)
            window = windows[step]
            nsup_win = sum(int(w["supervised"]) for w in window)
            assert nsup_win > 0, step
            state["ce"] = 0.0

            def chunk(bi, d, L):
                """Forward and backward one group of blocks at depth d, accumulating CE and token counts."""
                A = arrays[L]
                x = torch.from_numpy(A["blocks"][bi].astype(np.int64)).to(G.DEV)
                m = torch.from_numpy(A["mask"][bi].astype(np.int64)).to(G.DEV)
                with torch.autocast("cuda", dtype=torch.bfloat16):
                    ce, supervised = block_ce_sum(base, x, m, d)
                (ce / nsup_win).backward()
                content = int(A["length"][bi].sum())
                state["ce"] += float(ce.detach())
                state["sup"] += supervised
                state["real"] += int(x.numel())
                state["content"] += content
                state["lp"] += d * NL * content
                del x, m, ce

            before_window = state.copy()
            SPLIT = INITIAL_SPLIT       # an earlier window's OOM must not shrink every later one
            while True:
                try:
                    for mb in window:
                        d, L = int(mb["depth"]), int(mb["seq_len"])
                        if int(mb["supervised"]) == 0:
                            continue
                        bi = list(mb["blocks"])
                        n = max(1, len(bi) // SPLIT)
                        for j in range(0, len(bi), n):
                            chunk(bi[j:j + n], d, L)
                    break
                except torch.OutOfMemoryError as e:
                    meta.setdefault("oom_events", []).append(
                        "OOM step %d split %d: %s" % (step, SPLIT, str(e).split("\n")[0]))
                    print("[OOM] step %d split %d -> %d" % (step, SPLIT, SPLIT * 2), flush=True)
                    opt.zero_grad(set_to_none=True)
                    state.update(before_window)
                    e.__traceback__ = None
                    gc.collect(); torch.cuda.empty_cache(); gc.collect()
                    SPLIT *= 2
                    if SPLIT > max(len(mb["blocks"]) for mb in window):
                        raise
            torch.nn.utils.clip_grad_norm_([p for _, p in trainable], CLIP)
            opt.step()
            per_tok = state["ce"] / nsup_win
            losses.append(per_tok)
            step += 1
            if step % 10 == 0 or step == n_opt or step == 1 or n_opt <= 50:
                rec = {"opt_step": step, "loss_per_token": per_tok, "lr": lr_at(step - 1),
                       "step_seconds": round(time.time() - t_step, 3),
                       "n_sup_window": nsup_win, "supervised_tokens_cum": state["sup"],
                       "content_tokens_cum": state["content"],
                       "depths_in_window": [int(w["depth"]) for w in window],
                       "seq_lens_in_window": [int(w["seq_len"]) for w in window],
                       "seconds": round(time.time() - T0, 1),
                       "s_per_step": round((time.time() - t_train) / max(1, step - start), 3),
                       "peak_gb": round(torch.cuda.max_memory_allocated() / 1024 ** 3, 3)}
                LOGF.write(json.dumps(rec) + "\n")
                LOGF.flush()
                os.fsync(LOGF.fileno())
                print("  step %d/%d loss/tok %.4f lr %.2e nsup %d %.0fs %.2fs/step peak %.2f GB"
                      % (step, n_opt, per_tok, rec["lr"], nsup_win, rec["seconds"],
                         rec["s_per_step"], rec["peak_gb"]), flush=True)
            if step % ckpt_every == 0 or step == n_opt:
                with atomic_checkpoint(CKPT) as staging:
                    pmodel.save_pretrained(os.path.join(staging, "adapter"))
                    torch.save(opt.state_dict(), os.path.join(staging, "opt.pt"))
                    G.jdump({"name": NAME, "arm": arm, "opt_step": step, "n_opt": n_opt,
                             "warmup": warmup, "losses": losses,
                             "supervised_tokens": state["sup"],
                             "padded_tokens": state["real"],
                             "content_tokens": state["content"],
                             "layer_passes_fwd": state["lp"]},
                            os.path.join(staging, "state.json"))
    except Exception:
        meta["errors"]["train"] = traceback.format_exc()
        G.jdump(meta, META)
        print(meta["errors"]["train"], flush=True)
        raise

    pmodel.save_pretrained(os.path.join(P["adapters"], NAME))
    LOGF.close()
    dt = max(1e-9, time.time() - t_train)
    n_done = max(1, step - start)
    meta.update({
        "supervised_tokens": int(state["sup"]),
        "padded_tokens": int(state["real"]),          # block positions forwarded, padding included
        "content_tokens": int(state["content"]),      # the same blocks with padding removed
        "layer_passes_forward": int(state["lp"]), "layer_passes_fwd_bwd": int(3 * state["lp"]),
        "opt_steps_done": step,
        "mean_loss_first_10": float(np.mean(losses[:10])) if losses else None,
        "mean_loss_last_10": float(np.mean(losses[-10:])) if losses else None,
        "seconds": round(time.time() - T0, 1), "train_seconds": round(dt, 1),
        "seconds_per_opt_step": round(dt / n_done, 3),
        "content_tokens_per_s": round(state["content"] / dt, 1),
        "padded_tokens_per_s": round(state["real"] / dt, 1),
        "peak_gb": round(torch.cuda.max_memory_allocated() / 1024 ** 3, 3),
        "adapter": os.path.join(P["adapters"], NAME)})
    G.jdump(meta, META)
    print("DONE %s arm=%s %d opt steps sup %d loss/tok %.4f -> %.4f %.0fs %.2fs/step peak %.2f GB"
          % (NAME, arm, step, state["sup"], meta["mean_loss_first_10"] or 0,
             meta["mean_loss_last_10"] or 0, meta["seconds"], meta["seconds_per_opt_step"],
             meta["peak_gb"]), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
