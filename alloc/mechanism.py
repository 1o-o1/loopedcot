"""Compute label-free read-out commitment and predict accuracy fractions from calibration labels at each depth and token cap."""
import numpy as np


def commitment(cells, pos, caps=None):
    """Return Boolean commitment at requested token caps and prompt positions, checking every measured cap through the final cap."""
    requested = list(cells.caps) if caps is None else list(caps)
    if not requested or any(c not in cells.caps for c in requested):
        raise ValueError("caps must be nonempty measured token caps")
    A = np.zeros((len(cells.ks), len(cells.caps), len(pos)), bool)
    for a in range(len(cells.ks)):
        for ii, n in enumerate(pos):
            fin = cells.pred[a, -1, n]
            if fin is None:
                continue
            ok = True
            for j in range(len(cells.caps) - 1, -1, -1):
                ok = ok and (cells.pred[a, j, n] == fin)
                A[a, j, ii] = ok
    return A[:, [cells.caps.index(c) for c in requested], :]


def mechanism(cells, g_pos, label_pos=None, caps=None):
    """Return G, c, l, and A_hat=G*c+(1-G)*l from read-out positions and labelled positions; surfaces are fractions and RMSE is percentage points."""
    caps = cells.caps if caps is None else [c for c in caps if c in cells.caps]
    bi = {b: i for i, b in enumerate(cells.caps)}
    cix = [bi[c] for c in caps]
    label_pos = g_pos if label_pos is None else label_pos
    nk = len(cells.ks)

    G = commitment(cells, g_pos, caps).mean(2)
    AL = commitment(cells, label_pos, caps)
    CO = cells.acc[:, cix, :][:, :, label_pos]

    c = np.array([CO[i][AL[i] & np.isfinite(CO[i])].mean() if (AL[i] & np.isfinite(CO[i])).any() else np.nan for i in range(nk)])
    l = np.array([CO[i][~AL[i] & np.isfinite(CO[i])].mean() if (~AL[i] & np.isfinite(CO[i])).any() else np.nan for i in range(nk)])
    # A depth with no uncommitted cell has no l. Falling back to c keeps A_hat defined and is
    # exactly right there: every cell at that depth is committed, so the (1 - G) term is zero.
    c = np.where(np.isnan(c), l, c)
    l = np.where(np.isnan(l), c, l)
    A_hat = G * c[:, None] + (1 - G) * l[:, None]

    acc_measured = CO.mean(2)
    resid = A_hat - acc_measured
    rmse = float(100 * np.sqrt(np.nanmean(resid ** 2)))
    n_lab = len(label_pos)
    # Noise floor: the RMSE a PERFECT surface would still show, because the measured accuracy it is
    # compared against is itself a mean of n_lab Bernoulli draws. se^2 = p(1-p)/n per cell.
    se2 = acc_measured * (1 - acc_measured) / max(1, n_lab)
    noise_floor = float(100 * np.sqrt(np.nanmean(se2)))
    n_unc = [int((~AL[i]).sum()) for i in range(nk)]
    n_cells = int(AL.shape[1] * AL.shape[2])
    return {
        "ks": list(cells.ks), "caps": list(caps),
        "G": G.tolist(), "c": c.tolist(), "l": l.tolist(),
        "A_hat": A_hat.tolist(), "acc_measured": acc_measured.tolist(),
        "rmse_pts": rmse, "noise_floor_pts": noise_floor,
        "rmse_over_noise_floor": (rmse / noise_floor) if noise_floor > 0 else None,
        "n_g": int(len(g_pos)), "n_labels": int(n_lab),
        "uncommitted_cells": n_unc, "cells_per_depth": n_cells,
        "uncommitted_share": [round(x / max(1, n_cells), 4) for x in n_unc],
    }


def a_hat_matrix(m):
    """Return the predicted accuracy fractions of a mechanism result as a (depth,token cap) NumPy array."""
    return np.array(m["A_hat"], float)


# ---------------------------------------------------------------- settle time
# A settle cap needs this many labelled calibration questions of its own before it is given its own
# c_k(j); below that it takes its bin's pooled value, and a short bin takes the depth's pooled c --
# exactly the number the pooled identity carries. Every fallback is counted, so a surface fitted on
# too few labels says so rather than looking like one fitted on enough.
MIN_SETTLE_LABELS = 8
# The bins a sparse settle cap pools into. Caps are powers of two, and a bin holds one octave pair,
# so a cap with too few labels borrows from the caps nearest it in chain length rather than from the
# whole depth.
SETTLE_BINS = ((0, 0), (16, 32), (64, 128), (256, 512), (1024, 4096))


