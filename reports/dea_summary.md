# DEA results, school districts 2018-19

Run: 2026-10-23T09:40:07+00:00  |  n = 10,849 districts  |  n_jobs = 10  |  tolerance = 1e-06

Inputs: exp_current, staff_teachers_fte, staff_other_fte  
Outputs: out_math, out_rla

Models: input-oriented envelopment form, HiGHS. Variables were divided by their column means before solving (CCR/BCC are invariant to this). Slacks in the CSV are in original units.

## Runtime (wall-clock seconds)

| stage | seconds |
|---|---|
| ccr_phase1 | 74.16 |
| ccr_phase2 | 96.55 |
| super_eff | 0.15 |
| bcc_phase1 | 82.91 |
| total | 253.77 |
| ccr_phase1_serial | 460.11 |

CCR phase 1 alone: **74.16 s** for 10,849 LPs (6.84 ms per district, n_jobs = 10).

CCR phase 1, separate serial run (n_jobs = 1): **460.11 s** (42.41 ms per district). Scores identical to the parallel run: yes.

## Solver status

- status_ccr_p1: optimal = 10,849
- status_ccr_p2: optimal = 10,849
- status_super: skipped = 10,836, optimal = 13
- status_bcc: optimal = 10,849

## CCR (constant returns to scale)

- efficient (theta >= 1 - 1e-06): 13
- strongly efficient (all slacks <= 1e-06 rescaled): 13
- weakly efficient (theta = 1, positive slack): 0
- median theta: 0.4286

| statistic | value |
|---|---|
| n | 10849 |
| mean | 0.4386 |
| std | 0.1288 |
| min | 0.0266 |
| p05 | 0.2478 |
| p25 | 0.3522 |
| median | 0.4286 |
| p75 | 0.5108 |
| p95 | 0.6655 |
| max | 1.0000 |
| count <0.5 | 7825 |
| count 0.5-0.6 | 1908 |
| count 0.6-0.7 | 731 |
| count 0.7-0.8 | 258 |
| count 0.8-0.9 | 86 |
| count 0.9-<1 | 28 |
| count =1 | 13 |

## BCC (variable returns to scale)

- efficient: 36
- median theta: 0.4471

| statistic | value |
|---|---|
| n | 10849 |
| mean | 0.4615 |
| std | 0.1316 |
| min | 0.0927 |
| p05 | 0.2756 |
| p25 | 0.3737 |
| median | 0.4471 |
| p75 | 0.5303 |
| p95 | 0.7009 |
| max | 1.0000 |
| count <0.5 | 7278 |
| count 0.5-0.6 | 2155 |
| count 0.6-0.7 | 868 |
| count 0.7-0.8 | 342 |
| count 0.8-0.9 | 121 |
| count 0.9-<1 | 49 |
| count =1 | 36 |

## Scale efficiency and CCR vs BCC

- correlation CCR vs BCC: Pearson 0.9468, Spearman 0.9553
- median scale efficiency: 0.9840
- units with theta_CCR > theta_BCC + 1e-06 (must be 0): 0

| statistic | value |
|---|---|
| n | 10849 |
| mean | 0.9503 |
| std | 0.0793 |
| min | 0.2313 |
| p05 | 0.7826 |
| p25 | 0.9410 |
| median | 0.9840 |
| p75 | 0.9955 |
| p95 | 0.9996 |
| max | 1.0000 |
| count <0.5 | 29 |
| count 0.5-0.6 | 64 |
| count 0.6-0.7 | 146 |
| count 0.7-0.8 | 393 |
| count 0.8-0.9 | 1072 |
| count 0.9-<1 | 9132 |
| count =1 | 13 |

## 13 highest super-efficiency scores (outlier review)

Super-efficiency > 1 is only computed for CCR-efficient units. Values far above the rest indicate a unit without close comparators; review before deciding whether to keep it.

| leaid | district_name | state | super_eff | theta_bcc | peer_count | n_peers |
|---|---|---|---|---|---|---|
| 2003360 | Andover | KS | 1.2594 | 1.0000 | 10208 | 1 |
| 1742960 | Wolf Branch SD 113 | IL | 1.2428 | 1.0000 | 619 | 1 |
| 0607350 | Canyon Elementary | CA | 1.0754 | 1.0000 | 540 | 1 |
| 0610290 | Cupertino Union | CA | 1.0677 | 1.0000 | 3872 | 1 |
| 2708100 | CENTENNIAL PUBLIC SCHOOL DISTRICT | MN | 1.0514 | 1.0000 | 216 | 1 |
| 0604530 | Belmont-Redwood Shores Elementary | CA | 1.0447 | 1.0000 | 1133 | 1 |
| 0608850 | Clay Joint Elementary | CA | 1.0236 | 1.0000 | 4553 | 1 |
| 0637500 | South Pasadena Unified | CA | 1.0193 | 1.0000 | 638 | 1 |
| 4503570 | Spartanburg 04 | SC | 1.0126 | 1.0000 | 179 | 1 |
| 1728110 | New Hope CCSD 6 | IL | 1.0090 | 1.0000 | 168 | 1 |
| 0620130 | La Canada Unified | CA | 1.0021 | 1.0000 | 127 | 1 |
| 0622590 | Los Alamitos Unified | CA | 1.0009 | 1.0000 | 39 | 1 |
| 3812720 | MENOKEN 33 | ND | 1.0008 | 1.0000 | 5 | 1 |

