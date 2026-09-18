"""Check the two weight tables the objective draws from: the commitment definitions, the budget and
depth formulas, the content pin, and that the realised draw reproduces the tables it was given."""
import json
import re
import sys
import types
from pathlib import Path

import numpy as np
import pytest

from test_recipe import (G, FakeTok, backend, cfg, tok, use_block_lens,   # noqa: F401  fixtures
                         CONFIG, Q, GOLD)

sys.path.insert(0, str(Path(G.__file__).parent))
import theory_weights as TW                                              # noqa: E402


# ================================================================= a synthetic grid
# Five caps and one depth. Three groups of questions, each with the read-out it shows at every cap:
# `X` is the read-out the question ends on and `Y` any other parse. A question is settled at the
# first cap from which the read-out never moves again, so the group's settle cap is one past its
# last `Y`. The label follows the read-out: `X` is right, `Y` is wrong.
CAPS = [0, 16, 32, 64, 128]
PLANTED = ((0.5, "XXXXX"),      # settles at cap 0
           (0.4, "XXYXX"),      # the read-out moves at 32, so it settles at 64
           (0.1, "XXXYX"))      # it moves at 64, so it settles at 128
FLAT = ((1.0, "XXXXX"),)        # everything settles at the first cap: nothing is ever unrealised
TEST_GRID = [0, 16, 32, 64, 128, None]      # the source grid the weights are read at


def tables(groups=PLANTED, n=200, caps=CAPS):
    """Return the commitment tables of a synthetic one-depth grid built from read-out patterns."""
    pred = np.empty((1, len(caps), n), dtype=object)
    acc = np.zeros((1, len(caps), n))
    i = 0
    for share, pattern in groups:
        assert len(pattern) == len(caps)
        for _ in range(int(round(share * n))):
            for j, ch in enumerate(pattern):
                pred[0, j, i] = ("str", ch.lower())
                acc[0, j, i] = 1.0 if ch == "X" else 0.0
            i += 1
    assert i == n, (i, n)
    return TW.commitment_tables(pred, acc, np.arange(n))


def test_the_settle_cap_is_the_first_cap_the_readout_never_moves_from_again():
    """Commitment is a suffix in the cap, so a read-out that moves at 32 is settled nowhere below 64."""
    tab = tables()
    s = tab["settle_index"][0]
    assert sorted(set(s.tolist())) == [0, 3, 4]                # caps 0, 64 and 128
    assert [float(x) for x in tab["G"][0]] == [0.5, 0.5, 0.5, 0.9, 1.0]
    never = tables(groups=((1.0, "XYX"),), n=10, caps=[0, 16, 32])
    assert never["G"][0].tolist() == [0.0, 0.0, 1.0]


def test_a_readout_that_never_parses_settles_nowhere():
    """A final read-out that does not parse is encoded BEYOND the last cap, never at it."""
    caps = [0, 16, 32]
    pred = np.empty((1, 3, 4), dtype=object)
    pred[:] = None
    acc = np.zeros((1, 3, 4))
    tab = TW.commitment_tables(pred, acc, np.arange(4))
    assert tab["G"][0].tolist() == [0.0, 0.0, 0.0]
    assert (tab["settle_index"][0] == len(caps)).all()


def test_a_planted_unrealised_peak_takes_the_largest_budget_weight():
    """The cap that leaves the most accuracy on the table must be the cap the draw prefers.

    Only at cap 32 is a large share of the mixture both unsettled and wrong: half the questions have
    not settled and their read-out there is right 20 percent of the time against 100 percent at the
    end. Cap 64 leaves a tenth of the mixture unrealised, and 0, 16 and 128 leave nothing.
    """
    tab = tables()
    gain = TW.unrealised_gain(tab)[0]
    assert np.argmax(gain) == CAPS.index(32)
    assert gain[CAPS.index(32)] == pytest.approx(0.4, abs=1e-9)
    assert gain[CAPS.index(64)] == pytest.approx(0.1, abs=1e-9)
    assert [gain[CAPS.index(T)] for T in (0, 16, 128)] == [0.0, 0.0, 0.0]
    w, raw = TW.budget_weights(tab, CAPS, TEST_GRID)
    assert max(w, key=w.get) == "32"
    assert w["32"] > w["64"] > w["0"] == w["16"] == w["128"]
    assert raw["32"] == pytest.approx(0.4, abs=1e-9)


def test_every_budget_keeps_half_the_uniform_share_and_the_no_limit_entry_takes_all_of_it():
    """The floor: the uniform half of the mixture means no cap of the grid is ever starved."""
    w, _raw = TW.budget_weights(tables(), CAPS, TEST_GRID)
    n = len(TEST_GRID)
    assert sum(w.values()) == pytest.approx(1.0, abs=1e-12)
    assert min(w.values()) == pytest.approx(TW.UNIFORM_MIX / n, abs=1e-12)
    assert all(v >= TW.UNIFORM_MIX / n - 1e-12 for v in w.values()), w
    assert w["none"] == pytest.approx(1.0 / n, abs=1e-12)


