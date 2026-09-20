"""
build_dataset.py
Build the DEA analysis sample from IPEDS 2024 raw files.

Input  : data/raw/*.csv   (5 IPEDS files)
Output : data/processed/dea_dataset_2024.csv

Usage: python src/build_dataset.py
"""

import pandas as pd
from pathlib import Path

RAW = Path("data/raw")
OUT = Path("data/processed")

# --- Sample selection criteria ---------------------------------------------
CONTROL_PUBLIC = 1                 # public institutions
ICLEVEL_4YEAR = 1                  # four-year institutions
CARNEGIE_MASTERS = [18, 19, 20]    # Master's: Larger / Medium / Small

# Award level codes, confirmed against the C2024_C dictionary.
AWLEVEL_BACHELOR = 5
AWLEVEL_MASTER = 7
AWLEVEL_DOCTOR = 9 #2, 10, 11, 12 are certificates, not degrees

# Education & General expenses (excludes auxiliary enterprises).
EG_COLS = [
    "F1C011", #instruction
    "F1C021", #research
    "F1C031", #public service
    "F1C051", #academic support
    "F1C061", #student services
    "F1C071"
]   # institutional support

PT_FACULTY_WEIGHT = 1 / 3  #IPEDS convention for part-time staff

RENAME = {
    "UNITID":   "unitid",
    "INSTNM":   "inst_name",
    "STABBR":   "state",
    "C21BASIC": "carnegie",
    "F1C011":   "exp_instruction",
    "F1C021":   "exp_research",
    "F1C031":   "exp_public_service",
    "F1C051":   "exp_academic_support",
    "F1C061":   "exp_student_services",
    "F1C071":   "exp_institutional",
    "F1C191":   "exp_total",
    "FTEUG":    "stud_ug_fte",
    "FTEGD":    "stud_grad_fte",
}


def read_ipeds(filename, drop_flags=True):
    df = pd.read_csv(RAW / filename, encoding="utf-8-sig", low_memory=False)
    if drop_flags:
        flags = [c for c in df.columns
                 if c.startswith("X") and c[1:] in df.columns]
        df = df.drop(columns=flags)
    return df


def select_sample(hd):
    keep = ["UNITID", "INSTNM", "STABBR", "C21BASIC", "LOCALE", "HBCU"]

    df = hd.copy()
    print(f"{len(df):>6}  all institutions")

    df = df[df.CONTROL == CONTROL_PUBLIC]
    print(f"{len(df):>6}  public")

    df = df[df.ICLEVEL == ICLEVEL_4YEAR]
    print(f"{len(df):>6}  four-year")

    df = df[df.C21BASIC.isin(CARNEGIE_MASTERS)]
    print(f"{len(df):>6}  Master's institutions")

    df = df[df.MEDICAL != 1]
    print(f"{len(df):>6}  no medical school")

    return df[keep].reset_index(drop=True)


def build_expenses(fin):
    cols = ["UNITID"] + EG_COLS + ["F1C191"]
    df = fin[cols].copy()
    df["exp_eg"] = df[EG_COLS].fillna(0).sum(axis=1)
    return df


def build_faculty(staff):
    df = staff[(staff.OCCUPCAT == 210) & (staff.FTPT.isin([2, 3]))]

    wide = (df.pivot_table(index="UNITID", columns="FTPT",
                           values="HRTOTLT", aggfunc="sum")
              .fillna(0)
              .rename(columns={2: "fac_ft", 3: "fac_pt"})
              .reset_index())
    wide.columns.name = None

    wide["fac_fte"] = wide.fac_ft + PT_FACULTY_WEIGHT * wide.fac_pt
    return wide


def build_students(efia):
    df = efia[["UNITID", "FTEUG", "FTEGD"]].copy()
    df["stud_fte"] = df.FTEUG.fillna(0) + df.FTEGD.fillna(0)
    return df


def build_degrees(completions):
    levels = {AWLEVEL_BACHELOR: "deg_bachelor",
              AWLEVEL_MASTER:   "deg_master",
              AWLEVEL_DOCTOR:   "deg_doctor"}

    df = completions[completions.AWLEVELC.isin(levels)]

    wide = (df.pivot_table(index="UNITID", columns="AWLEVELC",
                           values="CSTOTLT", aggfunc="sum")
              .fillna(0)
              .rename(columns=levels)
              .reset_index())
    wide.columns.name = None
    return wide


def validate(df):
    inputs  = ["exp_eg", "fac_fte", "stud_fte"]
    outputs = ["deg_bachelor", "deg_master"]
    dea_vars = inputs + outputs

    print("\n--- validation ---")

    # 1. No duplicate DMUs
    dups = df.unitid.duplicated().sum()
    print(f"duplicate unitid: {dups}")
    assert dups == 0, "duplicate institutions in the sample"

    # 2. Positivity: CCR requires strictly positive data
    bad = df[(df[dea_vars] <= 0).any(axis=1)]
    print(f"rows with non-positive DEA values: {len(bad)}")
    if len(bad):
        print(bad[["inst_name"] + dea_vars].to_string(index=False))

    # 3. Sample adequacy: n >= 3 * (m + s)
    need = 3 * len(dea_vars)
    print(f"sample size: {len(df)} (need >= {need})")
    assert len(df) >= need, "sample too small for this many variables"

    # 4. Isotonicity: inputs and outputs must move together
    corr = df[dea_vars].corr(method="spearman").loc[inputs, outputs]
    print("\nSpearman correlations (inputs x outputs):")
    print(corr.round(3).to_string())
    if (corr < 0).any().any():
        print("WARNING: negative correlation — check variable definitions")

    return len(bad) == 0


def main():
    sample = select_sample(read_ipeds("hd2024.csv"))

    parts = [
        build_expenses(read_ipeds("f2324_f1a.csv")),
        build_faculty(read_ipeds("s2024_oc.csv")),
        build_students(read_ipeds("efia2024_rv.csv")),
        build_degrees(read_ipeds("c2024_c_rv.csv")),
    ]

    df = sample
    for part in parts:
        df = df.merge(part, on="UNITID", how="inner")
        print(f"{len(df):>6}  after merge")

    df = df.rename(columns=RENAME)
    validate(df)

    OUT.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT / "dea_dataset_2024.csv", index=False)
    print(f"\nwrote {len(df)} rows, {len(df.columns)} columns")


if __name__ == "__main__":
    main()