"""Surface tests: rank one, same peak, and the additive fit with its raw contrasts beside it.

Measurement rule 1 (PLAN.md "Framework of record"): fitted a(k), m(k), g(B) are NEVER reported
without the raw contrasts, so `fit_additive` returns both and `card_fit_block` puts them in one
record.

Ported: `fit_affine_rank1` from `b1t_v3.py` (the SVD on the row-centred grid, g(0) = 0, max|g| = 1,
flat tolerance 0.02) and the rank-one energy line of `v4_commitment.py`.

Two facts of record the tests exist to check (LEDGER):
  * 2026-09-05: a MULTIPLICATIVE law A = a(k) b(B) fails where accuracies are near zero (held-out
    RMSE 0.17-0.18 against 0.015-0.03 for the additive centred law); the additive law stands.
  * 2026-09-05: A0(k) + m(k) g(B) predicts that the cap where returns peak is the SAME for every k
    (dA/dB = m(k) g'(B)); if the peak moves with k the surface is rank two and the theory changes.
    `same_peak` is that test.
"""
import numpy as np

FLAT_TOL = 0.02


def fit_affine_rank1(A, tol=FLAT_TOL):
    """b1t_v3.fit_affine_rank1, verbatim. Returns (a, m, g, resid, info)."""
    rowmean = A.mean(1, keepdims=True)
    Ac = A - rowmean
    U, S, Vt = np.linalg.svd(Ac, full_matrices=False)
    m0 = U[:, 0] * S[0]
    v = Vt[0]
    energy = float(S[0] ** 2 / max(np.sum(S ** 2), 1e-12))
    g = v - v[0]
    scale = float(np.abs(g).max())
    if scale < tol:
        a = rowmean[:, 0]
        return (a, np.zeros_like(m0), np.zeros_like(g), A - a[:, None],
                {"flat": True, "energy": energy})
    sgn = np.sign(g[np.argmax(np.abs(g))]) or 1.0
    g = g * sgn / scale
    m = m0 * sgn * scale
    a = rowmean[:, 0] + m0 * v[0]
    resid = A - (a[:, None] + m[:, None] * g[None, :])
    return a, m, g, resid, {"flat": False, "energy": energy}


def rank_one_test(A):
    """Energy in the first singular value of the ROW-CENTRED grid, and the RMSE of the rank-one
    reconstruction in accuracy points."""
    M = A - A.mean(1, keepdims=True)
    U, S, Vt = np.linalg.svd(M, full_matrices=False)
    R1 = A.mean(1, keepdims=True) + S[0] * np.outer(U[:, 0], Vt[0])
    return {"energy_rank_one": float(S[0] ** 2 / max(np.sum(S ** 2), 1e-12)),
            "singular_values": [float(s) for s in S],
            "rmse_rank_one_pp": float(100 * np.sqrt(np.mean((R1 - A) ** 2)))}


def holdout_rmse(A, ks, Bs, hold_ks=None, hold_Bs=None):
    """Fit the additive law on the complement of the held-out cells and score it on them.

    "The law fitted on a subset and validated on held-out cells" is the ICLR bar of record (LEDGER
    "ICLR bar of record"). Two kinds of hold-out, because they ask different questions:

      hold_Bs  CAPS held out. The fit sees every depth, so a(k) and m(k) are measured and only
               g(cap) is interpolated at the held-out caps (in log2(1 + cap), the coordinate b1t_v3
               uses). This is the interpolation claim LEDGER 2026-09-06 says the law supports.
      hold_ks  a DEPTH row held out. That row contributes nothing to the fit, so a(k) and m(k) must
               be interpolated from the neighbouring measured depths -- which is exactly the
               unmeasured-depth question Brief C answered negatively for the cross-task transfer
               (residual 10 to 36 points). Reported so the same quantity is visible per grid.
    """
    A = np.asarray(A, float)
    ks, Bs = list(ks), list(Bs)
    hold_ks = [k for k in (hold_ks or []) if k in ks]
    hold_Bs = [b for b in (hold_Bs or []) if b in Bs]
    if not hold_ks and not hold_Bs:
        return {"held_out": 0, "rmse_pp": None}
    keep_k = [i for i, k in enumerate(ks) if k not in hold_ks]
    keep_b = [j for j, b in enumerate(Bs) if b not in hold_Bs]
    if len(keep_k) < 2 or len(keep_b) < 3:
        return {"held_out": 0, "rmse_pp": None, "note": "not enough kept cells to fit"}
    a_f, m_f, g_f, _r, info = fit_affine_rank1(A[np.ix_(keep_k, keep_b)])
    # g on the FULL cap axis: interpolate in log2(1 + cap), b1t_v3's coordinate
    u_keep = np.log2(1.0 + np.array([Bs[j] for j in keep_b], float))
    u_all = np.log2(1.0 + np.array(Bs, float))
    g_all = np.interp(u_all, u_keep, g_f)
    # a and m on the FULL depth axis: interpolate linearly in k
    k_keep = np.array([ks[i] for i in keep_k], float)
    k_all = np.array(ks, float)
    a_all = np.interp(k_all, k_keep, a_f)
    m_all = np.interp(k_all, k_keep, m_f)
    R = a_all[:, None] + m_all[:, None] * g_all[None, :]
    mask = np.zeros_like(A, bool)
    for i, k in enumerate(ks):
        for j, b in enumerate(Bs):
            if k in hold_ks or b in hold_Bs:
                mask[i, j] = True
    err = (R - A)[mask]
    return {"held_out": int(mask.sum()), "rmse_pp": float(100 * np.sqrt(np.mean(err ** 2))),
            "max_abs_err_pp": float(100 * np.max(np.abs(err))),
            "hold_ks": hold_ks, "hold_Bs": hold_Bs,
            "kind": "depth row" if hold_ks else "caps",
            "fit_energy": info["energy"]}


