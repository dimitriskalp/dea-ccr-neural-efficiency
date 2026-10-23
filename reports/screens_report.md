# Report-only screens: temporal and enrollment consistency

Sample: 10,849 districts (current main dataset). Threshold: |robust z| > 5. Nothing here has been applied.

## Andover, KS (2003360)

| measure | value |
|---|---|
| V33 FY2018 / FY2019 / FY2020 | 8,707 / 8,825 / 9,185 |
| current expenditure per student FY2018 / FY2019 / FY2020 | 5,658 / 5,807 / 6,061 |
| SEDA grade 3-8 enrollment (cov_enrl_g38) | 4,721 |
| V33 / cov_enrl_g38 | 1.87 |
| students per teacher FTE | 25.8 |
| offers grades 9-12 | yes |
| enrollment-screen z (within group) | -3.16 |
| caught by temporal screen | no |
| caught by enrollment screen | no |

## 1. Temporal consistency (F-33 FY2018-FY2020)

- checkable (positive values in all three years): 10,840 of 10,849; cannot check: 9
- flagged, expenditure per student spike/dip: 20
- flagged, fall membership spike/dip: 17
- flagged, union: 33
- CCR-efficient units caught: none

- expenditure per student, FY18->19 log change: median +0.0379, robust SD 0.0443, so |z| > 5 means a change beyond about 25 %
- expenditure per student, FY19->20 log change: median +0.0230, robust SD 0.0478, so |z| > 5 means a change beyond about 27 %
- fall membership, FY18->19 log change: median -0.0053, robust SD 0.0308, so |z| > 5 means a change beyond about 17 %
- fall membership, FY19->20 log change: median -0.0022, robust SD 0.0285, so |z| > 5 means a change beyond about 15 %

### Flagged districts (33)

| leaid | district_name | state | v33_2018 | v33_2019 | v33_2020 | cur_per_stud_2018 | cur_per_stud_2019 | cur_per_stud_2020 | tc_reason |
|---|---|---|---|---|---|---|---|---|---|
| 0407630 | Seligman Unified District (4472) | AZ | 125.00 | 98.00 | 119.00 | 19,352.00 | 27,102.04 | 23,260.50 | fall membership dip in FY2019 (z -7.7 then +6.9) |
| 0409733 | Sedona-Oak Creek JUSD #9 (4467) | AZ | 948.00 | 509.00 | 786.00 | 10,495.78 | 20,899.80 | 10,362.60 | expenditure per student spike in FY2019 (z +14.7 then -15.1); fall membership dip in FY2019 (z -20.0 then +15.3) |
| 0617620 | Hornbrook Elementary | CA | 57.00 | 45.00 | 56.00 | 18,859.65 | 23,533.33 | 17,553.57 | fall membership dip in FY2019 (z -7.5 then +7.8) |
| 0624690 | Meridian Elementary | CA | 1,133.00 | 44.00 | 56.00 | 913.50 | 22,454.55 | 16,053.57 | expenditure per student spike in FY2019 (z +71.4 then -7.5); fall membership dip in FY2019 (z -105.2 then +8.5) |
| 0636570 | Shasta Union Elementary | CA | 156.00 | 114.00 | 139.00 | 9,743.59 | 13,973.68 | 11,546.76 | fall membership dip in FY2019 (z -10.0 then +7.0) |
| 0638070 | Stony Creek Joint Unified | CA | 85.00 | 62.00 | 76.00 | 23,294.12 | 31,129.03 | 24,618.42 | expenditure per student spike in FY2019 (z +5.7 then -5.4); fall membership dip in FY2019 (z -10.1 then +7.2) |
| 1700323 | Crescent Iroquois CUSD 249 | IL | 81.00 | 74.00 | 78.00 | 24,913.58 | 15,986.49 | 24,474.36 | expenditure per student dip in FY2019 (z -10.9 then +8.4) |
| 1712510 | Donovan CUSD 3 | IL | 287.00 | 284.00 | 280.00 | 15,317.07 | 12,130.28 | 16,517.86 | expenditure per student dip in FY2019 (z -6.1 then +6.0) |
| 1712840 | Dwight Common SD 232 | IL | 542.00 | 531.00 | 527.00 | 11,005.54 | 8,787.19 | 12,396.58 | expenditure per student dip in FY2019 (z -5.9 then +6.7) |
| 1713440 | Lindop SD 92 | IL | 419.00 | 439.00 | 411.00 | 15,095.47 | 31,000.00 | 16,452.55 | expenditure per student spike in FY2019 (z +15.4 then -13.7) |
| 1718270 | Harrisburg CUSD 3 | IL | 1,913.00 | 1,876.00 | 1,866.00 | 16,286.98 | 10,616.74 | 14,332.80 | expenditure per student dip in FY2019 (z -10.5 then +5.8) |
| 1729310 | Oakdale CCSD 1 | IL | 74.00 | 69.00 | 67.00 | 26,918.92 | 9,202.90 | 16,925.37 | expenditure per student dip in FY2019 (z -25.1 then +12.3) |
| 1734990 | Round Lake CUSD 116 | IL | 7,078.00 | 6,835.00 | 6,635.00 | 17,086.47 | 13,875.93 | 19,284.25 | expenditure per student dip in FY2019 (z -5.5 then +6.4) |
| 1738520 | Taft SD 90 | IL | 314.00 | 283.00 | 273.00 | 7,729.30 | 16,035.34 | 10,739.93 | expenditure per student spike in FY2019 (z +15.6 then -8.9) |
| 1739450 | Tri City CUSD 1 | IL | 558.00 | 571.00 | 547.00 | 14,324.37 | 9,739.05 | 13,435.10 | expenditure per student dip in FY2019 (z -9.6 then +6.2) |
| 1741600 | West Lincoln-Broadwell ESD 92 | IL | 235.00 | 195.00 | 225.00 | 14,012.77 | 16,164.10 | 14,453.33 | fall membership dip in FY2019 (z -5.9 then +5.1) |
| 1742990 | Shawnee CUSD 84 | IL | 327.00 | 311.00 | 291.00 | 16,122.32 | 27,646.30 | 13,054.98 | expenditure per student spike in FY2019 (z +11.3 then -16.2) |
| 2926550 | RIPLEY CO. R-III | MO | 86.00 | 73.00 | 98.00 | 13,500.00 | 14,863.01 | 9,826.53 | fall membership dip in FY2019 (z -5.1 then +10.4) |
| 3010950 | Olney-Bissell Elem | MT | 83.00 | 67.00 | 78.00 | 13,072.29 | 16,328.36 | 13,038.46 | fall membership dip in FY2019 (z -6.8 then +5.4) |
| 3018870 | Moore Elem | MT | 61.00 | 50.00 | 58.00 | 15,098.36 | 17,880.00 | 13,948.28 | fall membership dip in FY2019 (z -6.3 then +5.3) |
| 3304650 | Marlow School District | NH | 35.00 | 43.00 | 46.00 | 28,085.71 | 22,418.60 | 30,326.09 | expenditure per student dip in FY2019 (z -5.9 then +5.8) |
| 3410170 | Milford Borough School District | NJ | 72.00 | 88.00 | 61.00 | 32,291.67 | 28,011.36 | 31,983.61 | fall membership spike in FY2019 (z +6.7 then -12.8) |
| 3411940 | Oaklyn Public School District | NJ | 366.00 | 233.00 | 282.00 | 18,639.34 | 24,347.64 | 20,248.23 | fall membership dip in FY2019 (z -14.5 then +6.8) |
| 4003750 | BEAVER | OK | 347.00 | 312.00 | 302.00 | 10,665.71 | 21,278.85 | 13,013.25 | expenditure per student spike in FY2019 (z +14.7 then -10.8) |
| 4017040 | LANE | OK | 274.00 | 269.00 | 284.00 | 10,423.36 | 14,379.18 | 11,450.70 | expenditure per student spike in FY2019 (z +6.4 then -5.2) |
| 4816350 | DAWSON ISD | TX | 130.00 | 108.00 | 138.00 | 15,215.38 | 15,462.96 | 12,362.32 | fall membership dip in FY2019 (z -5.8 then +8.7) |
| 4827120 | LEGGETT ISD | TX | 179.00 | 167.00 | 196.00 | 10,916.20 | 18,952.10 | 10,872.45 | expenditure per student spike in FY2019 (z +11.6 then -12.1) |
| 4845990 | WILSON ISD | TX | 129.00 | 103.00 | 148.00 | 20,155.04 | 21,398.06 | 16,317.57 | fall membership dip in FY2019 (z -7.1 then +12.8) |
| 5303030 | Glenwood School District | WA | 69.00 | 90.00 | 69.00 | 29,217.39 | 22,844.44 | 29,942.03 | expenditure per student dip in FY2019 (z -6.4 then +5.2); fall membership spike in FY2019 (z +8.8 then -9.3) |
| 5304290 | Lamont School District | WA | 40.00 | 34.00 | 40.00 | 21,425.00 | 25,323.53 | 19,800.00 | fall membership dip in FY2019 (z -5.1 then +5.8) |
| 5307470 | Rochester School District | WA | 2,326.00 | 1,848.00 | 2,238.00 | 12,669.82 | 17,102.27 | 13,918.23 | fall membership dip in FY2019 (z -7.3 then +6.8) |
| 5500840 | Barneveld School District | WI | 450.00 | 438.00 | 452.00 | 13,253.33 | 39,785.39 | 20,769.91 | expenditure per student spike in FY2019 (z +23.9 then -14.1) |
| 5514820 | Thorp School District | WI | 614.00 | 602.00 | 614.00 | 14,172.64 | 18,617.94 | 12,612.38 | expenditure per student spike in FY2019 (z +5.3 then -8.6) |