def settle_time(cells, pos):
    """Return the FIRST settled token cap INDEX per (depth, prompt); len(caps) means never settled.

    Settled at cap T means the forced read-out at T and at every cap after it equals the last cap's
    read-out and parses -- `commitment` above. That Boolean is a suffix in the cap by construction,
    so "the first settled cap" is well defined, and a question whose read-out never stops moving, or
    whose final read-out does not parse, is encoded at len(caps): BEYOND the last cap, never equal
    to it. Label free: only read-outs are read, never a label.
    """
    A = commitment(cells, pos)
    nb = len(cells.caps)
    return np.where(A.any(1), A.argmax(1), nb)


def settle_bin(cap, bins=SETTLE_BINS):
    """Return the KEY of the bin a token cap pools into when it holds too few labels of its own.

    Only equality of keys is ever read, so the key needs to be stable, not ordered. A cap the table
    covers takes its table entry. A cap the table does not cover -- a grid with a cap set of its own,
    or a negative cap standing for "no cap at all" -- pools by OCTAVE PAIR instead, the same shape
    the table has, and can never join a table bin. So the production rule is exactly the table and
    nothing else, and a grid outside it still has a defined, deterministic bin rather than an error.
    """
    for i, (lo, hi) in enumerate(bins):
        if lo <= cap <= hi:
            return ("table", i)
    if cap <= 0:
        return ("cap", int(cap))
    return ("octave", int(np.floor(np.log2(float(cap)))) // 2)


def settle_distribution(cells, s):
    """Return one record per depth: the share settling at each cap, the share never, and the median.

    The median is taken over the ORDERED categories cap_0 < ... < cap_last < never, so a depth where
    most questions never settle reports `never` rather than a cap it never reached.
    """
    nb, caps = len(cells.caps), list(cells.caps)
    rows = []
    for a, k in enumerate(cells.ks):
        v = np.asarray(s[a])
        share = [float((v == j).mean()) for j in range(nb)]
        never = float((v == nb).mean())
        cum = np.cumsum(share + [never])
        mi = int(np.searchsorted(cum, 0.5 - 1e-12))
        rows.append({"k": int(k), "n": int(len(v)),
                     "share_by_cap": {str(caps[j]): share[j] for j in range(nb)},
                     "share_settle_first": share[0],
                     "share_never": never,
                     "median_settle_cap": (float(caps[mi]) if mi < nb else None),
                     "median_settle_label": (str(caps[mi]) if mi < nb else "never")})
    return rows


def resolved_mechanism(cells, g_pos, label_pos=None, n_labels=None, caps=None,
                       min_labels=MIN_SETTLE_LABELS, bins=SETTLE_BINS):
    """Return the identity resolved by settle time: P_k(s=j), c_k(j), l_k(T) and A_res(k,T).

        A_res(k,T) = sum_{j<=T} P_k(s=j) c_k(j) + P_k(s>T) l_k(T)

    `P` comes from the read-out positions `g_pos` and is LABEL FREE -- every one of them counts.
    `c_k(j)`, the accuracy of the questions that settled at cap j, and `l_k(T)`, the accuracy at cap
    T of the questions not settled by T, come from the labelled positions alone. `c_k(j)` is well
    defined because a question settled at j carries the same read-out, and so the same label, at
    every cap from j on; it is read at the LAST cap. The two terms partition the same questions, so
    A_res reproduces the calibration surface exactly when every settle cap is estimated from its own
    labels and the labels are all of the read-out positions.

    Against `mechanism` above: that carries ONE c_k and ONE l_k for the whole depth, so its surface
    rises with T wherever c_k > l_k and can never rank the first cap first. Resolving by settle time
    is what makes a grid whose best cell is cap 0 -- the class sets, where the first answer is the
    good one -- rankable.

    `n_labels` takes the first n_labels of `g_pos`, which are the first n_labels calibration ids in
    id order, the same subset the pooled version takes. Pass `label_pos` instead to name them.

    Sparse settle caps: a cap holding fewer than `min_labels` labelled questions takes its bin's
    pooled c (`SETTLE_BINS`), and a bin that is itself short takes the depth's pooled c -- the
    pooled identity's own number. `c_source` records which of the three each cell used.
    """
    if caps is not None and list(caps) != list(cells.caps):
        raise ValueError("the resolved identity is defined over the grid's measured caps: the "
                         "settle cap of a question is found by looking at every cap through the "
                         "last, so a cap subset would change what 'settled' means. Narrow the grid "
                         "with cells.load(caps=...) instead")
    g = np.asarray(g_pos, dtype=int)
    if not len(g):
        raise ValueError("the resolved identity needs at least one read-out position")
    if label_pos is not None and n_labels is not None:
        raise ValueError("pass label_pos or n_labels, not both")
    if label_pos is None:
        if n_labels is not None and int(n_labels) <= 0:
            raise ValueError("n_labels must be positive")
        label_pos = g if n_labels is None else g[:int(n_labels)]
    lab = np.asarray(label_pos, dtype=int)
    if not len(lab):
        raise ValueError("the resolved identity needs at least one labelled position")

    nk, nb = len(cells.ks), len(cells.caps)
    last = nb - 1
    acc = cells.acc
    s_g, s_lab = settle_time(cells, g), settle_time(cells, lab)

    P = np.zeros((nk, nb))
    c = np.full((nk, nb), np.nan)
    l = np.full((nk, nb), np.nan)
    src = np.empty((nk, nb), dtype=object)
    n_at = np.zeros((nk, nb), int)
    n_uns = np.zeros((nk, nb), int)
    pooled_c, pooled_l = np.full(nk, np.nan), np.full(nk, np.nan)
    bin_of = [settle_bin(T, bins) for T in cells.caps]
    for a in range(nk):
        P[a] = [float((s_g[a] == j).mean()) for j in range(nb)]
        ls = s_lab[a]
        # the depth's pooled c and l over CELLS, exactly as `mechanism` forms them: a cell (j, n) is
        # committed when question n has settled by cap j, which is ls[n] <= j
        AL = np.array([ls <= j for j in range(nb)])
        CO = acc[a][:, lab]
        ok = np.isfinite(CO)
        pooled_c[a] = float(CO[AL & ok].mean()) if (AL & ok).any() else np.nan
        pooled_l[a] = float(CO[~AL & ok].mean()) if (~AL & ok).any() else np.nan
        fb = pooled_c[a] if np.isfinite(pooled_c[a]) else pooled_l[a]
        for j in range(nb):
            sel = ls == j
            n_at[a, j] = int(sel.sum())
            if sel.sum() >= int(min_labels):
                c[a, j] = float(acc[a, last, lab[sel]].mean())
                src[a, j] = "cap"
            else:
                members = np.array([jj for jj in range(nb) if bin_of[jj] == bin_of[j]])
                selb = np.isin(ls, members)
                if selb.sum() >= int(min_labels):
                    c[a, j] = float(acc[a, last, lab[selb]].mean())
                    src[a, j] = "bin"
                else:
                    c[a, j] = fb
                    src[a, j] = "pooled"
            uns = ls > j
            n_uns[a, j] = int(uns.sum())
            l[a, j] = float(acc[a, j, lab[uns]].mean()) if uns.any() else fb

    Pcum = np.cumsum(P, axis=1)
    A_res = np.cumsum(P * np.nan_to_num(c, nan=0.0), axis=1) + (1.0 - Pcum) * l
    acc_measured = np.nanmean(acc[:, :, lab], axis=2)
    resid = A_res - acc_measured
    rmse = float(100 * np.sqrt(np.nanmean(resid ** 2)))
    se2 = acc_measured * (1 - acc_measured) / max(1, len(lab))
    noise_floor = float(100 * np.sqrt(np.nanmean(se2)))
    pooled_cells = (src == "pooled")
    return {
        "ks": list(cells.ks), "caps": list(cells.caps),
        "P": P.tolist(), "c": c.tolist(), "l": l.tolist(),
        "A_res": A_res.tolist(), "acc_measured": acc_measured.tolist(),
        "rmse_pts": rmse, "noise_floor_pts": noise_floor,
        "rmse_over_noise_floor": (rmse / noise_floor) if noise_floor > 0 else None,
        "pooled_c": pooled_c.tolist(), "pooled_l": pooled_l.tolist(),
        "c_source": src.tolist(),
        "n_labels_at_cap": n_at.tolist(), "n_unsettled_at_cap": n_uns.tolist(),
        "n_g": int(len(g)), "n_labels": int(len(lab)),
        "min_labels": int(min_labels), "bins": [list(b) for b in bins],
        "n_caps_own": int((src == "cap").sum()),
        "n_caps_binned": int((src == "bin").sum()),
        "n_caps_pooled": int(pooled_cells.sum()),
        "n_caps_binned_with_mass": int(((src == "bin") & (P > 0)).sum()),
        "n_caps_pooled_with_mass": int((pooled_cells & (P > 0)).sum()),
        "cells_per_depth": int(nb),
        "share_settle_first": float((s_g == 0).mean()),
        "share_never": float((s_g == nb).mean()),
        "settle_distribution": settle_distribution(cells, s_g),
    }


def a_res_matrix(m):
    """Return the resolved predicted accuracy fractions as a (depth, token cap) NumPy array."""
    return np.array(m["A_res"], float)
