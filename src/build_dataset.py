"""
build_dataset_districts.py
Build the main DEA sample (US public school districts) for school year 2018-19.

Sources
  CCD LEA Directory (nonfiscal)       sample selection, district info
  CCD LEA Staff (nonfiscal)           teachers and other staff (FTE)
  F-33 School District Finance        expenditures, fall membership
  SEDA 6.0 admin district scores      math and RLA achievement (GCS scale)
  SEDA 6.0 admin district covariates  context variables for the ML stage

Input  : data/raw/  (files listed in FILES)
Output : data/processed/dea_districts_2019.csv

Usage (from the project root): python src/build_dataset_districts.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

RAW = Path("data/raw")
OUT = Path("data/processed")
OUTPUT_FILE = "dea_districts_2019.csv"

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

# Raw source names -> readable names (also the appendix mapping table).
RENAME = {
    "LEAID":               "leaid",
    "LEA_NAME":            "district_name",
    "ST":                  "state",
    "LEA_TYPE":            "lea_type",
    "OPERATIONAL_SCHOOLS": "n_schools",
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
    keep = ["LEAID", "LEA_NAME", "ST", "LEA_TYPE", "OPERATIONAL_SCHOOLS"]

    df = directory
    log(len(df), "all LEAs")

    df = df[df.UPDATED_STATUS.isin(OPEN_STATUS)]
    log(len(df), "operating")

    df = df[df.LEA_TYPE.isin(REGULAR_LEA_TYPES)]
    log(len(df), "regular districts")

    df = df[(df[TESTED_GRADES] == "Yes").any(axis=1)]
    log(len(df), "offer at least one of grades 3-8")

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


def main():
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
    df = df.dropna(subset=dea_vars)
    log(len(df), "complete DEA variables")
    df = df[(df[dea_vars] > 0).all(axis=1)]
    log(len(df), "strictly positive DEA variables")

    # Covariates: left merge, they only feed the ML stage.
    cov = build_covariates(read_csv("covariates"))
    cov = cov.rename(columns={"LEAID": "leaid"})
    df = df.merge(cov, on="leaid", how="left")
    print(f"districts without covariates: {df.cov_frl_share.isna().sum():,}")

    if not validate(df):
        print("\nWARNING: validation found issues, review before running DEA")

    OUT.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT / OUTPUT_FILE, index=False)
    print(f"\nwrote {len(df):,} rows, {len(df.columns)} columns -> {OUT / OUTPUT_FILE}")


if __name__ == "__main__":
    main()