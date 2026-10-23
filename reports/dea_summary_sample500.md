# DEA results, school districts 2018-19

Run: 2026-10-23T08:34:54+00:00  |  n = 500 districts  |  n_jobs = 1  |  tolerance = 1e-06

Inputs: exp_current, staff_teachers_fte, staff_other_fte  
Outputs: out_math, out_rla

Models: input-oriented envelopment form, HiGHS. Variables were divided by their column means before solving (CCR/BCC are invariant to this). Slacks in the CSV are in original units.

## Runtime (wall-clock seconds)

| stage | seconds |
|---|---|
| ccr_phase1 | 1.55 |
| ccr_phase2 | 1.85 |
| super_eff | 0.03 |
| bcc_phase1 | 1.69 |
| total | 5.12 |

CCR phase 1 alone: **1.55 s** for 500 LPs (3.09 ms per district, n_jobs = 1).

## Solver status

- status_ccr_p1: optimal = 500
- status_ccr_p2: optimal = 500
- status_super: skipped = 492, optimal = 8
- status_bcc: optimal = 500

## CCR (constant returns to scale)

- efficient (theta >= 1 - 1e-06): 8
- strongly efficient (all slacks <= 1e-06 rescaled): 8
- weakly efficient (theta = 1, positive slack): 0
- median theta: 0.5701

| statistic | value |
|---|---|
| n | 500 |
| mean | 0.5762 |
| std | 0.1656 |
| min | 0.1157 |
| p05 | 0.3177 |
| p25 | 0.4649 |
| median | 0.5701 |
| p75 | 0.6777 |
| p95 | 0.8732 |
| max | 1.0000 |
| count <0.5 | 162 |
| count 0.5-0.6 | 131 |
| count 0.6-0.7 | 96 |
| count 0.7-0.8 | 61 |
| count 0.8-0.9 | 35 |
| count 0.9-<1 | 7 |
| count =1 | 8 |

## BCC (variable returns to scale)

- efficient: 20
- median theta: 0.5960

| statistic | value |
|---|---|
| n | 500 |
| mean | 0.6141 |
| std | 0.1678 |
| min | 0.1166 |
| p05 | 0.3599 |
| p25 | 0.5061 |
| median | 0.5960 |
| p75 | 0.7189 |
| p95 | 0.9416 |
| max | 1.0000 |
| count <0.5 | 121 |
| count 0.5-0.6 | 134 |
| count 0.6-0.7 | 103 |
| count 0.7-0.8 | 73 |
| count 0.8-0.9 | 35 |
| count 0.9-<1 | 14 |
| count =1 | 20 |

## Scale efficiency and CCR vs BCC

- correlation CCR vs BCC: Pearson 0.9003, Spearman 0.9154
- median scale efficiency: 0.9763
- units with theta_CCR > theta_BCC + 1e-06 (must be 0): 0

| statistic | value |
|---|---|
| n | 500 |
| mean | 0.9403 |
| std | 0.0966 |
| min | 0.2321 |
| p05 | 0.7502 |
| p25 | 0.9332 |
| median | 0.9763 |
| p75 | 0.9922 |
| p95 | 0.9991 |
| max | 1.0000 |
| count <0.5 | 7 |
| count 0.5-0.6 | 1 |
| count 0.6-0.7 | 10 |
| count 0.7-0.8 | 15 |
| count 0.8-0.9 | 55 |
| count 0.9-<1 | 404 |
| count =1 | 8 |

## 8 highest super-efficiency scores (outlier review)

Super-efficiency > 1 is only computed for CCR-efficient units. Values far above the rest indicate a unit without close comparators; review before deciding whether to keep it.

| leaid | district_name | state | super_eff | theta_bcc | peer_count | n_peers |
|---|---|---|---|---|---|---|
| 1735770 | Selmaville CCSD 10 | IL | 2.5743 | 1.0000 | 29 | 1 |
| 0610290 | Cupertino Union | CA | 1.1954 | 1.0000 | 223 | 1 |
| 0640320 | Union Elementary | CA | 1.1702 | 1.0000 | 36 | 1 |
| 1603090 | SUGAR-SALEM JOINT DISTRICT | ID | 1.1072 | 1.0000 | 191 | 1 |
| 2628890 | Houghton-Portage Township School District | MI | 1.0817 | 1.0000 | 148 | 1 |
| 1808970 | Plainfield Community School Corp | IN | 1.0633 | 1.0000 | 380 | 1 |
| 4900360 | Granite District | UT | 1.0281 | 1.0000 | 10 | 1 |
| 0617040 | Hermosa Beach City Elementary | CA | 1.0217 | 1.0000 | 90 | 1 |

## 8 most frequent peers

peer_count = number of OTHER districts whose CCR phase-2 reference set includes this district (lambda > tolerance).

| leaid | district_name | state | peer_count | super_eff | theta_bcc |
|---|---|---|---|---|---|
| 1808970 | Plainfield Community School Corp | IN | 380 | 1.0633 | 1.0000 |
| 0610290 | Cupertino Union | CA | 223 | 1.1954 | 1.0000 |
| 1603090 | SUGAR-SALEM JOINT DISTRICT | ID | 191 | 1.1072 | 1.0000 |
| 2628890 | Houghton-Portage Township School District | MI | 148 | 1.0817 | 1.0000 |
| 0617040 | Hermosa Beach City Elementary | CA | 90 | 1.0217 | 1.0000 |
| 0640320 | Union Elementary | CA | 36 | 1.1702 | 1.0000 |
| 1735770 | Selmaville CCSD 10 | IL | 29 | 2.5743 | 1.0000 |
| 4900360 | Granite District | UT | 10 | 1.0281 | 1.0000 |

