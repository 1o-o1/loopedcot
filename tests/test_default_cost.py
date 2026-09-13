"""Fix 2 (PP3b, decision 7): "budget as a fraction of the default cost" is the MEAN REALISED
layer-pass cost of the default operating point (max measured depth, natural stop, uncapped) -- not
the grid's largest CAP cell (the old `X = budget_fraction * cmat.max()`).

  python -m pytest tests/test_default_cost.py -q
  python tests/test_default_cost.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prod.analyze.allocate import default_cost                       # noqa: E402
from prod.score import Cells                                         # noqa: E402


def _row(k, B, idx, natural_stop, n_cut, layer_passes, layer_passes_pf, n_prompt_tokens):
    return {"k": k, "B": B, "idx": idx, "natural_stop": natural_stop, "n_cut": n_cut,
            "layer_passes": layer_passes, "layer_passes_promptfree": layer_passes_pf,
            "n_prompt_tokens": n_prompt_tokens, "n_answer_tokens": 8, "n_suffix_tokens": 4,
            "split": "eval", "correct_v2": True, "model": "toy", "task": "toy",
            "protocol": "natural"}


def _synthetic_rows():
    """Two problems, k in {1, 2}, B in {0, 16, 64}. Problem 10 stops at 10 (first uncapped at
    B=16); problem 11 stops at 40 (first uncapped at B=64). k=2 is the max depth present, so it is
    the default absent an explicit k. `layer_passes` is a deterministic, distinct-per-cell synthetic
    value (100000*k + 1000*idx + B) so picking the WRONG cell is caught, not averaged away."""
    rows = []
    nstop = {10: 10, 11: 40}
    for k in (1, 2):
        for idx in (10, 11):
            ns = nstop[idx]
            for B in (0, 16, 64):
                cut = min(ns, B)
                lp = 100000 * k + 1000 * idx + B
                rows.append(_row(k, B, idx, ns, cut, float(lp), float(lp) - 50.0,
                                 n_prompt_tokens=100 + idx))
    return rows


def test_default_cost_picks_the_smallest_uncapped_cap_per_problem():
    cells = Cells(_synthetic_rows(), label="v2")
    dc = default_cost(cells, promptfree=False)
    assert dc["k"] == 2                              # the max depth present, no explicit k given
    assert dc["n"] == 2
    # idx10 first uncapped at B=16 -> lp = 100000*2 + 1000*10 + 16 = 210016
    # idx11 first uncapped at B=64 -> lp = 100000*2 + 1000*11 + 64 = 211064
    assert abs(dc["mean"] - (210016 + 211064) / 2.0) < 1e-6


def test_default_cost_promptfree_variant():
    cells = Cells(_synthetic_rows(), label="v2")
    dc = default_cost(cells, promptfree=True)
    assert abs(dc["mean"] - ((210016 - 50) + (211064 - 50)) / 2.0) < 1e-6


def test_default_cost_explicit_k():
    cells = Cells(_synthetic_rows(), label="v2")
    dc1 = default_cost(cells, promptfree=False, k=1)
    assert dc1["k"] == 1
    # idx10 -> 100000*1 + 1000*10 + 16 = 110016 ; idx11 -> 100000*1 + 1000*11 + 64 = 111064
    assert abs(dc1["mean"] - (110016 + 111064) / 2.0) < 1e-6


def test_default_cost_never_uncapped_is_none_not_a_wrong_number():
    """Every cap truncates the natural stop: the function must report None, never silently fall
    back to a capped (and therefore wrong) number."""
    rows = [_row(2, 0, 10, natural_stop=999, n_cut=0, layer_passes=1.0, layer_passes_pf=1.0,
                n_prompt_tokens=100)]
    cells = Cells(rows, label="v2")
    dc = default_cost(cells, promptfree=False)
    assert dc["mean"] is None
    assert dc["n"] == 0


def test_default_cost_differs_from_grid_max():
    """The regression this fix guards against: the old `cmat.max()` definition and the new mean-
    at-natural-stop definition must not coincide on a grid where they clearly should differ."""
    cells = Cells(_synthetic_rows(), label="v2")
    dc = default_cost(cells, promptfree=False)
    grid_max_cell = max(r["layer_passes"] for r in _synthetic_rows() if r["k"] == 2)
    assert dc["mean"] != grid_max_cell


if __name__ == "__main__":
    fs = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for f in fs:
        f()
        print("ok", f.__name__)
    print("%d test functions" % len(fs))
