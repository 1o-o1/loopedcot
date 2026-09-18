"""Read cell JSONL files and write calibration cards, policy statistics, and cost-fraction tables to the output directory."""
import argparse
import json
import os

import numpy as np

from . import cells as C
from . import evaluate as E
from . import policy as P


def _args(argv=None):
    p = argparse.ArgumentParser(prog="alloc.cli")
    p.add_argument("--cells", required=True, help="directory holding the cells jsonl files")
    p.add_argument("--task", required=True)
    p.add_argument("--checkpoint", required=True)
    p.add_argument("--protocol", default="natural", choices=("natural", "natural2", "natural2h"),
                   help="which grid of the pair to read: the natural-stop grid (default), the "
                        "think-tag continuation (natural2) or the horizon extension (natural2h); "
                        "the loader takes only the files carrying that protocol segment")
    p.add_argument("--reference", default=None, help="a second checkpoint to contrast against")
    p.add_argument("--reference-cells", default=None,
                   help="directory for the reference's cells (default: --cells)")
    p.add_argument("--reference-bbh-base", action="store_true",
                   help="the reference file holds raw multiple-choice rows: re-parse the "
                        "answer letter and re-derive the calibration split")
    p.add_argument("--out", required=True)
    p.add_argument("--c-gate", type=float, default=P.DEFAULT_C_GATE)
    p.add_argument("--gate-mode", default=P.DEFAULT_GATE_MODE, choices=list(P.GATE_MODES),
                   help="where the gated arms measure their margin: `split` fits the ranking and "
                        "the multiplier on the first --n-select calibration ids and measures the "
                        "margin on the next --n-verify, which took no part in the fit; `whole` is "
                        "the old rule, one set fitting and measuring, kept for comparison")
    p.add_argument("--gate-folds", type=int, default=None,
                   choices=list(P.GATE_FOLD_CHOICES),
                   help="how many directions of the calibration split a deviation must be earned "
                        "in. %d, the frozen default, fits on the selection half and verifies on "
                        "the verification half and then fits on the verification half and verifies "
                        "on the selection half, and deviates only when BOTH verified margins clear "
                        "c_gate sd; 1 is the first direction alone. The arm that runs is always "
                        "the 1-fold policy, so a second fold can only withhold a deviation. Under "
                        "--gate-mode whole one set both fits and measures, so the default there is "
                        "1 and asking for 2 is refused" % P.GATE_FOLDS)
    p.add_argument("--one-se", action="store_true",
                   help="the one-standard-error rule: deviate only on a margin above 1.0 sd, "
                        "whatever --c-gate says")
    p.add_argument("--n-select", type=int, default=None,
                   help="calibration ids, in id order, that fit the ranking and the multiplier "
                        # argparse expands `help % params` when it prints, so the literal per-cent
                        # sign this leaves behind has to survive that second pass as well
                        "(default: %.0f%%%% of the calibration split)" % (100 * P.GATE_SELECT_FRAC))
    p.add_argument("--n-verify", type=int, default=None,
                   help="the ids after those, which measure the gate margin and nothing else "
                        "(default: the rest of the calibration split)")
    p.add_argument("--n-cal", type=int, default=None,
                   help="calibration questions; default max(%d, min(%d, %g N)) of the grid's N. "
                        "Evaluation ids are promoted into calibration, in the dataset's seeded "
                        "order, until the split holds this many, and the evaluation split shrinks "
                        "by as many" % (C.N_CAL_MIN, C.N_CAL_MAX, C.N_CAL_FRAC))
    p.add_argument("--no-families", action="store_true",
                   help="test only the free set of cells at the gate, as v4 did, instead of the "
                        "frozen structured families F0 (deepest depth at cap 0), F1 (deepest "
                        "depth at any cap), F2 (one depth shallower) and F3 (the free set) in "
                        "that order. The comparison flag, not the default")
    p.add_argument("--n-labels", type=int, default=None)
    p.add_argument("--boot", type=int, default=2000)
    p.add_argument("--cal-draws", type=int, default=100)
    p.add_argument("--promptfree", action="store_true")
    p.add_argument("--accounting", default="cap", choices=list(P.ACCOUNTINGS) + ["all"],
                   help="how a cell is charged: `cap` the whole cap, `expected` the calibration "
                        "mean realised length at that cell, `realised` the prompt's own measured "
                        "cost (an audit price, not available at decision time), `all` writes one "
                        "Table 1 per accounting")
    p.add_argument("--avg-budget", action="store_true",
                   help="add the average-budget arms (%s) to Table 1: "
                        % ", ".join("`%s`" % n for n in P.AVG_ARMS) +
                        "a multiplier fitted on the calibration prompts holds their MEAN price at "
                        "or below the budget, in place of a cap on every prompt")
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--model", default=None,
                   help="model name to look up in --model-config (default: --checkpoint)")
    p.add_argument("--model-config", default=None,
                   help="a production config file to read the checkpoint's layer shape from")
    p.add_argument("--layers-per-loop", type=int, default=None,
                   help="transformer layers inside one loop pass")
    p.add_argument("--fixed-layers", type=int, default=0,
                   help="transformer layers paid once per token whatever the depth")
    p.add_argument("--ks", default=None,
                   help="comma-separated depths to keep; must be a subset of what the rows hold")
    p.add_argument("--caps", default=None,
                   help="comma-separated token caps to keep; must be a subset of the rows'")
    p.add_argument("--cache-dir", default=None,
                   help="where the parsed-file caches live (default: beside each cells file; pass "
                        "a directory to keep a shared or read-only --cells tree clean). The cache "
                        "is keyed by each file's size, mtime and header, so a regenerated grid "
                        "invalidates its own entry and nothing has to be told to rebuild it")
    p.add_argument("--no-cache", dest="cache", action="store_false",
                   help="parse every cells file: read no cache and write none. The parse is the "
                        "ground truth, so the cache must always be able to be taken out")
    p.set_defaults(cache=True)
    return p.parse_args(argv)


