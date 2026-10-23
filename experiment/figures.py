"""Figures for the paper, sized for one IEEE column (3.5 in)."""
import os

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from common import IMAGENET_MEAN, IMAGENET_STD, RESULTS_DIR, RUN_DIR
from explainers import METHODS, normalise
from sanity import STAGES, test_images

matplotlib.rcParams.update({
    "font.family": "serif", "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
    "font.size": 8, "axes.titlesize": 8, "axes.labelsize": 8, "legend.fontsize": 7,
    "xtick.labelsize": 7, "ytick.labelsize": 7, "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#6b6b66", "axes.linewidth": 0.6, "xtick.color": "#6b6b66", "ytick.color": "#6b6b66",
    "savefig.dpi": 300,
})
# Fixed categorical order; markers are a second channel so identity survives greyscale printing.
STYLE = {
    "Gradient": ("#2a78d6", "o"),
    "Guided Backprop": ("#eb6834", "s"),
    "Integrated Gradients": ("#1baf7a", "^"),
    "Grad-CAM": ("#eda100", "D"),
}
FIG_DIR = os.path.join(RESULTS_DIR, "figures")


def randomisation_curves():
    df = pd.read_csv(os.path.join(RESULTS_DIR, "sanity_randomisation.csv"))
    stages = ["Trained"] + [s for s, _ in STAGES]
    fig, axes = plt.subplots(1, 2, figsize=(3.5, 1.9), sharex=True)
    for ax, metric, label in zip(axes, ["spearman_brain", "ssim"], ["Spearman (brain pixels)", "SSIM"]):
        for method, (colour, marker) in STYLE.items():
            g = df[df.method == method].groupby("stage", sort=False)[metric]
            mean = np.r_[1.0, g.mean().reindex(stages[1:]).values]
            std = np.r_[0.0, g.std().reindex(stages[1:]).values]
            xs = np.arange(len(stages))
            ax.fill_between(xs, mean - std, mean + std, color=colour, alpha=0.12, linewidth=0)
            ax.plot(xs, mean, color=colour, marker=marker, markersize=3.5, linewidth=1.2, label=method)
        ax.set_ylabel(label)
        ax.set_ylim(-0.35, 1.05)
        ax.set_xticks(range(len(stages)))
        ax.set_xticklabels(stages, rotation=60, ha="right")
        ax.grid(axis="y", color="#e4e3dd", linewidth=0.5)
        ax.set_axisbelow(True)
    axes[0].set_xlabel("Randomised down to", labelpad=1)
    axes[1].set_xlabel("Randomised down to", labelpad=1)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=2, frameon=False, bbox_to_anchor=(0.5, 1.04))
    fig.tight_layout(rect=(0, 0, 1, 0.86), w_pad=1.0)
    save(fig, "randomisation_curves")


def example_maps(index=0):
    d = np.load(os.path.join(RUN_DIR, "maps_examples.npz"))
    image = (d["images"][index:index + 1] * IMAGENET_STD.numpy() + IMAGENET_MEAN.numpy())[0]
    flair = np.clip(image[1], 0, 1)
    mask = test_images()[1][index]
    columns = ["Trained", "Logits", "Layer 4", "Conv 1"]
    fig, axes = plt.subplots(len(METHODS), len(columns) + 1, figsize=(3.0, 2.85),
                             gridspec_kw={"wspace": 0.04, "hspace": 0.06})
    for r, method in enumerate(METHODS):
        axes[r, 0].imshow(flair, cmap="gray")
        axes[r, 0].contour(mask, levels=[0.5], colors="#eb6834", linewidths=0.6)
        axes[r, 0].set_ylabel(method.replace("Integrated Gradients", "Int. Grad.").replace(" ", "\n", 1),
                              rotation=0, ha="right", va="center", labelpad=4)
        for c, stage in enumerate(columns, start=1):
            m = normalise(d[f"{method}|{stage}"][index:index + 1])[0]
            axes[r, c].imshow(m, cmap="Blues", vmin=0, vmax=np.quantile(m, 0.995) or 1)
            if r == 0:
                axes[r, c].set_title(stage, pad=2)
    axes[0, 0].set_title("FLAIR", pad=2)
    for ax in axes.ravel():
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
    save(fig, "example_maps")


def save(fig, name):
    os.makedirs(FIG_DIR, exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(FIG_DIR, f"{name}.{ext}"), bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    randomisation_curves()
    example_maps()
