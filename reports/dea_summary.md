# DEA results, school districts 2018-19

Run: 2026-10-23T11:11:01+00:00  |  n = 10,680 districts  |  n_jobs = 10  |  tolerance = 1e-06

Inputs: exp_current, staff_teachers_fte, staff_other_fte  
Outputs: out_math, out_rla

Models: input-oriented envelopment form, HiGHS. Variables were divided by their column means before solving (CCR/BCC are invariant to this). Slacks in the CSV are in original units.

## Runtime (wall-clock seconds)

| stage | seconds |
|---|---|
| ccr_phase1 | 68.02 |
| ccr_phase2 | 93.37 |
| super_eff | 0.17 |
| bcc_phase1 | 82.62 |
| total | 244.18 |
| ccr_phase1_serial | 437.52 |

CCR phase 1 alone: **68.02 s** for 10,680 LPs (6.37 ms per district, n_jobs = 10).

CCR phase 1, separate serial run (n_jobs = 1): **437.52 s** (40.97 ms per district). Scores identical to the parallel run: yes.

## Solver status

- status_ccr_p1: optimal = 10,680
- status_ccr_p2: optimal = 10,680
- status_super: skipped = 10,662, optimal = 18
- status_bcc: optimal = 10,680

## CCR (constant returns to scale)

- efficient (theta >= 1 - 1e-06): 18
- strongly efficient (all slacks <= 1e-06 rescaled): 18
- weakly efficient (theta = 1, positive slack): 0
- median theta: 0.4850

| statistic | value |
|---|---|
| n | 10680 |
| mean | 0.4936 |
| std | 0.1414 |
| min | 0.0283 |
| p05 | 0.2777 |
| p25 | 0.3967 |
| median | 0.4850 |
| p75 | 0.5795 |
| p95 | 0.7438 |
| max | 1.0000 |
| count <0.5 | 5797 |
| count 0.5-0.6 | 2632 |
| count 0.6-0.7 | 1402 |
| count 0.7-0.8 | 566 |
| count 0.8-0.9 | 204 |
| count 0.9-<1 | 61 |
| count =1 | 18 |

## BCC (variable returns to scale)

- efficient: 44
- median theta: 0.4999

| statistic | value |
|---|---|
| n | 10680 |
| mean | 0.5123 |
| std | 0.1446 |
| min | 0.0999 |
| p05 | 0.2991 |
| p25 | 0.4127 |
| median | 0.4999 |
| p75 | 0.5971 |
| p95 | 0.7722 |
| max | 1.0000 |
| count <0.5 | 5341 |
| count 0.5-0.6 | 2729 |
| count 0.6-0.7 | 1503 |
| count 0.7-0.8 | 715 |
| count 0.8-0.9 | 259 |
| count 0.9-<1 | 89 |
| count =1 | 44 |

## Scale efficiency and CCR vs BCC

- correlation CCR vs BCC: Pearson 0.9755, Spearman 0.9796
- median scale efficiency: 0.9807
- units with theta_CCR > theta_BCC + 1e-06 (must be 0): 0

| statistic | value |
|---|---|
| n | 10680 |
| mean | 0.9631 |
| std | 0.0564 |
| min | 0.2331 |
| p05 | 0.8664 |
| p25 | 0.9564 |
| median | 0.9807 |
| p75 | 0.9932 |
| p95 | 0.9990 |
| max | 1.0000 |
| count <0.5 | 13 |
| count 0.5-0.6 | 21 |
| count 0.6-0.7 | 74 |
| count 0.7-0.8 | 161 |
| count 0.8-0.9 | 514 |
| count 0.9-<1 | 9879 |
| count =1 | 18 |

## 18 highest super-efficiency scores (outlier review)

Super-efficiency > 1 is only computed for CCR-efficient units. Values far above the rest indicate a unit without close comparators; review before deciding whether to keep it.

