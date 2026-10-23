"""
build_dataset.py
Build the main DEA sample (US public school districts) for school year 2018-19.

Sources
  CCD LEA Directory (nonfiscal)       sample selection, district info
  CCD LEA Staff (nonfiscal)           teachers and other staff (FTE)
  F-33 School District Finance        expenditures, fall membership
  SEDA 6.0 admin district scores      math and RLA achievement (GCS scale)
  SEDA 6.0 admin district covariates  context variables for the ML stage

Input  : data/raw/  (files listed in FILES)
Output : data/processed/dea_districts_2019.csv
         data/processed/dea_districts_2019_unscreened.csv  (before exclusions)
         data/processed/excluded_state_rule.csv
         data/processed/excluded_data_quality.csv
         data/processed/excluded_temporal.csv
         data/processed/excluded_enrollment.csv
         data/processed/excluded_virtual.csv
         reports/sample_flow.md                 (districts removed per rule)
         (all with a suffix, _dq{T}, _allstates and/or _vs{P}, when run with
         non-default options, so the main dataset is never overwritten)

Sample rules, in order: complete and strictly positive DEA variables ->
state comparability (UT, NV) -> data-quality screen -> temporal
consistency -> enrollment consistency -> virtual-school share.

Usage (from the project root):
  python src/build_dataset.py                        # main dataset
  python src/build_dataset.py --dq-threshold 4       # stricter screen
  python src/build_dataset.py --keep-states          # without the state rule
  python src/build_dataset.py --virtual-threshold 0.05   # or 0.20
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

RAW = Path("data/raw")
OUT = Path("data/processed")
OUTPUT_FILE = "dea_districts_2019.csv"
UNSCREENED_FILE = "dea_districts_2019_unscreened.csv"   # before exclusions

FILES = {
    "directory":  "ccd_LEA_029_1819_w_1a_091019.csv",
    "staff":      "ccd_LEA_059_1819_l_1a_091019.csv",
    "finance":    "sdf19_2a.txt",                       # tab-delimited
    "scores":     "seda_admindist_annualsub_gcs_6.0.csv",
    "covariates": "seda_cov_admindist_annual_6.0.csv",
}

SEDA_YEAR = 2019        # SEDA "year" is the spring of the school year: 2018-19

# --- Sample selection (CCD Directory) ---------------------------------------
# UPDATED_STATUS: 1 Open, 3 New, 4 Added, 5 Changed boundary, 8 Reopened.
# Excluded: 2 Closed, 6 Inactive, 7 Future.
OPEN_STATUS = ["1", "3", "4", "5", "8"]

# LEA_TYPE: 1 regular district, 2 regular district inside a supervisory union.
# Excluded: 3 supervisory union (admin layer over type 2, would double count),
# 4 service agency, 5 state, 6 federal, 7 independent charter, 8 other,
# 9 specialized.
REGULAR_LEA_TYPES = ["1", "2"]

# SEDA scores cover grades 3-8, so the district must offer at least one of them.
TESTED_GRADES = [f"G_{g}_OFFERED" for g in range(3, 9)]

# Grade span (GSLO, GSHI, LEVEL and an elementary-only flag) is carried into
# the dataset for the ML stage and for a planned robustness run with separate
# CCR frontiers for elementary-only and K-12 districts. It is not used in the
# main DEA. Elementary-only = offers none of grades 9-12.
HIGH_SCHOOL_GRADES = [f"G_{g}_OFFERED" for g in range(9, 13)]

# --- Staff (CCD Staff, long format) -----------------------------------------
# TOTAL_INDICATOR mixes three aggregation levels in one file:
#   "Category Set A"                     detailed categories
#   "Derived - Major Staffing Category"  sums of the above (Teachers, ...)
#   "Education Unit Total"               grand total
# Summing everything would count every person three times.
TEACHERS = ("Derived - Major Staffing Category", "Teachers")
STAFF_TOTAL = "Education Unit Total"
UNUSABLE_FLAGS = ["Missing", "Not reported", "Suppressed"]

# --- Finance (F-33) ---------------------------------------------------------
# Negative values are codes, not amounts:
#   -1 missing, -2 not applicable, -3 membership suppressed, -9 suppressed.
F33_COLS = [
    "V33",        # fall membership (students)
    "TCURELSC",   # total current expenditures, elementary/secondary
    "TCURINST",   # current expenditures, instruction
    "Z32",        # total salaries
    "TOTALEXP",   # total expenditures (incl. capital, debt), reporting only
]

# --- Achievement (SEDA 6.0) -------------------------------------------------
# GCS: 4 = national average of 4th graders, 8 = of 8th graders, so values are
# positive grade-level equivalents.
# OUTPUT_MODE "by_subject": two outputs (math, RLA), from annualsub_gcs.
# OUTPUT_MODE "pooled":     one output (math+RLA average), from annual_gcs.
OUTPUT_MODE = "by_subject"
ESTIMATOR = "eb"            # "eb" shrinks noisy small-district estimates; "ol" raw
REFERENCE_GRADE = 5.5       # re-anchor every estimate to the middle of grades 3-8

# --- Covariates (ML stage only, never enter DEA) ----------------------------
COVARIATES = {
    "totenrl":    "cov_enrl_g38",       # enrollment, grades 3-8
    "perfrl":     "cov_frl_share",      # free/reduced lunch
    "perecd":     "cov_ecd_share",      # economically disadvantaged
    "perell":     "cov_ell_share",      # English language learners
    "perspeced":  "cov_sped_share",     # special education
    "perblk":     "cov_black_share",
    "perhsp":     "cov_hisp_share",
    "perwht":     "cov_white_share",
    "sesall":     "cov_ses",            # SES composite (ACS)
    "lninc50all": "cov_ln_median_inc",
    "povertyall": "cov_poverty",
    "urban":      "cov_urban_share",
    "suburb":     "cov_suburb_share",
    "town":       "cov_town_share",
    "rural":      "cov_rural_share",
}

# --- DEA specification ------------------------------------------------------
DEA_INPUTS = ["exp_current", "staff_teachers_fte", "staff_other_fte"]
DEA_OUTPUTS = (["out_math", "out_rla"] if OUTPUT_MODE == "by_subject"
               else ["out_score"])

# --- State comparability rule -----------------------------------------------
# Utah and Nevada report "other staff" on a different basis from every other
# state: their median is about 90 students per other-staff FTE against 13.8
# nationally, with no overlap of the interquartile ranges (see
# reports/figures/dq_state_other_staff_ratio.pdf and the per-state table in
# reports/data_quality_screen.md). Their districts are not comparable on that
# input, so both states leave the sample before the data-quality screen,
# which is then calibrated on the remaining states. --keep-states turns the
# rule off for robustness checks.
EXCLUDED_STATES = ["UT", "NV"]
EXCLUDED_STATE_FILE = "excluded_state_rule.csv"

# --- Data-quality screen ----------------------------------------------------
# Implausible input ratios point to reporting errors (e.g. 1 teacher FTE for
# 1,030 students). Under CCR one such district can dominate the frontier, so
# the screen runs after validation and is logged like any other sample step.
# Rule: a district is flagged if the natural log of any ratio lies more than
# DQ_THRESHOLD robust standard deviations from the median, where
# robust SD = MAD_TO_SD * median absolute deviation of the log ratio
# (1.4826 makes the MAD consistent with the SD of a normal distribution).
DQ_RATIOS = {                       # name: (numerator, denominator)
    "students_per_teacher":     ("students", "staff_teachers_fte"),
    "students_per_other_staff": ("students", "staff_other_fte"),
    "exp_per_student":          ("exp_current", "students"),
}
DQ_THRESHOLD = 5.0                  # main dataset
DQ_THRESHOLD_ROBUSTNESS = 4.0       # stricter variant, --dq-threshold 4
MAD_TO_SD = 1.4826
EXCLUDED_FILE = "excluded_data_quality.csv"

# --- Screens beyond the main dataset (functions in src/screens.py) ----------
# Applied after the data-quality screen, in this order. Each was first run
# report-only (reports/screens_report.md) on the 10,849-district sample.
#   temporal consistency   FY2019 is a one-year spike or dip in F-33 current
#                          expenditure per student or fall membership
#                          (both adjacent log changes beyond DQ_THRESHOLD
#                          robust SDs, opposite signs).
#   enrollment consistency ln(V33 / SEDA grade 3-8 enrollment), robust z
#                          within grade-span groups (variant B: CCD LEVEL or
#                          an "Elementary" name counts as K-8). HIGH side
#                          only: a low ratio is a grade-span artefact.
#   virtual-school share   membership in CCD FULLVIRTUAL schools divided by
#                          the district's school membership
#                          >= VIRTUAL_THRESHOLD. A statewide virtual school
#                          is a different production technology (Andover,
#                          KS). FACEVIRTUAL, SUPPVIRTUAL and schools with a
#                          MISSING / Not reported status count as not virtual.
TC_EXCLUDED_FILE = "excluded_temporal.csv"
EC_EXCLUDED_FILE = "excluded_enrollment.csv"
VS_EXCLUDED_FILE = "excluded_virtual.csv"
VIRTUAL_THRESHOLD = 0.10                # main dataset
VIRTUAL_THRESHOLD_ROBUSTNESS = (0.05, 0.20)
SAMPLE_FLOW_FILE = Path("reports/sample_flow.md")

# Raw source names -> readable names (also the appendix mapping table).
RENAME = {
    "LEAID":               "leaid",
    "LEA_NAME":            "district_name",
    "ST":                  "state",
    "LEA_TYPE":            "lea_type",
    "OPERATIONAL_SCHOOLS": "n_schools",
    "GSLO":                "grade_lo",
    "GSHI":                "grade_hi",
    "LEVEL":               "lea_level",
    "ELEMENTARY_ONLY":     "elementary_only",
    "V33":                 "students",
    "TCURELSC":            "exp_current",
    "TCURINST":            "exp_instruction",
    "Z32":                 "salaries_total",
    "TOTALEXP":            "exp_total",
}


def log(n, label):
    print(f"{n:>7,}  {label}")


def to_leaid(series):
    """Normalise any ID column to the 7-character NCES LEAID string.

    SEDA stores the ID as a number, which drops the leading zero of states
    with FIPS < 10 (0100005 -> 100005). Without zfill those states would
    silently fail to merge.
    """
    return (series.astype(str)
                  .str.strip()
                  .str.replace(r"\.0$", "", regex=True)
                  .str.zfill(7))


def read_csv(name, **kwargs):
    df = pd.read_csv(RAW / FILES[name], low_memory=False, **kwargs)
    print(f"read {FILES[name]}: {len(df):,} rows")
    return df


def select_sample(directory):
    """Operating, regular districts that offer at least one tested grade."""
    keep = ["LEAID", "LEA_NAME", "ST", "LEA_TYPE", "OPERATIONAL_SCHOOLS",
            "GSLO", "GSHI", "LEVEL", "ELEMENTARY_ONLY"]

    df = directory
    log(len(df), "all LEAs")

    df = df[df.UPDATED_STATUS.isin(OPEN_STATUS)]
    log(len(df), "operating")

    df = df[df.LEA_TYPE.isin(REGULAR_LEA_TYPES)]
    log(len(df), "regular districts")

    df = df[(df[TESTED_GRADES] == "Yes").any(axis=1)]
    log(len(df), "offer at least one of grades 3-8")

    df = df.assign(ELEMENTARY_ONLY=~(df[HIGH_SCHOOL_GRADES] == "Yes").any(axis=1))
    df = df[keep].copy()
    df["LEAID"] = to_leaid(df.LEAID)
    return df.reset_index(drop=True)


def build_staff(staff):
    """Inputs 2 and 3: teachers and all other staff, in FTE."""
    df = staff.copy()
    df["LEAID"] = to_leaid(df.LEAID)
    df.loc[df.DMS_FLAG.isin(UNUSABLE_FLAGS), "STAFF_COUNT"] = np.nan

    teachers = (df[(df.TOTAL_INDICATOR == TEACHERS[0]) & (df.STAFF == TEACHERS[1])]
                  .set_index("LEAID").STAFF_COUNT.rename("staff_teachers_fte"))
    total = (df[df.TOTAL_INDICATOR == STAFF_TOTAL]
               .set_index("LEAID").STAFF_COUNT.rename("staff_total_fte"))

    out = pd.concat([teachers, total], axis=1).reset_index()
    out["staff_other_fte"] = out.staff_total_fte - out.staff_teachers_fte
    return out


def build_finance(f33):
    """Input 1 (current expenditures) and student count (for the outputs)."""
    df = f33[["LEAID"] + F33_COLS].copy()
    df["LEAID"] = to_leaid(df.LEAID)
    df[F33_COLS] = df[F33_COLS].where(df[F33_COLS] >= 0)   # codes -> NaN
    return df


def build_scores(seda):
    """Achievement per district, re-anchored to REFERENCE_GRADE."""
    df = seda[(seda.year == SEDA_YEAR) & (seda.subgroup == "all")].copy()
    assert len(df), "no SEDA rows for this year/subgroup, check the file"
    df["LEAID"] = to_leaid(df.sedaadmin)

    # Each estimate is centred on the grade in `gradecenter`: a nationally
    # average district scores exactly that grade. Converting to "grades ahead
    # of average" and back onto one common grade makes districts with
    # different tested grades comparable. If gradecenter is constant this
    # changes nothing.
    print(f"gradecenter values: {sorted(df.gradecenter.dropna().unique())}")

    if OUTPUT_MODE == "by_subject":
        cols = {"mth": "score_math", "rla": "score_rla"}
        for subj, name in cols.items():
            raw = df[f"gcs_mn_avg_{subj}_{ESTIMATOR}"]
            df[name] = raw - df.gradecenter + REFERENCE_GRADE
    else:
        cols = {"": "score"}
        df["score"] = df[f"gcs_mn_avg_{ESTIMATOR}"] - df.gradecenter + REFERENCE_GRADE

    return df[["LEAID"] + list(cols.values())]


def build_covariates(cov):
    df = cov[cov.year == SEDA_YEAR].copy()
    df["LEAID"] = to_leaid(df.sedaadmin)
    return df[["LEAID"] + list(COVARIATES)].rename(columns=COVARIATES)


def build_outputs(df):
    """Outputs = students x achievement (volume, not just a quality index).

    CCR needs quantities that scale with size. A score alone does not: a
    district twice as large does not score twice as high. Students times
    grade-level achievement does.
    """
    if OUTPUT_MODE == "by_subject":
        df["out_math"] = df.students * df.score_math
        df["out_rla"] = df.students * df.score_rla
    else:
        df["out_score"] = df.students * df.score
    return df


def validate(df):
    """Checks that must pass before running DEA. Returns True if all clean."""
    dea_vars = DEA_INPUTS + DEA_OUTPUTS

    print("\n--- validation ---")

    dups = df.leaid.duplicated().sum()
    print(f"duplicate leaid: {dups}")
    assert dups == 0, "duplicate districts in the sample"

    missing = df[dea_vars].isna().any(axis=1).sum()
    print(f"rows with missing DEA values: {missing}")
    assert missing == 0, "missing values reached validation"

    bad = df[(df[dea_vars] <= 0).any(axis=1)]
    print(f"rows with non-positive DEA values: {len(bad)}")

    need = 3 * len(dea_vars)
    print(f"sample size: {len(df):,} (need >= {need})")
    assert len(df) >= need, "sample too small for this many variables"

    corr = (df[dea_vars].corr(method="spearman")
              .loc[DEA_INPUTS, DEA_OUTPUTS])
    print("\nSpearman correlations (inputs x outputs):")
    print(corr.round(3).to_string())
    negative = (corr < 0).any().any()
    if negative:
        print("WARNING: negative correlation, check variable definitions")

    return len(bad) == 0 and not negative


def data_quality_screen(df, threshold=DQ_THRESHOLD):
    """Flag districts with implausible input ratios (see DQ_RATIOS).

    Returns a frame aligned with df: each ratio, its robust z-score
    (z_<ratio>), `dq_flag` (bool) and `dq_reason` (which rules fired).
    Median and MAD are computed on the sample passed in, so the screen is
    relative to the data, not to fixed cut-offs.
    """
    out = pd.DataFrame(index=df.index)
    reasons = pd.Series("", index=df.index, dtype=str)
    for name, (num, den) in DQ_RATIOS.items():
        ratio = df[num] / df[den]
        logr = np.log(ratio)
        med = logr.median()
        robust_sd = MAD_TO_SD * (logr - med).abs().median()
        z = (logr - med) / robust_sd
        out[name] = ratio
        out[f"z_{name}"] = z
        hit = z.abs() > threshold
        side = np.where(z > 0, "high", "low")
        tag = pd.Series([f"{name} {sd} (z={v:.1f})" for sd, v in zip(side, z)],
                        index=df.index)
        sep = reasons.where(reasons == "", reasons + "; ")
        reasons = reasons.where(~hit, sep + tag)
    out["dq_flag"] = reasons != ""
    out["dq_reason"] = reasons
    return out


def flow_step(flow, label, before, after, note=""):
    """Record one sample rule: districts removed given the previous rules."""
    flow.append({"step": label, "removed": before - after,
                 "remaining": after, "note": note})
    log(after, label)


def flow_table(flow):
    lines = ["| step | removed | remaining | note |", "|---|---|---|---|"]
    for r in flow:
        lines.append(f"| {r['step']} | {r['removed']:,} | {r['remaining']:,} | "
                     f"{r['note']} |")
    return "\n".join(lines)


def main(dq_threshold=DQ_THRESHOLD, apply_state_rule=True,
         virtual_threshold=VIRTUAL_THRESHOLD):
    # Non-default settings write to suffixed files so the main dataset is
    # never overwritten by a robustness run.
    suffix = "" if dq_threshold == DQ_THRESHOLD else f"_dq{dq_threshold:g}"
    suffix += "" if apply_state_rule else "_allstates"
    suffix += ("" if virtual_threshold == VIRTUAL_THRESHOLD
               else f"_vs{round(100 * virtual_threshold)}")
    output_file = Path(OUTPUT_FILE).stem + suffix + ".csv"
    excluded_file = Path(EXCLUDED_FILE).stem + suffix + ".csv"
    excluded_state_file = Path(EXCLUDED_STATE_FILE).stem + suffix + ".csv"
    tc_excluded_file = Path(TC_EXCLUDED_FILE).stem + suffix + ".csv"
    ec_excluded_file = Path(EC_EXCLUDED_FILE).stem + suffix + ".csv"
    vs_excluded_file = Path(VS_EXCLUDED_FILE).stem + suffix + ".csv"
    flow_file = SAMPLE_FLOW_FILE.with_name(SAMPLE_FLOW_FILE.stem + suffix + ".md")
    flow = []

    sample = select_sample(read_csv("directory", dtype=str, encoding="latin-1"))

    parts = {
        "staff":   build_staff(read_csv(
                       "staff", dtype={"LEAID": str}, encoding="latin-1",
                       usecols=["LEAID", "STAFF", "STAFF_COUNT",
                                "TOTAL_INDICATOR", "DMS_FLAG"])),
        "finance": build_finance(read_csv(
                       "finance", sep="\t", dtype={"LEAID": str})),
        "scores":  build_scores(read_csv("scores")),
    }

    print()
    df = sample
    for name, part in parts.items():
        df = df.merge(part, on="LEAID", how="inner")
        log(len(df), f"after merge with {name}")

    df = df.rename(columns=RENAME)
    df = build_outputs(df)

    # Explicit, logged sample restrictions: DEA cannot handle missing or
    # non-positive data, so these districts leave the sample here.
    dea_vars = DEA_INPUTS + DEA_OUTPUTS
    flow.append({"step": "merged (directory, staff, finance, scores)",
                 "removed": 0, "remaining": len(df), "note": ""})
    n = len(df)
    df = df.dropna(subset=dea_vars)
    flow_step(flow, "complete DEA variables", n, len(df))
    n = len(df)
    df = df[(df[dea_vars] > 0).all(axis=1)]
    flow_step(flow, "strictly positive DEA variables", n, len(df))

    # Covariates: left merge, they only feed the ML stage.
    cov = build_covariates(read_csv("covariates"))
    cov = cov.rename(columns={"LEAID": "leaid"})
    df = df.merge(cov, on="leaid", how="left")
    print(f"districts without covariates: {df.cov_frl_share.isna().sum():,}")

    if not validate(df):
        print("\nWARNING: validation found issues, review before running DEA")

    OUT.mkdir(parents=True, exist_ok=True)

    # The validated sample before any exclusion, kept for the data-quality
    # figures (src/figures.py) and for robustness runs.
    df.to_csv(OUT / UNSCREENED_FILE, index=False)
    print(f"\nwrote {len(df):,} rows (before exclusions) -> {OUT / UNSCREENED_FILE}")

    # State comparability rule (see EXCLUDED_STATES). Applied before the
    # data-quality screen so that the screen's median and MAD are computed
    # on comparable states only.
    if apply_state_rule:
        print(f"\n--- state comparability rule ({', '.join(EXCLUDED_STATES)}) ---")
        drop = df.state.isin(EXCLUDED_STATES)
        excluded = df.loc[drop, ["leaid", "district_name", "state"]].copy()
        excluded["students_per_other_staff"] = (
            df.loc[drop, "students"] / df.loc[drop, "staff_other_fte"])
        excluded["reason"] = ("state reports other staff on a different basis "
                              "(EXCLUDED_STATES)")
        excluded.to_csv(OUT / excluded_state_file, index=False)
        print(f"{int(drop.sum()):>7,}  excluded -> {OUT / excluded_state_file}")
        n = len(df)
        df = df[~drop]
        flow_step(flow, f"state comparability rule ({', '.join(EXCLUDED_STATES)})",
                  n, len(df), "other staff reported on a different basis")

    # Data-quality screen: exclude districts with implausible input ratios
    # and keep them, with the reason, in a separate file.
    print(f"\n--- data-quality screen (threshold {dq_threshold:g}) ---")
    dq = data_quality_screen(df, dq_threshold)
    for name in DQ_RATIOS:
        n_hit = int((dq[f"z_{name}"].abs() > dq_threshold).sum())
        print(f"{n_hit:>7,}  flagged by {name}")
    excluded = pd.concat([df[["leaid", "district_name", "state"]], dq], axis=1)
    excluded[dq.dq_flag].to_csv(OUT / excluded_file, index=False)
    print(f"{int(dq.dq_flag.sum()):>7,}  excluded -> {OUT / excluded_file}")
    n = len(df)
    df = df[~dq.dq_flag].reset_index(drop=True)
    flow_step(flow, f"data-quality screen (|robust z| <= {dq_threshold:g})",
              n, len(df), "implausible input ratios")

    # --- Screens beyond the main dataset (see the block of constants) -------
    # screens.py imports constants from this module, so import it here.
    from screens import (build_school_membership, enrollment_consistency_screen,
                         load_school_virtual, offers_high_school, school_table,
                         temporal_consistency_screen, virtual_share_screen)
    ids = ["leaid", "district_name", "state"]
    post_dq = df            # reference sample for the overlap statistics

    # Standalone flags on the post-data-quality sample. The temporal and
    # virtual flags do not depend on the sample they are evaluated in (the
    # virtual share is a school-level quantity; the temporal robust z is
    # computed here on exactly this sample). The enrollment robust z does
    # depend on the sample, so it is recomputed on its actual input below
    # and the standalone count is reported next to it.
    tc = temporal_consistency_screen(post_dq, dq_threshold)
    hs_b = offers_high_school(post_dq.leaid, post_dq.district_name, refine=True)
    ec_all = enrollment_consistency_screen(post_dq, hs_b, dq_threshold)
    ec_all_hit = ec_all.ec_flag & (ec_all.z_enrl > 0)
    vs_all = virtual_share_screen(
        post_dq, school_table(load_school_virtual(), build_school_membership()))
    vs_all_hit = (vs_all.share_full >= virtual_threshold).fillna(False)

    # Temporal consistency.
    print(f"\n--- temporal consistency screen (|z| > {dq_threshold:g}, F-33 FY2018-FY2020) ---")
    print(f"{int((~tc.checkable).sum()):>7,}  cannot be checked (a negative F-33 code in one year)")
    cols = [c for c in tc.columns if c.startswith(("v33_", "cur_per_stud_"))]
    excluded = pd.concat([df[ids], tc[cols]], axis=1)[tc.tc_flag].copy()
    excluded["reason"] = tc.tc_reason[tc.tc_flag]
    excluded.to_csv(OUT / tc_excluded_file, index=False)
    print(f"{int(tc.tc_flag.sum()):>7,}  excluded -> {OUT / tc_excluded_file}")
    n = len(df)
    df = df[~tc.tc_flag]
    flow_step(flow, "temporal consistency screen", n, len(df),
              "FY2019 one-year spike or dip in F-33")

    # Enrollment consistency, variant B grouping, high side only.
    print(f"\n--- enrollment consistency screen (variant B, high side, |z| > {dq_threshold:g}) ---")
    hs = offers_high_school(df.leaid, df.district_name, refine=True)
    ec = enrollment_consistency_screen(df, hs, dq_threshold)
    hit = ec.ec_flag & (ec.z_enrl > 0)
    print(f"{int((~ec.checkable).sum()):>7,}  cannot be checked (no SEDA grade 3-8 enrollment)")
    print(f"{int((ec.ec_flag & (ec.z_enrl < 0)).sum()):>7,}  low-side flags, kept (grade-span artefact)")
    excluded = pd.concat([df[ids], df[["students", "cov_enrl_g38"]],
                          ec[["group", "enrl_ratio", "z_enrl"]]], axis=1)[hit].copy()
    excluded["reason"] = ec.ec_reason[hit]
    excluded.to_csv(OUT / ec_excluded_file, index=False)
    print(f"{int(hit.sum()):>7,}  excluded -> {OUT / ec_excluded_file}")
    # The robust z is recomputed on the current sample (as the data-quality
    # screen is computed after the state rule), so a borderline district can
    # cross the threshold once the temporal screen has removed its 33.
    standalone = set(post_dq.leaid[ec_all_hit])
    already = standalone & set(post_dq.leaid[tc.tc_flag])
    dropped = standalone - already - set(df.leaid[hit])
    added = set(df.leaid[hit]) - standalone
    who = ", ".join(sorted(post_dq.district_name[post_dq.leaid.isin(dropped | added)]))
    n = len(df)
    df = df[~hit]
    flow_step(flow, "enrollment consistency screen (variant B, high side)", n, len(df),
              f"V33 high vs SEDA grade 3-8 enrollment; standalone on the post-DQ "
              f"sample {len(standalone)}: {len(already)} already removed by earlier "
              f"rules, {len(dropped)} below the threshold once median and MAD are "
              f"recomputed after the temporal screen, {len(added)} newly above it"
              + (f" ({who})" if who else ""))

    # Virtual-school share.
    print(f"\n--- virtual-school share (FULLVIRTUAL >= {100 * virtual_threshold:g} % of membership) ---")
    vs = vs_all.loc[df.index]
    hit = (vs.share_full >= virtual_threshold).fillna(False)
    print(f"{int((~vs.checkable).sum()):>7,}  cannot be checked (no CCD school membership)")
    print(f"{int((vs.members_unknown > 0).sum()):>7,}  districts with a school of unknown virtual "
          f"status (counted as not virtual)")
    excluded = pd.concat([df[ids], df[["students"]],
                          vs[["members", "members_full", "n_full", "share_full"]]],
                         axis=1)[hit].copy()
    excluded["reason"] = [f"membership in fully virtual schools {100 * x:.1f} % "
                          f">= {100 * virtual_threshold:g} % (FULLVIRTUAL)"
                          for x in vs.share_full[hit]]
    excluded.to_csv(OUT / vs_excluded_file, index=False)
    print(f"{int(hit.sum()):>7,}  excluded -> {OUT / vs_excluded_file}")
    already = int(vs_all_hit.sum() - hit.sum())
    n = len(df)
    df = df[~hit]
    flow_step(flow, f"virtual-school share (FULLVIRTUAL >= {100 * virtual_threshold:g} %)",
              n, len(df), f"standalone on the post-DQ sample {int(vs_all_hit.sum())}, "
                          f"of which {already} already removed")

    # Sample flow: districts removed at each rule given the previous rules.
    print("\n--- sample flow ---")
    print(flow_table(flow))
    flow_file.parent.mkdir(parents=True, exist_ok=True)
    flow_file.write_text(
        "# Sample flow, school districts 2018-19\n\n"
        f"Settings: data-quality threshold {dq_threshold:g}, state rule "
        f"{'on' if apply_state_rule else 'off'}, virtual threshold "
        f"{100 * virtual_threshold:g} %. Each row removes districts given the "
        "rules above it; 'standalone' counts are flags evaluated on the sample "
        "after the data-quality screen, so the difference is the overlap with "
        "earlier rules.\n\nThe screens based on a robust z (data-quality, "
        "temporal, enrollment) compute their median and MAD on the sample they "
        "receive, so each is calibrated on the districts that survive the "
        "earlier rules (sequential recomputation). The virtual share is a "
        "school-level quantity and does not depend on the sample.\n\n"
        + flow_table(flow) + "\n", encoding="utf-8")
    print(f"wrote {flow_file}")

    df.to_csv(OUT / output_file, index=False)
    print(f"\nwrote {len(df):,} rows, {len(df.columns)} columns -> {OUT / output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build the DEA district dataset.")
    parser.add_argument("--dq-threshold", type=float, default=DQ_THRESHOLD,
                        help=f"robust-z cut-off of the data-quality screen "
                             f"(default {DQ_THRESHOLD:g}; robustness variant "
                             f"{DQ_THRESHOLD_ROBUSTNESS:g})")
    parser.add_argument("--keep-states", action="store_true",
                        help="do not apply the state comparability rule "
                             f"(keep {', '.join(EXCLUDED_STATES)})")
    parser.add_argument("--virtual-threshold", type=float, default=VIRTUAL_THRESHOLD,
                        help="share of membership in fully virtual schools at "
                             f"which a district is excluded (default "
                             f"{VIRTUAL_THRESHOLD:g}; robustness variants "
                             f"{', '.join(f'{t:g}' for t in VIRTUAL_THRESHOLD_ROBUSTNESS)})")
    args = parser.parse_args()
    main(args.dq_threshold, apply_state_rule=not args.keep_states,
         virtual_threshold=args.virtual_threshold)