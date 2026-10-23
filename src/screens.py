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

3. Virtual-school share: enrollment in virtual schools (CCD School
   Characteristics field VIRTUAL) as a share of the district's CCD school
   membership. A statewide virtual school is a different production
   technology (Andover, KS runs one), not a reporting error. Reported at
   5 / 10 / 20 % for two definitions (fully virtual only; fully or
   primarily virtual). The school-level membership table is built once
   from the 2.5 GB Membership file and cached in data/interim/.

None of the screens changes the dataset. Output: reports/screens_report.md.
Usage (from the project root): python src/screens.py [--rebuild-membership]
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
# 3. Virtual-school share
# ---------------------------------------------------------------------------

INTERIM = Path("data/interim")
SCHOOL_MEMBERSHIP_FILE = INTERIM / "school_membership_1819.csv"
SCHOOL_FILES = {
    "membership":      "ccd_SCH_052_1819_l_1a_091019.csv",   # long, 2.5 GB
    "characteristics": "ccd_sch_129_1819_w_1a_091019.csv",   # VIRTUAL field
}
SCHOOL_TOTAL = "Education Unit Total"       # the one total row per school
# CCD 2018-19 VIRTUAL categories, labels from the School Characteristics
# companion (data/dictionaries/2018-19_School_CCD_School_Companion.xlsx):
#   FULLVIRTUAL  Full Virtual               FACEVIRTUAL  Virtual with face to
#   SUPPVIRTUAL  Supplemental Virtual                    face options
#   NOTVIRTUAL   Not Virtual                MISSING / Not reported
VIRTUAL_FULL = ["FULLVIRTUAL"]
VIRTUAL_PRIMARILY = ["FACEVIRTUAL"]
VIRTUAL_UNKNOWN = ["MISSING", "Not reported"]
VIRTUAL_DEFINITIONS = {"full": VIRTUAL_FULL,
                       "full_prim": VIRTUAL_FULL + VIRTUAL_PRIMARILY}
VIRTUAL_THRESHOLDS = (0.05, 0.10, 0.20)
# Name-based proxy, used only to cross-check the official field.
# Word boundaries keep "Preschool" from matching e-?school.
VIRTUAL_NAME_PATTERN = (r"virtual|online|cyber|\be-?cademy|\be-?school|\be-?learning"
                        r"|distance learning|digital academy|internet")


def build_school_membership(force: bool = False) -> pd.DataFrame:
    """One row per school: LEAID, NCESSCH, STUDENT_COUNT, DMS_FLAG.

    The CCD Membership file is long (school x grade x race x sex, about
    12 million rows). Only the SCHOOL_TOTAL rows are kept, read in chunks
    with the needed columns. The result is cached in data/interim/
    (gitignored) and rebuilt only with force=True.
    """
    if SCHOOL_MEMBERSHIP_FILE.exists() and not force:
        return pd.read_csv(SCHOOL_MEMBERSHIP_FILE,
                           dtype={"LEAID": str, "NCESSCH": str})
    cols = ["LEAID", "NCESSCH", "STUDENT_COUNT", "TOTAL_INDICATOR", "DMS_FLAG"]
    parts = []
    for chunk in pd.read_csv(RAW / SCHOOL_FILES["membership"], dtype=str,
                             usecols=cols, chunksize=2_000_000,
                             encoding="latin-1", low_memory=False):
        parts.append(chunk[chunk.TOTAL_INDICATOR == SCHOOL_TOTAL]
                     .drop(columns="TOTAL_INDICATOR"))
    df = pd.concat(parts, ignore_index=True)
    df["LEAID"] = to_leaid(df.LEAID)
    df["STUDENT_COUNT"] = pd.to_numeric(df.STUDENT_COUNT, errors="coerce")
    assert df.NCESSCH.is_unique, "more than one total row per school"
    INTERIM.mkdir(parents=True, exist_ok=True)
    df.to_csv(SCHOOL_MEMBERSHIP_FILE, index=False)
    return df


def load_school_virtual() -> pd.DataFrame:
    """LEAID, NCESSCH, SCH_NAME, VIRTUAL and the name proxy, every school."""
    ch = pd.read_csv(RAW / SCHOOL_FILES["characteristics"], dtype=str,
                     encoding="latin-1", low_memory=False,
                     usecols=["LEAID", "NCESSCH", "SCH_NAME", "VIRTUAL"])
    ch["LEAID"] = to_leaid(ch.LEAID)
    ch["name_proxy"] = ch.SCH_NAME.str.contains(VIRTUAL_NAME_PATTERN,
                                                case=False, regex=True)
    return ch


def school_table(schools: pd.DataFrame, membership: pd.DataFrame
                 ) -> pd.DataFrame:
    """Schools with a reported membership total, joined to VIRTUAL."""
    m = membership[membership.DMS_FLAG == "Reported"]
    m = m.merge(schools[["NCESSCH", "SCH_NAME", "VIRTUAL", "name_proxy"]],
                on="NCESSCH", how="left")
    m["VIRTUAL"] = m.VIRTUAL.fillna("Not in characteristics file")
    m["name_proxy"] = m.name_proxy.fillna(False).astype(bool)
    return m


