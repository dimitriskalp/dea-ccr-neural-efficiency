"""
figures.py
Thesis figures, one function per figure, saved as PDF and PNG (300 dpi).

Style rules shared by every figure (set_style):
  one font, no titles inside the image (captions live in the thesis),
  axis labels with units, colour-blind-safe palette (Okabe-Ito), light grid.

Usage (from the project root): python src/figures.py [--data PATH] [--out DIR]
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from build_dataset import (DQ_RATIOS, DQ_THRESHOLD, EXCLUDED_STATES,  # noqa: E402
                           MAD_TO_SD, UNSCREENED_FILE, data_quality_screen)

# The data-quality figures describe the screen, so they are drawn from the
# sample BEFORE the state rule and the screen were applied.
DATA_FILE = Path("data/processed") / UNSCREENED_FILE
FIG_DIR = Path("reports/figures")

FONT = "DejaVu Sans"            # ships with matplotlib, identical on every machine
DPI = 300
TEXT_WIDTH_IN = 6.3             # typical thesis text width, A4 with 2.5 cm margins

# Okabe-Ito palette (colour-blind safe). Roles, not slots: a figure never
# uses more than three of these for data.
C = {
    "blue": "#0072B2",
    "vermilion": "#D55E00",
    "vermilion_light": "#EFB08A",   # same hue, lighter: "less severe"
    "green": "#009E73",
    "grey": "#B5B5B5",
    "ink": "#1A1A1A",
    "ink_2": "#5A5A5A",
    "ink_3": "#9A9A9A",
}
THRESHOLDS = (3.5, 4.0, 5.0)
THRESHOLD_INK = (C["ink"], C["ink_2"], C["ink_3"])     # increasing lightness

TOLTEC, SELMAVILLE = "0408550", "1735770"

RATIO_LABEL = {
    "students_per_teacher": "ln(students / teacher FTE)",
    "students_per_other_staff": "ln(students / other-staff FTE)",
    "exp_per_student": "ln(current expenditure / student, USD)",
}

# Hand-placed label anchors (data coordinates: teachers FTE, students) for the
# named districts in the scatter, chosen in empty regions of the plot so that
# no label covers a point. Districts not listed get a small offset.
LABEL_POS = {                    # leaid: (x, y, ha, leader start on text box)
    "0408550": (1.6, 2500, "left", (0.5, 0.5)),    # Toltec
    "0691002": (1.6, 5000, "left", (0.8, 0.0)),    # Butte County OE
    "1735770": (2.5, 600, "left", (0.5, 0.5)),     # Selmaville
    "0405430": (40, 40, "left", (0.5, 0.5)),       # Naco Elementary
    "0691030": (200, 320, "left", (0.5, 0.5)),     # San Diego County OE
    "3200120": (25, 30000, "left", (0.5, 0.5)),    # Elko County
}
# CCD names for Arizona carry the state's own district number, e.g.
# "Naco Elementary District (4176)"; it is dropped from labels only.
STATE_NUMBER = re.compile(r"\s*\(\d+\)\s*$")


def set_style() -> None:
    plt.rcParams.update({
        "font.family": FONT,
        "font.size": 8,
        "axes.labelsize": 8,
        "axes.titlesize": 8,
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
        "legend.fontsize": 7,
        "legend.frameon": False,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.edgecolor": C["ink_2"],
        "axes.linewidth": 0.6,
        "xtick.color": C["ink_2"],
        "ytick.color": C["ink_2"],
        "axes.labelcolor": C["ink"],
        "axes.grid": True,
        "grid.color": "#E6E6E6",
        "grid.linewidth": 0.5,
        "axes.axisbelow": True,
        "lines.linewidth": 1.0,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
        "pdf.fonttype": 42,          # embed TrueType, editable text in the PDF
    })


def save(fig: plt.Figure, name: str, out_dir: Path = FIG_DIR) -> list[Path]:
    """Write <name>.pdf and <name>.png (300 dpi); return the paths."""
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = [out_dir / f"{name}.pdf", out_dir / f"{name}.png"]
    for p in paths:
        fig.savefig(p, dpi=DPI)
    plt.close(fig)
    return paths


# ---------------------------------------------------------------------------
# Figure 1: histograms of the log ratios with median and thresholds
# ---------------------------------------------------------------------------

def fig_log_ratio_histograms(df: pd.DataFrame, out_dir: Path = FIG_DIR
                             ) -> list[Path]:
    """Three panels, one per ratio: histogram of ln(ratio), median (solid),
    median +/- k robust SD for k in THRESHOLDS (dashed, lighter as k grows).
    Counts on a log scale so the tails stay visible."""
    fig, axes = plt.subplots(1, 3, figsize=(TEXT_WIDTH_IN * 1.25, 2.5),
                             sharey=True)
    handles = []
    for ax, (name, (num, den)) in zip(axes, DQ_RATIOS.items()):
        logr = np.log(df[num] / df[den])
        med = logr.median()
        sd = MAD_TO_SD * (logr - med).abs().median()

        ax.hist(logr, bins=80, color=C["blue"], edgecolor="none", alpha=0.9)
        ax.set_yscale("log")
        h_med = ax.axvline(med, color=C["ink"], lw=1.0, zorder=3,
                           label="median")
        handles = [h_med]
        for k, col in zip(THRESHOLDS, THRESHOLD_INK):
            for sign in (-1, 1):
                h = ax.axvline(med + sign * k * sd, color=col, lw=0.8, ls="--",
                               zorder=3, label=f"median ± {k:g} robust SD")
            handles.append(h)
        ax.set_xlabel(RATIO_LABEL[name])
        ax.grid(axis="x", visible=False)
    axes[0].set_ylabel("Districts (log scale)")
    fig.legend(handles=handles, loc="lower center", ncol=4,
               bbox_to_anchor=(0.5, 0.97), columnspacing=1.5)
    fig.subplots_adjust(wspace=0.12, top=0.95)
    return save(fig, "dq_log_ratio_histograms", out_dir)


# ---------------------------------------------------------------------------
# Figure 2: students vs teacher FTE, flagged districts highlighted
# ---------------------------------------------------------------------------

def _label_points(ax, pts: pd.DataFrame, x: str, y: str) -> None:
    """Name labels at hand-placed anchors (LABEL_POS) with a thin leader."""
    for r in pts.itertuples(index=False):
        px, py = getattr(r, x), getattr(r, y)
        if r.leaid in LABEL_POS:
            tx, ty, ha, relpos = LABEL_POS[r.leaid]
            kw = dict(xytext=(tx, ty), textcoords="data")
        else:
            ha, relpos = "left", (0.5, 0.5)
            kw = dict(xytext=(8, 6), textcoords="offset points")
        ax.annotate(STATE_NUMBER.sub("", r.district_name), (px, py),
                    fontsize=6, ha=ha, va="center", color=C["ink"],
                    arrowprops=dict(arrowstyle="-", lw=0.4, color=C["ink_2"],
                                    shrinkA=0, shrinkB=2.5, relpos=relpos),
                    **kw)


def fig_students_vs_teachers(df: pd.DataFrame, out_dir: Path = FIG_DIR
                             ) -> list[Path]:
    """Log-log scatter of students against teacher FTE. Districts flagged at
    |z| > 5 in vermilion, flagged only at |z| > 4 in a lighter tint, the rest
    grey. Toltec, Selmaville and the five most extreme districts are named."""
    dq4 = data_quality_screen(df, 4.0)
    dq5 = data_quality_screen(df, 5.0)
    zcols = [f"z_{k}" for k in DQ_RATIOS]
    d = df[["leaid", "district_name", "students", "staff_teachers_fte"]].copy()
    d["max_abs_z"] = dq4[zcols].abs().max(axis=1)
    d["group"] = np.where(dq5.dq_flag, "5", np.where(dq4.dq_flag, "4", "0"))

    fig, ax = plt.subplots(figsize=(TEXT_WIDTH_IN * 0.85, 4.2))
    x, y = "staff_teachers_fte", "students"
    groups = [("0", C["grey"], f"not flagged (n = {(d.group == '0').sum():,})", 6, 0.35),
              ("4", C["vermilion_light"], f"4 < |z| ≤ 5 (n = {(d.group == '4').sum()})", 16, 0.95),
              ("5", C["vermilion"], f"|z| > 5 (n = {(d.group == '5').sum()})", 16, 0.95)]
    for g, col, label, size, alpha in groups:
        sub = d[d.group == g]
        ax.scatter(sub[x], sub[y], s=size, c=col, alpha=alpha, label=label,
                   edgecolors="white" if g != "0" else "none", linewidths=0.4,
                   zorder=2 if g == "0" else 3)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Teachers (FTE)")
    ax.set_ylabel("Students (fall membership)")

    # Reference lines: median ratio and the DQ_THRESHOLD band, so the
    # colouring is readable without the text.
    logr = np.log(d[y] / d[x])
    med = logr.median()
    sd = MAD_TO_SD * (logr - med).abs().median()
    xx = np.array([d[x].min(), d[x].max()])
    ax.plot(xx, xx * np.exp(med), color=C["ink_2"], lw=0.8, zorder=1)
    for sign in (-1, 1):
        ax.plot(xx, xx * np.exp(med + sign * DQ_THRESHOLD * sd),
                color=C["ink_2"], lw=0.6, ls="--", zorder=1)
    ax.text(xx[1], xx[1] * np.exp(med), " median", fontsize=6,
            color=C["ink_2"], va="center")
    ax.text(xx[1], xx[1] * np.exp(med + DQ_THRESHOLD * sd),
            f" +{DQ_THRESHOLD:g} SD", fontsize=6, color=C["ink_2"], va="center")
    ax.text(xx[1], xx[1] * np.exp(med - DQ_THRESHOLD * sd),
            f" −{DQ_THRESHOLD:g} SD", fontsize=6, color=C["ink_2"], va="center")

    named = pd.concat([d[d.leaid.isin([TOLTEC, SELMAVILLE])],
                       d.nlargest(5, "max_abs_z")]).drop_duplicates("leaid")
    _label_points(ax, named, x, y)

    ax.legend(loc="upper left", markerscale=1.2, handletextpad=0.3)
    return save(fig, "dq_students_vs_teachers", out_dir)


# ---------------------------------------------------------------------------
# Figure 3: students per other-staff FTE by state (median and IQR)
# ---------------------------------------------------------------------------

def state_other_staff_table(df: pd.DataFrame) -> pd.DataFrame:
    """Per state: n, median and quartiles of ln(students / other-staff FTE),
    plus the number of districts the other-staff rule flags at DQ_THRESHOLD.
    Sorted by median, descending."""
    logr = np.log(df["students"] / df["staff_other_fte"])
    dq = data_quality_screen(df, DQ_THRESHOLD)
    hit = dq["z_students_per_other_staff"].abs() > DQ_THRESHOLD
    t = (pd.DataFrame({"state": df["state"], "logr": logr, "hit": hit})
         .groupby("state")
         .agg(n=("logr", "size"), q25=("logr", lambda s: s.quantile(0.25)),
              median=("logr", "median"),
              q75=("logr", lambda s: s.quantile(0.75)),
              flagged_other_staff=("hit", "sum"))
         .sort_values("median", ascending=False)
         .reset_index())
    for c in ("q25", "median", "q75"):
        t[f"ratio_{c}"] = np.exp(t[c])
    return t


def fig_state_other_staff_ratio(df: pd.DataFrame, out_dir: Path = FIG_DIR
                                ) -> list[Path]:
    """Horizontal dot-and-whisker plot, one row per state: median (dot) and
    interquartile range (whisker) of ln(students / other-staff FTE), sorted.
    National median as a vertical reference line. States whose median is
    more than twice the national median are highlighted."""
    t = state_other_staff_table(df)
    logr = np.log(df["students"] / df["staff_other_fte"])
    nat_med = logr.median()
    outlying = t["median"] > nat_med + np.log(2)

    fig, ax = plt.subplots(figsize=(TEXT_WIDTH_IN * 0.8, 0.135 * len(t) + 0.8))
    ypos = np.arange(len(t))[::-1]
    for y, r, out in zip(ypos, t.itertuples(index=False), outlying):
        col = C["vermilion"] if out else C["blue"]
        ax.plot([r.q25, r.q75], [y, y], color=col, lw=1.2, solid_capstyle="butt",
                zorder=2)
        ax.plot(r.median, y, "o", ms=3.5, color=col, mec="white", mew=0.5,
                zorder=3)
    ax.axvline(nat_med, color=C["ink_2"], lw=0.8, zorder=1)
    ax.text(nat_med, len(t) - 0.2, "national median", fontsize=6,
            color=C["ink_2"], ha="left", va="bottom")

    ax.set_yticks(ypos)
    ax.set_yticklabels([f"{s} ({n})" for s, n in zip(t.state, t.n)], fontsize=6)
    ax.set_ylim(-0.8, len(t) + 0.6)
    ax.set_xlabel("ln(students / other-staff FTE), median and IQR")
    ax.grid(axis="y", visible=False)
    ax.tick_params(axis="y", length=0)

    # Second scale on top in ratio units, so the reader need not exponentiate.
    top = ax.secondary_xaxis(
        "top", functions=(np.exp, lambda v: np.log(np.maximum(v, 1e-9))))
    top.set_xlabel("students per other-staff FTE")
    top.set_xticks([2, 5, 10, 20, 50, 100])
    top.tick_params(labelsize=7)

    from matplotlib.lines import Line2D
    handles = [Line2D([], [], color=C["blue"], marker="o", ms=3.5, lw=1.2,
                      label="state median and IQR"),
               Line2D([], [], color=C["vermilion"], marker="o", ms=3.5, lw=1.2,
                      label="median > 2 × national median")]
    ax.legend(handles=handles, loc="lower right", fontsize=6)
    return save(fig, "dq_state_other_staff_ratio", out_dir)


# ---------------------------------------------------------------------------
# Figure 4: V33 vs SEDA grade 3-8 enrollment, by grade span
# ---------------------------------------------------------------------------

def fig_enrollment_ratio_histograms(df: pd.DataFrame, out_dir: Path = FIG_DIR
                                    ) -> list[Path]:
    """Two panels: histogram of ln(students / cov_enrl_g38) for districts
    that offer any of grades 9-12 and for K-8-only districts (variant B
    grouping, as in the build), each with its own median and
    +/- DQ_THRESHOLD robust SD lines. Drawn from the sample the screen is
    evaluated on in the build: after the state rule and the data-quality
    screen, before the screen itself (see main)."""
    from screens import enrollment_consistency_screen, offers_high_school
    hs = offers_high_school(df.leaid, df.district_name, refine=True)
    ec = enrollment_consistency_screen(df, hs)

    fig, axes = plt.subplots(1, 2, figsize=(TEXT_WIDTH_IN, 2.5), sharey=True,
                             sharex=True)
    handles = []
    bins = np.linspace(ec.log_ratio.min(), ec.log_ratio.max(), 90)
    for ax, g in zip(axes, ("offers 9-12", "K-8 only")):
        lr = ec.loc[ec.group == g, "log_ratio"].dropna()
        med = lr.median()
        sd = MAD_TO_SD * (lr - med).abs().median()
        ax.hist(lr, bins=bins, color=C["blue"], edgecolor="none", alpha=0.9)
        ax.set_yscale("log")
        h_med = ax.axvline(med, color=C["ink"], lw=1.0, zorder=3, label="median")
        for sign in (-1, 1):
            h = ax.axvline(med + sign * DQ_THRESHOLD * sd, color=C["ink_2"],
                           lw=0.8, ls="--", zorder=3,
                           label=f"median ± {DQ_THRESHOLD:g} robust SD")
        handles = [h_med, h]
        ax.text(0.98, 0.95, f"{g}\nn = {len(lr):,}", transform=ax.transAxes,
                ha="right", va="top", fontsize=7, color=C["ink"])
        ax.set_xlabel("ln(fall membership / grade 3-8 enrollment)")
        ax.grid(axis="x", visible=False)
    axes[0].set_ylabel("Districts (log scale)")
    fig.legend(handles=handles, loc="lower center", ncol=2,
               bbox_to_anchor=(0.5, 0.97))
    fig.subplots_adjust(wspace=0.1, top=0.95)
    return save(fig, "dq_enrollment_ratio_histograms", out_dir)


# ---------------------------------------------------------------------------

ALL_FIGURES = [fig_log_ratio_histograms, fig_students_vs_teachers,
               fig_state_other_staff_ratio]
POST_DQ_FIGURES = [fig_enrollment_ratio_histograms]   # sample after state rule + DQ


def post_dq_sample(df: pd.DataFrame) -> pd.DataFrame:
    """The unscreened sample after the state rule and the data-quality
    screen, i.e. the sample the later screens are evaluated on in the build.
    Rebuilt here because the main dataset has already had them applied."""
    df = df[~df.state.isin(EXCLUDED_STATES)].reset_index(drop=True)
    dq = data_quality_screen(df, DQ_THRESHOLD)
    return df[~dq.dq_flag].reset_index(drop=True)


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--data", type=Path, default=DATA_FILE,
                   help="unscreened sample for the data-quality figures")
    p.add_argument("--out", type=Path, default=FIG_DIR)
    args = p.parse_args(argv)

    set_style()
    df = pd.read_csv(args.data, dtype={"leaid": str})
    for func in ALL_FIGURES:
        for path in func(df, args.out):
            print(f"wrote {path}")
    post_dq = post_dq_sample(df)
    print(f"post-data-quality sample: {len(post_dq):,} districts")
    for func in POST_DQ_FIGURES:
        for path in func(post_dq, args.out):
            print(f"wrote {path}")


if __name__ == "__main__":
    main()
