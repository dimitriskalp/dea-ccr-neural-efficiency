"""
diagnostics.py
Report-only diagnostics of the final sample. Nothing here changes the data.

1. Concentration of the exclusions: districts removed per state (count and
   share of the state's districts after the state rule, states losing more
   than STATE_LOSS_FLAG are marked), and excluded vs retained districts on
   enrollment and locale (SEDA covariates; the CCD LEA directory has no
   locale field).
2. CCR-efficient units: one row per efficient district with its inputs,
   ratios, the robust z of every screen, the FULLVIRTUAL share,
   super-efficiency and peer count, plus context (grade span, SEDA
   precision, SEDA scores over time for the focus districts) and notes.

Input  : data/processed/dea_districts_2019{,_unscreened}.csv, excluded_*.csv,
         data/processed/dea_scores_2019.csv, raw CCD / SEDA / F-33 files
Output : reports/sample_diagnostics.md, reports/efficient_units.md
Usage (from the project root): python src/diagnostics.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from build_dataset import (DQ_RATIOS, DQ_THRESHOLD, EXCLUDED_STATES, FILES,
                           MAD_TO_SD, OUT, OUTPUT_FILE, RAW, UNSCREENED_FILE,
                           data_quality_screen, to_leaid)
from dea import EFF_TOL, SCORES_FILE
from screens import (build_school_membership, enrollment_consistency_screen,
                     load_school_virtual, offers_high_school, school_table,
                     temporal_consistency_screen, virtual_share_screen)

CONCENTRATION_FILE = Path("reports/sample_diagnostics.md")
EFFICIENT_FILE = Path("reports/efficient_units.md")

RULE_FILES = {                      # order of application in the build
    "data-quality screen": "excluded_data_quality.csv",
    "temporal consistency": "excluded_temporal.csv",
    "enrollment consistency": "excluded_enrollment.csv",
    "virtual-school share": "excluded_virtual.csv",
}
LOCALES = {"cov_urban_share": "urban", "cov_suburb_share": "suburb",
           "cov_town_share": "town", "cov_rural_share": "rural"}
STATE_LOSS_FLAG = 0.05
DQ_FOCUS_STATE = "IN"               # most data-quality exclusions of any state
FOCUS = {"4004470": "Bishop, OK", "1603420": "West Side Joint District, ID"}
SEDA_YEARS = (2016, 2017, 2018, 2019)

NOTES = """\
### Notes on Bishop, OK and West Side Joint District, ID

Both districts entered the efficient set when Andover left; before that
they were on the list of extreme output-per-dollar ratios with theta 0.92
and 0.91. Nothing in the data points to a reporting error:

- **Bishop, OK** is a one-school PK-6 dependent elementary district of 584
  pupils, 70 % free or reduced-price lunch, spending 7,118 USD per pupil
  (national median 12,003) with 20.6 pupils per teacher FTE and 37.3 per
  other-staff FTE. Its per-pupil spending is stable over FY2018-FY2020 and
  its F-33 record shows no payments to private or charter schools, no
  tuition payments to other systems of note, and no virtual or shared-time
  school in the CCD. SEDA puts its pupils 1.8 (math) and 1.0 (RLA) grade
  levels above the national average; the empirical-Bayes and raw
  estimates agree within one standard error (0.17-0.25) and the earlier
  years are of the same order (math 7.3-8.2 since 2009, with 2019 among the
  lower values), so the 2019 score is not a one-year spike. Its
  enrollment-ratio z of +4.6 is the highest of the 18 but is a grade-span
  effect, not a membership error: only grades 3-6 of its PK-6 span are
  tested, so fall membership (584) is 2.2 times the SEDA grade 3-8 count
  (265), against a median of about 1.5 in the K-8 group.
  What makes it efficient is the combination of a cheap grade span (no
  middle or high school), low other-staff and high scores for its poverty
  level; the same grade-span pattern holds for 10 of the 18 efficient
  units, which are K-8 or PK-6 elementary districts.