def virtual_share_screen(df: pd.DataFrame, schools_m: pd.DataFrame
                         ) -> pd.DataFrame:
    """One row per district of df, aligned with df.index.

    members = CCD school membership (reported schools); members_<def> and
    share_<def> for each VIRTUAL_DEFINITIONS entry; members_unknown for
    schools whose status is missing; vs_flag_<def>_<pct> at each threshold
    (share >= threshold).
    """
    m = schools_m.copy()
    agg = {"members": ("STUDENT_COUNT", "sum"), "n_schools": ("NCESSCH", "size")}
    for name, cats in VIRTUAL_DEFINITIONS.items():
        m[f"members_{name}"] = m.STUDENT_COUNT.where(m.VIRTUAL.isin(cats), 0.0)
        m[f"n_{name}"] = m.VIRTUAL.isin(cats)
        agg[f"members_{name}"] = (f"members_{name}", "sum")
        agg[f"n_{name}"] = (f"n_{name}", "sum")
    m["members_unknown"] = m.STUDENT_COUNT.where(
        m.VIRTUAL.isin(VIRTUAL_UNKNOWN + ["Not in characteristics file"]), 0.0)
    agg["members_unknown"] = ("members_unknown", "sum")
    g = m.groupby("LEAID").agg(**agg)
    out = g.reindex(df.leaid.values)
    out.index = df.index
    out["checkable"] = out.members > 0
    for name in VIRTUAL_DEFINITIONS:
        out[f"share_{name}"] = out[f"members_{name}"] / out.members
        for t in VIRTUAL_THRESHOLDS:
            out[f"vs_flag_{name}_{round(100 * t)}"] = (
                out[f"share_{name}"] >= t).fillna(False)
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