def test_a_source_with_nothing_unrealised_draws_uniformly():
    """No signal is not a licence to pick a cap by floating-point noise."""
    w, raw = TW.budget_weights(tables(groups=FLAT), CAPS, TEST_GRID)
    assert set(raw.values()) == {0.0}
    assert all(v == pytest.approx(1.0 / len(TEST_GRID), abs=1e-12) for v in w.values()), w


def test_a_budget_the_grid_never_measured_is_refused():
    """The settle cap is found by looking at every cap through the last, so a weight at an unmeasured cap is not the same quantity."""
    with pytest.raises(SystemExit) as raised:
        TW.budget_weights(tables(), CAPS, [0, 16, 48, None])
    assert "measured caps" in str(raised.value)


# ================================================================= the shipped tables
@pytest.fixture
def shipped():
    return json.loads(Path(G.THEORY_WEIGHTS).read_text(encoding="utf-8"))


def test_the_config_pins_the_shipped_theory_weights(cfg):
    """The two tables ARE the objective, so they are pinned by content exactly like the pool."""
    assert re.fullmatch(r"[0-9a-f]{64}", str(cfg["theory_weights_sha256"]))
    assert G.check_theory_weights(cfg) == str(cfg["theory_weights_sha256"])


def test_the_theory_weights_file_is_pinned_by_sha256(tmp_path, cfg, shipped):
    """An edited weight file must stop stage 2, not silently retrain on another distribution."""
    p = tmp_path / "theory_weights.json"
    p.write_text(json.dumps(shipped), encoding="utf-8")
    cfg["theory_weights_sha256"] = G.file_sha256(str(p))
    assert G.check_theory_weights(cfg, str(p)) == cfg["theory_weights_sha256"]
    edited = json.loads(json.dumps(shipped))
    edited["sources"]["gsm8k"]["budget_weights"]["0"] += 0.01
    p.write_text(json.dumps(edited), encoding="utf-8")
    with pytest.raises(SystemExit) as raised:
        G.check_theory_weights(cfg, str(p))
    assert "theory_weights_sha256 mismatch" in str(raised.value)
    with pytest.raises(SystemExit) as gone:
        G.check_theory_weights(cfg, str(tmp_path / "absent.json"))
    assert "MISSING" in str(gone.value)


def test_a_table_that_does_not_cover_a_source_grid_is_refused(tmp_path, cfg, shipped):
    """A cap with no weight, or a weight at a cap the source never draws, is a different draw."""
    edited = json.loads(json.dumps(shipped))
    edited["sources"]["gsm8k"]["budget_weights"].pop("1024")
    p = tmp_path / "tw.json"
    p.write_text(json.dumps(edited), encoding="utf-8")
    cfg["theory_weights_sha256"] = G.file_sha256(str(p))
    with pytest.raises(SystemExit) as raised:
        G.load_theory_weights(cfg, str(p))
    assert "budget weights cover" in str(raised.value)


def test_the_shipped_tables_cover_every_source_and_are_probabilities(cfg, shipped):
    """Every source of the mixture has both tables, over its own grid and the config's depths."""
    tw, sha = G.load_theory_weights(cfg)
    assert sha == str(cfg["theory_weights_sha256"])
    assert sorted(tw["sources"]) == sorted(cfg.sources)
    for src in cfg.sources:
        grid, p = G.budget_draw(cfg, tw, "budget_longest", src)
        assert grid == cfg.budget_grid_for(src)
        assert p.sum() == pytest.approx(1.0) and p.min() > 0
        depths, q = G.depth_draw(cfg, tw, "budget_longest", src)
        assert depths == cfg.depths
        assert q.sum() == pytest.approx(1.0) and q.min() > 0
    assert shipped["split"] == "cal"
    for src, files in shipped["grid_files"].items():
        assert sorted(files) == ["k%d" % d for d in cfg.depths], src
        assert all(re.fullmatch(r"[0-9a-f]{64}", f["sha256"]) for f in files.values()), src