def _int_list(s):
    return None if s is None else [int(x) for x in s.split(",") if x.strip()]


def resolve_geometry(a):
    """Return (layers_per_loop, fixed_layers) for the run, or exit with what is missing.

    Three ways to pin it, in order: the explicit flags; a model config file, which also covers a
    model with a fixed prelude and coda around a recurrent core; and, only for a checkpoint whose
    name says it is the 24-layer fully recurrent model, the built-in default. Anything else is
    refused, because pricing another family at 24 layers per pass would silently misprice
    every cell.
    """
    if a.layers_per_loop is not None:
        return int(a.layers_per_loop), int(a.fixed_layers)
    model = a.model or a.checkpoint
    if a.model_config:
        try:
            return C.model_geometry(model, a.model_config)
        except KeyError as e:
            raise SystemExit("cannot price %s: %s" % (model, e))
    low = model.lower()
    if "ouro" in low and ("1_4b" in low or "1.4b" in low):
        return C.L_LOOP_DEFAULT, C.L_FIXED_DEFAULT
    raise SystemExit(
        "cannot price %r: pass --layers-per-loop (and --fixed-layers), or --model-config with a "
        "file that holds this model's shape. Only a 24-layer fully recurrent checkpoint has a "
        "built-in default." % model)


def accountings_of(a):
    """Return the accountings to tabulate and the one the gains and contrasts are priced under."""
    if a.accounting == "all":
        return list(P.ACCOUNTINGS), P.ACCOUNTINGS[0]
    return [a.accounting], a.accounting


def _rmse_pts(A, B):
    """Return the RMSE between two (depth, cap) accuracy surfaces, in percentage points."""
    return float(100 * np.sqrt(np.nanmean((np.asarray(A, float) - np.asarray(B, float)) ** 2)))


