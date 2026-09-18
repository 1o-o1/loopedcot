"""Turn the base model's measured commitment into the budget and depth weights the objective draws from.

Stage 0 of the recipe, CPU, run once. It reads the base model's PRODUCTION grid -- the same
`cells_ouro_1_4b_base_<task>_natural_k{1,2,3,4}.jsonl` files Table 1 is placed beside -- and writes
`train/data/theory_weights.json`: one budget table and one depth table per training source.

Nothing here imports `alloc`. The two definitions the paper's theory rests on are COPIED below, with
their contracts restated, so this stage is readable on its own and cannot drift when the analysis
package moves:

  commitment    a question is SETTLED at token cap T when its forced read-out at T and at every cap
                after it equals the last cap's read-out AND parses. Label free: only read-outs are
                read. The Boolean is a suffix in the cap by construction, so the SETTLE CAP -- the
                first settled cap -- is well defined, and a question whose read-out never stops
                moving, or whose final read-out does not parse, is encoded BEYOND the last cap.
  the identity  G_k(T) is the settled share, c_k(j) the accuracy of the questions that settle at cap
                j, l_k(T) the accuracy at T of the questions NOT settled by T, and c_k(>T) the
                accuracy those same not-yet-settled questions reach at the last cap.

Only the CALIBRATION split enters either table; the evaluation half of the base grid is never read.

The two weights, in words:

  budget   w(T) is proportional to the accuracy the base model LEAVES ON THE TABLE by stopping at T:
           the share of questions not yet settled at T times how much more of them are right once
           they are allowed to finish. Averaged over depths, clipped at zero, and then mixed half
           and half with the uniform draw, so no budget of the source's grid is ever starved. The
           no-limit entry is given the uniform share outright: it has no cap to leave anything at.
  depth    the share of calibration prompts an average-budget lookup allocator assigns to each
           depth, pooled over 16 log-spaced compute budgets between the cheapest cell of the grid
           and the cost of the default operating point, priced (L_fixed + kL)(P + E_cal[min(len_k,T)]
           + R). Mixed half and half with the uniform draw, the same rule as the budget weights, so
           no depth is starved; then the DEEPEST depth is raised to at least 0.20 and the shallower
           depths keep their proportions inside what is left. The deepest depth is the released
           default and the cell Table 1 checks at 1.0x, so the mixture may not starve it.

    python train/theory_weights.py --cells-dir=<dir of the base grids> [--out=<json>]
    sha256sum train/data/theory_weights.json   # paste into config.yaml as theory_weights_sha256
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import targets as G                                            # noqa: E402  the shared library

# The grid the weights are read off: the base model's own production cells, one file per depth.
CELL_PATTERN = "cells_ouro_1_4b_base_%s_natural_k%d.jsonl"
CELLS_DIR_CANDIDATES = ("E:/Research/loopedcot/artifacts",
                        "~/loopedcot/artifacts", "~/latent-loop/loopedcot/artifacts")
# Training source -> the evaluation task whose base grid carries its measurements. Same mapping the
# config's `harvest.<src>.eval_task` carries; asserted against it rather than trusted.
GRID_TASK = {"gsm8k": "gsm8k", "math": "math500", "csqa": "csqa", "aqua": "aqua"}

# Ouro-1.4B holds its whole 24-layer stack inside the recurrence, so a token at depth k costs
# k * 24 layer passes and nothing is paid outside the loop.
L_LOOP = 24
L_FIXED = 0
# The read-out reserve: the forced suffix the row measured plus the task's answer allowance. Same
# allowances as `config.yaml: n_answer_tokens`, asserted against it.
ANSWER_ALLOWANCE = {"gsm8k": 12, "math500": 32}
ANSWER_ALLOWANCE_DEFAULT = 8

N_BUDGETS = 16          # log-spaced compute budgets the depth allocator is run at
AVG_ITERS = 80          # bisection steps for the multiplier; the spend is a step function of it
BUDGET_TOL = 1e-9       # a grid point built by exponentiating a logarithm can land an ulp low
UNIFORM_MIX = 0.5       # w = UNIFORM_MIX * uniform + (1 - UNIFORM_MIX) * the theory weight
DEEPEST_DEPTH_FLOOR = 0.20   # the deepest depth is the released default; the mix never starves it

BUDGET_FORMULA = ("w(T) proportional to mean over depths k of clip((1 - G_k(T)) * (c_k(>T) - "
                  "l_k(T)), 0), normalised over the source's numeric budgets and then mixed "
                  "w = 0.5 * uniform + 0.5 * normalised; the no-limit entry takes the uniform "
                  "share. G_k(T) is the settled share at cap T, c_k(>T) the last-cap accuracy of "
                  "the questions not settled by T, l_k(T) their accuracy at T. Calibration split "
                  "only.")
DEPTH_FORMULA = ("the share of calibration prompts an average-budget lookup allocator assigns to "
                 "each depth, pooled over 16 log-spaced budgets from the cheapest cell of the "
                 "median-prompt cost matrix to the default cost (deepest depth at natural stop), "
                 "priced (L_fixed + kL)(P + E_cal[min(len_k, T)] + R) with L=24, L_fixed=0 and "
                 "R = suffix + answer allowance; normalised and then mixed w = 0.5 * uniform + "
                 "0.5 * normalised, the same rule as the budget weights; then the deepest depth is "
                 "raised to at least 0.20 and the shallower depths rescaled to 1 - 0.20, because "
                 "the deepest depth is the released default Table 1 checks at 1.0x.")


# ================================================================= reading one grid file
def _norm_answer(p):
    """Return a comparable key for a read-out, or None when it does not parse; numbers round to six decimals."""
    if p is None or p in ("None", ""):
        return None
    s = str(p).strip().strip("()").strip().lower().replace(",", "")
    try:
        return ("num", round(float(s), 6))
    except ValueError:
        return ("str", s)


def _label_v2(r):
    """Return the protocol-v2 correctness label of one row: the own answer inside the cut when it parsed, else the forced read-out."""
    if r.get("correct_v2") is not None:
        return bool(r["correct_v2"] in (True, "True"))
    if r.get("trace_answer") not in (None, "None", ""):
        return bool(r.get("trace_correct") in (True, "True"))
    return bool(r.get("correct") in (True, "True"))


def _f(x, default=np.nan):
    """Return a numeric field as a float, or the default when it is missing or unparseable."""
    if x is None:
        return default
    try:
        return float(x)
    except (TypeError, ValueError):
        return default


def answer_allowance(task):
    """Return the task's answer allowance in tokens; it never depends on the realised read-out length."""
    return int(ANSWER_ALLOWANCE.get(task, ANSWER_ALLOWANCE_DEFAULT))