## Extreme input-output ratios (flagged, not removed)

ratio = (out_math + out_rla) / input. These districts are kept in the sample; they are listed so the decision can be made explicitly.

### Top 20 output per teacher FTE

| leaid | district_name | state | ratio | ratio_over_median | theta_ccr | efficient | top20_peer |
|---|---|---|---|---|---|---|---|
| 0610290 | Cupertino Union | CA | 440.9222 | 2.8045 | 1.0000 | yes | yes |
| 0640320 | Union Elementary | CA | 389.0800 | 2.4748 | 1.0000 | yes | yes |
| 0617040 | Hermosa Beach City Elementary | CA | 360.0006 | 2.2898 | 1.0000 | yes | yes |
| 0609030 | Clovis Unified | CA | 341.5280 | 2.1723 | 0.8565 | no | no |
| 0602160 | Alta Loma Elementary | CA | 338.9275 | 2.1558 | 0.8751 | no | no |
| 0626280 | Mountain View Whisman | CA | 321.6966 | 2.0462 | 0.7960 | no | no |
| 1808970 | Plainfield Community School Corp | IN | 311.7574 | 1.9830 | 1.0000 | yes | yes |
| 3904718 | Chardon Local | OH | 294.9820 | 1.8763 | 0.8442 | no | no |
| 2627960 | Pewamo-Westphalia Community Schools | MI | 290.5338 | 1.8480 | 0.8798 | no | no |
| 0627450 | Norris Elementary | CA | 290.4906 | 1.8477 | 0.8486 | no | no |
| 0635880 | Santee | CA | 286.8953 | 1.8248 | 0.6949 | no | no |
| 0631470 | Portola Valley Elementary | CA | 285.3506 | 1.8150 | 0.6863 | no | no |
| 3904734 | Forest Hills Local | OH | 281.2792 | 1.7891 | 0.8161 | no | no |
| 0633570 | Rosemead Elementary | CA | 278.1655 | 1.7693 | 0.6924 | no | no |
| 0404380 | Litchfield Elementary District (4281) | AZ | 277.4813 | 1.7649 | 0.9936 | no | no |
| 1805450 | Lake Central School Corporation | IN | 275.5803 | 1.7528 | 0.8766 | no | no |
| 1811460 | Tri-Creek School Corporation | IN | 275.0450 | 1.7494 | 0.8992 | no | no |
| 4218960 | Peters Township SD | PA | 274.8810 | 1.7484 | 0.7902 | no | no |
| 0609510 | Columbine Elementary | CA | 267.8713 | 1.7038 | 0.8531 | no | no |
| 3904498 | Wapakoneta City | OH | 264.0173 | 1.6793 | 0.8166 | no | no |

### Top 20 output per current-expenditure dollar

| leaid | district_name | state | ratio | ratio_over_median | theta_ccr | efficient | top20_peer |
|---|---|---|---|---|---|---|---|
| 1603090 | SUGAR-SALEM JOINT DISTRICT | ID | 0.001788 | 1.973475 | 1.000000 | yes | yes |
| 0404380 | Litchfield Elementary District (4281) | AZ | 0.001728 | 1.907734 | 0.993619 | no | no |
| 1808970 | Plainfield Community School Corp | IN | 0.001724 | 1.902810 | 1.000000 | yes | yes |
| 4832490 | NEW HOME ISD | TX | 0.001610 | 1.777590 | 0.925759 | no | no |
| 4812810 | CANYON ISD | TX | 0.001583 | 1.747182 | 0.888565 | no | no |
| 1920910 | North Polk Comm School District | IA | 0.001583 | 1.746973 | 0.925336 | no | no |
| 4618120 | Dell Rapids School District 49-3 | SD | 0.001536 | 1.695927 | 0.870313 | no | no |
| 0610290 | Cupertino Union | CA | 0.001533 | 1.692139 | 1.000000 | yes | yes |
| 1811460 | Tri-Creek School Corporation | IN | 0.001531 | 1.690237 | 0.899169 | no | no |
| 4600052 | Tea Area School District 41-5 | SD | 0.001531 | 1.690163 | 0.882586 | no | no |
| 4834440 | PEARLAND ISD | TX | 0.001529 | 1.688199 | 0.904040 | no | no |
| 2617910 | Hartland Consolidated Schools | MI | 0.001528 | 1.686116 | 0.964934 | no | no |
| 4814730 | COMAL ISD | TX | 0.001519 | 1.676130 | 0.866278 | no | no |
| 3904861 | Bethel Local | OH | 0.001507 | 1.663563 | 0.869668 | no | no |
| 4024930 | PRAGUE | OK | 0.001506 | 1.661829 | 0.876766 | no | no |
| 4002460 | ADAIR | OK | 0.001488 | 1.642365 | 0.844215 | no | no |
| 2628890 | Houghton-Portage Township School District | MI | 0.001482 | 1.635571 | 1.000000 | yes | yes |
| 0617040 | Hermosa Beach City Elementary | CA | 0.001470 | 1.622894 | 1.000000 | yes | yes |
| 1602550 | PARMA DISTRICT | ID | 0.001446 | 1.595561 | 0.838283 | no | no |
| 1729310 | Oakdale CCSD 1 | IL | 0.001428 | 1.575723 | 0.854401 | no | no |

## Flags

- 5 district(s) serve as peer for more than 10 % of the sample.
- max super-efficiency 2.57 (> 2): check that district's data.
- 2 district(s) report fewer than 5 teacher FTE.