## 2. Enrollment consistency (V33 vs SEDA grade 3-8 enrollment)

| group | n | median ratio | robust SD (log) | |z| <= 5 keeps ratios in | flagged high | flagged low |
|---|---|---|---|---|---|---|
| K-8 only | 1,703 | 1.55 | 0.077 | [1.05, 2.27] | 17 | 1 |
| offers 9-12 | 9,146 | 2.21 | 0.053 | [1.69, 2.89] | 88 | 79 |

- cannot check (missing cov_enrl_g38): 2
- flagged: 185
- CCR-efficient units caught: none

### Flagged districts (185)

| leaid | district_name | state | group | students | cov_enrl_g38 | enrl_ratio | z_enrl | stud_per_teacher | ec_reason |
|---|---|---|---|---|---|---|---|---|---|
| 0628950 | Oro Grande | CA | offers 9-12 | 2,401.00 | 55.00 | 43.65 | 55.79 | 22.19 | V33 / grade 3-8 enrollment high (z=55.8, offers 9-12) |
| 2201170 | Orleans Parish | LA | offers 9-12 | 4,642.00 | 22,772.00 | 0.20 | -44.63 | 17.63 | V33 / grade 3-8 enrollment low (z=-44.6, offers 9-12) |
| 5307020 | Quillayute Valley School District | WA | offers 9-12 | 3,283.00 | 482.00 | 6.81 | 21.03 | 20.76 | V33 / grade 3-8 enrollment high (z=21.0, offers 9-12) |
| 0630210 | Perris Union High | CA | offers 9-12 | 10,893.00 | 1,717.00 | 6.34 | 19.70 | 25.99 | V33 / grade 3-8 enrollment high (z=19.7, offers 9-12) |
| 2930870 | MARIES CO. R-I | MO | offers 9-12 | 479.00 | 93.00 | 5.15 | 15.80 | 11.80 | V33 / grade 3-8 enrollment high (z=15.8, offers 9-12) |
| 1706600 | Scott-Morgan CUSD 2 | IL | offers 9-12 | 228.00 | 46.00 | 4.96 | 15.08 | 10.62 | V33 / grade 3-8 enrollment high (z=15.1, offers 9-12) |
| 2308160 | Medway Public Schools | ME | offers 9-12 | 113.00 | 113.00 | 1.00 | -14.87 | 9.26 | V33 / grade 3-8 enrollment low (z=-14.9, offers 9-12) |
| 4212600 | Juniata County SD | PA | offers 9-12 | 2,720.00 | 568.00 | 4.79 | 14.44 | 13.64 | V33 / grade 3-8 enrollment high (z=14.4, offers 9-12) |
| 2922500 | NIANGUA R-V | MO | offers 9-12 | 338.00 | 72.00 | 4.69 | 14.06 | 11.08 | V33 / grade 3-8 enrollment high (z=14.1, offers 9-12) |
| 1910690 | Eldora-New Providence Comm School District | IA | offers 9-12 | 623.00 | 133.00 | 4.68 | 14.02 | 12.99 | V33 / grade 3-8 enrollment high (z=14.0, offers 9-12) |
| 4834410 | PAWNEE ISD | TX | K-8 only | 318.00 | 71.00 | 4.48 | 13.77 | 16.07 | V33 / grade 3-8 enrollment high (z=13.8, K-8 only) |
| 2008940 | Centre | KS | offers 9-12 | 533.00 | 121.00 | 4.40 | 12.87 | 22.00 | V33 / grade 3-8 enrollment high (z=12.9, offers 9-12) |
| 0691063 | Del Norte County Office of Education | CA | offers 9-12 | 364.00 | 83.00 | 4.39 | 12.79 | 20.45 | V33 / grade 3-8 enrollment high (z=12.8, offers 9-12) |
| 2605430 | Berrien Springs Public Schools | MI | offers 9-12 | 3,827.00 | 890.00 | 4.30 | 12.42 | 23.48 | V33 / grade 3-8 enrollment high (z=12.4, offers 9-12) |
| 2008700 | Lewis | KS | offers 9-12 | 132.00 | 31.00 | 4.26 | 12.24 | 14.67 | V33 / grade 3-8 enrollment high (z=12.2, offers 9-12) |
| 2923640 | MEADOW HEIGHTS R-II | MO | offers 9-12 | 543.00 | 128.00 | 4.24 | 12.17 | 15.06 | V33 / grade 3-8 enrollment high (z=12.2, offers 9-12) |
| 1908130 | Corning Comm School District | IA | offers 9-12 | 407.00 | 96.00 | 4.24 | 12.16 | 10.67 | V33 / grade 3-8 enrollment high (z=12.2, offers 9-12) |
| 0803630 | Edison Joint District No. 54 of the counties of El Paso and | CO | offers 9-12 | 232.00 | 55.00 | 4.22 | 12.06 | 16.16 | V33 / grade 3-8 enrollment high (z=12.1, offers 9-12) |
| 2502580 | Berlin-Boylston | MA | offers 9-12 | 583.00 | 500.00 | 1.17 | -12.00 | 12.21 | V33 / grade 3-8 enrollment low (z=-12.0, offers 9-12) |
| 3401440 | Belvidere School District | NJ | offers 9-12 | 679.00 | 163.00 | 4.17 | 11.83 | 10.15 | V33 / grade 3-8 enrollment high (z=11.8, offers 9-12) |
| 1912230 | Galva-Holstein Comm School District | IA | offers 9-12 | 461.00 | 112.00 | 4.12 | 11.60 | 11.91 | V33 / grade 3-8 enrollment high (z=11.6, offers 9-12) |
| 4006930 | CAVE SPRINGS | OK | offers 9-12 | 209.00 | 51.00 | 4.10 | 11.52 | 13.22 | V33 / grade 3-8 enrollment high (z=11.5, offers 9-12) |
| 3407350 | Hoboken Public School District | NJ | offers 9-12 | 2,858.00 | 720.00 | 3.97 | 10.93 | 13.08 | V33 / grade 3-8 enrollment high (z=10.9, offers 9-12) |
| 2910200 | COUCH R-I | MO | offers 9-12 | 206.00 | 52.00 | 3.96 | 10.89 | 10.52 | V33 / grade 3-8 enrollment high (z=10.9, offers 9-12) |
| 3409420 | Manasquan School District | NJ | offers 9-12 | 1,548.00 | 391.00 | 3.96 | 10.88 | 11.14 | V33 / grade 3-8 enrollment high (z=10.9, offers 9-12) |
| 1913320 | Guthrie Center Comm School District | IA | offers 9-12 | 532.00 | 144.00 | 3.69 | 9.58 | 10.62 | V33 / grade 3-8 enrollment high (z=9.6, offers 9-12) |
| 1929280 | Villisca Comm School District | IA | offers 9-12 | 319.00 | 240.00 | 1.33 | -9.55 | 13.45 | V33 / grade 3-8 enrollment low (z=-9.5, offers 9-12) |
| 4828830 | MALTA ISD | TX | K-8 only | 229.00 | 71.00 | 3.23 | 9.52 | 14.48 | V33 / grade 3-8 enrollment high (z=9.5, K-8 only) |
| 2610080 | Clintondale Community Schools | MI | offers 9-12 | 2,722.00 | 740.00 | 3.68 | 9.50 | 24.67 | V33 / grade 3-8 enrollment high (z=9.5, offers 9-12) |
| 0627840 | Oak Grove Union Elementary | CA | offers 9-12 | 853.00 | 635.00 | 1.34 | -9.35 | 22.60 | V33 / grade 3-8 enrollment low (z=-9.3, offers 9-12) |
| 1740890 | Warsaw CUSD 316 | IL | offers 9-12 | 402.00 | 111.00 | 3.62 | 9.21 | 12.57 | V33 / grade 3-8 enrollment high (z=9.2, offers 9-12) |
| 0401810 | Cedar Unified District (4395) | AZ | offers 9-12 | 134.00 | 99.00 | 1.35 | -9.21 | 12.76 | V33 / grade 3-8 enrollment low (z=-9.2, offers 9-12) |
| 0642900 | Winship-Robbins | CA | offers 9-12 | 118.00 | 87.00 | 1.36 | -9.17 | 14.75 | V33 / grade 3-8 enrollment low (z=-9.2, offers 9-12) |
| 2311910 | MSAD 76 | ME | offers 9-12 | 34.00 | 25.00 | 1.36 | -9.12 | 7.23 | V33 / grade 3-8 enrollment low (z=-9.1, offers 9-12) |
| 0607260 | Camptonville Elementary | CA | offers 9-12 | 48.00 | 35.00 | 1.37 | -8.96 | 14.12 | V33 / grade 3-8 enrollment low (z=-9.0, offers 9-12) |
| 4620100 | Eagle Butte School District 20-1 | SD | offers 9-12 | 347.00 | 252.00 | 1.38 | -8.88 | 8.26 | V33 / grade 3-8 enrollment low (z=-8.9, offers 9-12) |
| 0602070 | Alpine County Unified | CA | offers 9-12 | 79.00 | 57.00 | 1.39 | -8.76 | 7.18 | V33 / grade 3-8 enrollment low (z=-8.8, offers 9-12) |
| 1920830 | North Kossuth Comm School District | IA | offers 9-12 | 314.00 | 226.00 | 1.39 | -8.72 | 10.58 | V33 / grade 3-8 enrollment low (z=-8.7, offers 9-12) |
| 1925380 | Schaller-Crestland Comm School District | IA | offers 9-12 | 396.00 | 284.00 | 1.39 | -8.65 | 14.42 | V33 / grade 3-8 enrollment low (z=-8.6, offers 9-12) |
| 2011970 | Stafford | KS | offers 9-12 | 274.00 | 78.00 | 3.51 | 8.64 | 11.32 | V33 / grade 3-8 enrollment high (z=8.6, offers 9-12) |
| 3415090 | Somerville Public School District | NJ | offers 9-12 | 2,398.00 | 683.00 | 3.51 | 8.63 | 11.71 | V33 / grade 3-8 enrollment high (z=8.6, offers 9-12) |
| 3411970 | Ocean City School District | NJ | offers 9-12 | 2,123.00 | 606.00 | 3.50 | 8.59 | 11.67 | V33 / grade 3-8 enrollment high (z=8.6, offers 9-12) |
| 0631860 | Ravenswood City Elementary | CA | offers 9-12 | 2,391.00 | 1,703.00 | 1.40 | -8.52 | 22.18 | V33 / grade 3-8 enrollment low (z=-8.5, offers 9-12) |
| 1914310 | Hubbard-Radcliffe Comm School District | IA | offers 9-12 | 404.00 | 287.00 | 1.41 | -8.47 | 13.50 | V33 / grade 3-8 enrollment low (z=-8.5, offers 9-12) |
| 1924120 | Remsen-Union Comm School District | IA | offers 9-12 | 337.00 | 239.00 | 1.41 | -8.44 | 9.93 | V33 / grade 3-8 enrollment low (z=-8.4, offers 9-12) |
| 0619140 | Julian Union Elementary | CA | offers 9-12 | 282.00 | 199.00 | 1.42 | -8.35 | 19.38 | V33 / grade 3-8 enrollment low (z=-8.3, offers 9-12) |
| 3414550 | Salem City School District | NJ | offers 9-12 | 1,272.00 | 369.00 | 3.45 | 8.29 | 10.97 | V33 / grade 3-8 enrollment high (z=8.3, offers 9-12) |
| 1903090 | Adair-Casey Comm School District | IA | offers 9-12 | 258.00 | 181.00 | 1.43 | -8.24 | 11.17 | V33 / grade 3-8 enrollment low (z=-8.2, offers 9-12) |
| 0402740 | Mary C O'Brien Accommodation District (4435) | AZ | offers 9-12 | 220.00 | 64.00 | 3.44 | 8.23 | 11.58 | V33 / grade 3-8 enrollment high (z=8.2, offers 9-12) |
| 0606750 | Byron Union Elementary | CA | offers 9-12 | 1,475.00 | 1,034.00 | 1.43 | -8.22 | 24.70 | V33 / grade 3-8 enrollment low (z=-8.2, offers 9-12) |
| 0803030 | Plateau Valley School District No. 50 in the county of Mesa | CO | offers 9-12 | 442.00 | 129.00 | 3.43 | 8.17 | 13.93 | V33 / grade 3-8 enrollment high (z=8.2, offers 9-12) |
| 4027000 | SAVANNA | OK | offers 9-12 | 403.00 | 118.00 | 3.42 | 8.11 | 16.78 | V33 / grade 3-8 enrollment high (z=8.1, offers 9-12) |
| 0691023 | Nevada County Office of Education | CA | offers 9-12 | 1,444.00 | 423.00 | 3.41 | 8.10 | 20.25 | V33 / grade 3-8 enrollment high (z=8.1, offers 9-12) |
| 0601428 | Wiseburn Unified | CA | offers 9-12 | 2,525.00 | 1,757.00 | 1.44 | -8.08 | 25.20 | V33 / grade 3-8 enrollment low (z=-8.1, offers 9-12) |
| 2314814 | Cherryfield Public Schools | ME | offers 9-12 | 115.00 | 80.00 | 1.44 | -8.08 | 10.65 | V33 / grade 3-8 enrollment low (z=-8.1, offers 9-12) |
| 2906480 | CALHOUN R-VIII | MO | offers 9-12 | 143.00 | 42.00 | 3.40 | 8.05 | 9.29 | V33 / grade 3-8 enrollment high (z=8.1, offers 9-12) |
| 0619890 | Kit Carson Union Elementary | CA | offers 9-12 | 399.00 | 277.00 | 1.44 | -8.04 | 21.14 | V33 / grade 3-8 enrollment low (z=-8.0, offers 9-12) |
| 0622560 | Loomis Union Elementary | CA | offers 9-12 | 2,911.00 | 2,008.00 | 1.45 | -7.92 | 22.90 | V33 / grade 3-8 enrollment low (z=-7.9, offers 9-12) |
| 2007590 | Humboldt | KS | offers 9-12 | 955.00 | 283.00 | 3.37 | 7.89 | 24.36 | V33 / grade 3-8 enrollment high (z=7.9, offers 9-12) |
| 2000020 | Western Plains | KS | offers 9-12 | 118.00 | 35.00 | 3.37 | 7.87 | 7.20 | V33 / grade 3-8 enrollment high (z=7.9, offers 9-12) |
| 0606270 | Buckeye Union Elementary | CA | offers 9-12 | 4,706.00 | 3,234.00 | 1.46 | -7.85 | 23.80 | V33 / grade 3-8 enrollment low (z=-7.9, offers 9-12) |
| 1999019 | Southeast Webster Grand Comm School District | IA | offers 9-12 | 576.00 | 395.00 | 1.46 | -7.81 | 13.36 | V33 / grade 3-8 enrollment low (z=-7.8, offers 9-12) |
| 0605280 | Blochman Union Elementary | CA | offers 9-12 | 212.00 | 145.00 | 1.46 | -7.76 | 23.56 | V33 / grade 3-8 enrollment low (z=-7.8, offers 9-12) |
| 2635970 | Westwood Heights Schools | MI | offers 9-12 | 1,510.00 | 451.00 | 3.35 | 7.74 | 21.79 | V33 / grade 3-8 enrollment high (z=7.7, offers 9-12) |
| 0615600 | Gorman Joint | CA | offers 9-12 | 82.00 | 56.00 | 1.46 | -7.73 | 23.43 | V33 / grade 3-8 enrollment low (z=-7.7, offers 9-12) |
| 2314824 | Northport Public Schools | ME | offers 9-12 | 136.00 | 92.00 | 1.48 | -7.56 | 9.65 | V33 / grade 3-8 enrollment low (z=-7.6, offers 9-12) |
| 0628530 | Orange Center | CA | offers 9-12 | 311.00 | 209.00 | 1.49 | -7.43 | 18.29 | V33 / grade 3-8 enrollment low (z=-7.4, offers 9-12) |
| 0621420 | Lennox | CA | offers 9-12 | 5,327.00 | 3,577.00 | 1.49 | -7.42 | 22.37 | V33 / grade 3-8 enrollment low (z=-7.4, offers 9-12) |
| 0405460 | Nadaburg Unified School District (4252) | AZ | offers 9-12 | 797.00 | 535.00 | 1.49 | -7.41 | 20.18 | V33 / grade 3-8 enrollment low (z=-7.4, offers 9-12) |
| 2306260 | Hancock Public Schools | ME | offers 9-12 | 231.00 | 155.00 | 1.49 | -7.40 | 11.27 | V33 / grade 3-8 enrollment low (z=-7.4, offers 9-12) |
| 0621210 | Lawndale Elementary | CA | offers 9-12 | 5,291.00 | 3,543.00 | 1.49 | -7.37 | 23.40 | V33 / grade 3-8 enrollment low (z=-7.4, offers 9-12) |
| 4612300 | Chester Area School District 39-1 | SD | offers 9-12 | 570.00 | 174.00 | 3.28 | 7.33 | 15.58 | V33 / grade 3-8 enrollment high (z=7.3, offers 9-12) |
| 0627120 | Newcastle Elementary | CA | offers 9-12 | 461.00 | 308.00 | 1.50 | -7.32 | 23.05 | V33 / grade 3-8 enrollment low (z=-7.3, offers 9-12) |
| 1700102 | Brussels CUSD 42 | IL | offers 9-12 | 121.00 | 37.00 | 3.27 | 7.30 | 8.64 | V33 / grade 3-8 enrollment high (z=7.3, offers 9-12) |
| 0616320 | Guerneville Elementary | CA | offers 9-12 | 267.00 | 178.00 | 1.50 | -7.28 | 24.72 | V33 / grade 3-8 enrollment low (z=-7.3, offers 9-12) |
| 4028710 | STILWELL | OK | offers 9-12 | 1,308.00 | 401.00 | 3.26 | 7.25 | 14.39 | V33 / grade 3-8 enrollment high (z=7.3, offers 9-12) |
| 0619440 | Keppel Union Elementary | CA | offers 9-12 | 2,630.00 | 1,748.00 | 1.50 | -7.23 | 25.66 | V33 / grade 3-8 enrollment low (z=-7.2, offers 9-12) |
| 0618870 | Jefferson Elementary | CA | offers 9-12 | 5,986.00 | 3,977.00 | 1.51 | -7.22 | 21.32 | V33 / grade 3-8 enrollment low (z=-7.2, offers 9-12) |
| 0601710 | Adelanto Elementary | CA | offers 9-12 | 8,234.00 | 5,469.00 | 1.51 | -7.21 | 25.34 | V33 / grade 3-8 enrollment low (z=-7.2, offers 9-12) |
| 2314820 | St George Public Schools | ME | offers 9-12 | 208.00 | 138.00 | 1.51 | -7.19 | 10.61 | V33 / grade 3-8 enrollment low (z=-7.2, offers 9-12) |
| 0605730 | Bradley Union Elementary | CA | offers 9-12 | 74.00 | 49.00 | 1.51 | -7.16 | 13.45 | V33 / grade 3-8 enrollment low (z=-7.2, offers 9-12) |
| 4011760 | FLOWER MOUND | OK | K-8 only | 327.00 | 122.00 | 2.68 | 7.13 | 18.81 | V33 / grade 3-8 enrollment high (z=7.1, K-8 only) |
| 2006720 | Kiowa County | KS | offers 9-12 | 469.00 | 145.00 | 3.23 | 7.09 | 14.91 | V33 / grade 3-8 enrollment high (z=7.1, offers 9-12) |
| 2306180 | Greenbush Public Schools | ME | offers 9-12 | 147.00 | 97.00 | 1.52 | -7.09 | 10.14 | V33 / grade 3-8 enrollment low (z=-7.1, offers 9-12) |
| 2309990 | Princeton Public Schools | ME | offers 9-12 | 141.00 | 93.00 | 1.52 | -7.08 | 10.85 | V33 / grade 3-8 enrollment low (z=-7.1, offers 9-12) |
| 4831920 | MULLIN ISD | TX | offers 9-12 | 340.00 | 106.00 | 3.21 | 6.94 | 9.51 | V33 / grade 3-8 enrollment high (z=6.9, offers 9-12) |
| 3412960 | Phillipsburg School District | NJ | offers 9-12 | 3,937.00 | 1,230.00 | 3.20 | 6.90 | 11.68 | V33 / grade 3-8 enrollment high (z=6.9, offers 9-12) |
| 3812030 | MAPLETON 7 | ND | K-8 only | 163.00 | 62.00 | 2.63 | 6.88 | 13.25 | V33 / grade 3-8 enrollment high (z=6.9, K-8 only) |
| 0610710 | Dehesa Elementary | CA | offers 9-12 | 138.00 | 90.00 | 1.53 | -6.87 | 15.33 | V33 / grade 3-8 enrollment low (z=-6.9, offers 9-12) |
| 0629580 | Palmdale Elementary | CA | offers 9-12 | 19,085.00 | 12,428.00 | 1.54 | -6.84 | 24.32 | V33 / grade 3-8 enrollment low (z=-6.8, offers 9-12) |
| 0616620 | Harmony Union Elementary | CA | offers 9-12 | 249.00 | 162.00 | 1.54 | -6.83 | 21.65 | V33 / grade 3-8 enrollment low (z=-6.8, offers 9-12) |
| 0624540 | Menifee Union Elementary | CA | offers 9-12 | 10,393.00 | 6,757.00 | 1.54 | -6.81 | 24.12 | V33 / grade 3-8 enrollment low (z=-6.8, offers 9-12) |
| 2614280 | Ferndale Public Schools | MI | offers 9-12 | 3,092.00 | 976.00 | 3.17 | 6.71 | 19.08 | V33 / grade 3-8 enrollment high (z=6.7, offers 9-12) |
| 2305360 | Eastport Public Schools | ME | offers 9-12 | 171.00 | 54.00 | 3.17 | 6.70 | 9.29 | V33 / grade 3-8 enrollment high (z=6.7, offers 9-12) |
| 0642210 | Westside Elementary | CA | offers 9-12 | 188.00 | 121.00 | 1.55 | -6.62 | 23.50 | V33 / grade 3-8 enrollment low (z=-6.6, offers 9-12) |
| 1701390 | Flanagan-Cornell Dist 74 | IL | offers 9-12 | 350.00 | 111.00 | 3.15 | 6.62 | 10.61 | V33 / grade 3-8 enrollment high (z=6.6, offers 9-12) |
| 2312100 | Education in Unorganized Terr | ME | offers 9-12 | 189.00 | 60.00 | 3.15 | 6.60 | 14.77 | V33 / grade 3-8 enrollment high (z=6.6, offers 9-12) |
| 1925410 | Schleswig Comm School District | IA | offers 9-12 | 193.00 | 124.00 | 1.56 | -6.59 | 12.71 | V33 / grade 3-8 enrollment low (z=-6.6, offers 9-12) |
| 2314010 | Woodland Public Schools | ME | offers 9-12 | 156.00 | 100.00 | 1.56 | -6.55 | 9.63 | V33 / grade 3-8 enrollment low (z=-6.5, offers 9-12) |
| 0624720 | Mesa Union Elementary | CA | offers 9-12 | 615.00 | 394.00 | 1.56 | -6.54 | 22.95 | V33 / grade 3-8 enrollment low (z=-6.5, offers 9-12) |
| 1734870 | Rossville-Alvin CUSD 7 | IL | offers 9-12 | 300.00 | 192.00 | 1.56 | -6.52 | 16.67 | V33 / grade 3-8 enrollment low (z=-6.5, offers 9-12) |
| 2513321 | Farmington River Reg | MA | K-8 only | 115.00 | 45.00 | 2.56 | 6.51 | 8.98 | V33 / grade 3-8 enrollment high (z=6.5, K-8 only) |
| 3416560 | Upper Freehold Regional School District | NJ | offers 9-12 | 2,257.00 | 721.00 | 3.13 | 6.48 | 11.87 | V33 / grade 3-8 enrollment high (z=6.5, offers 9-12) |
| 0613170 | Evergreen Union | CA | offers 9-12 | 1,217.00 | 777.00 | 1.57 | -6.47 | 21.35 | V33 / grade 3-8 enrollment low (z=-6.5, offers 9-12) |
| 2012900 | Weskan | KS | offers 9-12 | 100.00 | 32.00 | 3.12 | 6.45 | 5.46 | V33 / grade 3-8 enrollment high (z=6.5, offers 9-12) |
| 2300067 | Machiasport Public Schools | ME | offers 9-12 | 75.00 | 24.00 | 3.12 | 6.45 | 12.71 | V33 / grade 3-8 enrollment high (z=6.5, offers 9-12) |
| 3174580 | NORTHWEST PUBLIC SCHOOLS | NE | offers 9-12 | 1,546.00 | 495.00 | 3.12 | 6.44 | 14.57 | V33 / grade 3-8 enrollment high (z=6.4, offers 9-12) |
| 3411400 | NEWTON PUBLIC SCHOOL DISTRICT | NJ | offers 9-12 | 1,546.00 | 495.00 | 3.12 | 6.44 | 11.12 | V33 / grade 3-8 enrollment high (z=6.4, offers 9-12) |
| 3400930 | Asbury Park School District | NJ | offers 9-12 | 2,078.00 | 667.00 | 3.12 | 6.39 | 10.11 | V33 / grade 3-8 enrollment high (z=6.4, offers 9-12) |
| 4400510 | Jamestown | RI | offers 9-12 | 507.00 | 322.00 | 1.57 | -6.38 | 11.71 | V33 / grade 3-8 enrollment low (z=-6.4, offers 9-12) |
| 2913440 | PLEASANT VIEW R-VI | MO | K-8 only | 139.00 | 55.00 | 2.53 | 6.36 | 10.15 | V33 / grade 3-8 enrollment high (z=6.4, K-8 only) |
| 4205860 | Chester-Upland SD | PA | offers 9-12 | 2,942.00 | 946.00 | 3.11 | 6.36 | 14.21 | V33 / grade 3-8 enrollment high (z=6.4, offers 9-12) |
| 2308250 | Milford Public Schools | ME | offers 9-12 | 309.00 | 196.00 | 1.58 | -6.35 | 11.62 | V33 / grade 3-8 enrollment low (z=-6.4, offers 9-12) |
| 4702400 | Lenoir City | TN | offers 9-12 | 2,340.00 | 754.00 | 3.10 | 6.32 | 17.92 | V33 / grade 3-8 enrollment high (z=6.3, offers 9-12) |
| 2009930 | Ness City | KS | offers 9-12 | 307.00 | 99.00 | 3.10 | 6.31 | 10.74 | V33 / grade 3-8 enrollment high (z=6.3, offers 9-12) |
| 0612810 | Enterprise Elementary | CA | offers 9-12 | 3,745.00 | 2,367.00 | 1.58 | -6.29 | 24.09 | V33 / grade 3-8 enrollment low (z=-6.3, offers 9-12) |
| 3418090 | Woodbine School District | NJ | K-8 only | 239.00 | 96.00 | 2.49 | 6.17 | 10.13 | V33 / grade 3-8 enrollment high (z=6.2, K-8 only) |
| 2314776 | RSU 02 | ME | offers 9-12 | 2,071.00 | 674.00 | 3.07 | 6.13 | 11.33 | V33 / grade 3-8 enrollment high (z=6.1, offers 9-12) |
| 5308490 | Steptoe School District | WA | K-8 only | 67.00 | 27.00 | 2.48 | 6.13 | 18.21 | V33 / grade 3-8 enrollment high (z=6.1, K-8 only) |
| 2310980 | RSU 87/MSAD 23 | ME | offers 9-12 | 629.00 | 394.00 | 1.60 | -6.12 | 11.87 | V33 / grade 3-8 enrollment low (z=-6.1, offers 9-12) |
| 0802940 | Cheyenne Mountain School District No. 12 in the county of E | CO | offers 9-12 | 5,274.00 | 1,719.00 | 3.07 | 6.11 | 14.57 | V33 / grade 3-8 enrollment high (z=6.1, offers 9-12) |
| 3817670 | STARKWEATHER 44 | ND | offers 9-12 | 56.00 | 35.00 | 1.60 | -6.08 | 6.06 | V33 / grade 3-8 enrollment low (z=-6.1, offers 9-12) |
| 3406330 | HADDON HEIGHTS School District | NJ | offers 9-12 | 1,481.00 | 484.00 | 3.06 | 6.06 | 11.30 | V33 / grade 3-8 enrollment high (z=6.1, offers 9-12) |
| 0609450 | Columbia Elementary | CA | offers 9-12 | 769.00 | 480.00 | 1.60 | -6.05 | 19.49 | V33 / grade 3-8 enrollment low (z=-6.1, offers 9-12) |
| 0805550 | Mapleton School District No. 1 in the county of Adams & St | CO | offers 9-12 | 8,934.00 | 2,923.00 | 3.06 | 6.04 | 19.77 | V33 / grade 3-8 enrollment high (z=6.0, offers 9-12) |
| 0627750 | Nuestro Elementary | CA | offers 9-12 | 170.00 | 106.00 | 1.60 | -6.03 | 18.89 | V33 / grade 3-8 enrollment low (z=-6.0, offers 9-12) |
| 0640230 | Twin Hills Union Elementary | CA | offers 9-12 | 1,207.00 | 752.00 | 1.61 | -6.02 | 21.06 | V33 / grade 3-8 enrollment low (z=-6.0, offers 9-12) |
| 1301050 | Chattahoochee County | GA | offers 9-12 | 918.00 | 301.00 | 3.05 | 5.99 | 16.08 | V33 / grade 3-8 enrollment high (z=6.0, offers 9-12) |
| 2905700 | BRADLEYVILLE R-I | MO | offers 9-12 | 228.00 | 75.00 | 3.04 | 5.93 | 12.12 | V33 / grade 3-8 enrollment high (z=5.9, offers 9-12) |
| 0603180 | Armona Union Elementary | CA | offers 9-12 | 1,137.00 | 704.00 | 1.62 | -5.90 | 22.51 | V33 / grade 3-8 enrollment low (z=-5.9, offers 9-12) |
| 3401950 | Boonton Town School District | NJ | offers 9-12 | 1,413.00 | 466.00 | 3.03 | 5.89 | 11.11 | V33 / grade 3-8 enrollment high (z=5.9, offers 9-12) |
| 4823700 | HUBBARD ISD | TX | K-8 only | 107.00 | 44.00 | 2.43 | 5.87 | 11.35 | V33 / grade 3-8 enrollment high (z=5.9, K-8 only) |
| 3172910 | LITCHFIELD PUBLIC SCHOOLS | NE | offers 9-12 | 121.00 | 40.00 | 3.02 | 5.84 | 6.27 | V33 / grade 3-8 enrollment high (z=5.8, offers 9-12) |
| 0903515 | REGIONAL SCHOOL DISTRICT 06 | CT | offers 9-12 | 909.00 | 301.00 | 3.02 | 5.81 | 14.89 | V33 / grade 3-8 enrollment high (z=5.8, offers 9-12) |
| 2008910 | Logan | KS | offers 9-12 | 157.00 | 52.00 | 3.02 | 5.81 | 6.54 | V33 / grade 3-8 enrollment high (z=5.8, offers 9-12) |
| 3402430 | Burlington City Public School District | NJ | offers 9-12 | 1,659.00 | 550.00 | 3.02 | 5.79 | 9.96 | V33 / grade 3-8 enrollment high (z=5.8, offers 9-12) |
| 0601427 | Penn Valley Union Elementary | CA | offers 9-12 | 591.00 | 363.00 | 1.63 | -5.75 | 24.62 | V33 / grade 3-8 enrollment low (z=-5.7, offers 9-12) |
| 3302670 | Dresden School District | NH | offers 9-12 | 1,125.00 | 374.00 | 3.01 | 5.74 | 11.19 | V33 / grade 3-8 enrollment high (z=5.7, offers 9-12) |
| 0637350 | South Bay Union Elementary | CA | offers 9-12 | 472.00 | 289.00 | 1.63 | -5.69 | 20.72 | V33 / grade 3-8 enrollment low (z=-5.7, offers 9-12) |
| 2712210 | FLOODWOOD PUBLIC SCHOOL DISTRICT | MN | offers 9-12 | 222.00 | 74.00 | 3.00 | 5.69 | 11.11 | V33 / grade 3-8 enrollment high (z=5.7, offers 9-12) |
| 2927090 | SALEM R-80 | MO | offers 9-12 | 1,404.00 | 468.00 | 3.00 | 5.69 | 13.36 | V33 / grade 3-8 enrollment high (z=5.7, offers 9-12) |
| 5301890 | Curlew School District | WA | offers 9-12 | 231.00 | 77.00 | 3.00 | 5.69 | 15.91 | V33 / grade 3-8 enrollment high (z=5.7, offers 9-12) |
| 3401290 | Beach Haven School District | NJ | K-8 only | 55.00 | 23.00 | 2.39 | 5.65 | 4.58 | V33 / grade 3-8 enrollment high (z=5.6, K-8 only) |
| 0621990 | Live Oak Elementary | CA | offers 9-12 | 1,968.00 | 1,202.00 | 1.64 | -5.64 | 20.75 | V33 / grade 3-8 enrollment low (z=-5.6, offers 9-12) |
| 5304290 | Lamont School District | WA | K-8 only | 34.00 | 34.00 | 1.00 | -5.64 | 9.69 | V33 / grade 3-8 enrollment low (z=-5.6, K-8 only) |
| 0632040 | Redding Elementary | CA | offers 9-12 | 3,158.00 | 1,928.00 | 1.64 | -5.64 | 22.74 | V33 / grade 3-8 enrollment low (z=-5.6, offers 9-12) |
| 0628710 | Orcutt Union Elementary | CA | offers 9-12 | 5,181.00 | 3,162.00 | 1.64 | -5.63 | 24.82 | V33 / grade 3-8 enrollment low (z=-5.6, offers 9-12) |
| 1730780 | Paris CUSD 4 | IL | offers 9-12 | 487.00 | 296.00 | 1.65 | -5.55 | 17.39 | V33 / grade 3-8 enrollment low (z=-5.6, offers 9-12) |
| 3411160 | Neptune Township School District | NJ | offers 9-12 | 4,063.00 | 1,366.00 | 2.97 | 5.53 | 10.92 | V33 / grade 3-8 enrollment high (z=5.5, offers 9-12) |
| 5604380 | Park County School District #16 | WY | offers 9-12 | 116.00 | 39.00 | 2.97 | 5.53 | 6.97 | V33 / grade 3-8 enrollment high (z=5.5, offers 9-12) |
| 0616680 | Hawthorne | CA | offers 9-12 | 8,072.00 | 4,898.00 | 1.65 | -5.52 | 23.29 | V33 / grade 3-8 enrollment low (z=-5.5, offers 9-12) |
| 1932010 | Woodward-Granger Comm School District | IA | offers 9-12 | 1,214.00 | 409.00 | 2.97 | 5.49 | 12.67 | V33 / grade 3-8 enrollment high (z=5.5, offers 9-12) |
| 0627030 | New Jerusalem Elementary | CA | offers 9-12 | 1,768.00 | 596.00 | 2.97 | 5.48 | 25.81 | V33 / grade 3-8 enrollment high (z=5.5, offers 9-12) |
| 2309650 | Perry Public Schools | ME | offers 9-12 | 124.00 | 75.00 | 1.65 | -5.46 | 14.59 | V33 / grade 3-8 enrollment low (z=-5.5, offers 9-12) |
| 4032700 | WHITEFIELD | OK | K-8 only | 172.00 | 73.00 | 2.36 | 5.46 | 17.70 | V33 / grade 3-8 enrollment high (z=5.5, K-8 only) |
| 5516590 | White Lake School District | WI | offers 9-12 | 145.00 | 49.00 | 2.96 | 5.43 | 9.74 | V33 / grade 3-8 enrollment high (z=5.4, offers 9-12) |
| 0616650 | Hart-Ransom Union Elementary | CA | offers 9-12 | 1,173.00 | 708.00 | 1.66 | -5.42 | 21.68 | V33 / grade 3-8 enrollment low (z=-5.4, offers 9-12) |
| 0500026 | PINE BLUFF SCHOOL DISTRICT | AR | offers 9-12 | 3,299.00 | 1,991.00 | 1.66 | -5.42 | 14.30 | V33 / grade 3-8 enrollment low (z=-5.4, offers 9-12) |
| 3402520 | Butler Public School District | NJ | offers 9-12 | 1,221.00 | 413.00 | 2.96 | 5.41 | 12.01 | V33 / grade 3-8 enrollment high (z=5.4, offers 9-12) |
| 3305580 | Pembroke School District | NH | offers 9-12 | 1,436.00 | 486.00 | 2.95 | 5.40 | 11.67 | V33 / grade 3-8 enrollment high (z=5.4, offers 9-12) |
| 3404440 | Edgewater School District | NJ | K-8 only | 1,022.00 | 436.00 | 2.34 | 5.39 | 14.54 | V33 / grade 3-8 enrollment high (z=5.4, K-8 only) |
| 2718390 | LYND PUBLIC SCHOOL DISTRICT | MN | K-8 only | 180.00 | 77.00 | 2.34 | 5.35 | 8.45 | V33 / grade 3-8 enrollment high (z=5.4, K-8 only) |
| 5500570 | Athens School District | WI | offers 9-12 | 415.00 | 141.00 | 2.94 | 5.33 | 12.92 | V33 / grade 3-8 enrollment high (z=5.3, offers 9-12) |
| 2930520 | TWIN RIVERS R-X | MO | offers 9-12 | 882.00 | 300.00 | 2.94 | 5.31 | 12.13 | V33 / grade 3-8 enrollment high (z=5.3, offers 9-12) |
| 5505670 | Grantsburg School District | WI | offers 9-12 | 1,463.00 | 498.00 | 2.94 | 5.29 | 17.81 | V33 / grade 3-8 enrollment high (z=5.3, offers 9-12) |
| 2010440 | Oxford | KS | offers 9-12 | 455.00 | 155.00 | 2.94 | 5.28 | 15.29 | V33 / grade 3-8 enrollment high (z=5.3, offers 9-12) |
| 4003360 | ATOKA | OK | offers 9-12 | 890.00 | 304.00 | 2.93 | 5.23 | 15.65 | V33 / grade 3-8 enrollment high (z=5.2, offers 9-12) |
| 2801490 | FORREST COUNTY SCHOOL DISTRICT | MS | offers 9-12 | 2,245.00 | 1,341.00 | 1.67 | -5.23 | 12.53 | V33 / grade 3-8 enrollment low (z=-5.2, offers 9-12) |
| 0402370 | Cottonwood-Oak Creek Elementary District (4487) | AZ | offers 9-12 | 2,077.00 | 1,240.00 | 1.68 | -5.22 | 18.26 | V33 / grade 3-8 enrollment low (z=-5.2, offers 9-12) |
| 4007140 | CENTRAL | OK | offers 9-12 | 491.00 | 168.00 | 2.92 | 5.20 | 13.27 | V33 / grade 3-8 enrollment high (z=5.2, offers 9-12) |
| 0606570 | Burton Elementary | CA | offers 9-12 | 4,887.00 | 2,912.00 | 1.68 | -5.18 | 23.56 | V33 / grade 3-8 enrollment low (z=-5.2, offers 9-12) |
| 3414790 | Seaside Heights School District | NJ | K-8 only | 219.00 | 95.00 | 2.31 | 5.17 | 10.09 | V33 / grade 3-8 enrollment high (z=5.2, K-8 only) |
| 4024180 | PITTSBURG | OK | offers 9-12 | 143.00 | 49.00 | 2.92 | 5.17 | 13.18 | V33 / grade 3-8 enrollment high (z=5.2, offers 9-12) |
| 0903120 | NORWICH SCHOOL DISTRICT | CT | offers 9-12 | 3,510.00 | 2,090.00 | 1.68 | -5.17 | 13.82 | V33 / grade 3-8 enrollment low (z=-5.2, offers 9-12) |
| 2615600 | Engadine Consolidated Schools | MI | offers 9-12 | 356.00 | 122.00 | 2.92 | 5.17 | 14.94 | V33 / grade 3-8 enrollment high (z=5.2, offers 9-12) |
| 4700210 | Bells | TN | K-8 only | 419.00 | 182.00 | 2.30 | 5.16 | 14.45 | V33 / grade 3-8 enrollment high (z=5.2, K-8 only) |
| 0904260 | SPRAGUE SCHOOL DISTRICT | CT | offers 9-12 | 313.00 | 186.00 | 1.68 | -5.13 | 12.52 | V33 / grade 3-8 enrollment low (z=-5.1, offers 9-12) |
| 3176650 | SHICKLEY PUBLIC SCHOOLS | NE | offers 9-12 | 163.00 | 56.00 | 2.91 | 5.12 | 7.04 | V33 / grade 3-8 enrollment high (z=5.1, offers 9-12) |
| 4665460 | Oglala Lakota County 65-1 | SD | offers 9-12 | 1,415.00 | 839.00 | 1.69 | -5.09 | 13.66 | V33 / grade 3-8 enrollment low (z=-5.1, offers 9-12) |
| 4026580 | RYAL | OK | K-8 only | 87.00 | 38.00 | 2.29 | 5.08 | 17.13 | V33 / grade 3-8 enrollment high (z=5.1, K-8 only) |
| 2500556 | TEC Connections Academy Commonwealth Virtual School District | MA | offers 9-12 | 2,143.00 | 739.00 | 2.90 | 5.05 | 26.06 | V33 / grade 3-8 enrollment high (z=5.1, offers 9-12) |
| 4031380 | WAINWRIGHT | OK | K-8 only | 89.00 | 39.00 | 2.28 | 5.04 | 14.50 | V33 / grade 3-8 enrollment high (z=5.0, K-8 only) |
| 0619620 | Keyes Union | CA | offers 9-12 | 1,105.00 | 653.00 | 1.69 | -5.03 | 21.29 | V33 / grade 3-8 enrollment low (z=-5.0, offers 9-12) |
| 2004080 | Brewster | KS | offers 9-12 | 139.00 | 48.00 | 2.90 | 5.03 | 6.82 | V33 / grade 3-8 enrollment high (z=5.0, offers 9-12) |
| 2306000 | Glenburn Public Schools | ME | offers 9-12 | 510.00 | 301.00 | 1.69 | -5.00 | 14.25 | V33 / grade 3-8 enrollment low (z=-5.0, offers 9-12) |