def card(cs, n_labels=None):
    cal, ev = cs.select("cal"), cs.select("eval")
    cost = P.cost_of(cs)
    Pm, Rm = P.median_point(cs, ev)
    elen = C.expected_lengths(cs)
    A_hat, m = E.surface(cs, cal, n_labels=n_labels)
    A_res, mr = E.resolved_surface(cs, cal, n_labels=n_labels)
    eq, pred = P.rank_equation(cs, A_hat, cost, Pm, Rm)
    rs, pred_res = P.rank_equation(cs, A_res, cost, Pm, Rm)
    lk, acc = P.rank_lookup(cs, cal, cost, Pm, Rm)
    # The two surfaces against what the questions actually measured, on both splits. The calibration
    # column is the fit's own residual and the evaluation column is the only one that says whether
    # the surface generalises; neither enters a policy.
    cal_mean = np.nanmean(cs.acc[:, :, cal], axis=2)
    ev_mean = np.nanmean(cs.acc[:, :, ev], axis=2)
    key = lambda c: "k%d_T%d" % c
    return {"checkpoint": cs.name, "task": cs.task, "n_cal": int(len(cal)),
            "n_eval": int(len(ev)),
            "ks": cs.ks, "caps": cs.caps,
            "answer_budget": cs.answer_budget_used(),
            "reserve_constant_per_task": bool(cs.reserve_is_constant()),
            "median_prompt_tokens": Pm, "median_reserve": Rm,
            "G": m["G"], "c": m["c"], "l": m["l"],
            "A_hat": m["A_hat"], "raw_surface": m["acc_measured"],
            "reconstruction_rmse_pts": m["rmse_pts"], "noise_floor_pts": m["noise_floor_pts"],
            "uncommitted_share": m["uncommitted_share"],
            # the identity resolved by settle time: P_k(s=j), c_k(j) per settle cap, l_k(T) per cap
            "settle_time": {
                "n_labels": mr["n_labels"], "n_readouts": mr["n_g"],
                "min_labels_per_cap": mr["min_labels"], "bins": mr["bins"],
                "share_settle_first_cap": mr["share_settle_first"],
                "share_never": mr["share_never"],
                "distribution": mr["settle_distribution"],
                "P": mr["P"], "c_by_settle_cap": mr["c"], "l_by_cap": mr["l"],
                "c_source": mr["c_source"], "n_labels_at_cap": mr["n_labels_at_cap"],
                "n_unsettled_at_cap": mr["n_unsettled_at_cap"],
                "pooled_c": mr["pooled_c"], "pooled_l": mr["pooled_l"],
                "n_caps_own": mr["n_caps_own"], "n_caps_binned": mr["n_caps_binned"],
                "n_caps_pooled": mr["n_caps_pooled"],
                "n_caps_binned_with_mass": mr["n_caps_binned_with_mass"],
                "n_caps_pooled_with_mass": mr["n_caps_pooled_with_mass"]},
            "A_res": mr["A_res"],
            "rmse_pts": {"pooled_cal": _rmse_pts(A_hat, cal_mean),
                         "resolved_cal": _rmse_pts(A_res, cal_mean),
                         "pooled_eval": _rmse_pts(A_hat, ev_mean),
                         "resolved_eval": _rmse_pts(A_res, ev_mean),
                         "noise_floor_cal": m["noise_floor_pts"],
                         "noise_floor_eval": float(100 * np.sqrt(np.nanmean(
                             ev_mean * (1 - ev_mean) / max(1, len(ev)))))},
            "ranking_lookup": [key(c) for c in lk],
            "ranking_equation": [key(c) for c in eq],
            "ranking_equation_resolved": [key(c) for c in rs],
            "cal_accuracy": {key(c): round(acc[c], 4) for c in acc},
            "predicted_accuracy": {key(c): round(pred[c], 4) for c in pred},
            "predicted_accuracy_resolved": {key(c): round(pred_res[c], 4) for c in pred_res},
            "median_cost_layer_passes": {key(c): int(cost(c[0], c[1], Pm, Rm)) for c in acc},
            "expected_length_tokens": {key(c): round(float(elen[cs.ks.index(c[0]),
                                                           cs.caps.index(c[1])]), 3)
                                       for c in acc}}


