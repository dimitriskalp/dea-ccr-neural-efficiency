"""
dea.py
Data Envelopment Analysis for the school district sample (2018-19).

Models (all input-oriented, envelopment form, one LP per district, HiGHS):
  CCR   constant returns to scale, two phases: phase 1 gives theta, phase 2
        fixes theta and maximises the slacks (strong vs weak efficiency).
  BCC   variable returns to scale (sum of lambda = 1), phase 1 only.
  Scale efficiency = theta_CCR / theta_BCC.
  Super-efficiency (Andersen-Petersen, CCR) for the CCR-efficient units.

The DEA variables are imported from build_dataset.py so that the dataset and
the model can never disagree.

Numerical conditioning: every column is divided by its mean before solving.
CCR and BCC are invariant to such a rescaling, so the scores do not change
(tests/test_dea.py proves it); slacks are converted back to original units.

Input  : data/processed/dea_districts_2019.csv
Output : data/processed/dea_scores_2019.csv
         reports/dea_summary.md
         reports/dea_run_meta.json
         (with the suffix _sample{N} when --sample is used)

Usage (from the project root):
  python src/dea.py --model ccr|bcc|all [--sample N] [--seed S] [--n-jobs K]
                    [--time-serial-phase1] [--compare SCORES_CSV]

--time-serial-phase1 re-solves CCR phase 1 with n_jobs = 1 after the main
run and records that wall-clock time separately (the benchmark against the
neural-network prediction time). --compare adds a section to the summary
contrasting peer concentration and top super-efficiency units with an
earlier scores file (e.g. the 500-district sample).
"""

from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from scipy.optimize import linprog

from build_dataset import DEA_INPUTS, DEA_OUTPUTS

DATA_FILE = Path("data/processed/dea_districts_2019.csv")
SCORES_FILE = Path("data/processed/dea_scores_2019.csv")
SUMMARY_FILE = Path("reports/dea_summary.md")
META_FILE = Path("reports/dea_run_meta.json")

# Tolerance for "efficient": theta >= 1 - EFF_TOL, and for "strongly
# efficient" additionally every rescaled slack <= EFF_TOL.
# Why 1e-6: HiGHS solves to a primal/dual feasibility tolerance of 1e-7, so
# optimal values carry noise of that order. One order of magnitude above the
# solver tolerance separates true ties from noise, while 1e-6 is still far
# below any economically meaningful difference in efficiency (0.0001 %).
# The same constant is used for the lambda cut-off that defines a peer.
EFF_TOL = 1e-6

# scipy.optimize.linprog status codes -> short labels for the CSV.
STATUS = {0: "optimal", 1: "iteration_limit", 2: "infeasible",
          3: "unbounded", 4: "numerical_difficulties"}
SKIPPED = "skipped"


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

def load_data(path: Path = DATA_FILE, sample: int | None = None,
              seed: int = 42) -> pd.DataFrame:
    """Read the district dataset, optionally a seeded random subset."""
    df = pd.read_csv(path, dtype={"leaid": str})
    if sample is not None and sample < len(df):
        df = df.sample(n=sample, random_state=seed).sort_values("leaid")
    return df.reset_index(drop=True)