- **West Side Joint District, ID** is a three-school PK-12 district of 794
  pupils (one elementary, one middle, one high school, none virtual), 46 %
  free or reduced-price lunch, spending 6,545 USD per pupil, the lowest of
  the 18. Idaho has the lowest per-pupil spending of any state, so this is
  a state-level pattern rather than a district anomaly. Staffing ratios
  (18.8 pupils per teacher, 22.1 per other staff) are within 1.5 robust SD
  of the national medians, spending is stable over the three years, and
  the SEDA estimates (2.0 and 1.3 grade levels above average) agree
  between the empirical-Bayes and raw versions and across years.

Both are small, rural and high-performing for their resources. That is a
different point on the same technology, not evidence of a different
technology or of an error, so under the evidence-based rule neither is a
candidate for exclusion. The systematic feature worth discussing in the
thesis is grade span: elementary-only districts face lower unit costs than
K-12 districts, and the CCR frontier is largely spanned by them.
"""


def _md(frame: pd.DataFrame, fmt: dict | None = None) -> str:
    fmt = fmt or {}
    cols = list(frame.columns)
    lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for row in frame.itertuples(index=False):
        cells = []
        for c, v in zip(cols, row):
            if c in fmt:
                cells.append(fmt[c].format(v) if pd.notna(v) else "")
            elif isinstance(v, (float, np.floating)):
                cells.append("" if not np.isfinite(v) else f"{v:,.2f}")
            elif isinstance(v, (int, np.integer)):
                cells.append(f"{v:,}")
            else:
                cells.append(str(v))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def load_inputs():
    unscreened = pd.read_csv(OUT / UNSCREENED_FILE, dtype={"leaid": str})
    final = pd.read_csv(OUT / OUTPUT_FILE, dtype={"leaid": str})
    scores = pd.read_csv(SCORES_FILE, dtype={"leaid": str})
    return unscreened, final, scores


def exclusion_rule(base: pd.DataFrame, final: pd.DataFrame) -> pd.Series:
    """'retained' or the name of the rule that removed each district of base."""
    rule = pd.Series("retained", index=base.leaid.values)
    for name, f in RULE_FILES.items():
        ex = pd.read_csv(OUT / f, dtype={"leaid": str})
        rule[rule.index.isin(ex.leaid)] = name
    unexplained = (rule == "retained") & ~rule.index.isin(final.leaid)
    assert not unexplained.any(), "district missing from the final sample without a rule"
    return pd.Series(rule.values, index=base.index)


# ---------------------------------------------------------------------------
# 1. Concentration of the exclusions
# ---------------------------------------------------------------------------

def concentration_report(unscreened: pd.DataFrame, final: pd.DataFrame) -> list[str]:
    base = unscreened[~unscreened.state.isin(EXCLUDED_STATES)].reset_index(drop=True)
    base["rule"] = exclusion_rule(base, final)
    base["excluded"] = base.rule != "retained"

    L = ["# Sample diagnostics: where the exclusions fall", "",
         f"Base: {len(base):,} districts after the state rule "
         f"({', '.join(EXCLUDED_STATES)} removed); {int(base.excluded.sum()):,} "
         f"excluded by the four later rules, {len(final):,} retained. Report only.", ""]

    # Per state.
    st = (base.groupby("state")
              .agg(districts=("leaid", "size"), removed=("excluded", "sum"))
              .astype(int))
    st["share"] = st.removed / st.districts
    by_rule = pd.crosstab(base.state, base.rule).reindex(columns=list(RULE_FILES), fill_value=0)
    st = st.join(by_rule).sort_values("share", ascending=False).reset_index()
    st["flag"] = np.where(st.share > STATE_LOSS_FLAG, f"> {100 * STATE_LOSS_FLAG:.0f} %", "")
    flagged = st[st.flag != ""]
    L += ["## Districts removed per state", "",
          f"Share = removed / districts after the state rule. States losing more than "
          f"{100 * STATE_LOSS_FLAG:.0f} % are flagged: "
          + (", ".join(f"{r.state} ({r.removed} of {r.districts}, {100 * r.share:.1f} %)"
                       for r in flagged.itertuples()) or "none") + ".", "",
          _md(st.rename(columns={"share": "share removed"}),
              {"share removed": "{:.1%}"}), ""]

    # Enrollment, excluded vs retained and by rule.
    def q(s):
        return pd.Series({"n": len(s), "median": s.median(), "q25": s.quantile(0.25),
                          "q75": s.quantile(0.75), "min": s.min(), "max": s.max()})
    groups = [("retained", base[~base.excluded]), ("excluded (all rules)", base[base.excluded])]
    groups += [(name, base[base.rule == name]) for name in RULE_FILES]
    enr = pd.DataFrame({g: q(sub.students) for g, sub in groups}).T.reset_index()
    enr = enr.rename(columns={"index": "group"})
    enr["n"] = enr.n.astype(int)
    L += ["## Enrollment (fall membership) of excluded vs retained districts", "",
          _md(enr, {"median": "{:,.0f}", "q25": "{:,.0f}", "q75": "{:,.0f}",
                    "min": "{:,.0f}", "max": "{:,.0f}"}), ""]

    # Locale from the SEDA covariates (share of pupils by locale).
    has = base[list(LOCALES)].notna().all(axis=1)
    loc = base[has].copy()
    loc["dominant"] = loc[list(LOCALES)].idxmax(axis=1).map(LOCALES)
    rows = []
    for g, sub in groups:
        sub = loc[loc.index.isin(sub.index)]
        row = {"group": g, "n with locale": len(sub)}
        for name in LOCALES.values():
            row[f"{name} (dominant)"] = (sub.dominant == name).mean() if len(sub) else np.nan
        for col, name in LOCALES.items():
            row[f"mean {name} share"] = sub[col].mean() if len(sub) else np.nan
        rows.append(row)
    locale = pd.DataFrame(rows)
    pct = {c: "{:.1%}" for c in locale.columns if c not in ("group", "n with locale")}
    L += ["## Locale of excluded vs retained districts", "",
          "Locale comes from the SEDA covariates (share of pupils in urban, suburban, "
          "town and rural schools); the CCD LEA directory for 2018-19 has no locale "
          "field. 'Dominant' is the locale with the largest share. "
          f"{int((~has).sum())} districts of the base have no locale covariates.", "",
          _md(locale, pct), ""]
    return L


def state_dq_section(unscreened: pd.DataFrame, state: str = DQ_FOCUS_STATE) -> list[str]:
    """Is one state's run of data-quality exclusions a state-level pattern
    (as for UT/NV) or a tail of individual districts?"""
    base = unscreened[~unscreened.state.isin(EXCLUDED_STATES)].reset_index(drop=True)
    dq = data_quality_screen(base, DQ_THRESHOLD)
    in_state = base.state == state
    hit = dq.dq_flag & in_state
    sides = {name: (int((dq.loc[hit, f"z_{name}"] > DQ_THRESHOLD).sum()),
                    int((dq.loc[hit, f"z_{name}"] < -DQ_THRESHOLD).sum()))
             for name in DQ_RATIOS}

    rows = []
    for name, (num, den) in DQ_RATIOS.items():
        lr = np.log(base[num] / base[den])
        med, sd = lr.median(), MAD_TO_SD * (lr - lr.median()).abs().median()
        st_med = lr.groupby(base.state).median().sort_values(ascending=False)
        s = lr[in_state]
        rows.append({"ratio": name, "national median": np.exp(med),
                     f"{state} median": np.exp(s.median()),
                     "z of state median": (s.median() - med) / sd,
                     "rank of state median": f"{int(np.flatnonzero(st_med.index == state)[0]) + 1} of {len(st_med)}",
                     f"{state} IQR (log)": s.quantile(0.75) - s.quantile(0.25),
                     "national IQR (log)": lr.quantile(0.75) - lr.quantile(0.25),
                     "flagged high / low": f"{sides[name][0]} / {sides[name][1]}"})
    tbl = pd.DataFrame(rows)

    # The firing ratio: tail within the state and the reported FTE values.
    firing = max(sides, key=lambda k: sum(sides[k]))
    z = dq.loc[in_state, f"z_{firing}"]
    den = DQ_RATIOS[firing][1]
    fte_hit = base.loc[hit, den]
    fte_rest = base.loc[in_state & ~dq.dq_flag, den]
    integer_hit = float((fte_hit == fte_hit.round()).mean()) if len(fte_hit) else np.nan
    integer_rest = float((fte_rest == fte_rest.round()).mean()) if len(fte_rest) else np.nan
    zr = z.describe()
    L = [f"## Data-quality exclusions in {state}", "",
         f"{int(hit.sum())} of the {int(in_state.sum())} {state} districts after the "
         f"state rule are removed by the data-quality screen, all by "
         f"`{firing}` and all on the "
         f"{'high' if sides[firing][0] >= sides[firing][1] else 'low'} side "
         f"(robust z {dq.loc[hit, f'z_{firing}'].min():.1f} to "
         f"{dq.loc[hit, f'z_{firing}'].max():.1f}); their other two ratios are "
         "unremarkable.", "",
         _md(tbl, {"national median": "{:,.2f}", f"{state} median": "{:,.2f}",
                   "z of state median": "{:+.2f}", f"{state} IQR (log)": "{:.3f}",
                   "national IQR (log)": "{:.3f}"}), "",
         f"The state median of `{firing}` is close to the national median "
         f"(z {tbl.loc[tbl.ratio == firing, 'z of state median'].iloc[0]:+.2f}) and "
         f"the within-state spread matches the national one, so unlike Utah and "
         f"Nevada, {state} does not report the input on a different basis. What "
         f"it has is a one-sided tail: within {state} the robust z of this ratio "
         f"exceeds 3 for {int((z > 3).sum())} districts, 4 for {int((z > 4).sum())} "
         f"and 5 for {int((z > 5).sum())}, with none below -3 (state median z "
         f"{zr['50%']:+.2f}, maximum {zr['max']:+.2f}). The flagged districts report "
         f"{fte_hit.min():.0f} to {fte_hit.max():.0f} other-staff FTE against "
         f"{base.loc[hit, 'staff_teachers_fte'].min():.0f} to "
         f"{base.loc[hit, 'staff_teachers_fte'].max():.0f} teacher FTE, and "
         f"{integer_hit:.0%} of them report a whole number of other-staff FTE "
         f"against {integer_rest:.0%} of the other {state} districts, which points "
         "to partial reporting of the non-teaching categories by those districts "
         "rather than to a state convention. The screen is doing what it should: "
         "removing individual districts with an implausible input, not a state.", ""]
    return L


# ---------------------------------------------------------------------------
# 2. CCR-efficient units
# ---------------------------------------------------------------------------

def load_seda_detail(leaids: set, years=SEDA_YEARS) -> pd.DataFrame:
    """SEDA EB and OL estimates, SEs and test counts for some districts."""
    use = ["sedaadmin", "year", "subgroup", "gradecenter",
           "gcs_mn_avg_mth_eb", "gcs_mn_avg_rla_eb", "gcs_mn_avg_mth_ol",
           "gcs_mn_avg_rla_ol", "gcs_mn_avg_mth_eb_se", "gcs_mn_avg_rla_eb_se",
           "tot_asmts_mth", "tot_asmts_rla"]
    parts = []
    for ch in pd.read_csv(RAW / FILES["scores"], usecols=use, chunksize=500_000,
                          low_memory=False):
        ch = ch[(ch.subgroup == "all") & ch.year.isin(years)]
        ch = ch.assign(leaid=to_leaid(ch.sedaadmin))
        parts.append(ch[ch.leaid.isin(leaids)])
    return pd.concat(parts).drop(columns=["sedaadmin", "subgroup"])


def efficient_units_report(unscreened: pd.DataFrame, final: pd.DataFrame,
                           scores: pd.DataFrame) -> list[str]:
    eff = scores[scores.theta_ccr >= 1 - EFF_TOL]
    ids = set(eff.leaid)

    # Re-create each screen on the sample it saw in the build.
    base = unscreened[~unscreened.state.isin(EXCLUDED_STATES)].reset_index(drop=True)
    dq = data_quality_screen(base, DQ_THRESHOLD)
    post_dq = base[~dq.dq_flag].reset_index(drop=True)
    tc = temporal_consistency_screen(post_dq, DQ_THRESHOLD)
    post_tc = post_dq[~tc.tc_flag].reset_index(drop=True)
    ec = enrollment_consistency_screen(
        post_tc, offers_high_school(post_tc.leaid, post_tc.district_name, refine=True),
        DQ_THRESHOLD)
    vs = virtual_share_screen(
        final, school_table(load_school_virtual(), build_school_membership()))

    d = (final[final.leaid.isin(ids)]
         .merge(eff[["leaid", "super_eff", "peer_count", "theta_bcc"]], on="leaid")
         .set_index("leaid"))
    z = dq.set_index(base.leaid)[[f"z_{k}" for k in DQ_RATIOS]].reindex(d.index)
    t = tc.set_index(post_dq.leaid)[[f"cur_per_stud_{y}" for y in (2018, 2019, 2020)]].reindex(d.index)
    e = ec.set_index(post_tc.leaid)[["z_enrl", "group"]].reindex(d.index)
    v = vs.set_index(final.leaid)[["share_full"]].reindex(d.index)

    tbl = pd.DataFrame({
        "district": d.district_name, "state": d.state, "pupils": d.students.astype(int),
        "teachers FTE": d.staff_teachers_fte, "other FTE": d.staff_other_fte,
        "USD per pupil": d.exp_current / d.students,
        "pupils per teacher": d.students / d.staff_teachers_fte,
        "z pupils/teacher": z["z_students_per_teacher"],
        "z pupils/other": z["z_students_per_other_staff"],
        "z USD/pupil": z["z_exp_per_student"],
        "USD/pupil FY18": t.cur_per_stud_2018, "FY19": t.cur_per_stud_2019,
        "FY20": t.cur_per_stud_2020,
        "z enrollment ratio": e.z_enrl, "FULLVIRTUAL share": v.share_full,
        "super-eff": d.super_eff, "peer count": d.peer_count.astype(int),
    }).sort_values("peer count", ascending=False)
    fmt = {"teachers FTE": "{:,.1f}", "other FTE": "{:,.1f}", "USD per pupil": "{:,.0f}",
           "pupils per teacher": "{:.1f}", "z pupils/teacher": "{:+.2f}",
           "z pupils/other": "{:+.2f}", "z USD/pupil": "{:+.2f}",
           "USD/pupil FY18": "{:,.0f}", "FY19": "{:,.0f}", "FY20": "{:,.0f}",
           "z enrollment ratio": "{:+.2f}", "FULLVIRTUAL share": "{:.1%}",
           "super-eff": "{:.4f}"}

    L = ["# CCR-efficient units: diagnostics", "",
         f"The {len(tbl)} CCR-efficient districts of the current run "
         f"(n = {len(final):,}), sorted by the number of other districts that use "
         "them as a peer. Robust z scores are those of the build: the data-quality "
         "z on the sample after the state rule, the enrollment-ratio z (variant B "
         "grouping) on the sample after the temporal screen. Report only; no "
         "district is excluded for being efficient or a frequent peer.", "",
         "## Inputs, ratios and screen statistics", "", _md(tbl.reset_index(drop=True), fmt), ""]

    # Context: grade span, schools, poverty, locale, SEDA precision.
    lea = pd.read_csv(RAW / FILES["directory"], dtype=str, encoding="latin-1",
                      usecols=["LEAID", "GSLO", "GSHI", "LEVEL"], low_memory=False)
    lea["LEAID"] = to_leaid(lea.LEAID)
    lea = lea.set_index("LEAID").reindex(d.index)
    seda = load_seda_detail(ids)
    s19 = seda[seda.year == 2019].set_index("leaid").reindex(d.index)
    ctx = pd.DataFrame({
        "district": d.district_name, "state": d.state,
        "grades": lea.GSLO + "-" + lea.GSHI, "CCD level": lea.LEVEL,
        "schools": d.n_schools.astype(int), "FRL share": d.cov_frl_share,
        "rural share": d.cov_rural_share, "grade 3-8 pupils": d.cov_enrl_g38,
        "math EB": s19.gcs_mn_avg_mth_eb, "math OL": s19.gcs_mn_avg_mth_ol,
        "math SE": s19.gcs_mn_avg_mth_eb_se, "RLA EB": s19.gcs_mn_avg_rla_eb,
        "RLA OL": s19.gcs_mn_avg_rla_ol, "RLA SE": s19.gcs_mn_avg_rla_eb_se,
        "tests math": s19.tot_asmts_mth, "peer count": d.peer_count.astype(int),
    }).sort_values("peer count", ascending=False)
    cfmt = {"FRL share": "{:.0%}", "rural share": "{:.0%}", "grade 3-8 pupils": "{:,.0f}",
            "math EB": "{:.2f}", "math OL": "{:.2f}", "math SE": "{:.2f}",
            "RLA EB": "{:.2f}", "RLA OL": "{:.2f}", "RLA SE": "{:.2f}",
            "tests math": "{:,.0f}"}
    n_elem = int(lea.LEVEL.eq("Elementary").sum())
    L += ["## Context: grade span, poverty, SEDA precision", "",
          "SEDA scores are grade-level equivalents re-anchored to grade 5.5, so a "
          "nationally average district scores 5.5; EB is the empirical-Bayes "
          "estimate used in the DEA outputs, OL the raw estimate. "
          f"{n_elem} of the {len(ctx)} efficient units are elementary (K-8 or PK-6) "
          "districts.", "", _md(ctx.reset_index(drop=True), cfmt), ""]

    # Focus districts over time.
    foc = seda[seda.leaid.isin(FOCUS)].copy()
    foc["district"] = foc.leaid.map(FOCUS)
    foc = foc.sort_values(["district", "year"])[
        ["district", "year", "gcs_mn_avg_mth_eb", "gcs_mn_avg_mth_ol", "gcs_mn_avg_mth_eb_se",
         "gcs_mn_avg_rla_eb", "gcs_mn_avg_rla_ol", "gcs_mn_avg_rla_eb_se", "tot_asmts_mth"]]
    foc.columns = ["district", "year", "math EB", "math OL", "math SE", "RLA EB", "RLA OL",
                   "RLA SE", "tests math"]
    L += ["## SEDA scores over time, focus districts", "",
          _md(foc, {"year": "{:.0f}", **{c: "{:.2f}" for c in foc.columns[2:8]},
                    "tests math": "{:,.0f}"}), "", NOTES]
    return L


def main() -> None:
    unscreened, final, scores = load_inputs()
    for path, lines in ((CONCENTRATION_FILE, concentration_report(unscreened, final)
                                             + state_dq_section(unscreened)),
                        (EFFICIENT_FILE, efficient_units_report(unscreened, final, scores))):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(lines), encoding="utf-8")
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