def test_the_depth_mix_is_half_uniform_and_then_the_deepest_depth_is_floored(shipped):
    """The depth draw is mixed like the budget draw, and only then is the deepest depth raised.

    w = 0.5 * uniform + 0.5 * the allocator's usage. If that mixture still leaves the deepest depth
    under the floor, it is raised to the floor and the shallower depths keep their proportions to
    each other inside the remaining 1 - floor.
    """
    floor = float(shipped["deepest_depth_floor"])
    mix = float(shipped["uniform_mix"])
    ks = [str(int(k)) for k in shipped["depths"]]
    deep = ks[-1]
    for src, s in shipped["sources"].items():
        raw = {k: float(s["depth_weights_before_floor"][k]) for k in ks}
        assert sum(raw.values()) == pytest.approx(1.0, abs=1e-9), src
        want = {k: mix / len(ks) + (1.0 - mix) * raw[k] for k in ks}
        if want[deep] < floor:
            scale = (1.0 - floor) / sum(want[k] for k in ks[:-1])
            want = {k: want[k] * scale for k in ks[:-1]} | {deep: floor}
        assert sorted(s["depth_weights"]) == sorted(ks), src
        for k in ks:
            assert float(s["depth_weights"][k]) == pytest.approx(want[k], abs=1e-9), (src, k)
        assert sum(float(v) for v in s["depth_weights"].values()) == pytest.approx(1.0, abs=1e-12)
        assert min(float(v) for v in s["depth_weights"].values()) >= mix / len(ks) - 1e-12, src
    assert any(min(s["depth_weights_before_floor"].values()) == 0.0
               for s in shipped["sources"].values())


def test_the_deepest_depth_is_never_starved(cfg, shipped):
    """The deepest depth is the released default and the cell Table 1 checks at 1.0x.

    Whatever the allocator ranks it, no source may train the checkpoint's own operating point below
    the floor, or the non-inferiority row of Table 1 would be read off a starved depth.
    """
    assert float(shipped["deepest_depth_floor"]) == 0.20
    deep = str(int(cfg.depths[-1]))
    assert deep == str(int(max(int(k) for k in shipped["depths"])))
    for src, s in shipped["sources"].items():
        assert float(s["depth_weights"][deep]) >= 0.20 - 1e-12, (src, s["depth_weights"])


# ================================================================= the realised draw
def draw_run(tmp_path, cfg, tok, monkeypatch, arm, budget, chains=None):
    """Run stage 2 on a synthetic pool and return its manifest."""
    chains = chains or {"gsm8k": "A" * 40, "math": "M" * 60}
    transformers = types.ModuleType("transformers")
    transformers.AutoTokenizer = types.SimpleNamespace(from_pretrained=lambda *a, **k: tok)
    monkeypatch.setitem(sys.modules, "transformers", transformers)
    monkeypatch.setattr(FakeTok, "pad_token", 0, raising=False)
    monkeypatch.setattr(FakeTok, "eos_token", 1, raising=False)
    pool = tmp_path / "pool.jsonl"
    pool.write_text("".join(json.dumps(
        {"src": src, "pool_i": i, "question": "%s %s #%d" % (Q, src, i), "gold": GOLD}) + "\n"
        for src in chains for i in range(40)), encoding="utf-8")
    cfg["pool_jsonl"] = str(pool)
    cfg["pool_sha256"] = G.file_sha256(str(pool))
    cfg["harvest"] = {s: dict(cfg["harvest"][s]) for s in chains}
    use_block_lens(cfg, 512, micro=4, blocks=8)
    cfg["supervised_token_budget"] = budget
    P = G.paths(str(tmp_path))
    G.ensure_dirs(P)
    for src, chain in chains.items():
        for tag in ("A", "B"):
            Path(P["artifacts"], "harvest_%s_%s_k4.jsonl" % (src, tag)).write_text("".join(
                json.dumps({"pool_i": i, "kept": True, "chain": chain,
                            "question": "%s %s #%d" % (Q, src, i)}) + "\n" for i in range(40)),
                encoding="utf-8")
    monkeypatch.setattr(G, "load_config", lambda *a, **k: cfg)
    assert G.main(["--arm=%s" % arm, "--root=%s" % tmp_path]) == 0
    return json.loads(Path(P["artifacts"], "target_manifest_%s.json" % arm)
                      .read_text(encoding="utf-8"))


def test_the_draw_histograms_match_the_weights_on_a_large_draw(tmp_path, cfg, tok, monkeypatch):
    """The objective on disk is the objective on paper: V10, on a manifest of thousands of visits."""
    man = draw_run(tmp_path, cfg, tok, monkeypatch, "budget_longest", 200000)
    assert man["n_visits"] > 5000, man["n_visits"]
    assert man["draw_rule"] == "theory"
    assert man["theory_weights_sha256"] == str(cfg["theory_weights_sha256"])
    v10 = man["v10_draw_weights"]
    assert v10["ok"], v10["by_source"]
    assert v10["worst"] <= 0.02, v10["worst"]
    assert set(v10["by_source"]) == {"budget_gsm8k", "budget_math", "depth_gsm8k", "depth_math"}
    for name, rec in v10["by_source"].items():
        assert rec["sampling_bound_binds"] is False, name       # 0.05 is what binds at this n
        for k, w in rec["intended"].items():
            assert rec["realised"][k] == pytest.approx(w, abs=0.05), (name, k)
    assert man["draw_weights_intended"]["budget"]["math"] == \
        {k: pytest.approx(v) for k, v in
         json.loads(Path(G.THEORY_WEIGHTS).read_text(encoding="utf-8"))
         ["sources"]["math"]["budget_weights"].items()}