def rescale(M: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Divide each column by its mean. Returns (scaled matrix, means)."""
    means = M.mean(axis=0)
    return M / means, means


# ---------------------------------------------------------------------------
# Linear programs (one district at a time)
# ---------------------------------------------------------------------------

def _solve(**kwargs):
    return linprog(method="highs", **kwargs)


def solve_phase1(X: np.ndarray, Y: np.ndarray, o: int, convex: bool = False,
                 exclude_self: bool = False) -> tuple[float, str]:
    """Input-oriented envelopment LP for unit o.  Returns (theta, status).

        min  theta
        s.t. sum_j lambda_j x_ij <= theta x_io        (inputs)
             sum_j lambda_j y_rj >= y_ro              (outputs)
             sum_j lambda_j = 1          if convex    (BCC)
             lambda_o = 0                if exclude_self (super-efficiency)
             lambda >= 0

    Variables: [theta, lambda_1 .. lambda_n].
    """
    n, m = X.shape
    s = Y.shape[1]
    c = np.zeros(n + 1)
    c[0] = 1.0

    A_ub = np.empty((m + s, n + 1))
    A_ub[:m, 0] = -X[o]
    A_ub[:m, 1:] = X.T
    A_ub[m:, 0] = 0.0
    A_ub[m:, 1:] = -Y.T
    b_ub = np.concatenate([np.zeros(m), -Y[o]])

    A_eq = b_eq = None
    if convex:
        A_eq = np.ones((1, n + 1))
        A_eq[0, 0] = 0.0
        b_eq = np.ones(1)

    bounds: tuple | np.ndarray = (0.0, None)
    if exclude_self:
        bounds = np.column_stack([np.zeros(n + 1), np.full(n + 1, np.inf)])
        bounds[o + 1, 1] = 0.0

    res = _solve(c=c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq,
                 bounds=bounds)
    theta = float(res.x[0]) if res.status == 0 else np.nan
    return theta, STATUS.get(res.status, str(res.status))


def solve_phase2(X: np.ndarray, Y: np.ndarray, o: int, theta: float
                 ) -> tuple[np.ndarray, np.ndarray, np.ndarray, str]:
    """CCR phase 2: fix theta, maximise the sum of slacks.

        max  sum(s_in) + sum(s_out)
        s.t. sum_j lambda_j x_ij + s_in_i  = theta x_io
             sum_j lambda_j y_rj - s_out_r = y_ro
             lambda, s_in, s_out >= 0

    Variables: [lambda_1 .. lambda_n, s_in_1 .. s_in_m, s_out_1 .. s_out_s].
    Returns (lambda, input slacks, output slacks, status); NaN on failure.
    """
    n, m = X.shape
    s = Y.shape[1]
    if not np.isfinite(theta):
        nan = np.full
        return nan(n, np.nan), nan(m, np.nan), nan(s, np.nan), SKIPPED

    c = np.concatenate([np.zeros(n), -np.ones(m + s)])
    A_eq = np.zeros((m + s, n + m + s))
    A_eq[:m, :n] = X.T
    A_eq[:m, n:n + m] = np.eye(m)
    A_eq[m:, :n] = Y.T
    A_eq[m:, n + m:] = -np.eye(s)
    b_eq = np.concatenate([theta * X[o], Y[o]])

    res = _solve(c=c, A_eq=A_eq, b_eq=b_eq, bounds=(0.0, None))
    if res.status != 0:
        nan = np.full
        return (nan(n, np.nan), nan(m, np.nan), nan(s, np.nan),
                STATUS.get(res.status, str(res.status)))
    lam = res.x[:n]
    return lam, res.x[n:n + m], res.x[n + m:], STATUS[0]


# ---------------------------------------------------------------------------
# Running a stage over many districts (serial or joblib)
# ---------------------------------------------------------------------------

def _chunk_phase1(X, Y, idx, convex, exclude_self):
    return [solve_phase1(X, Y, o, convex, exclude_self) for o in idx]


def _chunk_phase2(X, Y, idx, theta):
    return [solve_phase2(X, Y, o, theta[o]) for o in idx]


def _run_chunks(func, idx: np.ndarray, n_jobs: int, *args) -> list:
    """Apply func to chunks of indices, serially or with joblib.

    Every LP is independent and HiGHS is deterministic, so the result does
    not depend on n_jobs or on the chunking (tests check serial == parallel).
    """
    if n_jobs == 1:
        return func(*args[:2], idx, *args[2:])
    chunks = np.array_split(idx, max(1, 4 * n_jobs))
    chunks = [c for c in chunks if len(c)]
    parts = joblib.Parallel(n_jobs=n_jobs)(
        joblib.delayed(func)(*args[:2], c, *args[2:]) for c in chunks)
    return [r for part in parts for r in part]


# ---------------------------------------------------------------------------
# Full DEA run
# ---------------------------------------------------------------------------

def run_dea(X: np.ndarray, Y: np.ndarray, model: str = "all",
            n_jobs: int = 1, do_rescale: bool = True,
            verbose: bool = True) -> dict:
    """Solve the requested models for every row of X (inputs) and Y (outputs).

    Returns a dict of arrays, keyed by name, plus "timings" (seconds per
    stage) and "status_*" lists. Slacks and lambdas are in ORIGINAL units.
    """
    X = np.asarray(X, dtype=float)
    Y = np.asarray(Y, dtype=float)
    n, m = X.shape
    s = Y.shape[1]
    idx = np.arange(n)
    out: dict = {"n": n, "timings": {}}

    if do_rescale:
        Xs, x_mean = rescale(X)
        Ys, y_mean = rescale(Y)
    else:
        Xs, Ys = X, Y
        x_mean, y_mean = np.ones(m), np.ones(s)

    def stage(name, func, *args):
        if verbose:
            print(f"  {name:<22s}", end="", flush=True)
        t0 = time.perf_counter()
        res = _run_chunks(func, idx, n_jobs, Xs, Ys, *args)
        dt = time.perf_counter() - t0
        out["timings"][name] = dt
        if verbose:
            print(f"{dt:8.1f} s")
        return res

    if model in ("ccr", "all", "ccr_phase1_only"):
        p1 = stage("ccr_phase1", _chunk_phase1, False, False)
        out["theta_ccr"] = np.array([t for t, _ in p1])
        out["status_ccr_p1"] = [st for _, st in p1]

    if model == "ccr_phase1_only":            # timing benchmark only
        out["timings"]["total"] = out["timings"]["ccr_phase1"]
        return out

    if model in ("ccr", "all"):
        p2 = stage("ccr_phase2", _chunk_phase2, out["theta_ccr"])
        lam = np.vstack([r[0] for r in p2])              # (n, n)
        s_in = np.vstack([r[1] for r in p2])              # rescaled units
        s_out = np.vstack([r[2] for r in p2])
        out["status_ccr_p2"] = [r[3] for r in p2]
        out["lambda"] = lam                               # lambda is unit-free

        # Strong efficiency is decided on the rescaled slacks, so that one
        # tolerance applies to dollars and FTE alike.
        max_slack = np.nanmax(np.hstack([s_in, s_out]), axis=1, initial=0.0)

        # Slacks below the tolerance are solver noise (e.g. -0.0 or 1e-12):
        # set them to exactly 0, then convert back to original units.
        s_in = np.where(s_in <= EFF_TOL, 0.0, s_in)
        s_out = np.where(s_out <= EFF_TOL, 0.0, s_out)
        out["slack_in"] = s_in * x_mean
        out["slack_out"] = s_out * y_mean
        efficient = out["theta_ccr"] >= 1.0 - EFF_TOL
        out["efficient_ccr"] = efficient
        out["strongly_efficient"] = efficient & (max_slack <= EFF_TOL)

        # Peers: units with lambda above the tolerance in the phase-2 solution.
        peers = [np.flatnonzero(lam[o] > EFF_TOL) if np.isfinite(lam[o, 0])
                 else np.array([], dtype=int) for o in idx]
        out["peers"] = peers
        out["n_peers"] = np.array([len(p) for p in peers])
        peer_count = np.zeros(n, dtype=int)
        for o, p in enumerate(peers):
            peer_count[p[p != o]] += 1                    # exclude self
        out["peer_count"] = peer_count

        # Super-efficiency only for the CCR-efficient units (NaN otherwise).
        eff_idx = np.flatnonzero(efficient)
        sup = np.full(n, np.nan)
        status_sup = [SKIPPED] * n
        if len(eff_idx):
            if verbose:
                print(f"  {'super_eff':<22s}", end="", flush=True)
            t0 = time.perf_counter()
            res = _run_chunks(_chunk_phase1, eff_idx, n_jobs, Xs, Ys,
                              False, True)
            out["timings"]["super_eff"] = time.perf_counter() - t0
            if verbose:
                print(f"{out['timings']['super_eff']:8.1f} s")
            for o, (t, st) in zip(eff_idx, res):
                sup[o], status_sup[o] = t, st
        out["super_eff"] = sup
        out["status_super"] = status_sup

    if model in ("bcc", "all"):
        b1 = stage("bcc_phase1", _chunk_phase1, True, False)
        out["theta_bcc"] = np.array([t for t, _ in b1])
        out["status_bcc"] = [st for _, st in b1]

    if "theta_ccr" in out and "theta_bcc" in out:
        out["scale_eff"] = out["theta_ccr"] / out["theta_bcc"]

    out["timings"]["total"] = sum(out["timings"].values())
    return out


# ---------------------------------------------------------------------------
# Results table
# ---------------------------------------------------------------------------

def results_frame(df: pd.DataFrame, res: dict) -> pd.DataFrame:
    """Combine the DEA results with district identifiers into one table."""
    n = res["n"]
    leaid = df["leaid"].to_numpy()
    nan = np.full(n, np.nan)
    tbl = pd.DataFrame({
        "leaid": leaid,
        "district_name": df["district_name"].to_numpy(),
        "state": df["state"].to_numpy(),
        "theta_ccr": res.get("theta_ccr", nan),
        "theta_bcc": res.get("theta_bcc", nan),
        "scale_eff": res.get("scale_eff", nan),
        "super_eff": res.get("super_eff", nan),
        "strongly_efficient": res.get("strongly_efficient",
                                      np.zeros(n, dtype=bool)),
    })
    if "slack_in" in res:
        # Slacks in original units (dollars, FTE, output units).
        for k, v in enumerate(DEA_INPUTS):
            tbl[f"slack_{v}"] = res["slack_in"][:, k]
        for k, v in enumerate(DEA_OUTPUTS):
            tbl[f"slack_{v}"] = res["slack_out"][:, k]
        tbl["n_peers"] = res["n_peers"]
        tbl["peer_count"] = res["peer_count"]
        tbl["peers"] = [
            json.dumps({leaid[j]: round(float(res["lambda"][o, j]), 6)
                        for j in p}, separators=(",", ":"))
            for o, p in enumerate(res["peers"])]
    for key in ("status_ccr_p1", "status_ccr_p2", "status_super",
                "status_bcc"):
        if key in res:
            tbl[key] = res[key]
    return tbl


# ---------------------------------------------------------------------------
# Reports
# ---------------------------------------------------------------------------

def _md_table(frame: pd.DataFrame, floatfmt: str = "{:.4f}") -> str:
    """Minimal markdown table (avoids a tabulate dependency)."""
    def fmt(v):
        if isinstance(v, (float, np.floating)):
            if not np.isfinite(v):
                return "nan"
            return floatfmt.format(v)
        return str(v)
    cols = list(frame.columns)
    lines = ["| " + " | ".join(cols) + " |",
             "|" + "|".join("---" for _ in cols) + "|"]
    for row in frame.itertuples(index=False):
        lines.append("| " + " | ".join(fmt(v) for v in row) + " |")
    return "\n".join(lines)


def _distribution(x: pd.Series) -> pd.DataFrame:
    q = x.quantile([0.05, 0.25, 0.5, 0.75, 0.95])
    bins = [0, 0.5, 0.6, 0.7, 0.8, 0.9, 1 - EFF_TOL, np.inf]
    labels = ["<0.5", "0.5-0.6", "0.6-0.7", "0.7-0.8", "0.8-0.9",
              "0.9-<1", "=1"]
    counts = pd.cut(x, bins=bins, labels=labels, right=False).value_counts(
        sort=False)
    f = "{:.4f}".format
    rows = [("n", str(len(x))), ("mean", f(x.mean())), ("std", f(x.std())),
            ("min", f(x.min())), ("p05", f(q[0.05])), ("p25", f(q[0.25])),
            ("median", f(q[0.5])), ("p75", f(q[0.75])), ("p95", f(q[0.95])),
            ("max", f(x.max()))]
    rows += [(f"count {lab}", str(int(c))) for lab, c in counts.items()]
    return pd.DataFrame(rows, columns=["statistic", "value"])


def _outlier_table(df: pd.DataFrame, tbl: pd.DataFrame, denom: str,
                   top_peers: set, k: int = 20) -> pd.DataFrame:
    """Top-k districts by (out_math + out_rla) / denom."""
    total_out = df[DEA_OUTPUTS].sum(axis=1)
    ratio = total_out / df[denom]
    med = ratio.median()
    t = pd.DataFrame({
        "leaid": df["leaid"], "district_name": df["district_name"],
        "state": df["state"], "ratio": ratio, "ratio_over_median": ratio / med,
        "theta_ccr": tbl["theta_ccr"],
        "efficient": np.where(tbl["theta_ccr"] >= 1 - EFF_TOL, "yes", "no"),
        "top20_peer": ["yes" if l in top_peers else "no" for l in df["leaid"]],
    })
    return t.sort_values("ratio", ascending=False).head(k)


def write_summary(df: pd.DataFrame, tbl: pd.DataFrame, res: dict,
                  path: Path, n_jobs: int, meta: dict) -> None:
    has_ccr = "theta_ccr" in res
    has_bcc = "theta_bcc" in res
    L = [f"# DEA results, school districts 2018-19", "",
         f"Run: {meta['timestamp']}  |  n = {res['n']:,} districts  |  "
         f"n_jobs = {n_jobs}  |  tolerance = {EFF_TOL:g}", "",
         f"Inputs: {', '.join(DEA_INPUTS)}  ", f"Outputs: {', '.join(DEA_OUTPUTS)}",
         "", "Models: input-oriented envelopment form, HiGHS. Variables were "
         "divided by their column means before solving (CCR/BCC are invariant "
         "to this). Slacks in the CSV are in original units.", ""]

    L += ["## Runtime (wall-clock seconds)", ""]
    L.append(_md_table(pd.DataFrame(list(res["timings"].items()),
                                    columns=["stage", "seconds"]), "{:.2f}"))
    if has_ccr:
        L.append(f"\nCCR phase 1 alone: **{res['timings']['ccr_phase1']:.2f} s** "
                 f"for {res['n']:,} LPs ({1000 * res['timings']['ccr_phase1'] / res['n']:.2f} ms per district, n_jobs = {n_jobs}).")
        if "ccr_phase1_serial" in res["timings"]:
            t = res["timings"]["ccr_phase1_serial"]
            L.append(f"\nCCR phase 1, separate serial run (n_jobs = 1): "
                     f"**{t:.2f} s** ({1000 * t / res['n']:.2f} ms per district). "
                     "Scores identical to the parallel run: "
                     f"{'yes' if res.get('serial_identical') else 'NO'}.")
    L.append("")

    L += ["## Solver status", ""]
    for key in ("status_ccr_p1", "status_ccr_p2", "status_super", "status_bcc"):
        if key in tbl:
            L.append(f"- {key}: " + ", ".join(
                f"{k} = {v:,}" for k, v in tbl[key].value_counts().items()))
    L.append("")

    if has_ccr:
        eff = tbl["theta_ccr"] >= 1 - EFF_TOL
        L += ["## CCR (constant returns to scale)", "",
              f"- efficient (theta >= 1 - {EFF_TOL:g}): {int(eff.sum()):,}",
              f"- strongly efficient (all slacks <= {EFF_TOL:g} rescaled): "
              f"{int(tbl['strongly_efficient'].sum()):,}",
              f"- weakly efficient (theta = 1, positive slack): "
              f"{int((eff & ~tbl['strongly_efficient']).sum()):,}",
              f"- median theta: {tbl['theta_ccr'].median():.4f}", "",
              _md_table(_distribution(tbl["theta_ccr"].dropna())), ""]
    if has_bcc:
        effb = tbl["theta_bcc"] >= 1 - EFF_TOL
        L += ["## BCC (variable returns to scale)", "",
              f"- efficient: {int(effb.sum()):,}",
              f"- median theta: {tbl['theta_bcc'].median():.4f}", "",
              _md_table(_distribution(tbl["theta_bcc"].dropna())), ""]
    if has_ccr and has_bcc:
        pr = tbl["theta_ccr"].corr(tbl["theta_bcc"])
        sp = tbl["theta_ccr"].corr(tbl["theta_bcc"], method="spearman")
        L += ["## Scale efficiency and CCR vs BCC", "",
              f"- correlation CCR vs BCC: Pearson {pr:.4f}, Spearman {sp:.4f}",
              f"- median scale efficiency: {tbl['scale_eff'].median():.4f}",
              f"- units with theta_CCR > theta_BCC + {EFF_TOL:g} (must be 0): "
              f"{int((tbl['theta_ccr'] > tbl['theta_bcc'] + EFF_TOL).sum())}",
              "", _md_table(_distribution(tbl["scale_eff"].dropna())), ""]

    if has_ccr:
        cols = ["leaid", "district_name", "state", "super_eff", "theta_bcc",
                "peer_count", "n_peers"]
        cols = [c for c in cols if c in tbl]
        top_sup = (tbl[tbl["super_eff"].notna()]
                   .sort_values("super_eff", ascending=False).head(20))
        L += [f"## {len(top_sup)} highest super-efficiency scores (outlier review)", "",
              "Super-efficiency > 1 is only computed for CCR-efficient units. "
              "Values far above the rest indicate a unit without close "
              "comparators; review before deciding whether to keep it.", "",
              _md_table(top_sup[cols]), ""]

        top_peer = (tbl[tbl["peer_count"] > 0]
                    .sort_values("peer_count", ascending=False).head(20))
        cols = ["leaid", "district_name", "state", "peer_count", "super_eff",
                "theta_bcc"]
        cols = [c for c in cols if c in tbl]
        L += [f"## {len(top_peer)} most frequent peers", "",
              "peer_count = number of OTHER districts whose CCR phase-2 "
              "reference set includes this district (lambda > tolerance).", "",
              _md_table(top_peer[cols]), ""]

        top_peers = set(top_peer["leaid"])
        L += ["## Extreme input-output ratios (flagged, not removed)", "",
              "ratio = (out_math + out_rla) / input. These districts are kept "
              "in the sample; they are listed so the decision can be made "
              "explicitly.", "",
              "### Top 20 output per teacher FTE", "",
              _md_table(_outlier_table(df, tbl, "staff_teachers_fte", top_peers)),
              "", "### Top 20 output per current-expenditure dollar", "",
              _md_table(_outlier_table(df, tbl, "exp_current", top_peers),
                        "{:.6f}"), ""]

        notes = []
        n_dom = int((tbl["peer_count"] > 0.1 * res["n"]).sum())
        if n_dom:
            notes.append(f"{n_dom} district(s) serve as peer for more than 10 % "
                         "of the sample.")
        if tbl["super_eff"].max() > 2:
            notes.append(f"max super-efficiency {tbl['super_eff'].max():.2f} "
                         "(> 2): check that district's data.")
        n_small = int((df["staff_teachers_fte"] < 5).sum())
        if n_small:
            notes.append(f"{n_small} district(s) report fewer than 5 teacher FTE.")
        L += ["## Flags", ""] + [f"- {x}" for x in notes or ["none"]] + [""]

    if meta.get("compare_with"):
        L += comparison_section(tbl, Path(meta["compare_with"]))

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(L), encoding="utf-8")


def peer_concentration(tbl: pd.DataFrame) -> dict:
    """Summary numbers on how concentrated the reference sets are."""
    n = len(tbl)
    eff = tbl["theta_ccr"] >= 1 - EFF_TOL
    pc = tbl["peer_count"]
    return {
        "n": n,
        "efficient_ccr": int(eff.sum()),
        "peers_used_by_>10%": int((pc > 0.1 * n).sum()),
        "peers_used_by_>50%": int((pc > 0.5 * n).sum()),
        "top_peer_share": float(pc.max() / n),
        "top3_peer_share": float(pc.nlargest(3).sum() / (3 * n)),
        "median_n_peers": float(tbl["n_peers"].median()),
        "max_super_eff": float(tbl["super_eff"].max()),
        "super_eff_>1.5": int((tbl["super_eff"] > 1.5).sum()),
    }


def comparison_section(tbl: pd.DataFrame, other_path: Path) -> list[str]:
    """Markdown comparing this run with an earlier scores file."""
    other = pd.read_csv(other_path, dtype={"leaid": str})
    a, b = peer_concentration(tbl), peer_concentration(other)

    def fmt(v):
        return f"{v:,}" if isinstance(v, int) else f"{v:.3f}"
    rows = pd.DataFrame({"measure": list(a),
                         "this run": [fmt(v) for v in a.values()],
                         other_path.name: [fmt(v) for v in b.values()]})
    L = [f"## Comparison with {other_path.name}", "",
         "Peer concentration and super-efficiency, this run versus the earlier "
         "file. Shares are fractions of the respective sample size.", "",
         _md_table(rows, "{:.3f}"), ""]

    def top(t, col, k=5):
        t = t[t[col].notna()].sort_values(col, ascending=False).head(k)
        f = "{:.3f}" if col == "super_eff" else "{:,.0f}"
        return [f"{r.district_name} ({r.state}, {f.format(getattr(r, col))})"
                for r in t.itertuples(index=False)]
    for col, label in (("super_eff", "Top 5 super-efficiency"),
                       ("peer_count", "Top 5 most frequent peers")):
        L += [f"### {label}", "", f"- this run: " + "; ".join(top(tbl, col)),
              f"- {other_path.name}: " + "; ".join(top(other, col)), ""]
    both = set(tbl.leaid) & set(other.leaid)
    eff_other = other[other.theta_ccr >= 1 - EFF_TOL].leaid
    still = tbl[tbl.leaid.isin(eff_other) & (tbl.theta_ccr >= 1 - EFF_TOL)]
    gone = sorted(set(eff_other) - set(tbl.leaid))
    L += [f"- districts in both files: {len(both):,}; CCR-efficient in "
          f"{other_path.name}: {len(eff_other)}, of which still efficient here: "
          f"{len(still)}, no longer in the sample: {len(gone)}", ""]
    return L


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"],
                                       text=True).strip()
    except Exception:  # not a repo, git missing
        return "unknown"


def run_meta(args, res: dict) -> dict:
    import scipy
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "python": platform.python_version(),
        "packages": {"numpy": np.__version__, "pandas": pd.__version__,
                     "scipy": scipy.__version__, "joblib": joblib.__version__},
        "solver": "scipy.optimize.linprog(method='highs')",
        "tolerance": EFF_TOL,
        "model": args.model, "sample": args.sample, "seed": args.seed,
        "n_jobs": args.n_jobs, "n_units": res["n"],
        "inputs": DEA_INPUTS, "outputs": DEA_OUTPUTS,
        "rescaled_by_column_mean": True,
        "runtime_seconds": res["timings"],
        "serial_phase1_identical_to_parallel": res.get("serial_identical"),
        "compare_with": str(args.compare) if args.compare else None,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _with_suffix(path: Path, suffix: str) -> Path:
    return path.with_name(path.stem + suffix + path.suffix)


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--model", choices=["ccr", "bcc", "all"], default="all")
    p.add_argument("--sample", type=int, default=None,
                   help="random seeded subset of N districts")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--n-jobs", type=int, default=1)
    p.add_argument("--data", type=Path, default=DATA_FILE)
    p.add_argument("--time-serial-phase1", action="store_true",
                   help="also time CCR phase 1 with n_jobs = 1, separately")
    p.add_argument("--compare", type=Path, default=None,
                   help="earlier scores CSV to compare against in the summary")
    args = p.parse_args(argv)

    df = load_data(args.data, args.sample, args.seed)
    print(f"{len(df):,} districts, model = {args.model}, n_jobs = {args.n_jobs}")
    X = df[DEA_INPUTS].to_numpy(float)
    Y = df[DEA_OUTPUTS].to_numpy(float)

    res = run_dea(X, Y, model=args.model, n_jobs=args.n_jobs)

    if args.time_serial_phase1 and args.model in ("ccr", "all"):
        # The benchmark number: one LP per district, one core, nothing else.
        print("  serial CCR phase 1   ", end="", flush=True)
        t0 = time.perf_counter()
        serial = run_dea(X, Y, model="ccr_phase1_only", n_jobs=1, verbose=False)
        res["timings"]["ccr_phase1_serial"] = time.perf_counter() - t0
        print(f"{res['timings']['ccr_phase1_serial']:8.1f} s")
        res["serial_identical"] = bool(np.array_equal(
            serial["theta_ccr"], res["theta_ccr"], equal_nan=True))
        if not res["serial_identical"]:
            print("WARNING: serial phase-1 scores differ from the parallel run")

    tbl = results_frame(df, res)
    meta = run_meta(args, res)

    suffix = f"_sample{args.sample}" if args.sample else ""
    scores, summary, metaf = (_with_suffix(f, suffix) for f in
                              (SCORES_FILE, SUMMARY_FILE, META_FILE))
    scores.parent.mkdir(parents=True, exist_ok=True)
    tbl.to_csv(scores, index=False)
    write_summary(df, tbl, res, summary, args.n_jobs, meta)
    metaf.parent.mkdir(parents=True, exist_ok=True)
    metaf.write_text(json.dumps(meta, indent=2), encoding="utf-8")

    print(f"\nwrote {scores}\n      {summary}\n      {metaf}")
    if "theta_ccr" in tbl:
        print(f"\nCCR efficient: {int((tbl.theta_ccr >= 1 - EFF_TOL).sum()):,}"
              f"  strongly: {int(tbl.strongly_efficient.sum()):,}"
              f"  median theta_ccr: {tbl.theta_ccr.median():.4f}")
    if "theta_bcc" in res:
        print(f"BCC efficient: {int((tbl.theta_bcc >= 1 - EFF_TOL).sum()):,}"
              f"  median theta_bcc: {tbl.theta_bcc.median():.4f}")
    bad = {k: int((~tbl[k].isin(["optimal", SKIPPED])).sum())
           for k in tbl if k.startswith("status_")}
    print("non-optimal LPs:", bad)


if __name__ == "__main__":
    main()