def same_peak(A, ks, Bs):
    """Does the cap of peak accuracy, and the cap of peak MARGINAL return, agree across depths?

    The additive law implies both are shared. Reported as the caps themselves plus the spread, so a
    reader sees the raw rows and not only a verdict.
    """
    peak_cap = [int(Bs[int(np.argmax(A[i]))]) for i in range(len(ks))]
    d = np.diff(A, axis=1)
    marg_cap = [int(Bs[1:][int(np.argmax(d[i]))]) for i in range(len(ks))]
    return {"ks": list(ks), "peak_cap_per_k": peak_cap, "marginal_peak_cap_per_k": marg_cap,
            "peak_cap_same": len(set(peak_cap)) == 1,
            "marginal_peak_cap_same": len(set(marg_cap)) == 1,
            "peak_cap_spread_log2": float(np.log2(max(peak_cap) + 1) - np.log2(min(peak_cap) + 1)),
            "note": ("the additive law A0(k) + m(k) g(B) implies dA/dB = m(k) g'(B), so both caps "
                     "are shared across k; a moving peak makes the surface rank two")}


def raw_contrasts(A, ks, Bs, k_hi=4, k_lo=2, caps=(64, 128, 256, 512)):
    """Measurement rule 1's raw contrasts: A(k_hi, T) - A(k_lo, T) at the listed caps, in points."""
    if k_hi not in ks or k_lo not in ks:
        k_hi, k_lo = ks[-1], ks[max(0, len(ks) - 2)]
    i, j = ks.index(k_hi), ks.index(k_lo)
    out = {}
    for T in caps:
        if T in Bs:
            out[str(T)] = float(100 * (A[i, Bs.index(T)] - A[j, Bs.index(T)]))
    return {"k_hi": k_hi, "k_lo": k_lo, "contrast_pp": out}


def card_fit_block(A, ks, Bs):
    """The card's fit block: the raw contrasts FIRST, then the fitted a/m/g with their fit quality."""
    a, m, g, resid, info = fit_affine_rank1(np.asarray(A, float))
    return {"raw_contrasts": raw_contrasts(np.asarray(A, float), list(ks), list(Bs)),
            "rank_one": rank_one_test(np.asarray(A, float)),
            "same_peak": same_peak(np.asarray(A, float), list(ks), list(Bs)),
            "fit": {"a": [float(x) for x in a], "m": [float(x) for x in m],
                    "g": [float(x) for x in g], "flat": bool(info["flat"]),
                    "energy": info["energy"],
                    "residual_rmse_pp": float(100 * np.sqrt(np.mean(resid ** 2)))},
            "holdout_depth_rows": [holdout_rmse(np.asarray(A, float), list(ks), list(Bs),
                                                 hold_ks=[k]) for k in ks[1:-1]] or None,
            "holdout_caps": [holdout_rmse(np.asarray(A, float), list(ks), list(Bs),
                                          hold_Bs=[b]) for b in list(Bs)[1:-1]] or None}