def main(rebuild_membership: bool = False) -> None:
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
    L += ["## Overlap of screens 1 and 2", "", f"- flagged by both screens: {int(both.sum())}",
          f"- flagged by either: {int((tc.tc_flag | ec.ec_flag).sum())}", ""]

    # --- Virtual ----------------------------------------------------------
    membership = build_school_membership(force=rebuild_membership)
    schools = load_school_virtual()
    sm = school_table(schools, membership)
    vs = virtual_share_screen(df, sm)
    in_sample = sm[sm.LEAID.isin(df.leaid)]

    L += ["## 3. Virtual-school share (CCD School Characteristics, VIRTUAL)", "",
          f"School-level membership: {len(membership):,} schools in the Membership "
          f"file, {int((membership.DMS_FLAG == 'Reported').sum()):,} with a reported "
          f"total; cached in {SCHOOL_MEMBERSHIP_FILE}. Characteristics file: "
          f"{len(schools):,} schools.", "",
          "VIRTUAL categories, all schools with a reported total vs schools of the "
          "sample districts:", "",
          "| VIRTUAL | schools (all) | members (all) | schools (sample districts) | members (sample districts) |",
          "|---|---|---|---|---|"]
    for cat in sm.VIRTUAL.value_counts().index:
        a_, b_ = sm[sm.VIRTUAL == cat], in_sample[in_sample.VIRTUAL == cat]
        L.append(f"| {cat} | {len(a_):,} | {a_.STUDENT_COUNT.sum():,.0f} | "
                 f"{len(b_):,} | {b_.STUDENT_COUNT.sum():,.0f} |")
    recon = np.log(vs.members / df.students)
    L += ["", "Reconciliation of the denominator with F-33 fall membership (V33):",
          f"- districts with CCD school membership: {int(vs.checkable.sum()):,} of {len(df):,}",
          f"- ln(CCD members / V33): median {recon.median():+.4f}, p05 {recon.quantile(0.05):+.3f}, "
          f"p95 {recon.quantile(0.95):+.3f}; |ln ratio| > 0.1 in {int((recon.abs() > 0.1).sum())} districts",
          f"- districts with any membership in schools of unknown virtual status: "
          f"{int((vs.members_unknown > 0).sum())}", ""]

    # Andover
    v = vs[a].iloc[0]
    L += ["### Andover, KS", "",
          f"- CCD school membership {v.members:,.0f} (V33 {r.students:,.0f}); "
          f"fully virtual {v.members_full:,.0f} in {int(v.n_full)} school(s) "
          f"(share {100 * v.share_full:.1f} %); fully or primarily virtual share "
          f"{100 * v.share_full_prim:.1f} %", ""]
    andover_schools = in_sample[in_sample.LEAID == ANDOVER].sort_values("STUDENT_COUNT", ascending=False)
    L += [_md(andover_schools[["SCH_NAME", "STUDENT_COUNT", "VIRTUAL"]]), ""]

    # Distribution
    labels = {"full": "fully virtual (FULLVIRTUAL)",
              "full_prim": "fully or primarily virtual (FULLVIRTUAL + FACEVIRTUAL)"}
    bins = [0, 0.01, 0.05, 0.10, 0.20, 0.50, 1.0001]
    bin_labels = ["(0, 1 %)", "[1, 5 %)", "[5, 10 %)", "[10, 20 %)", "[20, 50 %)", "[50, 100 %]"]
    L += ["### Distribution of the virtual-enrollment share", ""]
    for name, label in labels.items():
        sh = vs[f"share_{name}"]
        pos = sh[sh > 0]
        L += [f"**{label}**", "",
              f"- districts with any: {len(pos):,} of {int(vs.checkable.sum()):,} "
              f"({100 * len(pos) / vs.checkable.sum():.1f} %); zero: {int((sh == 0).sum()):,}",
              f"- among those with any: median {100 * pos.median():.1f} %, p75 "
              f"{100 * pos.quantile(0.75):.1f} %, p90 {100 * pos.quantile(0.9):.1f} %, "
              f"max {100 * pos.max():.1f} %",
              f"- Andover: {100 * sh[a].iloc[0]:.1f} %, rank {int((pos > sh[a].iloc[0]).sum()) + 1} of {len(pos)}", "",
              "| share | districts |", "|---|---|"]
        counts = pd.cut(pos, bins=bins, labels=bin_labels, right=False).value_counts(sort=False)
        L += [f"| {k} | {int(c)} |" for k, c in counts.items()] + [""]

    # Thresholds and expected final sample
    ec_b_high = ec_b.ec_flag & (ec_b.z_enrl > 0)
    base = tc.tc_flag | ec_b_high
    L += ["### Thresholds", "",
          "A district is excluded when its share is >= the threshold. 'Final sample' "
          "applies, on the current 10,849, the temporal screen "
          f"({int(tc.tc_flag.sum())}), the enrollment screen variant B high side only "
          f"({int(ec_b_high.sum())}; union of the two {int(base.sum())}) and the virtual rule.", "",
          "| definition | threshold | excluded | CCR-efficient excluded | remaining (rule alone) | final sample (all rules) |",
          "|---|---|---|---|---|---|"]
    for name, label in labels.items():
        for t in VIRTUAL_THRESHOLDS:
            flag = vs[f"vs_flag_{name}_{round(100 * t)}"]
            eff_hit = df.loc[flag & df.leaid.isin(efficient), "district_name"].tolist()
            L.append(f"| {label} | {100 * t:.0f} % | {int(flag.sum())} | "
                     f"{', '.join(eff_hit) or 'none'} | {len(df) - int(flag.sum()):,} | "
                     f"{len(df) - int((base | flag).sum()):,} |")
    L.append("")

    # Districts at or above 5 % (wider definition)
    hit5 = vs.vs_flag_full_prim_5
    tbl = pd.concat([ids, df[["students"]],
                     vs[["members", "members_full", "members_full_prim", "share_full",
                         "share_full_prim", "n_full", "n_full_prim"]]], axis=1)[hit5]
    tbl = tbl.sort_values("share_full_prim", ascending=False)
    tbl["efficient"] = np.where(tbl.leaid.isin(efficient), "yes", "")
    tbl["share_full"] = 100 * tbl.share_full
    tbl["share_full_prim"] = 100 * tbl.share_full_prim
    L += [f"### Districts with a fully-or-primarily virtual share >= 5 % ({len(tbl)})", "",
          "Shares in percent.", "",
          _md(tbl[["leaid", "district_name", "state", "students", "members_full", "members_full_prim",
                   "share_full", "share_full_prim", "n_full", "n_full_prim", "efficient"]]), ""]

    # Name proxy cross-check
    official = in_sample.VIRTUAL.isin(VIRTUAL_FULL + VIRTUAL_PRIMARILY)
    only_proxy = in_sample[in_sample.name_proxy & ~official]
    only_official = in_sample[official & ~in_sample.name_proxy]
    L += ["### Cross-check: name-based proxy vs the official field", "",
          f"Proxy: school name matches `{VIRTUAL_NAME_PATTERN}` (case-insensitive). "
          "Schools of the sample districts only.", "",
          f"- proxy hits: {int(in_sample.name_proxy.sum()):,}; official fully/primarily virtual: "
          f"{int(official.sum()):,}; both: {int((in_sample.name_proxy & official).sum()):,}",
          f"- proxy only (name says virtual, field does not): {len(only_proxy):,}, "
          f"members {only_proxy.STUDENT_COUNT.sum():,.0f}; by VIRTUAL value: "
          + ", ".join(f"{k} = {v}" for k, v in only_proxy.VIRTUAL.value_counts().items()),
          f"- official only (field says virtual, name does not): {len(only_official):,}, "
          f"members {only_official.STUDENT_COUNT.sum():,.0f}", ""]
    for label, sub in (("Proxy only, 40 largest", only_proxy),
                       ("Official only, 40 largest", only_official)):
        sub = (sub.merge(ids, left_on="LEAID", right_on="leaid")
                  .sort_values("STUDENT_COUNT", ascending=False).head(40))
        L += [f"#### {label}", "",
              _md(sub[["LEAID", "district_name", "state", "SCH_NAME", "STUDENT_COUNT", "VIRTUAL"]]), ""]

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--rebuild-membership", action="store_true",
                   help="re-read the 2.5 GB Membership file instead of the cache")
    main(p.parse_args().rebuild_membership)
