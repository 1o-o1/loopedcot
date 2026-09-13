"""Figures. Every one has compute on the x-axis where a compute axis exists (LEDGER compute rule).

  python -m prod.analyze.figures --cells=artifacts --model=... --task=... [--out=DIR]

Six figures, matching the ICLR bar of record:
  fig_heatmap_<model>_<task>.pdf     accuracy over (k, cap), the law's raw surface
  fig_frontier_<model>_<task>.pdf    accuracy against layer-token passes, prompt-inclusive
  fig_frontier_pf_<model>_<task>.pdf the same, prompt-free
  fig_card_<model>_<task>.pdf        raw contrasts beside the fitted profiles (measurement rule 1)
  fig_gain_<model>_<task>.pdf        allocator against normal operation per budget (decision D2)
  fig_arrival_<model>_<task>.pdf     commitment arrival share G(k, cap) with c and l beside it

matplotlib is imported lazily with the Agg backend so this module can be imported on a headless
host and by the gates, which do not draw.
"""
import argparse
import os

import numpy as np

from ..score import load_grid
from .allocate import Grid, gain_over_normal
from .tests import card_fit_block


def _plt():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    return plt


def heatmap(cells, path, title):
    plt = _plt()
    A = 100 * cells.mean_acc(cells.select("eval"))
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    im = ax.imshow(A, aspect="auto", origin="lower", cmap="viridis")
    ax.set_xticks(range(len(cells.Bs)), [str(b) for b in cells.Bs])
    ax.set_yticks(range(len(cells.ks)), ["k=%d" % k for k in cells.ks])
    ax.set_xlabel("CoT length cap (tokens)")
    ax.set_title(title)
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            ax.text(j, i, "%.0f" % A[i, j], ha="center", va="center", fontsize=6,
                    color="w" if A[i, j] < A.max() * 0.6 else "k")
    fig.colorbar(im, ax=ax, label="accuracy (%)")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    return path


def frontier(cells, path, title, promptfree=False):
    plt = _plt()
    sel = cells.select("eval")
    A = 100 * cells.mean_acc(sel)
    X = np.nanmean(cells.passes_pf[:, :, sel] if promptfree else cells.passes[:, :, sel], 2)
    fig, ax = plt.subplots(figsize=(5.6, 3.6))
    for i, k in enumerate(cells.ks):
        ax.plot(X[i], A[i], marker="o", ms=3, label="k=%d" % k)
    ax.set_xscale("log")
    ax.set_xlabel("layer-token passes per question (%s)"
                  % ("prompt-free" if promptfree else "prompt-inclusive"))
    ax.set_ylabel("accuracy (%)")
    ax.set_title(title)
    ax.legend(fontsize=7)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    return path


def card_figure(cells, path, title):
    """Raw contrasts on the left, the fitted a/m/g on the right: measurement rule 1 in one picture."""
    plt = _plt()
    A = cells.mean_acc(cells.select("eval"))
    blk = card_fit_block(A, cells.ks, cells.Bs)
    fig, axes = plt.subplots(1, 3, figsize=(9.4, 3.0))
    for i, k in enumerate(cells.ks):
        axes[0].plot(cells.Bs, 100 * A[i], marker="o", ms=3, label="k=%d" % k)
    axes[0].set_xscale("symlog")
    axes[0].set_title("raw rows (measured)")
    axes[0].set_xlabel("cap")
    axes[0].set_ylabel("accuracy (%)")
    axes[0].legend(fontsize=7)
    axes[1].plot(cells.ks, 100 * np.array(blk["fit"]["a"]), marker="s", label="a(k)")
    axes[1].plot(cells.ks, 100 * np.array(blk["fit"]["m"]), marker="^", label="m(k)")
    axes[1].set_title("fitted a(k), m(k)\nrank-one energy %.3f, resid %.2f pp"
                      % (blk["rank_one"]["energy_rank_one"], blk["fit"]["residual_rmse_pp"]))
    axes[1].set_xlabel("loops k")
    axes[1].legend(fontsize=7)
    axes[2].plot(cells.Bs, blk["fit"]["g"], marker="o", ms=3)
    axes[2].set_xscale("symlog")
    axes[2].set_title("fitted g(cap)")
    axes[2].set_xlabel("cap")
    fig.suptitle(title, fontsize=9)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    return path


