"""
screens.py
Report-only data-quality screens that need data beyond the main dataset.

1. Temporal consistency (F-33, FY2018-FY2020): a district is flagged when
   FY2019 is a one-year spike or dip, i.e. the FY2018->FY2019 and
   FY2019->FY2020 log changes have opposite signs and each is beyond
   DQ_THRESHOLD robust SDs of its own distribution. Checked for current
   expenditure per student (TCURELSC / V33) and for fall membership (V33)
   alone. A negative F-33 code in any of the three years means "cannot
   check", never a flag.

2. Enrollment consistency: ln(V33 / SEDA grade 3-8 enrollment). Districts
   that offer grades 9-12 naturally have a higher ratio, so the robust z is
   computed within two groups (offers any of grades 9-12 / K-8 only).

Neither screen changes the dataset. Output: reports/screens_report.md.
Usage (from the project root): python src/screens.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from build_dataset import (DQ_THRESHOLD, FILES, MAD_TO_SD, RAW, to_leaid)

DATA_FILE = Path("data/processed/dea_districts_2019.csv")
SCORES_FILE = Path("data/processed/dea_scores_2019.csv")
REPORT_FILE = Path("reports/screens_report.md")

F33_FILES = {2018: "sdf18_1a.txt", 2019: FILES["finance"], 2020: "sdf20_2a.txt"}
HIGH_SCHOOL_GRADES = [f"G_{g}_OFFERED" for g in range(9, 13)]
K8_NAME_PATTERN = r"\bElem(?:entary)?\b|\bESD\b"
ANDOVER = "2003360"


def robust_z(x: pd.Series) -> pd.Series:
    """(x - median) / (1.4826 * MAD), NaN where x is NaN."""
    med = x.median()
    return (x - med) / (MAD_TO_SD * (x - med).abs().median())


# ---------------------------------------------------------------------------
# 1. Temporal consistency
# ---------------------------------------------------------------------------

def load_f33(year: int) -> pd.DataFrame:
    """LEAID, TCURELSC, V33 for one fiscal year; negative codes -> NaN."""
    df = pd.read_csv(RAW / F33_FILES[year], sep="\t", dtype={"LEAID": str},
                     usecols=["LEAID", "TCURELSC", "V33"], low_memory=False)
    df["LEAID"] = to_leaid(df.LEAID)
    for c in ("TCURELSC", "V33"):
        df[c] = df[c].where(df[c] > 0)
    return df.set_index("LEAID")


def temporal_consistency_screen(df: pd.DataFrame,
                                threshold: float = DQ_THRESHOLD) -> pd.DataFrame:
    """One row per district of df, aligned with df.index.

    Columns: v33_<yr>, cur_per_stud_<yr>, the two log changes and their
    robust z for each series, `checkable`, `tc_flag`, `tc_reason`.
    """
    years = (2018, 2019, 2020)
    f33 = {y: load_f33(y) for y in years}
    out = pd.DataFrame(index=df.index)
    for y in years:
        f = f33[y].reindex(df.leaid.values)
        out[f"v33_{y}"] = f.V33.values
        out[f"cur_per_stud_{y}"] = (f.TCURELSC / f.V33).values

    reasons = pd.Series("", index=df.index, dtype=str)
    out["checkable"] = out[[f"v33_{y}" for y in years]].notna().all(axis=1)
    for series, label in (("cur_per_stud", "expenditure per student"),
                          ("v33", "fall membership")):
        d1 = np.log(out[f"{series}_2019"] / out[f"{series}_2018"])
        d2 = np.log(out[f"{series}_2020"] / out[f"{series}_2019"])
        z1, z2 = robust_z(d1), robust_z(d2)
        out[f"d1_{series}"], out[f"d2_{series}"] = d1, d2
        out[f"z1_{series}"], out[f"z2_{series}"] = z1, z2
        hit = ((np.sign(d1) == -np.sign(d2)) & (z1.abs() > threshold)
               & (z2.abs() > threshold)).fillna(False)
        kind = np.where(d1 > 0, "spike", "dip")
        tag = pd.Series([f"{label} {k} in FY2019 (z {a:+.1f} then {b:+.1f})"
                         for k, a, b in zip(kind, z1, z2)], index=df.index)
        sep = reasons.where(reasons == "", reasons + "; ")
        reasons = reasons.where(~hit, sep + tag)
    out["tc_flag"] = reasons != ""
    out["tc_reason"] = reasons
    return out


# ---------------------------------------------------------------------------
# 2. Enrollment consistency
# ---------------------------------------------------------------------------

def offers_high_school(leaids: pd.Series, names: pd.Series | None = None,
                       refine: bool = False) -> pd.Series:
    """True when the CCD directory says the LEA offers any of grades 9-12.

    With refine=True, an LEA is moved to the K-8 group when the CCD LEVEL
    field is "Elementary" or its name says Elementary. The CCD grade flags
    mark some California elementary districts (e.g. "Oak Grove Union
    Elementary") as KG-12, apparently because of a charter or community-day
    school they oversee, although nearly all their pupils are in K-8.
    """
    d = pd.read_csv(RAW / FILES["directory"], dtype=str, encoding="latin-1",
                    usecols=["LEAID", "LEVEL"] + HIGH_SCHOOL_GRADES,
                    low_memory=False)
    d["LEAID"] = to_leaid(d.LEAID)
    d = d.set_index("LEAID").reindex(leaids.values)
    hs = (d[HIGH_SCHOOL_GRADES] == "Yes").any(axis=1).fillna(False)
    if refine:
        hs &= ~(d.LEVEL == "Elementary").values
        if names is not None:
            hs &= ~names.str.contains(K8_NAME_PATTERN, regex=True).values
    return pd.Series(hs.values, index=leaids.index)


def enrollment_consistency_screen(df: pd.DataFrame, high_school: pd.Series,
                                  threshold: float = DQ_THRESHOLD
                                  ) -> pd.DataFrame:
    """ln(students / cov_enrl_g38) with a robust z within each grade group."""
    out = pd.DataFrame(index=df.index)
    out["group"] = np.where(high_school, "offers 9-12", "K-8 only")
    # A zero or missing SEDA enrollment cannot be checked (not a flag).
    out["enrl_ratio"] = df.students / df.cov_enrl_g38.where(df.cov_enrl_g38 > 0)
    out["log_ratio"] = np.log(out.enrl_ratio)
    out["z_enrl"] = out.groupby("group").log_ratio.transform(robust_z)
    out["checkable"] = out.log_ratio.notna()
    hit = (out.z_enrl.abs() > threshold).fillna(False)
    side = np.where(out.z_enrl > 0, "high", "low")
    out["ec_flag"] = hit
    out["ec_reason"] = np.where(hit, [f"V33 / grade 3-8 enrollment {s} "
                                      f"(z={z:.1f}, {g})" for s, z, g in
                                      zip(side, out.z_enrl, out.group)], "")
    return out


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def _md(frame: pd.DataFrame) -> str:
    cols = list(frame.columns)
    lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for row in frame.itertuples(index=False):
        lines.append("| " + " | ".join(
            f"{v:,.2f}" if isinstance(v, (float, np.floating)) else str(v)
            for v in row) + " |")
    return "\n".join(lines)


def main() -> None:
    df = pd.read_csv(DATA_FILE, dtype={"leaid": str})
    scores = pd.read_csv(SCORES_FILE, dtype={"leaid": str})
    efficient = set(scores.loc[scores.theta_ccr >= 1 - 1e-6, "leaid"])
    ids = df[["leaid", "district_name", "state"]]

    tc = temporal_consistency_screen(df)
    hs = offers_high_school(df.leaid)
    ec = enrollment_consistency_screen(df, hs)
    hs_b = offers_high_school(df.leaid, df.district_name, refine=True)
    ec_b = enrollment_consistency_screen(df, hs_b)

    L = ["# Report-only screens: temporal and enrollment consistency", "",
         f"Sample: {len(df):,} districts (current main dataset). Threshold: "
         f"|robust z| > {DQ_THRESHOLD:g}. Nothing here has been applied.", ""]

    # --- Andover ----------------------------------------------------------
    a = df.leaid == ANDOVER
    r, t = df[a].iloc[0], tc[a].iloc[0]
    L += ["## Andover, KS (2003360)", "",
          "| measure | value |", "|---|---|",
          f"| V33 FY2018 / FY2019 / FY2020 | {t.v33_2018:,.0f} / {t.v33_2019:,.0f} / {t.v33_2020:,.0f} |",
          f"| current expenditure per student FY2018 / FY2019 / FY2020 | {t.cur_per_stud_2018:,.0f} / {t.cur_per_stud_2019:,.0f} / {t.cur_per_stud_2020:,.0f} |",
          f"| SEDA grade 3-8 enrollment (cov_enrl_g38) | {r.cov_enrl_g38:,.0f} |",
          f"| V33 / cov_enrl_g38 | {r.students / r.cov_enrl_g38:.2f} |",
          f"| students per teacher FTE | {r.students / r.staff_teachers_fte:.1f} |",
          f"| offers grades 9-12 | {'yes' if hs[a].iloc[0] else 'no'} |",
          f"| enrollment-screen z (within group) | {ec[a].z_enrl.iloc[0]:+.2f} |",
          f"| caught by temporal screen | {'yes' if tc[a].tc_flag.iloc[0] else 'no'} |",
          f"| caught by enrollment screen | {'yes' if ec[a].ec_flag.iloc[0] else 'no'} |", ""]

    # --- Temporal ---------------------------------------------------------
    n_chk = int(tc.checkable.sum())
    L += ["## 1. Temporal consistency (F-33 FY2018-FY2020)", "",
          f"- checkable (positive values in all three years): {n_chk:,} of {len(df):,}; "
          f"cannot check: {len(df) - n_chk:,}",
          f"- flagged, expenditure per student spike/dip: {int(tc.tc_reason.str.contains('expenditure').sum())}",
          f"- flagged, fall membership spike/dip: {int(tc.tc_reason.str.contains('membership').sum())}",
          f"- flagged, union: {int(tc.tc_flag.sum())}",
          f"- CCR-efficient units caught: {sorted(set(df.leaid[tc.tc_flag]) & efficient) or 'none'}", ""]
    for series, label in (("cur_per_stud", "expenditure per student"), ("v33", "fall membership")):
        for k in ("d1", "d2"):
            d = tc[f"{k}_{series}"]
            L.append(f"- {label}, {'FY18->19' if k == 'd1' else 'FY19->20'} log change: "
                     f"median {d.median():+.4f}, robust SD {MAD_TO_SD * (d - d.median()).abs().median():.4f}, "
                     f"so |z| > 5 means a change beyond about {100 * (np.exp(5 * MAD_TO_SD * (d - d.median()).abs().median()) - 1):.0f} %")
    L.append("")
    flagged = pd.concat([ids, tc], axis=1)[tc.tc_flag]
    cols = ["leaid", "district_name", "state", "v33_2018", "v33_2019", "v33_2020",
            "cur_per_stud_2018", "cur_per_stud_2019", "cur_per_stud_2020", "tc_reason"]
    L += [f"### Flagged districts ({len(flagged)})", "", _md(flagged[cols]), ""]

    # --- Enrollment -------------------------------------------------------
    L += ["## 2. Enrollment consistency (V33 vs SEDA grade 3-8 enrollment)", ""]
    L += ["| group | n | median ratio | robust SD (log) | |z| <= 5 keeps ratios in | flagged high | flagged low |",
          "|---|---|---|---|---|---|---|"]
    for g, sub in ec.groupby("group"):
        lr = sub.log_ratio.dropna()
        med = lr.median(); sd = MAD_TO_SD * (lr - med).abs().median()
        L.append(f"| {g} | {len(sub):,} | {np.exp(med):.2f} | {sd:.3f} | "
                 f"[{np.exp(med - 5 * sd):.2f}, {np.exp(med + 5 * sd):.2f}] | "
                 f"{int((sub.z_enrl > 5).sum())} | {int((sub.z_enrl < -5).sum())} |")
    L += ["", f"- cannot check (missing cov_enrl_g38): {int((~ec.checkable).sum())}",
          f"- flagged: {int(ec.ec_flag.sum())}",
          f"- CCR-efficient units caught: {sorted(set(df.leaid[ec.ec_flag]) & efficient) or 'none'}", ""]
    fl = pd.concat([ids, df[["students", "cov_enrl_g38", "staff_teachers_fte"]], ec], axis=1)[ec.ec_flag]
    fl["stud_per_teacher"] = fl.students / fl.staff_teachers_fte
    fl = fl.sort_values("z_enrl", key=abs, ascending=False)
    cols = ["leaid", "district_name", "state", "group", "students", "cov_enrl_g38",
            "enrl_ratio", "z_enrl", "stud_per_teacher", "ec_reason"]
    L += [f"### Flagged districts ({len(fl)})", "", _md(fl[cols]), ""]

    # Variant B grouping: CCD LEVEL = Elementary or an "Elementary" name
    # counts as K-8 even when the CCD grade flags say 9-12 is offered.
    moved = int((hs & ~hs_b).sum())
    L += ["### Variant B: refined grade grouping", "",
          f"{moved} districts move from 'offers 9-12' to 'K-8 only' because "
          "the CCD LEVEL field is Elementary or the name says Elementary. "
          "Flags recomputed within the refined groups:", "",
          "| group | n | median ratio | robust SD (log) | flagged high | flagged low |",
          "|---|---|---|---|---|---|"]
    for g, sub in ec_b.groupby("group"):
        lr = sub.log_ratio.dropna()
        med = lr.median(); sd = MAD_TO_SD * (lr - med).abs().median()
        L.append(f"| {g} | {len(sub):,} | {np.exp(med):.2f} | {sd:.3f} | "
                 f"{int((sub.z_enrl > 5).sum())} | {int((sub.z_enrl < -5).sum())} |")
    L += ["", f"- flagged under B: {int(ec_b.ec_flag.sum())} "
          f"(A: {int(ec.ec_flag.sum())}); in both A and B: {int((ec.ec_flag & ec_b.ec_flag).sum())}",
          f"- CCR-efficient units caught under B: {sorted(set(df.leaid[ec_b.ec_flag]) & efficient) or 'none'}",
          f"- Andover z under B: {ec_b.loc[a, 'z_enrl'].iloc[0]:+.2f}", ""]
    flb = pd.concat([ids, df[["students", "cov_enrl_g38"]], ec_b], axis=1)[ec_b.ec_flag & (ec_b.z_enrl < 0)]
    flb = flb.sort_values("z_enrl")
    L += [f"#### Low-side flags remaining under B ({len(flb)})", "",
          _md(flb[["leaid", "district_name", "state", "group", "students", "cov_enrl_g38", "enrl_ratio", "z_enrl"]]), ""]

    both = tc.tc_flag & ec.ec_flag
    L += ["## Overlap", "", f"- flagged by both screens: {int(both.sum())}",
          f"- flagged by either: {int((tc.tc_flag | ec.ec_flag).sum())}", ""]

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