### Variant B: refined grade grouping

48 districts move from 'offers 9-12' to 'K-8 only' because the CCD LEVEL field is Elementary or the name says Elementary. Flags recomputed within the refined groups:

| group | n | median ratio | robust SD (log) | flagged high | flagged low |
|---|---|---|---|---|---|
| K-8 only | 1,751 | 1.55 | 0.078 | 19 | 1 |
| offers 9-12 | 9,098 | 2.21 | 0.053 | 88 | 44 |

- flagged under B: 152 (A: 185); in both A and B: 150
- CCR-efficient units caught under B: none
- Andover z under B: -3.18

#### Low-side flags remaining under B (45)

| leaid | district_name | state | group | students | cov_enrl_g38 | enrl_ratio | z_enrl |
|---|---|---|---|---|---|---|---|
| 2201170 | Orleans Parish | LA | offers 9-12 | 4,642.00 | 22,772.00 | 0.20 | -44.85 |
| 2308160 | Medway Public Schools | ME | offers 9-12 | 113.00 | 113.00 | 1.00 | -14.95 |
| 2502580 | Berlin-Boylston | MA | offers 9-12 | 583.00 | 500.00 | 1.17 | -12.06 |
| 1929280 | Villisca Comm School District | IA | offers 9-12 | 319.00 | 240.00 | 1.33 | -9.60 |
| 0401810 | Cedar Unified District (4395) | AZ | offers 9-12 | 134.00 | 99.00 | 1.35 | -9.25 |
| 0642900 | Winship-Robbins | CA | offers 9-12 | 118.00 | 87.00 | 1.36 | -9.22 |
| 2311910 | MSAD 76 | ME | offers 9-12 | 34.00 | 25.00 | 1.36 | -9.16 |
| 4620100 | Eagle Butte School District 20-1 | SD | offers 9-12 | 347.00 | 252.00 | 1.38 | -8.93 |
| 0602070 | Alpine County Unified | CA | offers 9-12 | 79.00 | 57.00 | 1.39 | -8.81 |
| 1920830 | North Kossuth Comm School District | IA | offers 9-12 | 314.00 | 226.00 | 1.39 | -8.76 |
| 1925380 | Schaller-Crestland Comm School District | IA | offers 9-12 | 396.00 | 284.00 | 1.39 | -8.69 |
| 1914310 | Hubbard-Radcliffe Comm School District | IA | offers 9-12 | 404.00 | 287.00 | 1.41 | -8.52 |
| 1924120 | Remsen-Union Comm School District | IA | offers 9-12 | 337.00 | 239.00 | 1.41 | -8.48 |
| 1903090 | Adair-Casey Comm School District | IA | offers 9-12 | 258.00 | 181.00 | 1.43 | -8.28 |
| 0601428 | Wiseburn Unified | CA | offers 9-12 | 2,525.00 | 1,757.00 | 1.44 | -8.13 |
| 2314814 | Cherryfield Public Schools | ME | offers 9-12 | 115.00 | 80.00 | 1.44 | -8.12 |
| 1999019 | Southeast Webster Grand Comm School District | IA | offers 9-12 | 576.00 | 395.00 | 1.46 | -7.85 |
| 0615600 | Gorman Joint | CA | offers 9-12 | 82.00 | 56.00 | 1.46 | -7.78 |
| 2314824 | Northport Public Schools | ME | offers 9-12 | 136.00 | 92.00 | 1.48 | -7.60 |
| 0628530 | Orange Center | CA | offers 9-12 | 311.00 | 209.00 | 1.49 | -7.47 |
| 0621420 | Lennox | CA | offers 9-12 | 5,327.00 | 3,577.00 | 1.49 | -7.46 |
| 0405460 | Nadaburg Unified School District (4252) | AZ | offers 9-12 | 797.00 | 535.00 | 1.49 | -7.45 |
| 2306260 | Hancock Public Schools | ME | offers 9-12 | 231.00 | 155.00 | 1.49 | -7.44 |
| 2314820 | St George Public Schools | ME | offers 9-12 | 208.00 | 138.00 | 1.51 | -7.23 |
| 2306180 | Greenbush Public Schools | ME | offers 9-12 | 147.00 | 97.00 | 1.52 | -7.13 |
| 2309990 | Princeton Public Schools | ME | offers 9-12 | 141.00 | 93.00 | 1.52 | -7.12 |
| 1925410 | Schleswig Comm School District | IA | offers 9-12 | 193.00 | 124.00 | 1.56 | -6.63 |
| 2314010 | Woodland Public Schools | ME | offers 9-12 | 156.00 | 100.00 | 1.56 | -6.58 |
| 1734870 | Rossville-Alvin CUSD 7 | IL | offers 9-12 | 300.00 | 192.00 | 1.56 | -6.55 |
| 0613170 | Evergreen Union | CA | offers 9-12 | 1,217.00 | 777.00 | 1.57 | -6.51 |
| 4400510 | Jamestown | RI | offers 9-12 | 507.00 | 322.00 | 1.57 | -6.41 |
| 2308250 | Milford Public Schools | ME | offers 9-12 | 309.00 | 196.00 | 1.58 | -6.39 |
| 2310980 | RSU 87/MSAD 23 | ME | offers 9-12 | 629.00 | 394.00 | 1.60 | -6.15 |
| 3817670 | STARKWEATHER 44 | ND | offers 9-12 | 56.00 | 35.00 | 1.60 | -6.11 |
| 5304290 | Lamont School District | WA | K-8 only | 34.00 | 34.00 | 1.00 | -5.62 |
| 1730780 | Paris CUSD 4 | IL | offers 9-12 | 487.00 | 296.00 | 1.65 | -5.58 |
| 0616680 | Hawthorne | CA | offers 9-12 | 8,072.00 | 4,898.00 | 1.65 | -5.55 |
| 2309650 | Perry Public Schools | ME | offers 9-12 | 124.00 | 75.00 | 1.65 | -5.49 |
| 0500026 | PINE BLUFF SCHOOL DISTRICT | AR | offers 9-12 | 3,299.00 | 1,991.00 | 1.66 | -5.45 |
| 2801490 | FORREST COUNTY SCHOOL DISTRICT | MS | offers 9-12 | 2,245.00 | 1,341.00 | 1.67 | -5.26 |
| 0903120 | NORWICH SCHOOL DISTRICT | CT | offers 9-12 | 3,510.00 | 2,090.00 | 1.68 | -5.20 |
| 0904260 | SPRAGUE SCHOOL DISTRICT | CT | offers 9-12 | 313.00 | 186.00 | 1.68 | -5.16 |
| 4665460 | Oglala Lakota County 65-1 | SD | offers 9-12 | 1,415.00 | 839.00 | 1.69 | -5.12 |
| 0619620 | Keyes Union | CA | offers 9-12 | 1,105.00 | 653.00 | 1.69 | -5.06 |
| 2306000 | Glenburn Public Schools | ME | offers 9-12 | 510.00 | 301.00 | 1.69 | -5.03 |

## Overlap

- flagged by both screens: 1
- flagged by either: 217