def gain_figure(grid, path, title):
    plt = _plt()
    g = gain_over_normal(grid)
    xs = [r["X"] for r in g["per_budget"]]
    pol = [None if r["policy_acc"] is None else 100 * r["policy_acc"] for r in g["per_budget"]]
    nor = [None if r["normal_acc"] is None else 100 * r["normal_acc"] for r in g["per_budget"]]
    fig, ax = plt.subplots(figsize=(5.6, 3.4))
    ax.plot(xs, pol, marker="o", ms=3, label="allocated policy (calibration-chosen)")
    ax.plot(xs, nor, marker="s", ms=3, label="normal operation (k_max, largest feasible cap)")
    ax.set_xscale("log")
    ax.set_xlabel("budget X: layer-token passes per question")
    ax.set_ylabel("accuracy on evaluation questions (%)")
    ttl = title
    if g.get("gain_mean") is not None:
        ttl += "\ngain %+.1f pp [%+.1f, %+.1f], worst budget %+.1f" % (
            100 * g["gain_mean"], 100 * g["gain_ci95"][0], 100 * g["gain_ci95"][1],
            100 * g["gain_worst_budget"])
    ax.set_title(ttl, fontsize=9)
    ax.legend(fontsize=7)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    return path, g


def arrival_figure(cells, path, title):
    plt = _plt()
    m = cells.mechanism("eval")
    G = np.array(m["G"])
    fig, axes = plt.subplots(1, 2, figsize=(8.0, 3.2))
    for i, k in enumerate(m["ks"]):
        axes[0].plot(m["caps"], 100 * G[i], marker="o", ms=3, label="k=%d" % k)
    axes[0].set_xscale("symlog")
    axes[0].set_xlabel("cap")
    axes[0].set_ylabel("share committed (%)")
    axes[0].set_title("commitment arrival G(k, cap)")
    axes[0].legend(fontsize=7)
    axes[1].plot(m["ks"], 100 * np.array(m["c"]), marker="s", label="c: right | committed")
    axes[1].plot(m["ks"], 100 * np.array(m["l"]), marker="^", label="l: right | not committed")
    axes[1].set_xlabel("loops k")
    axes[1].set_ylabel("accuracy (%)")
    axes[1].set_title("reconstruction RMSE %.1f pp (noise floor %.1f)"
                      % (m["rmse_commitment"], m["noise_floor"]))
    axes[1].legend(fontsize=7)
    fig.suptitle(title, fontsize=9)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    return path


def main(argv=None):
    p = argparse.ArgumentParser(prog="prod.analyze.figures")
    p.add_argument("--cells", required=True)
    p.add_argument("--model", required=True)
    p.add_argument("--task", required=True)
    p.add_argument("--protocol", default="natural")
    p.add_argument("--label", default="v2")
    p.add_argument("--out", default=None)
    a = p.parse_args(argv)
    out_dir = a.out or a.cells
    os.makedirs(out_dir, exist_ok=True)
    cells, _paths = load_grid(a.cells, a.model, a.task, a.protocol, a.label)
    stem = "%s_%s" % (a.model.replace("+", "-"), a.task)
    title = "%s / %s / %s (protocol v2)" % (a.model, a.task, a.protocol)
    made = [heatmap(cells, os.path.join(out_dir, "fig_heatmap_%s.pdf" % stem), title),
            frontier(cells, os.path.join(out_dir, "fig_frontier_%s.pdf" % stem), title),
            frontier(cells, os.path.join(out_dir, "fig_frontier_pf_%s.pdf" % stem), title,
                     promptfree=True),
            card_figure(cells, os.path.join(out_dir, "fig_card_%s.pdf" % stem), title),
            arrival_figure(cells, os.path.join(out_dir, "fig_arrival_%s.pdf" % stem), title)]
    from ..cost import model_shapes
    sh = model_shapes(a.model)
    grid = Grid(stem, cells.ks, cells.Bs, cells.idx, cells.acc, cells.ptok,
                sh["layers_per_loop"], cells.reserve, list(cells.split))
    try:
        pth, _g = gain_figure(grid, os.path.join(out_dir, "fig_gain_%s.pdf" % stem), title)
        made.append(pth)
    except ValueError as e:
        print("[skip] gain figure: %s" % e)
    for m in made:
        print("wrote", m)
    return made


if __name__ == "__main__":
    main()
