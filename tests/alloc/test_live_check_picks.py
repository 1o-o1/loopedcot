"""alloc is the single source of picks: what prod.live_check reads out of alloc.cli's results.json is
what alloc.evaluate computes for the same cells and budget, for both live arms and every fraction,
and the recorded prices are the budget's.

Runs alloc.cli on the S33 GSM8K A0 grid (24 layers per loop, no fixed layers), CPU, once per module.
Skipped when that grid is not beside the package (ALLOC_S33 names it explicitly).
"""
import contextlib
import io
import os
import sys
import tempfile
import unittest

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, PKG)
from alloc import cells as C, cli, evaluate as E, policy as P        # noqa: E402
try:
    from prod.live_check import check_split, load_picks               # noqa: E402
except ImportError:
    # `alloc` and this suite are also run from the spike tree, where the prod package is not beside
    # them. Everything here is about prod.live_check, so without it there is nothing to run.
    check_split = load_picks = None

ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
S33 = os.environ.get("ALLOC_S33") or os.path.join(ROOT, "s33_anytime", "artifacts")
TASK, CKPT, L = "gsm8k", "A0", 24
ARMS = ("lookup", "avg_gated_lookup")
_OUT = {}


def _run_cli():
    if "dir" not in _OUT:
        d = tempfile.mkdtemp()
        with contextlib.redirect_stdout(io.StringIO()):
            cli.main(["--cells", S33, "--task", TASK, "--checkpoint", CKPT,
                      "--layers-per-loop", str(L), "--fixed-layers", "0",
                      "--accounting", "expected", "--avg-budget", "--boot", "20",
                      "--cal-draws", "2", "--out", d])
        _OUT["dir"] = d
    return _OUT["dir"]


def _alloc_own_picks():
    """alloc.evaluate's own computation of both arms' picks, independent of the cli's wiring."""
    if "own" in _OUT:
        return _OUT["own"]
    raw = C.load(S33, TASK, CKPT, L=L, L_fixed=0)
    n_cal, _why = C.resolve_n_cal(raw)
    cs, _rec = C.promote_calibration(raw, n_cal)
    cost = P.cost_of(cs, promptfree=False, accounting="expected")
    ev, cal = cs.select("eval"), cs.select("cal")
    Pm, Rm = P.median_point(cs, ev)
    dc = E.default_cost(cs, promptfree=False)
    Xs = [f * dc["mean"] for f in E.BUDGET_FRACTIONS]
    own = {"raw": raw, "cells": cs, "Xs": Xs, "lookup": [], "avg_gated_lookup": []}
    order, _ = E.make_order(cs, cal, cost, Pm, Rm, "lookup", None)
    rec = []
    P.policy_vectors(cs, ev, cost, Xs, order, gate=None, picks=rec)
    for a, b, _na, _nb in rec:
        own["lookup"].append({int(cs.idx[n]): (None if a[i] < 0 else (int(cs.ks[a[i]]), int(cs.caps[b[i]])))
                              for i, n in enumerate(ev)})
    score = E.cell_scores(cs, cal, P.AVG_GATED, cost, Pm, Rm)
    for v in E.avg_gated_vectors(cs, ev, cal, cost, Xs, score, E.default_cell(cs)):
        own["avg_gated_lookup"].append({int(cs.idx[n]): (int(cs.ks[v["k_idx"][i]]), int(cs.caps[v["cap_idx"][i]]))
                                        for i, n in enumerate(ev)})
    _OUT["own"] = own
    return own


@unittest.skipUnless(os.path.isdir(S33) and load_picks is not None,
                     "S33 grids or the prod package not present")
class TestLiveCheckReadsAllocPicks(unittest.TestCase):
    def test_reader_picks_equal_alloc_evaluate_for_both_arms_and_all_fractions(self):
        d = _run_cli()
        own = _alloc_own_picks()
        for arm in ARMS:
            for j, frac in enumerate(E.BUDGET_FRACTIONS):
                entry, calib, res = load_picks(d, arm, frac)
                self.assertAlmostEqual(entry["budget"], own["Xs"][j], places=6, msg=arm)
                got = {int(r["row_idx"]): (None if r["k"] is None else (int(r["k"]), int(r["cap"])))
                       for r in entry["picks"]}
                self.assertEqual(got, own[arm][j], "%s at %.2fx" % (arm, frac))
                self.assertEqual(len(got), len(own["cells"].select("eval")))
        # the split check accepts the grid the picks came from
        ev_ids = check_split(own["raw"], calib)
        self.assertEqual(sorted(ev_ids), sorted(int(own["cells"].idx[n]) for n in own["cells"].select("eval")))
        self.assertEqual(res["table1_accounting"], "expected")

    def test_reader_refuses_a_foreign_split_and_a_missing_block(self):
        d = _run_cli()
        _entry, calib, _res = load_picks(d, "lookup", 1.0)
        own = _alloc_own_picks()
        foreign = dict(calib, ids_before_promotion=calib["ids_before_promotion"][:-1])
        with self.assertRaises(SystemExit):
            check_split(own["raw"], foreign)
        with self.assertRaises(SystemExit):
            load_picks(d, "lookup", 0.33)
        with self.assertRaises(SystemExit):
            load_picks(d, "equation_n30x", 1.0)
        with self.assertRaises(SystemExit):
            load_picks(d, "lookup", 1.0, accounting="realised")
        with self.assertRaises(SystemExit):
            load_picks(tempfile.mkdtemp(), "lookup", 1.0)

    def test_recorded_prices_are_the_budgets(self):
        """The lookup arm caps every prompt at the budget; the average arm's recorded mean price
        is the mean of its picks' prices and runs at most 2 percent over the budget (the tolerance
        alloc itself flags), and within 2 percent of it wherever the multiplier binds."""
        d = _run_cli()
        for arm in ARMS:
            for frac in E.BUDGET_FRACTIONS:
                entry, _c, res = load_picks(d, arm, frac)
                X = float(entry["budget"])
                prices = [r["price"] for r in entry["picks"] if r["price"] is not None]
                self.assertTrue(prices, "%s at %.2fx has no priced pick" % (arm, frac))
                self.assertAlmostEqual(entry["mean_price"], float(np.mean(prices)), places=6)
                if arm == "lookup":
                    self.assertLessEqual(max(prices), X * (1 + 1e-9), "%s at %.2fx" % (arm, frac))
                    continue
                self.assertLessEqual(entry["mean_price"], 1.02 * X, "%s at %.2fx" % (arm, frac))
                row = res["table1_by_accounting"]["expected"]["rows"][arm]
                j = E.BUDGET_FRACTIONS.index(frac)
                self.assertAlmostEqual(row["mean_price_layer_passes"][j], entry["mean_price"], places=6)
                if row["lambda"][j] > 0 and not row["gate_reverted"][j]:
                    self.assertGreaterEqual(entry["mean_price"], 0.98 * X, "%s at %.2fx" % (arm, frac))


if __name__ == "__main__":
    unittest.main()
