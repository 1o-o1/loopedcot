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
