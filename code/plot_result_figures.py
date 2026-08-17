from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "derived_results"
OUTS = [ROOT / "manuscript_digital_health"]
for output_dir in OUTS:
    output_dir.mkdir(parents=True, exist_ok=True)

mpl.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["DejaVu Serif"],
        "font.size": 8.5,
        "axes.labelsize": 9,
        "axes.titlesize": 9,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.fontsize": 8,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "axes.linewidth": 0.7,
    }
)

BLUE = "#0072B2"
VERMILION = "#D55E00"
TEAL = "#009E73"
OCHRE = "#E69F00"
PURPLE = "#CC79A7"
GRAY = "#6E6E6E"
INK = "#222222"
GRID = "#D9D9D9"


def save_figure(fig, name):
    for output_dir in OUTS:
        fig.savefig(output_dir / f"{name}.pdf", bbox_inches="tight", facecolor="white")
        fig.savefig(output_dir / f"{name}.png", dpi=600, bbox_inches="tight", facecolor="white")


def style_axes(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(GRID)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(length=3, width=0.6, color=GRAY)
    ax.grid(axis="y", color=GRID, linewidth=0.55)
    ax.set_axisbelow(True)


def calibration_figure():
    data = pd.read_csv(DATA / "primary_calibration_bins.csv")
    fig, ax = plt.subplots(figsize=(3.55, 3.15), dpi=300)
    ax.plot([0, 0.25], [0, 0.25], linestyle=(0, (3, 2)), color=GRAY, linewidth=1.0, label="Ideal")
    for mode, color, marker in [
        ("Uncalibrated", BLUE, "o"),
        ("Validation-only calibrated", VERMILION, "s"),
    ]:
        subset = data[data["mode"] == mode].sort_values("bin")
        ax.plot(
            subset["weighted_predicted"],
            subset["weighted_observed"],
            color=color,
            marker=marker,
            markersize=4.0,
            markeredgecolor="white",
            markeredgewidth=0.45,
            linewidth=1.35,
            label=mode,
        )
    ax.set_xlim(0, 0.25)
    ax.set_ylim(0, 0.25)
    ax.set_xlabel("Mean predicted 36-month risk")
    ax.set_ylabel("Weighted observed event rate")
    ax.legend(frameon=False, loc="upper left", handlelength=1.8)
    style_axes(ax)
    fig.tight_layout(pad=0.6)
    save_figure(fig, "primary_calibration")
    plt.close(fig)


def coverage_heatmap():
    data = pd.read_csv(DATA / "domain_coverage.csv")
    order = ["demographic", "metabolic", "cardiovascular", "renal"]
    labels = ["Demographic", "Metabolic", "Cardiovascular", "Renal"]
    pivot = data.pivot(index="cycle", columns="domain", values="weighted_variable_coverage")
    pivot = pivot[order] * 100.0
    cmap = LinearSegmentedColormap.from_list(
        "coverage", ["#F7FBFF", "#C6DBEF", "#6BAED6", "#2171B5"], N=256
    )
    fig, ax = plt.subplots(figsize=(4.05, 2.85), dpi=300)
    image = ax.imshow(pivot.to_numpy(), cmap=cmap, vmin=95, vmax=100, aspect="auto")
    ax.set_xticks(np.arange(len(labels)), labels, rotation=25, ha="right")
    ax.set_yticks(np.arange(len(pivot.index)), pivot.index)
    ax.tick_params(length=0)
    for row in range(pivot.shape[0]):
        for col in range(pivot.shape[1]):
            value = pivot.iloc[row, col]
            color = "#F8F7F2" if value >= 98.2 else INK
            ax.text(col, row, f"{value:.1f}%", ha="center", va="center", color=color, fontsize=8)
    ax.set_xlabel("Clinical domain")
    ax.set_ylabel("NHANES cycle")
    ax.spines[:].set_visible(False)
    colorbar = fig.colorbar(image, ax=ax, fraction=0.045, pad=0.03)
    colorbar.set_label("Observed feature fraction (%)", rotation=90, labelpad=8)
    colorbar.outline.set_visible(False)
    colorbar.ax.tick_params(length=2, width=0.5, labelsize=7)
    fig.tight_layout(pad=0.6)
    save_figure(fig, "domain_coverage_heatmap")
    plt.close(fig)


if __name__ == "__main__":
    calibration_figure()
    coverage_heatmap()