## 13 most frequent peers

peer_count = number of OTHER districts whose CCR phase-2 reference set includes this district (lambda > tolerance).

| leaid | district_name | state | peer_count | super_eff | theta_bcc |
|---|---|---|---|---|---|
| 2003360 | Andover | KS | 10208 | 1.2594 | 1.0000 |
| 0608850 | Clay Joint Elementary | CA | 4553 | 1.0236 | 1.0000 |
| 0610290 | Cupertino Union | CA | 3872 | 1.0677 | 1.0000 |
| 0604530 | Belmont-Redwood Shores Elementary | CA | 1133 | 1.0447 | 1.0000 |
| 0637500 | South Pasadena Unified | CA | 638 | 1.0193 | 1.0000 |
| 1742960 | Wolf Branch SD 113 | IL | 619 | 1.2428 | 1.0000 |
| 0607350 | Canyon Elementary | CA | 540 | 1.0754 | 1.0000 |
| 2708100 | CENTENNIAL PUBLIC SCHOOL DISTRICT | MN | 216 | 1.0514 | 1.0000 |
| 4503570 | Spartanburg 04 | SC | 179 | 1.0126 | 1.0000 |
| 1728110 | New Hope CCSD 6 | IL | 168 | 1.0090 | 1.0000 |
| 0620130 | La Canada Unified | CA | 127 | 1.0021 | 1.0000 |
| 0622590 | Los Alamitos Unified | CA | 39 | 1.0009 | 1.0000 |
| 3812720 | MENOKEN 33 | ND | 5 | 1.0008 | 1.0000 |

## Extreme input-output ratios (flagged, not removed)

ratio = (out_math + out_rla) / input. These districts are kept in the sample; they are listed so the decision can be made explicitly.

### Top 20 output per teacher FTE

| leaid | district_name | state | ratio | ratio_over_median | theta_ccr | efficient | top20_peer |
|---|---|---|---|---|---|---|---|
| 0607350 | Canyon Elementary | CA | 468.3193 | 3.0337 | 1.0000 | yes | yes |
| 0610290 | Cupertino Union | CA | 440.9222 | 2.8562 | 1.0000 | yes | yes |
| 0620130 | La Canada Unified | CA | 437.7746 | 2.8359 | 1.0000 | yes | yes |
| 0608850 | Clay Joint Elementary | CA | 432.7685 | 2.8034 | 1.0000 | yes | yes |
| 0684500 | Irvine Unified | CA | 428.1848 | 2.7737 | 0.9709 | no | no |
| 0622590 | Los Alamitos Unified | CA | 426.3321 | 2.7617 | 1.0000 | yes | yes |
| 0610740 | Del Mar Union Elementary | CA | 426.0121 | 2.7597 | 0.9525 | no | no |
| 0637500 | South Pasadena Unified | CA | 425.1722 | 2.7542 | 1.0000 | yes | yes |
| 0600025 | Manhattan Beach Unified | CA | 418.7480 | 2.7126 | 0.9468 | no | no |
| 0608610 | Chula Vista Elementary | CA | 410.7349 | 2.6607 | 0.9661 | no | no |
| 0614220 | Fountain Valley Elementary | CA | 410.1810 | 2.6571 | 0.9466 | no | no |
| 0602970 | Arcadia Unified | CA | 404.1226 | 2.6179 | 0.9194 | no | no |
| 0604530 | Belmont-Redwood Shores Elementary | CA | 403.1559 | 2.6116 | 1.0000 | yes | yes |
| 3904956 | Lakota Local | OH | 396.2084 | 2.5666 | 0.8808 | no | no |
| 0618030 | Huntington Beach City Elementary | CA | 395.7945 | 2.5639 | 0.9221 | no | no |
| 0600032 | Redondo Beach Unified | CA | 395.3259 | 2.5609 | 0.9093 | no | no |
| 0641280 | Walnut Valley Unified | CA | 392.5483 | 2.5429 | 0.9098 | no | no |
| 0635130 | San Ramon Valley Unified | CA | 391.8539 | 2.5384 | 0.9355 | no | no |
| 0620310 | Lafayette Elementary | CA | 391.6853 | 2.5373 | 0.9004 | no | no |
| 0600019 | Dublin Unified | CA | 389.2060 | 2.5212 | 0.9695 | no | no |

