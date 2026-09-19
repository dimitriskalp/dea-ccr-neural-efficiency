# DEA & Machine Learning for Efficiency Prediction

Measuring the technical efficiency of US public universities with Data
Envelopment Analysis, then predicting those efficiency scores with machine
learning models.

MSc thesis project.

---

## Motivation

DEA measures the relative efficiency of Decision Making Units (DMUs) by
solving one linear program per unit. This works well but has two practical
limits: it does not scale to very large samples, and it cannot produce a score
for a unit that was not part of the original problem without re-solving
everything from scratch.

This project tests whether a machine learning model trained on DEA scores can
approximate the efficiency frontier well enough to be useful — and what is lost
in the process.

The approach follows the line of work started by Athanassopoulos & Curram
(1996) and extended by Emrouznejad & Shale (2009).

---

## Approach

1. Compute CCR efficiency scores for every institution (input-oriented, CRS).
2. Use those scores as the target variable.
3. Train models on the DEA inputs and outputs, then on an extended feature set
   that also includes contextual variables not admissible in DEA itself.
4. Compare a neural network against linear regression and decision tree
   baselines under repeated k-fold cross-validation.

---

## Data

All data come from **IPEDS** (Integrated Postsecondary Education Data System),
National Center for Education Statistics — Complete Data Files.
Collection year 2024; finance data cover fiscal year 2023–24.

Download page: https://nces.ed.gov/ipeds/datacenter/DataFiles.aspx

| File | Survey | Used for |
|---|---|---|
| `HD2024` | Institutional Characteristics | Sample selection, contextual variables |
| `F2324_F1A` | Finance (GASB) | Operating expenses |
| `S2024_OC` | Fall Staff | Instructional staff |
| `EFIA2024_RV` | 12-Month Enrollment | FTE students |
| `C2024_C_RV` | Completions | Degrees conferred |

Raw files are **not** tracked in this repository. Download them from the link
above into `data/raw/` and run the build script.

### Sample selection

| Step | N |
|---|---|
| All institutions in HD2024 | 6,072 |
| Public (`CONTROL=1`) and 4-year (`ICLEVEL=1`) | 896 |
| Master's institutions (`C21BASIC` in 18, 19, 20) | 238 |
| No medical school (`MEDICAL≠1`) | 237 |
| Present in all five files | 231 |

Master's institutions were chosen for homogeneity of production technology:
none operate a hospital and research activity is limited, unlike R1/R2
universities.

### Variables

| Role | Variable | Construction |
|---|---|---|
| Input | `EG_EXP` | Education & General expenses: sum of `F1C011`, `F1C021`, `F1C031`, `F1C051`, `F1C061`, `F1C071` |
| Input | `FAC_FTE` | Instructional staff (`OCCUPCAT=210`): full-time + part-time / 3 |
| Input | `FTE_STUD` | `FTEUG` + `FTEGD` |
| Output | `BACH` | Bachelor's degrees (`AWLEVELC=5`) |
| Output | `MAST` | Master's degrees (`AWLEVELC=7`) |
| Contextual | `STABBR`, `LOCALE`, `HBCU`, `C21BASIC` | ML feature set only, excluded from DEA |

Auxiliary enterprise expenses (housing, dining, bookstores) are excluded —
roughly 24% of total expenses — since they do not contribute to degree
production.

---

## Repository structure

```
data/
  raw/                  # IPEDS downloads (gitignored)
  processed/            # built analysis sample
src/
  build_dataset.py      # download -> clean -> merge -> validate
  dea.py                # CCR and BCC models
  predict.py            # ML models and cross-validation
notebooks/              # exploratory analysis
requirements.txt
```

## Running

```bash
pip install -r requirements.txt
python src/build_dataset.py     # writes data/processed/dea_dataset_2024.csv
python src/dea.py               # computes efficiency scores
python src/predict.py           # trains and evaluates models
```

---

## Validation checks

The build script enforces four conditions before any analysis:

- **Positivity** — CCR requires strictly positive inputs and outputs.
- **Sample adequacy** — n ≥ 3(m + s); here 231 ≥ 15.
- **Isotonicity** — all input–output Spearman correlations positive
  (observed range 0.57 to 0.94).
- **No duplicate `UNITID`.**

The DEA implementation is verified by unit-invariance: multiplying all inputs
by a constant must leave every score unchanged.

---

## Known issues

- The finance file is a **provisional** release; the other files are revised.
  IPEDS files are periodically updated, so download dates matter.
- Two institutions (Louisiana State University–Shreveport and Colorado State
  University Global) show super-efficiency scores of 2.50 and 1.55 against
  1.01–1.11 for all other efficient units, and act as peers for a large share
  of the sample. Both appear to be distance-education institutions, i.e. a
  different production technology. Results are reported with and without them.
- Two institutions are lost in the merges due to survey non-response.
- DEA scores depend on the whole sample, since the frontier is defined jointly.
  Out-of-sample evaluation is therefore not fully independent — an inherent
  property of this design, discussed in the thesis limitations.

---

## Key references

- Charnes, A., Cooper, W. W., & Rhodes, E. (1978). Measuring the efficiency of
  decision making units. *European Journal of Operational Research*, 2(6),
  429–444.
- Athanassopoulos, A. D., & Curram, S. P. (1996). A comparison of data
  envelopment analysis and artificial neural networks as tools for assessing
  the efficiency of decision making units. *JORS*, 47(8), 1000–1016.
- Emrouznejad, A., & Shale, E. (2009). A combined neural network and DEA for
  measuring efficiency of large scale datasets. *Computers & Industrial
  Engineering*, 56(1), 249–254.
- Simar, L., & Wilson, P. W. (2007). Estimation and inference in two-stage,
  semi-parametric models of production processes. *Journal of Econometrics*,
  136(1), 31–64.

---

## License

MIT for the code. IPEDS data are in the public domain.