def main(argv=None):
    a = _args(argv)
    L, L_fixed = resolve_geometry(a)
    ks, caps = _int_list(a.ks), _int_list(a.caps)
    os.makedirs(a.out, exist_ok=True)
    bbh_base = a.task in C.BBH_TASKS and a.checkpoint in ("base", "A0_base")
    cs = C.load(a.cells, a.task, a.checkpoint, bbh_base=bbh_base, ks=ks, caps=caps,
                L=L, L_fixed=L_fixed, cache=a.cache, cache_dir=a.cache_dir, protocol=a.protocol)
    # v5: the calibration split is sized from the grid, not fixed at 100. Evaluation ids are
    # promoted into it in the dataset's seeded order until it holds n_cal, so the evaluation split
    # shrinks by exactly as many questions; --n-cal overrides the rule.
    n_cal, why = C.resolve_n_cal(cs, a.n_cal)
    cs, split_record = C.promote_calibration(cs, n_cal)
    split_record["reason"] = why
    cards = {cs.name: card(cs, a.n_labels)}
    accs, primary = accountings_of(a)
    gate_folds = P.resolve_gate_folds(a.gate_mode, a.gate_folds)
    gate_kw = dict(gate_mode=a.gate_mode, one_se=bool(a.one_se),
                   n_select=a.n_select, n_verify=a.n_verify,
                   families=not bool(a.no_families), gate_folds=gate_folds)
    res = {"task": a.task, "checkpoint": a.checkpoint, "protocol": a.protocol, "reference": a.reference,
           "promptfree": bool(a.promptfree), "c_gate": a.c_gate, "avg_budget": bool(a.avg_budget),
           "gate_mode": a.gate_mode, "one_se": bool(a.one_se),
           # The two frozen rulings of 2026-09-18, in the header so every artifact carries them:
           # the ranking of record and how many directions of the split a deviation was earned in.
           "ranking_of_record": P.RANKING_OF_RECORD,
           "gate_folds": int(gate_folds),
           "n_select": a.n_select, "n_verify": a.n_verify,
           "n_cal_rule": {"requested": a.n_cal, "resolved": n_cal,
                          "n_questions": int(len(cs.idx)), "split": split_record},
           # How the cells were read. `cached_files` of `files` says how much of this run was the
           # parsed-file cache rather than JSON; with --no-cache it is absent and every file was
           # parsed. The numbers only ever change the run's WALL TIME, never a result.
           "read": dict(cs.read_stats, cache=bool(a.cache), cache_dir=a.cache_dir),
           "families": not bool(a.no_families),
           "deviation_families": list(P.DEVIATION_FAMILIES),
           "accounting": a.accounting, "accounting_priced": primary,
           "accountings_tabulated": accs, "gain": {}}
    arms = [("lookup", dict(ranking="lookup", c_gate=0.0)),
            ("equation", dict(ranking="equation", c_gate=0.0)),
            ("equation_n30", dict(ranking="equation", n_labels=30, c_gate=0.0)),
            ("equation_n100", dict(ranking="equation", n_labels=100, c_gate=0.0)),
            ("equation_resolved", dict(ranking="equation_resolved", c_gate=0.0)),
            ("gated_equation", dict(ranking="equation", c_gate=a.c_gate)),
            ("gated_equation_resolved", dict(ranking="equation_resolved", c_gate=a.c_gate))]
    for name, spec in arms:
        res["gain"][name] = E.gain_over_normal(cs, promptfree=a.promptfree, n_boot=a.boot,
                                               n_cal_draws=a.cal_draws, seed=a.seed,
                                               accounting=primary, **dict(gate_kw, **spec))
    res["default_cost"] = E.default_cost(cs, promptfree=a.promptfree)
    tables = {acc: E.table1(cs, promptfree=a.promptfree, c_gate=a.c_gate, seed=a.seed,
                            accounting=acc, avg_budget=a.avg_budget, **gate_kw) for acc in accs}
    # Each table's picks block is lifted out of the table (it is the bulk of the file) into
    # `picks`, keyed by accounting, beside the calibration ids they were fitted on.
    picks_by_acc = {acc: t.pop("picks", None) for acc, t in tables.items()}
    t1 = tables[primary]
    res["table1"] = t1
    # `table1` is priced under the FIRST accounting of --accounting (`cap` under `all`);
    # the expected-accounting numbers are table1_by_accounting["expected"].
    res["table1_accounting"] = primary
    res["table1_by_accounting"] = tables
    cal_ids = sorted(int(cs.idx[n]) for n in cs.select("cal"))
    promoted = [int(i) for i in split_record.get("promoted_ids", [])]
    res["picks"] = {
        "note": "every arm's per-prompt pick, per accounting and budget fraction, as the Table 1 "
                "row was read; prod.live_check regenerates these and nothing else",
        "calibration": {"n_cal": int(len(cal_ids)), "ids": cal_ids,
                        "ids_before_promotion": sorted(set(cal_ids) - set(promoted)),
                        "promoted_ids": promoted,
                        "evaluation_ids": sorted(int(cs.idx[n]) for n in cs.select("eval")),
                        "seed": split_record.get("seed"),
                        "order_source": split_record.get("order_source"),
                        "reason": split_record.get("reason")},
        "by_accounting": picks_by_acc}
    # The oracle gap per arm at 1.0x of the default cost: the best single EVALUATION cell minus
    # the arm. A diagnostic -- the price of calibration noise -- never a policy result.
    res["oracle"] = t1.get("oracle")
    res["oracle_gap_pts"] = {name: row.get("oracle_gap_pts")
                             for name, row in t1.get("rows", {}).items()}

    if a.reference:
        rdir = a.reference_cells or a.cells
        ref = C.load(rdir, a.task, a.reference, ks=ks, caps=caps, L=L, L_fixed=L_fixed,
                     cache=a.cache, cache_dir=a.cache_dir, protocol=a.protocol,
                     bbh_base=a.reference_bbh_base or (a.task in C.BBH_TASKS
                                                       and a.reference == "base"))
        # The reference is re-split to the SAME calibration size, so the two checkpoints still
        # carry identical evaluation ids and `assert_paired` has something to pair.
        ref, _rrec = C.promote_calibration(ref, n_cal)
        cards[ref.name] = card(ref, a.n_labels)
        E.assert_paired(cs, ref)
        res["contrasts"] = {
            w: E.contrast(cs, ref, which=w, promptfree=a.promptfree, n_boot=a.boot, seed=a.seed,
                          accounting=primary)
            for w in ("Bstar", "Blow")}
        res["noninferiority"] = E.noninferiority(cs, ref, promptfree=a.promptfree,
                                                 n_boot=a.boot, seed=a.seed, accounting=primary)
        res["reference_default_cost"] = E.default_cost(ref, promptfree=a.promptfree)

    def _j(o):
        if isinstance(o, (np.floating, np.integer)):
            return o.item()
        if isinstance(o, np.ndarray):
            return o.tolist()
        raise TypeError(repr(o))

    with open(os.path.join(a.out, "cards.json"), "w") as fh:
        json.dump(cards, fh, indent=1, default=_j)
    with open(os.path.join(a.out, "results.json"), "w") as fh:
        json.dump(res, fh, indent=1, default=_j)
    for acc, table in tables.items():
        with open(os.path.join(a.out, "table1_%s.md" % acc), "w", encoding="utf-8") as fh:
            fh.write(E.table1_markdown(table))
    with open(os.path.join(a.out, "table1.md"), "w", encoding="utf-8") as fh:
        fh.write(E.table1_markdown(t1))
    print(json.dumps({k: (v.get("gain_mean_pts") if isinstance(v, dict) else v)
                      for k, v in res["gain"].items()}, indent=1))
    print("WROTE %s" % a.out)
    return res


if __name__ == "__main__":
    main()