| leaid | district_name | state | super_eff | theta_bcc | peer_count | n_peers |
|---|---|---|---|---|---|---|
| 1742960 | Wolf Branch SD 113 | IL | 1.2428 | 1.0000 | 530 | 1 |
| 4004470 | BISHOP | OK | 1.1169 | 1.0000 | 2005 | 1 |
| 1603420 | WEST SIDE JOINT DISTRICT | ID | 1.0948 | 1.0000 | 5688 | 1 |
| 0607350 | Canyon Elementary | CA | 1.0754 | 1.0000 | 527 | 1 |
| 0610290 | Cupertino Union | CA | 1.0688 | 1.0000 | 6560 | 1 |
| 1704740 | Aviston SD 21 | IL | 1.0676 | 1.0000 | 8135 | 1 |
| 0604530 | Belmont-Redwood Shores Elementary | CA | 1.0621 | 1.0000 | 845 | 1 |
| 2708100 | CENTENNIAL PUBLIC SCHOOL DISTRICT | MN | 1.0613 | 1.0000 | 84 | 1 |
| 1705160 | Bartelso SD 57 | IL | 1.0603 | 1.0000 | 1200 | 1 |
| 1728110 | New Hope CCSD 6 | IL | 1.0351 | 1.0000 | 115 | 1 |
| 0637500 | South Pasadena Unified | CA | 1.0333 | 1.0000 | 968 | 1 |
| 0608850 | Clay Joint Elementary | CA | 1.0236 | 1.0000 | 3259 | 1 |
| 4503570 | Spartanburg 04 | SC | 1.0230 | 1.0000 | 23 | 1 |
| 2914320 | HICKORY CO. R-I | MO | 1.0211 | 1.0000 | 30 | 1 |
| 2912030 | FESTUS R-VI | MO | 1.0132 | 1.0000 | 150 | 1 |
| 0620130 | La Canada Unified | CA | 1.0021 | 1.0000 | 126 | 1 |
| 0622590 | Los Alamitos Unified | CA | 1.0009 | 1.0000 | 37 | 1 |
| 3812720 | MENOKEN 33 | ND | 1.0008 | 1.0000 | 4 | 1 |

## 18 most frequent peers

peer_count = number of OTHER districts whose CCR phase-2 reference set includes this district (lambda > tolerance).

| leaid | district_name | state | peer_count | super_eff | theta_bcc |
|---|---|---|---|---|---|
| 1704740 | Aviston SD 21 | IL | 8135 | 1.0676 | 1.0000 |
| 0610290 | Cupertino Union | CA | 6560 | 1.0688 | 1.0000 |
| 1603420 | WEST SIDE JOINT DISTRICT | ID | 5688 | 1.0948 | 1.0000 |
| 0608850 | Clay Joint Elementary | CA | 3259 | 1.0236 | 1.0000 |
| 4004470 | BISHOP | OK | 2005 | 1.1169 | 1.0000 |
| 1705160 | Bartelso SD 57 | IL | 1200 | 1.0603 | 1.0000 |
| 0637500 | South Pasadena Unified | CA | 968 | 1.0333 | 1.0000 |
| 0604530 | Belmont-Redwood Shores Elementary | CA | 845 | 1.0621 | 1.0000 |
| 1742960 | Wolf Branch SD 113 | IL | 530 | 1.2428 | 1.0000 |
| 0607350 | Canyon Elementary | CA | 527 | 1.0754 | 1.0000 |
| 2912030 | FESTUS R-VI | MO | 150 | 1.0132 | 1.0000 |
| 0620130 | La Canada Unified | CA | 126 | 1.0021 | 1.0000 |
| 1728110 | New Hope CCSD 6 | IL | 115 | 1.0351 | 1.0000 |
| 2708100 | CENTENNIAL PUBLIC SCHOOL DISTRICT | MN | 84 | 1.0613 | 1.0000 |
| 0622590 | Los Alamitos Unified | CA | 37 | 1.0009 | 1.0000 |
| 2914320 | HICKORY CO. R-I | MO | 30 | 1.0211 | 1.0000 |
| 4503570 | Spartanburg 04 | SC | 23 | 1.0230 | 1.0000 |
| 3812720 | MENOKEN 33 | ND | 4 | 1.0008 | 1.0000 |

## Extreme input-output ratios (flagged, not removed)

ratio = (out_math + out_rla) / input. These districts are kept in the sample; they are listed so the decision can be made explicitly.

### Top 20 output per teacher FTE