### Top 20 output per current-expenditure dollar

| leaid | district_name | state | ratio | ratio_over_median | theta_ccr | efficient | top20_peer |
|---|---|---|---|---|---|---|---|
| 2003360 | Andover | KS | 0.002502 | 2.829086 | 1.000000 | yes | yes |
| 1705160 | Bartelso SD 57 | IL | 0.002182 | 2.467472 | 0.927352 | no | no |
| 1603420 | WEST SIDE JOINT DISTRICT | ID | 0.002174 | 2.457876 | 0.910010 | no | no |
| 4828830 | MALTA ISD | TX | 0.002164 | 2.447063 | 0.877746 | no | no |
| 1704740 | Aviston SD 21 | IL | 0.002080 | 2.351169 | 0.874613 | no | no |
| 1716530 | Germantown SD 60 | IL | 0.002049 | 2.316215 | 0.838934 | no | no |
| 4024150 | PIONEER | OK | 0.002026 | 2.290182 | 0.815893 | no | no |
| 1602100 | JOINT SCHOOL DISTRICT NO. 2 | ID | 0.002020 | 2.284222 | 0.809851 | no | no |
| 1703270 | Albers SD 63 | IL | 0.001956 | 2.210943 | 0.809823 | no | no |
| 1601570 | JEFFERSON COUNTY JOINT DISTRICT | ID | 0.001952 | 2.207423 | 0.819283 | no | no |
| 0403780 | Higley Unified School District (4248) | AZ | 0.001948 | 2.202728 | 0.791694 | no | no |
| 4004470 | BISHOP | OK | 0.001946 | 2.200759 | 0.924120 | no | no |
| 4011760 | FLOWER MOUND | OK | 0.001942 | 2.195248 | 0.805121 | no | no |
| 1602490 | ONEIDA COUNTY DISTRICT | ID | 0.001919 | 2.170115 | 0.804864 | no | no |
| 0401760 | Catalina Foothills Unified District (4410) | AZ | 0.001885 | 2.131628 | 0.767955 | no | no |
| 4026100 | ROBIN HILL | OK | 0.001863 | 2.106779 | 0.745760 | no | no |
| 1801020 | Brownsburg Community School Corp | IN | 0.001860 | 2.102651 | 0.786833 | no | no |
| 1708640 | Carterville CUSD 5 | IL | 0.001857 | 2.099366 | 0.784737 | no | no |
| 1738190 | Summersville SD 79 | IL | 0.001854 | 2.096524 | 0.743195 | no | no |
| 4700154 | Lakeland | TN | 0.001847 | 2.087976 | 0.752836 | no | no |

## Flags

- 4 district(s) serve as peer for more than 10 % of the sample.
- 50 district(s) report fewer than 5 teacher FTE.

## Comparison with dea_scores_2019_sample500.csv

Peer concentration and super-efficiency, this run versus the earlier file. Shares are fractions of the respective sample size.

| measure | this run | dea_scores_2019_sample500.csv |
|---|---|---|
| n | 10,849 | 500 |
| efficient_ccr | 13 | 8 |
| peers_used_by_>10% | 4 | 5 |
| peers_used_by_>50% | 1 | 1 |
| top_peer_share | 0.941 | 0.760 |
| top3_peer_share | 0.572 | 0.529 |
| median_n_peers | 2.000 | 2.000 |
| max_super_eff | 1.259 | 2.574 |
| super_eff_>1.5 | 0 | 1 |

### Top 5 super-efficiency

- this run: Andover (KS, 1.259); Wolf Branch SD 113 (IL, 1.243); Canyon Elementary (CA, 1.075); Cupertino Union (CA, 1.068); CENTENNIAL PUBLIC SCHOOL DISTRICT (MN, 1.051)
- dea_scores_2019_sample500.csv: Selmaville CCSD 10 (IL, 2.574); Cupertino Union (CA, 1.195); Union Elementary (CA, 1.170); SUGAR-SALEM JOINT DISTRICT (ID, 1.107); Houghton-Portage Township School District (MI, 1.082)

### Top 5 most frequent peers

- this run: Andover (KS, 10,208); Clay Joint Elementary (CA, 4,553); Cupertino Union (CA, 3,872); Belmont-Redwood Shores Elementary (CA, 1,133); South Pasadena Unified (CA, 638)
- dea_scores_2019_sample500.csv: Plainfield Community School Corp (IN, 380); Cupertino Union (CA, 223); SUGAR-SALEM JOINT DISTRICT (ID, 191); Houghton-Portage Township School District (MI, 148); Hermosa Beach City Elementary (CA, 90)

- districts in both files: 495; CCR-efficient in dea_scores_2019_sample500.csv: 8, of which still efficient here: 1, no longer in the sample: 2