def read_grid_rows(path):
    """Return the data rows of one base-grid JSONL and its header; the `_header` line and any `extra` row are dropped."""
    rows, header = [], None
    with open(os.path.expanduser(path), encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            if r.get("_header"):
                header = r
                continue
            if r.get("extra", False):
                continue
            rows.append(r)
    if not rows:
        raise SystemExit("no rows in %s" % path)
    return rows, header


class Grid(object):
    """One task's base grid as (depth, token cap, prompt) arrays, read off the rows.

    `pred` holds the parsed forced read-out of every cell (None when it does not parse) and is the
    only field commitment reads. `acc` is the protocol-v2 label. `ptok` and `reserve` are per prompt
    and must not depend on the cell: a reserve that moved with the cap would price a cell with the
    generation it is buying.
    """

    def __init__(self, rows, task):
        self.task = task
        self.ks = sorted({int(r["k"]) for r in rows})
        self.caps = sorted({int(r["B"]) for r in rows})
        self.idx = sorted({int(r.get("row_idx", r["idx"])) for r in rows})
        ki = {k: i for i, k in enumerate(self.ks)}
        bi = {b: i for i, b in enumerate(self.caps)}
        ni = {n: i for i, n in enumerate(self.idx)}
        shape = (len(self.ks), len(self.caps), len(self.idx))
        self.acc = np.full(shape, np.nan)
        self.pred = np.empty(shape, dtype=object)
        self.nstop = np.full(shape, np.nan)
        self.ncut = np.full(shape, np.nan)
        self.passes = np.full(shape, np.nan)
        self.ptok = np.full(len(self.idx), np.nan)
        self.reserve = np.full(len(self.idx), np.nan)
        self.split = np.empty(len(self.idx), dtype=object)
        for r in rows:
            a, c = ki[int(r["k"])], bi[int(r["B"])]
            n = ni[int(r.get("row_idx", r["idx"]))]
            self.acc[a, c, n] = float(_label_v2(r))
            self.pred[a, c, n] = _norm_answer(r.get("pred"))
            self.nstop[a, c, n] = _f(r.get("natural_stop"))
            self.ncut[a, c, n] = _f(r.get("n_cut"))
            self.passes[a, c, n] = _f(r.get("layer_passes"))
            p = float(r["n_prompt_tokens"])
            res = float(r.get("n_suffix_tokens", 0)) + answer_allowance(task)
            if not np.isnan(self.reserve[n]) and (self.reserve[n] != res or self.ptok[n] != p):
                raise SystemExit("%s: question %d prices differently in two cells; the prompt "
                                 "length and the reserve must not depend on the cell"
                                 % (task, self.idx[n]))
            self.ptok[n], self.reserve[n] = p, res
            self.split[n] = r.get("split", "eval")
        missing = np.argwhere(np.isnan(self.acc))
        if len(missing):
            a, c, n = missing[0]
            raise SystemExit("%s: %d cells have no label, first (k=%d, T=%d, id=%d)"
                             % (task, len(missing), self.ks[a], self.caps[c], self.idx[n]))

    def select(self, split="cal"):
        """Return the zero-based prompt positions of one split."""
        return np.array([i for i, s in enumerate(self.split) if s == split], dtype=int)


def load_grid(cells_dir, task, depths):
    """Return one task's Grid over the requested depths, plus the sha256 of every file it read."""
    rows, files = [], {}
    for k in depths:
        p = os.path.join(os.path.expanduser(cells_dir), CELL_PATTERN % (task, int(k)))
        if not os.path.exists(p):
            raise SystemExit("MISSING base grid %s" % p)
        rk, _h = read_grid_rows(p)
        got = sorted({int(r["k"]) for r in rk})
        if got != [int(k)]:
            raise SystemExit("%s holds depths %s, expected only k=%d" % (p, got, k))
        rows.extend(rk)
        files["k%d" % int(k)] = {"path": p, "sha256": G.file_sha256(p)}
    grid = Grid(rows, task)
    if grid.ks != [int(k) for k in depths]:
        raise SystemExit("%s: grid holds depths %s, the config asks for %s"
                         % (task, grid.ks, list(depths)))
    return grid, files


# ================================================================= definition 1: commitment
def commitment(pred, pos):
    """Return the settled Boolean at every measured cap, for the given prompt positions.

    COPIED definition, not imported. A question is settled at cap T when its forced read-out at T
    and at every cap AFTER it equals the LAST cap's read-out and parses. The scan runs from the last
    cap backwards, so the Boolean is a suffix in the cap by construction. A cell whose read-out does
    not parse is `None` and can never equal anything, so a question whose final read-out does not
    parse is settled nowhere. No label is read: commitment is label free.
    """
    pred = np.asarray(pred, dtype=object)
    nk, nb = pred.shape[0], pred.shape[1]
    A = np.zeros((nk, nb, len(pos)), bool)
    for a in range(nk):
        for ii, n in enumerate(pos):
            fin = pred[a, -1, n]
            if fin is None:
                continue
            ok = True
            for j in range(nb - 1, -1, -1):
                ok = ok and (pred[a, j, n] == fin)
                A[a, j, ii] = ok
    return A


def settle_index(A):
    """Return the FIRST settled cap index per (depth, prompt); the number of caps means never settled.

    COPIED definition, not imported. `len(caps)` is BEYOND the last cap, never equal to it, so a
    question whose read-out never stops moving sorts after every cap rather than at the last one.
    """
    nb = A.shape[1]
    return np.where(A.any(1), A.argmax(1), nb)


# ================================================================= definition 2: the identity
def commitment_tables(pred, acc, pos):
    """Return G_k(T), c_k(j), l_k(T) and c_k(>T) as (depth, cap) tables over the given prompts.

    G_k(T)    the settled share at cap T.
    c_k(j)    the accuracy of the questions whose settle cap IS j. A settled question carries the
              same read-out, and so the same label, at every cap from j on, so this is read at the
              last cap and is the accuracy that question ends with.
    l_k(T)    the accuracy AT T of the questions not settled by T: what stopping at T actually buys
              on the part of the mixture that has not made up its mind.
    c_k(>T)   the accuracy those SAME questions reach at the last cap. The gap c_k(>T) - l_k(T) is
              therefore the accuracy per unsettled question that stopping at T gives up.

    A table entry with no questions behind it is NaN, never a silent zero.
    """
    A = commitment(pred, pos)
    s = settle_index(A)
    acc = np.asarray(acc, float)[:, :, pos]
    nk, nb = A.shape[0], A.shape[1]
    Gt = A.mean(2)
    c_at, l_at, c_after, n_after = (np.full((nk, nb), np.nan) for _ in range(4))
    for a in range(nk):
        final = acc[a, -1, :]
        for j in range(nb):
            at_j = (s[a] == j)
            if at_j.any():
                c_at[a, j] = float(np.nanmean(final[at_j]))
            later = (s[a] > j)
            n_after[a, j] = int(later.sum())
            if later.any():
                l_at[a, j] = float(np.nanmean(acc[a, j, later]))
                c_after[a, j] = float(np.nanmean(final[later]))
    return {"G": Gt, "c_by_settle_cap": c_at, "l_by_cap": l_at, "c_after_cap": c_after,
            "n_after_cap": n_after, "settle_index": s, "n_prompts": int(len(pos))}


def unrealised_gain(tables):
    """Return the (depth, cap) accuracy a cap LEAVES ON THE TABLE: (1 - G_k(T)) * (c_k(>T) - l_k(T)), clipped at zero.

    A cap where every question has settled has no unsettled population, so `c_k(>T)` and `l_k(T)`
    are NaN there; the share (1 - G) is zero at that cap too, so the term is zero and not a hole.
    """
    share = 1.0 - np.asarray(tables["G"], float)
    gap = np.asarray(tables["c_after_cap"], float) - np.asarray(tables["l_by_cap"], float)
    out = np.where(np.isfinite(gap), share * np.nan_to_num(gap, nan=0.0), 0.0)
    return np.clip(out, 0.0, None)


# ================================================================= the budget table
def budget_weights(tables, caps, grid, uniform_mix=UNIFORM_MIX):
    """Return one source's budget draw weights, keyed the way every artifact spells a cap.

    `caps` are the grid's measured caps and `grid` the source's own budget grid, ending in None for
    the no-limit draw. Every numeric entry of `grid` must be a measured cap: the settle cap of a
    question is found by looking at every cap through the last, so a weight read at a cap the grid
    never measured would not be the same quantity.

    w = uniform_mix * uniform + (1 - uniform_mix) * q, where q puts the uniform share on the
    no-limit entry and splits the rest in proportion to `unrealised_gain` over the numeric caps.
    Every entry is therefore at least `uniform_mix / len(grid)` -- the floor -- and the no-limit
    entry is exactly the uniform share.
    """
    caps = [int(c) for c in caps]
    nums = [t for t in grid if t is not None]
    unknown = [t for t in nums if int(t) not in caps]
    if unknown:
        raise SystemExit("budget(s) %s are not measured caps %s; the settled Boolean is not "
                         "defined at a cap the grid never ran" % (unknown, caps))
    n = len(grid)
    if n < 2 or grid[-1] is not None:
        raise SystemExit("the budget grid must end in the no-limit draw, got %r" % (grid,))
    u = 1.0 / n
    gain = unrealised_gain(tables)
    raw = np.array([float(np.mean(gain[:, caps.index(int(t))])) for t in nums])
    total = float(raw.sum())
    if total > 0:
        q = (1.0 - u) * raw / total
    else:
        # a source whose base model leaves nothing unrealised anywhere has no signal to follow; the
        # draw stays uniform rather than picking a cap by floating-point noise
        q = np.full(len(nums), (1.0 - u) / len(nums))
    w = {G.budget_key(t): uniform_mix * u + (1.0 - uniform_mix) * float(qi)
         for t, qi in zip(nums, q)}
    w[G.budget_key(None)] = u
    return w, {G.budget_key(t): float(r) for t, r in zip(nums, raw)}


# ================================================================= the depth table
def natural_lengths(grid, pos):
    """Return the (depth, prompt) generated length in tokens when the chain is not cut, in tokens.

    Read from `natural_stop` at the cap standing for natural stop -- the largest measured cap --
    falling back to that cap's `n_cut` and then to the largest `n_cut` the depth measured, and
    clipped at the horizon, so a chain that never stopped is counted at the horizon rather than
    dropped.
    """
    horizon = float(grid.caps[-1])
    out = np.full((len(grid.ks), len(pos)), np.nan)
    for a in range(len(grid.ks)):
        for ii, n in enumerate(pos):
            v = grid.nstop[a, -1, n]
            if np.isnan(v):
                v = grid.ncut[a, -1, n]
            if np.isnan(v):
                row = grid.ncut[a, :, n]
                v = float(np.nanmax(row)) if np.isfinite(row).any() else np.nan
            out[a, ii] = min(v, horizon) if not np.isnan(v) else np.nan
    return out


def expected_lengths(grid, cal_pos):
    """Return the (depth, cap) table E_cal[min(len_k, T)] in tokens, over the calibration prompts only.

    A decision-time price: the table is fixed before any evaluation prompt is generated, and the
    prompt's own realised length -- not known when the cell is chosen -- never enters its price.
    """
    lens = natural_lengths(grid, cal_pos)
    out = np.full((len(grid.ks), len(grid.caps)), np.nan)
    for a in range(len(grid.ks)):
        row = lens[a][np.isfinite(lens[a])]
        if not len(row):
            continue
        for c, T in enumerate(grid.caps):
            out[a, c] = float(np.minimum(row, float(T)).mean())
    return out


def price_tensor(grid, pos, expected, L=L_LOOP, L_fixed=L_FIXED):
    """Return the (depth, cap, prompt) price in layer-token passes: (L_fixed + kL)(P + E_cal[min(len_k,T)] + R)."""
    w = np.array([L_fixed + int(k) * L for k in grid.ks], float)[:, None, None]
    body = np.asarray(expected, float)[:, :, None] \
        + (grid.ptok[pos] + grid.reserve[pos])[None, None, :]
    return w * body


def cost_matrix(grid, expected, pos, L=L_LOOP, L_fixed=L_FIXED):
    """Return the (depth, cap) price of the MEDIAN calibration prompt, in layer-token passes."""
    Pm = float(np.median(grid.ptok[pos]))
    Rm = float(np.median(grid.reserve[pos]))
    w = np.array([L_fixed + int(k) * L for k in grid.ks], float)[:, None]
    return w * (np.asarray(expected, float) + Pm + Rm), Pm, Rm


def default_cost(grid, pos):
    """Return the mean realised layer-token cost of the DEFAULT operating point on these prompts.

    The default is the deepest depth run to natural stop. Per prompt that is the cheapest cap whose
    cut did not bite (`n_cut >= natural_stop`); a prompt that never stopped is counted at the
    horizon rather than skipped, and its share is reported.
    """
    a = len(grid.ks) - 1
    vals, n_hor = [], 0
    for n in pos:
        ok = [j for j in range(len(grid.caps))
              if not (np.isnan(grid.nstop[a, j, n]) or np.isnan(grid.ncut[a, j, n]))
              and grid.ncut[a, j, n] >= grid.nstop[a, j, n] - 1e-9]
        if ok:
            j = min(ok, key=lambda j: grid.caps[j])
        else:
            j = len(grid.caps) - 1
            n_hor += 1
        v = grid.passes[a, j, n]
        if not np.isnan(v):
            vals.append(float(v))
    if not vals:
        raise SystemExit("no realised cost at the default cell")
    return {"k": int(grid.ks[-1]), "n": len(vals), "mean": float(np.mean(vals)),
            "n_at_horizon": int(n_hor), "horizon_share": n_hor / max(1, len(pos))}


def lookup_score(grid, cal_pos):
    """Return the (depth, cap) calibration accuracy of every cell: the label-only score the allocator ranks by."""
    return np.nanmean(grid.acc[:, :, cal_pos], axis=2)


def avg_picks(score, prices, lam):
    """Return per-prompt (depth index, cap index) maximising score - lam * price.

    A tie in the objective goes to the cheaper cell, and a tie in both to the lower depth and cap,
    so the pick is deterministic. A cell with no score or no price is never picked.
    """
    S, Pr = np.asarray(score, float), np.asarray(prices, float)
    nk, nb, nq = Pr.shape
    fin = (np.isfinite(S)[:, :, None] & np.isfinite(Pr)).reshape(nk * nb, nq)
    J = np.where(fin, (S[:, :, None] - float(lam) * Pr).reshape(nk * nb, nq), -np.inf)
    Pf = np.where(fin, Pr.reshape(nk * nb, nq), np.inf)
    best = J.max(0)
    tie = np.maximum(1.0, np.abs(np.where(np.isfinite(best), best, 0.0))) * 1e-12
    flat = np.where(J >= best - tie, Pf, np.inf).argmin(0)
    return flat // nb, flat % nb


def avg_spend(score, prices, lam):
    """Return the mean price over prompts of the cells chosen at multiplier lam, in layer-token passes."""
    Pr = np.asarray(prices, float)
    a, b = avg_picks(score, Pr, lam)
    return float(Pr[a, b, np.arange(Pr.shape[2])].mean())


def _lambda_ceiling(score, prices):
    """Return a multiplier beyond which price decides alone, so the bisection has a bracket."""
    S = np.asarray(score, float)
    fin = np.isfinite(S)
    spread = float(S[fin].max() - S[fin].min()) if fin.any() else 1.0
    Pr = np.asarray(prices, float)
    flat = np.sort(Pr.reshape(-1, Pr.shape[2]), axis=0)
    d = np.diff(flat, axis=0)
    d = d[np.isfinite(d) & (d > 0)]
    gap = float(d.min()) if d.size else 1.0
    return 4.0 * max(spread, np.finfo(float).tiny) / gap


def lambda_for_budget(score, prices, X, n_iter=AVG_ITERS):
    """Return the SMALLEST multiplier whose mean price fits X, its spend, and whether X was met.

    The spend is a non-increasing step function of the multiplier, so the smallest feasible one is
    the largest feasible spend: any larger multiplier would leave budget unspent.
    """
    at_zero = avg_spend(score, prices, 0.0)
    if at_zero <= X * (1 + BUDGET_TOL):
        return 0.0, at_zero, True
    hi = _lambda_ceiling(score, prices)
    floor_spend = avg_spend(score, prices, hi)
    if not floor_spend <= X * (1 + BUDGET_TOL):
        return hi, floor_spend, False
    lo = 0.0
    for _ in range(int(n_iter)):
        mid = 0.5 * (lo + hi)
        if avg_spend(score, prices, mid) <= X * (1 + BUDGET_TOL):
            hi = mid
        else:
            lo = mid
    return hi, avg_spend(score, prices, hi), True


def floor_deepest(w, floor=DEEPEST_DEPTH_FLOOR):
    """Return `w` with the deepest depth raised to at least `floor`, the shallower ones rescaled.

    The deepest depth is the checkpoint's released default and the cell Table 1 checks at 1.0x, so
    whatever the allocator ranks it, the draw may not starve it. Raising it is the only change: the
    shallower depths keep their proportions to each other inside the remaining 1 - floor, and a
    mixture already at or above the floor is returned untouched.
    """
    if not 0.0 <= float(floor) < 1.0:
        raise SystemExit("the deepest-depth floor must be in [0, 1), got %r" % (floor,))
    w = np.asarray(w, float).copy()
    if len(w) < 2 or w[-1] >= float(floor):
        return w / w.sum()
    rest, tot = w[:-1], float(w[:-1].sum())
    scaled = (rest * (1.0 - float(floor)) / tot if tot > 0
              else np.full(len(rest), (1.0 - float(floor)) / len(rest)))
    return np.concatenate([scaled, [float(floor)]])


def depth_weights(grid, cal_pos, n_budgets=N_BUDGETS, uniform_mix=UNIFORM_MIX,
                  deepest_floor=DEEPEST_DEPTH_FLOOR):
    """Return one source's depth draw weights and the allocator record behind them.

    The allocator is the average-budget LOOKUP arm: it scores each cell by its calibration accuracy
    and, at a compute budget X, buys the cells maximising score - lam*price with lam set so the MEAN
    price over prompts is at most X. Every depth's share is pooled over the whole budget ladder, so
    the table says which depths are worth buying across the compute range rather than at one point.
    Both the fit and the assignment run on the calibration prompts: this stage never opens the
    evaluation half of the base grid.

    The pooled usage becomes a draw under the SAME mixture rule as the budget weights,
    w = uniform_mix * uniform + (1 - uniform_mix) * usage, so every depth keeps at least
    uniform_mix / n_depths of the blocks; the deepest depth is then raised to `deepest_floor` if the
    mixture left it below.
    """
    expected = expected_lengths(grid, cal_pos)
    cmat, Pm, Rm = cost_matrix(grid, expected, cal_pos)
    dflt = default_cost(grid, cal_pos)
    lo, hi = float(np.nanmin(cmat)), float(dflt["mean"])
    if not hi > lo:
        raise SystemExit("%s: the default cost %g is not above the cheapest cell %g"
                         % (grid.task, hi, lo))
    Xs = np.exp(np.linspace(np.log(lo), np.log(hi), int(n_budgets)))
    score = lookup_score(grid, cal_pos)
    prices = price_tensor(grid, cal_pos, expected)
    counts = np.zeros(len(grid.ks))
    rows = []
    for X in Xs:
        lam, spend, met = lambda_for_budget(score, prices, float(X))
        a, b = avg_picks(score, prices, lam)
        share = np.array([float((a == i).mean()) for i in range(len(grid.ks))])
        counts += share
        rows.append({"X": float(X), "lambda": float(lam), "mean_price": float(spend),
                     "constraint_met": bool(met),
                     "depth_share": {str(k): float(share[i]) for i, k in enumerate(grid.ks)},
                     "cap_share": {str(T): float((b == j).mean())
                                   for j, T in enumerate(grid.caps) if (b == j).any()}})
    raw = counts / counts.sum()
    mixed = float(uniform_mix) / len(grid.ks) + (1.0 - float(uniform_mix)) * raw
    w = floor_deepest(mixed, deepest_floor)
    return ({str(int(k)): float(w[i]) for i, k in enumerate(grid.ks)},
            {str(int(k)): float(raw[i]) for i, k in enumerate(grid.ks)},
            {"default_cost": dflt, "cheapest_cell": lo, "n_budgets": int(n_budgets),
             "budgets": [float(x) for x in Xs], "median_prompt_tokens": Pm,
             "median_reserve_tokens": Rm, "L_loop": L_LOOP, "L_fixed": L_FIXED,
             "n_cal_prompts": int(len(cal_pos)), "per_budget": rows,
             "expected_lengths": {str(int(k)): {str(T): float(expected[i, j])
                                                for j, T in enumerate(grid.caps)}
                                  for i, k in enumerate(grid.ks)}})


# ================================================================= stage 0 main
def default_cells_dir():
    """Return the first base-grid directory on the candidate list that exists, or None."""
    env = os.environ.get("S36_CELLS_DIR")
    for d in ((env,) if env else ()) + CELLS_DIR_CANDIDATES:
        if d and os.path.isdir(os.path.expanduser(d)):
            return os.path.expanduser(d)
    return None


def table(cfg, cells_dir):
    """Return the whole theory-weights record: one budget table and one depth table per source."""
    depths = cfg.depths
    assert [int(d) for d in depths] == sorted(int(d) for d in cfg["depth_probabilities"]), depths
    out = {"generated_by": "train/theory_weights.py", "cells_dir": cells_dir,
           "cell_pattern": CELL_PATTERN, "depths": [int(d) for d in depths],
           "L_loop": L_LOOP, "L_fixed": L_FIXED, "uniform_mix": UNIFORM_MIX,
           "deepest_depth_floor": DEEPEST_DEPTH_FLOOR, "n_budgets": N_BUDGETS, "split": "cal",
           "answer_allowance": dict(ANSWER_ALLOWANCE, default=ANSWER_ALLOWANCE_DEFAULT),
           "formulas": {"budget": BUDGET_FORMULA, "depth": DEPTH_FORMULA},
           "grid_files": {}, "sources": {}}
    for src in cfg.sources:
        task = GRID_TASK[src]
        assert cfg.eval_task(src) == task, (src, cfg.eval_task(src), task)
        assert answer_allowance(task) == int(cfg["n_answer_tokens"][task]), task
        grid, files = load_grid(cells_dir, task, depths)
        out["grid_files"][src] = files
        cal = grid.select("cal")
        if not len(cal):
            raise SystemExit("%s: the base grid has no calibration split" % task)
        tab = commitment_tables(grid.pred, grid.acc, cal)
        bw, raw = budget_weights(tab, grid.caps, cfg.budget_grid_for(src))
        dw, draw, alloc = depth_weights(grid, cal)
        nb = len(grid.caps)
        out["sources"][src] = {
            "eval_task": task, "n_cal_prompts": int(len(cal)),
            "n_questions": int(len(grid.idx)), "caps": [int(c) for c in grid.caps],
            "budget_grid": [G.budget_key(t) for t in cfg.budget_grid_for(src)],
            "budget_weights": bw, "budget_weights_unnormalised": raw,
            "depth_weights": dw, "depth_weights_before_floor": draw,
            "allocator": alloc,
            "commitment": {
                "G": {str(int(k)): {str(T): float(tab["G"][i, j])
                                    for j, T in enumerate(grid.caps)}
                      for i, k in enumerate(grid.ks)},
                "c_by_settle_cap": {str(int(k)): {str(T): _n(tab["c_by_settle_cap"][i, j])
                                                  for j, T in enumerate(grid.caps)}
                                    for i, k in enumerate(grid.ks)},
                "l_by_cap": {str(int(k)): {str(T): _n(tab["l_by_cap"][i, j])
                                           for j, T in enumerate(grid.caps)}
                             for i, k in enumerate(grid.ks)},
                "c_after_cap": {str(int(k)): {str(T): _n(tab["c_after_cap"][i, j])
                                              for j, T in enumerate(grid.caps)}
                                for i, k in enumerate(grid.ks)},
                "unrealised_gain": {str(int(k)): {str(T): float(unrealised_gain(tab)[i, j])
                                                  for j, T in enumerate(grid.caps)}
                                    for i, k in enumerate(grid.ks)},
                "settle_share": {str(int(k)): {
                    **{str(T): float((tab["settle_index"][i] == j).mean())
                       for j, T in enumerate(grid.caps)},
                    "never": float((tab["settle_index"][i] == nb).mean())}
                    for i, k in enumerate(grid.ks)}}}
    return out


def _n(x):
    """Return a float, or None for a table entry no question stands behind."""
    return None if not np.isfinite(x) else float(x)


def main(argv):
    """Compute the weight tables from the base grids and write them; returns a process exit code."""
    cfg_path, cells_dir, out = G.DEFAULT_CONFIG, None, None
    for a in argv:
        k, _, v = a.lstrip("-").partition("=")
        if k == "config":
            cfg_path = v
        elif k == "cells-dir":
            cells_dir = v
        elif k == "out":
            out = v
    cells_dir = os.path.expanduser(cells_dir) if cells_dir else default_cells_dir()
    if not cells_dir or not os.path.isdir(cells_dir):
        raise SystemExit("theory_weights.py: --cells-dir=<dir holding %s> is required; none of %s "
                         "exists" % (CELL_PATTERN % ("<task>", 4), list(CELLS_DIR_CANDIDATES)))
    cfg = G.load_config(cfg_path)
    rec = table(cfg, cells_dir)
    dest = os.path.expanduser(out) if out else G.THEORY_WEIGHTS
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    G.jdump(rec, dest)
    digest = G.file_sha256(dest)
    for src, s in rec["sources"].items():
        print("[%s] T %s" % (src, {k: round(v, 4) for k, v in s["budget_weights"].items()}),
              flush=True)
        print("[%s] depth %s (allocator usage %s)"
              % (src, {k: round(v, 4) for k, v in s["depth_weights"].items()},
                 {k: round(v, 4) for k, v in s["depth_weights_before_floor"].items()}), flush=True)
    print("\nwrote %s\nsha256 %s" % (dest, digest), flush=True)
    pinned = str(cfg.get("theory_weights_sha256", "")).strip().lower()
    if pinned and pinned != digest:
        print("config.yaml pins theory_weights_sha256 %s; paste the digest above over it"
              % pinned, flush=True)
        return 1
    print("THEORY WEIGHTS OK", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