| leaid | district_name | state | ratio | ratio_over_median | theta_ccr | efficient | top20_peer |
|---|---|---|---|---|---|---|---|
| 0607350 | Canyon Elementary | CA | 468.3193 | 3.0277 | 1.0000 | yes | yes |
| 0610290 | Cupertino Union | CA | 440.9222 | 2.8506 | 1.0000 | yes | yes |
| 0620130 | La Canada Unified | CA | 437.7746 | 2.8302 | 1.0000 | yes | yes |
| 0608850 | Clay Joint Elementary | CA | 432.7685 | 2.7979 | 1.0000 | yes | yes |
| 0684500 | Irvine Unified | CA | 428.1848 | 2.7682 | 0.9709 | no | no |
| 0622590 | Los Alamitos Unified | CA | 426.3321 | 2.7563 | 1.0000 | yes | yes |
| 0610740 | Del Mar Union Elementary | CA | 426.0121 | 2.7542 | 0.9525 | no | no |
| 0637500 | South Pasadena Unified | CA | 425.1722 | 2.7488 | 1.0000 | yes | yes |
| 0600025 | Manhattan Beach Unified | CA | 418.7480 | 2.7072 | 0.9468 | no | no |
| 0614220 | Fountain Valley Elementary | CA | 410.1810 | 2.6518 | 0.9554 | no | no |
| 0602970 | Arcadia Unified | CA | 404.1226 | 2.6127 | 0.9194 | no | no |
| 0604530 | Belmont-Redwood Shores Elementary | CA | 403.1559 | 2.6064 | 1.0000 | yes | yes |
| 3904956 | Lakota Local | OH | 396.2084 | 2.5615 | 0.8808 | no | no |
| 0618030 | Huntington Beach City Elementary | CA | 395.7945 | 2.5588 | 0.9221 | no | no |
| 0600032 | Redondo Beach Unified | CA | 395.3259 | 2.5558 | 0.9093 | no | no |
| 0641280 | Walnut Valley Unified | CA | 392.5483 | 2.5378 | 0.9166 | no | no |
| 0635130 | San Ramon Valley Unified | CA | 391.8539 | 2.5334 | 0.9392 | no | no |
| 0620310 | Lafayette Elementary | CA | 391.6853 | 2.5323 | 0.9004 | no | no |
| 0600019 | Dublin Unified | CA | 389.2060 | 2.5162 | 0.9943 | no | no |
| 0640320 | Union Elementary | CA | 389.0800 | 2.5154 | 0.9597 | no | no |

### Top 20 output per current-expenditure dollar

| leaid | district_name | state | ratio | ratio_over_median | theta_ccr | efficient | top20_peer |
|---|---|---|---|---|---|---|---|
| 1705160 | Bartelso SD 57 | IL | 0.002182 | 2.464556 | 1.000000 | yes | yes |
| 1603420 | WEST SIDE JOINT DISTRICT | ID | 0.002174 | 2.454971 | 1.000000 | yes | yes |
| 1704740 | Aviston SD 21 | IL | 0.002080 | 2.348390 | 1.000000 | yes | yes |
| 1716530 | Germantown SD 60 | IL | 0.002049 | 2.313477 | 0.941608 | no | no |
| 4024150 | PIONEER | OK | 0.002026 | 2.287475 | 0.938090 | no | no |
| 1602100 | JOINT SCHOOL DISTRICT NO. 2 | ID | 0.002020 | 2.281522 | 0.968485 | no | no |
| 1703270 | Albers SD 63 | IL | 0.001956 | 2.208330 | 0.905054 | no | no |
| 1601570 | JEFFERSON COUNTY JOINT DISTRICT | ID | 0.001952 | 2.204814 | 0.971999 | no | no |
| 0403780 | Higley Unified School District (4248) | AZ | 0.001948 | 2.200125 | 0.927854 | no | no |
| 4004470 | BISHOP | OK | 0.001946 | 2.198157 | 1.000000 | yes | yes |
| 0401760 | Catalina Foothills Unified District (4410) | AZ | 0.001885 | 2.129108 | 0.910873 | no | no |
| 4026100 | ROBIN HILL | OK | 0.001863 | 2.104289 | 0.855677 | no | no |
| 1801020 | Brownsburg Community School Corp | IN | 0.001860 | 2.100166 | 0.955921 | no | no |
| 1708640 | Carterville CUSD 5 | IL | 0.001857 | 2.096884 | 0.880035 | no | no |
| 1738190 | Summersville SD 79 | IL | 0.001854 | 2.094046 | 0.851469 | no | no |
| 4700154 | Lakeland | TN | 0.001847 | 2.085508 | 0.932362 | no | no |
| 1709150 | Central SD 51 | IL | 0.001838 | 2.075999 | 0.948271 | no | no |
| 3018750 | Monforton Elem | MT | 0.001837 | 2.074465 | 0.871038 | no | no |
| 0400001 | Cave Creek Unified District (4244) | AZ | 0.001831 | 2.067260 | 0.982578 | no | no |
| 0407820 | Snowflake Unified District (4391) | AZ | 0.001829 | 2.065134 | 0.953471 | no | no |