def test_uniform_longest_reproduces_the_old_uniform_draw(tmp_path, cfg, tok, monkeypatch):
    """The ablation differs from the recipe in the draw and in nothing else."""
    recipe, ablation = cfg.arm("budget_longest"), cfg.arm("uniform_longest")
    assert {k: v for k, v in ablation.items() if k != "draw"} == \
           {k: v for k, v in recipe.items() if k != "draw"}
    assert G.uses_theory(cfg, "budget_longest") and not G.uses_theory(cfg, "uniform_longest")
    tw, _sha = G.load_theory_weights(cfg)
    for src in cfg.sources:
        grid, p = G.budget_draw(cfg, tw, "uniform_longest", src)
        assert list(p) == [pytest.approx(1.0 / len(grid))] * len(grid)
        _d, q = G.depth_draw(cfg, tw, "uniform_longest", src)
        assert list(q) == [pytest.approx(float(cfg["depth_probabilities"][d])) for d in cfg.depths]
    man = draw_run(tmp_path, cfg, tok, monkeypatch, "uniform_longest", 200000)
    assert man["draw_rule"] == "uniform"
    assert man["v10_draw_weights"]["ok"], man["v10_draw_weights"]["by_source"]
    for src in ("gsm8k", "math"):
        n = len(cfg.budget_grid_for(src))
        assert man["draw_weights_intended"]["budget"][src] == \
            {G.budget_key(t): pytest.approx(1.0 / n) for t in cfg.budget_grid_for(src)}
        assert man["draw_weights_intended"]["depth"][src] == \
            {str(d): pytest.approx(float(cfg["depth_probabilities"][d])) for d in cfg.depths}


def test_v10_catches_a_draw_that_missed_a_weight():
    """A gate that cannot fail proves nothing: a histogram that starved one budget must fail it."""
    intended = {"0": 0.25, "16": 0.25, "32": 0.25, "none": 0.25}
    man = {"arm": "budget_longest", "draw_rule": "theory",
           "draw_weights_intended": {"budget": {"gsm8k": intended}, "depth": {}},
           "visits_by_src_T": {"gsm8k": {"0": 3000, "16": 3000, "32": 3000, "none": 3000}},
           "visits_by_src_depth": {}}
    assert G.v10_draw_weights(man)["ok"]
    man["visits_by_src_T"]["gsm8k"] = {"0": 5000, "16": 3000, "32": 3000, "none": 1000}
    bad = G.v10_draw_weights(man)
    assert not bad["ok"]
    assert bad["by_source"]["budget_gsm8k"]["worst_key"] in ("0", "none")
    assert bad["worst"] > 0.05
    assert G.weight_deviation(intended, {}) == pytest.approx(0.25)


def test_v10_allows_only_the_sampling_error_of_a_small_manifest():
    """Below a few thousand visits the multinomial error of the histogram exceeds 0.05, and that,
    not 0.05, is the honest bound; the fixed 0.05 must bind on a full manifest."""
    assert G.draw_allowance(0.25, 200) > 0.05
    assert G.draw_allowance(0.25, 30000) == pytest.approx(0.05)
    assert G.draw_allowance(0.0, 10) == pytest.approx(0.05)


def test_the_readme_prints_both_formulas_and_both_weight_tables():
    """The tables a reviewer reads for plausibility live beside the formulas that produced them."""
    text = Path(G.__file__).resolve().parent.joinpath("README.md").read_text(encoding="utf-8")
    head = text[text.index("## Where the theory enters the objective"):text.index("## Ablations")]
    assert "clip( (1 - G_k(T)) * (c_k(>T) - l_k(T)) , 0 )" in head
    assert "(L_fixed + kL)(P + E_cal[min(len_k, T)] + R)" in head
    shipped = json.loads(Path(G.THEORY_WEIGHTS).read_text(encoding="utf-8"))["sources"]
    for src, s in shipped.items():
        assert "`%s`" % src in head, src
        for k, v in s["budget_weights"].items():
            assert "%.3f" % v in head, (src, k, v)
        for k, v in s["depth_weights"].items():
            assert "%.3f" % v in head, (src, k, v)
    assert "V10" in text and "theory_weights_sha256" in text
