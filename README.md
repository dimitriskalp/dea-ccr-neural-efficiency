# DEA and neural networks for the efficiency of US school districts

MSc thesis project. Technical efficiency of US public school districts in
school year 2018-19 is measured with Data Envelopment Analysis (CCR,
input-oriented), and a neural network is then trained to predict the DEA
scores from the same inputs and outputs plus context variables that DEA
cannot use.

## Research question

DEA solves one linear program per unit, so it scales poorly and cannot
score a unit that was not in the original problem without re-solving
everything. Can a neural network trained on DEA scores approximate the
efficiency frontier well enough to be useful, and what is lost in the
process? The approach follows Athanassopoulos and Curram (1996) and
Emrouznejad and Shale (2009).

## DEA specification

| role | variable | source |
|---|---|---|
| input | `exp_current`: total current expenditure, elementary/secondary (USD) | F-33 `TCURELSC` |
| input | `staff_teachers_fte`: teachers (FTE) | CCD LEA Staff |
| input | `staff_other_fte`: all other staff (FTE) | CCD LEA Staff |
| output | `out_math`: pupils x math achievement (grade-level equivalents) | F-33 `V33` x SEDA |
| output | `out_rla`: pupils x reading/language-arts achievement | F-33 `V33` x SEDA |

Achievement is the SEDA empirical-Bayes district mean on the grade-cohort
scale, re-anchored to grade 5.5 so that districts with different tested
grades are comparable. Multiplying by pupils turns a quality index into a
volume, which constant returns to scale require.

Models: CCR two-phase (radial score, then maximal slacks), BCC, scale
efficiency and Andersen-Petersen super-efficiency, all solved with HiGHS
through `scipy.optimize.linprog`.

## Data sources

Raw files are not tracked. Download them into `data/raw/` with exactly
these names; the companion documents are in `docs/data_dictionaries/`.

| file | source | used for |
|---|---|---|
| `ccd_lea_029_1819_w_1a_091019.csv` | CCD LEA Directory 2018-19 | sample selection, grade span |
| `ccd_lea_059_1819_l_1a_091019.csv` | CCD LEA Staff 2018-19 | teachers and other staff (FTE) |
| `ccd_sch_029_1819_w_1a_091019.csv` | CCD School Directory 2018-19 | school names (cross-check) |
| `ccd_sch_129_1819_w_1a_091019.csv` | CCD School Characteristics 2018-19 | virtual status (`VIRTUAL`) |
| `ccd_SCH_052_1819_l_1a_091019.csv` | CCD School Membership 2018-19 (2.5 GB) | school enrollment, reduced once to `data/interim/school_membership_1819.csv` |
| `sdf18_1a.txt`, `sdf19_2a.txt`, `sdf20_2a.txt` | F-33 School District Finance Survey FY2018-FY2020 | expenditures, fall membership, temporal check |
| `seda_admindist_annualsub_gcs_6.0.csv` | SEDA 6.0, administrative districts, annual, by subject | math and RLA achievement |
| `seda_cov_admindist_annual_6.0.csv` | SEDA 6.0 district covariates | context variables (ML stage only) |

Download pages: CCD nonfiscal files at
<https://nces.ed.gov/ccd/files.asp>; F-33 at
<https://nces.ed.gov/ccd/f33agency.asp>; SEDA 6.0 at
<https://edopportunity.org/get-the-data/>.

## Sample selection

Districts are regular public school districts (CCD LEA type 1 or 2) that
are open and offer at least one of grades 3-8. After merging the four
sources, the rules below are applied in this order; each removes districts
given the rules above it (`reports/sample_flow.md`, written by the build).

| rule | removed | remaining |
|---|---|---|
| merged (directory, staff, finance, scores) | | 11,252 |
| complete DEA variables | 273 | 10,979 |
| strictly positive DEA variables | 11 | 10,968 |
| state comparability: Utah and Nevada report other staff on a different basis | 52 | 10,916 |
| data-quality screen: any input ratio beyond 5 robust SD of the median (log scale) | 67 | 10,849 |
| temporal consistency: FY2019 is a one-year spike or dip in F-33 spending per pupil or membership | 33 | 10,816 |
| enrollment consistency: fall membership too high against SEDA grade 3-8 enrollment, within grade-span groups | 106 | 10,710 |
| virtual-school share: 10 % or more of pupils in fully virtual schools (CCD `FULLVIRTUAL`) | 30 | 10,680 |

Every excluded district is written to `data/processed/excluded_*.csv`
with the statistic that triggered the rule. Robust-z screens compute
their median and MAD on the sample they receive, so each is calibrated on
the districts that survive the earlier rules. The virtual rule treats
`FACEVIRTUAL`, `SUPPVIRTUAL` and schools with a missing status as not
virtual. Robustness variants: `--dq-threshold 4`, `--keep-states`,
`--virtual-threshold 0.05` or `0.20`; they write suffixed files and never
overwrite the main dataset.

## Robustness runs

Available as switches of the build (they write suffixed files): the
data-quality screen at 4 robust SD (`--dq-threshold 4`), keeping Utah and
Nevada (`--keep-states`), the virtual rule at 5 % or 20 %
(`--virtual-threshold 0.05`, `0.20`).

Planned, not yet run: separate CCR frontiers for elementary-only districts
(no grade 9-12 offered) and for K-12 / unified districts. Elementary
districts face lower unit costs, and most of the CCR-efficient units are
elementary districts. The dataset carries the grade span for this and for
the ML stage: `grade_lo`, `grade_hi`, `lea_level` (CCD) and
`elementary_only`.

## How to run

From the project root, with Python 3.11+ and `pip install -r requirements.txt`:

```
python src/build_dataset.py            # data/processed/dea_districts_2019.csv, sample flow
python src/dea.py --model all --n-jobs 10 --time-serial-phase1 \
       [--compare data/processed/<earlier scores>.csv]
                                       # scores CSV, reports/dea_summary.md, run metadata
python src/screens.py                  # report-only screens (reports/screens_report.md)
python src/diagnostics.py              # exclusion concentration, efficient-unit diagnostics
python src/figures.py                  # reports/figures/*.pdf and *.png
python -m pytest                       # tests
```

The first run of `screens.py` or `diagnostics.py` reduces the 2.5 GB
Membership file to `data/interim/school_membership_1819.csv`; later runs
use the cache (`screens.py --rebuild-membership` to redo it).

## Repository layout

```
src/build_dataset.py   build the district dataset: merge, validate, apply the sample rules
src/dea.py             CCR / BCC / scale / super-efficiency, summary and run metadata
src/screens.py         temporal, enrollment and virtual screens (functions + report)
src/diagnostics.py     report-only diagnostics of the final sample
src/figures.py         thesis figures (matplotlib, Okabe-Ito palette)
tests/                 pytest: hand-computed DEA cases, duality, invariance, screens
reports/               markdown reports, run metadata, figures/
docs/data_dictionaries/ CCD companion workbooks and F-33 record layouts
data/raw/              downloaded source files (ignored by git)
data/interim/          cached intermediate tables (ignored)
data/processed/        built dataset, exclusions, DEA scores (ignored)
```