## Flags

- 6 district(s) serve as peer for more than 10 % of the sample.
- 46 district(s) report fewer than 5 teacher FTE.

## Comparison with dea_scores_2019_n10849.csv

Peer concentration and super-efficiency, this run versus the earlier file. Shares are fractions of the respective sample size.

| measure | this run | dea_scores_2019_n10849.csv |
|---|---|---|
| n | 10,680 | 10,849 |
| efficient_ccr | 18 | 13 |
| peers_used_by_>10% | 6 | 4 |
| peers_used_by_>50% | 3 | 1 |
| top_peer_share | 0.762 | 0.941 |
| top3_peer_share | 0.636 | 0.572 |
| median_n_peers | 3.000 | 2.000 |
| max_super_eff | 1.243 | 1.259 |
| super_eff_>1.5 | 0 | 0 |

### Top 5 super-efficiency

- this run: Wolf Branch SD 113 (IL, 1.243); BISHOP (OK, 1.117); WEST SIDE JOINT DISTRICT (ID, 1.095); Canyon Elementary (CA, 1.075); Cupertino Union (CA, 1.069)
- dea_scores_2019_n10849.csv: Andover (KS, 1.259); Wolf Branch SD 113 (IL, 1.243); Canyon Elementary (CA, 1.075); Cupertino Union (CA, 1.068); CENTENNIAL PUBLIC SCHOOL DISTRICT (MN, 1.051)

### Top 5 most frequent peers

- this run: Aviston SD 21 (IL, 8,135); Cupertino Union (CA, 6,560); WEST SIDE JOINT DISTRICT (ID, 5,688); Clay Joint Elementary (CA, 3,259); BISHOP (OK, 2,005)
- dea_scores_2019_n10849.csv: Andover (KS, 10,208); Clay Joint Elementary (CA, 4,553); Cupertino Union (CA, 3,872); Belmont-Redwood Shores Elementary (CA, 1,133); South Pasadena Unified (CA, 638)

### Efficient units

- in both samples: 10,680; only in dea_scores_2019_n10849.csv: 169; only in this run: 0
- CCR-efficient in dea_scores_2019_n10849.csv: 13; in this run: 18
- efficient before and no longer in the sample (1): Andover (KS, 2003360)
- efficient before, still in the sample, no longer efficient (0): none
- newly efficient (6): Aviston SD 21 (IL, 1704740); BISHOP (OK, 4004470); Bartelso SD 57 (IL, 1705160); FESTUS R-VI (MO, 2912030); HICKORY CO. R-I (MO, 2914320); WEST SIDE JOINT DISTRICT (ID, 1603420)

### Units whose previous reference set included a departed peer

| departed peer | units that used it | median theta before | median theta now | median change | mean change | max change | share with higher theta |
|---|---|---|---|---|---|---|---|
| Andover (KS) | 10,057 | 0.4275 | 0.4863 | +0.0571 | +0.0580 | +0.1795 | 100.0% |
| any departed peer | 10,057 | 0.4275 | 0.4863 | +0.0571 | +0.0580 | +0.1795 | 100.0% |
| no departed peer | 623 | 0.4664 | 0.4664 | -0.0000 | -0.0000 | +0.0000 | 0.0% |

### Headline statistics

| measure | this run | dea_scores_2019_n10849.csv |
|---|---|---|
| n | 10,680 | 10,849 |
| median theta_CCR | 0.4850 | 0.4286 |
| min theta_CCR | 0.0283 | 0.0266 |
| median theta_BCC | 0.4999 | 0.4471 |
| Spearman CCR vs BCC | 0.9796 | 0.9553 |
| median scale efficiency | 0.9807 | 0.9840 |

### Agreement on the 10,680 common units

- Spearman theta_CCR this run vs dea_scores_2019_n10849.csv: 0.9784; Pearson 0.9776
- Spearman theta_BCC: 0.9734
- change in theta_CCR (this run minus dea_scores_2019_n10849.csv): median +0.0546, mean +0.0546, p95 +0.1069, max +0.1795; units with a lower theta: 0 (removing units cannot lower a CCR score; any such case is solver noise)
