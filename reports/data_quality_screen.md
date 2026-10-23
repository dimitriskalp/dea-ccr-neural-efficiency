# Data-quality screen, report only (dataset NOT yet filtered)

Sample: 10,968 districts. Rule: |robust z| of log(ratio) > threshold, robust SD = 1.4826 x MAD.

## Scale of each ratio

| ratio | median | robust SD (log) | |z| <= 4 keeps ratios in |
|---|---|---|---|
| students_per_teacher | 14.27 | 0.230 | [5.68, 35.86] |
| students_per_other_staff | 13.84 | 0.344 | [3.50, 54.70] |
| exp_per_student | 12,003.00 | 0.259 | [4,261.23, 33,809.94] |

## Counts by threshold

| threshold | students_per_teacher | students_per_other_staff | exp_per_student | union | remaining | Toltec | Selmaville |
|---|---|---|---|---|---|---|---|
| 3.5 | 99 | 198 | 80 | 340 | 10,628 | yes | yes |
| 4.0 | 53 | 132 | 40 | 202 | 10,766 | yes | yes |
| 5.0 | 17 | 86 | 11 | 107 | 10,861 | yes | yes |

## Direction of the flags at threshold 4

| rule | high | low |
|---|---|---|
| students_per_teacher | 7 | 46 |
| students_per_other_staff | 115 | 17 |
| exp_per_student | 39 | 1 |

## Flagged districts by state (threshold 4)

| state | flagged | share of state's districts |
|---|---|---|
| IL | 39 | 5.2% |
| UT | 34 | 97.1% |
| IN | 16 | 5.6% |
| NV | 15 | 88.2% |
| MO | 13 | 2.6% |
| CA | 10 | 1.3% |
| NJ | 10 | 2.1% |
| AZ | 6 | 3.4% |
| ND | 5 | 3.5% |
| CT | 5 | 3.2% |
| OH | 4 | 0.7% |
| KS | 4 | 1.4% |
| WA | 4 | 1.6% |
| NE | 4 | 1.7% |
| NH | 3 | 2.3% |

Names matching admin/service-agency patterns (county office|office of education|COE|BOCES|cooperative|co-op|special|regional|intermediate|ESD|service): 6 of 202

## All 202 flagged districts (threshold 4), sorted by max |z|

| leaid | district_name | state | students | staff_teachers_fte | staff_other_fte | students_per_teacher | students_per_other_staff | exp_per_student | dq_reason |
|---|---|---|---|---|---|---|---|---|---|
| 0408550 | Toltec School District (4450) | AZ | 1,030 | 1.0 | 123.6 | 1,030.0 | 8.3 | 7,568 | students_per_teacher high (z=18.6) |
| 0691002 | Butte County Office of Education | CA | 408 | 42.9 | 387.3 | 9.5 | 1.1 | 165,623 | students_per_other_staff low (z=-7.5); exp_per_student high (z=10.1) |
| 0691030 | San Diego County Office of Education | CA | 1,385 | 115.8 | 835.2 | 12.0 | 1.7 | 163,604 | students_per_other_staff low (z=-6.2); exp_per_student high (z=10.1) |
| 0405430 | Naco Elementary District (4176) | AZ | 306 | 14.0 | 1.0 | 21.9 | 306.0 | 11,271 | students_per_other_staff high (z=9.0) |
| 3200120 | ELKO COUNTY SCHOOL DISTRICT | NV | 10,133 | 209.0 | 36.0 | 48.5 | 281.5 | 11,417 | students_per_teacher high (z=5.3); students_per_other_staff high (z=8.8) |
| 0630450 | Piner-Olivet Union Elementary | CA | 1,060 | 11.0 | 25.0 | 96.4 | 42.4 | 15,122 | students_per_teacher high (z=8.3) |
| 0691025 | Placer County Office of Education | CA | 433 | 36.8 | 407.3 | 11.8 | 1.1 | 102,268 | students_per_other_staff low (z=-7.5); exp_per_student high (z=8.3) |
| 0403550 | Grand Canyon Unified District (4194) | AZ | 281 | 18.4 | 1.2 | 15.3 | 224.8 | 19,260 | students_per_other_staff high (z=8.1) |
| 3304260 | Lincoln-Woodstock School District | NH | 288 | 128.8 | 86.6 | 2.2 | 3.3 | 26,344 | students_per_teacher low (z=-8.0); students_per_other_staff low (z=-4.1) |
| 0691043 | Tehama County Department of Education | CA | 245 | 15.9 | 220.2 | 15.4 | 1.1 | 89,318 | students_per_other_staff low (z=-7.3); exp_per_student high (z=7.8) |
| 3200510 | WHITE PINE COUNTY SCHOOL DISTRICT | NV | 1,655 | 49.0 | 9.0 | 33.8 | 183.9 | 10,543 | students_per_other_staff high (z=7.5) |
| 1723970 | Madison CUSD 12 | IL | 674 | 59.0 | 55.0 | 11.4 | 12.3 | 83,114 | exp_per_student high (z=7.5) |
| 1735770 | Selmaville CCSD 10 | IL | 281 | 19.0 | 1.6 | 14.8 | 180.1 | 10,388 | students_per_other_staff high (z=7.5) |
| 1710570 | Cobden SUD 17 | IL | 526 | 44.9 | 3.1 | 11.7 | 172.5 | 13,447 | students_per_other_staff high (z=7.3) |
| 1718060 | Hamilton CCSD 328 | IL | 587 | 45.5 | 517.7 | 12.9 | 1.1 | 12,027 | students_per_other_staff low (z=-7.3) |
| 3401110 | Avalon School District | NJ | 61 | 13.8 | 18.7 | 4.4 | 3.3 | 78,754 | students_per_teacher low (z=-5.1); students_per_other_staff low (z=-4.2); exp_per_student high (z=7.3) |
| 4900570 | Morgan District | UT | 3,208 | 137.7 | 19.3 | 23.3 | 166.4 | 6,354 | students_per_other_staff high (z=7.2) |
| 1723640 | Brooklyn UD 188 | IL | 162 | 10.0 | 1.0 | 16.2 | 162.0 | 17,809 | students_per_other_staff high (z=7.2) |
| 1600690 | CASTLEFORD DISTRICT | ID | 353 | 21.8 | 2.2 | 16.2 | 160.5 | 9,235 | students_per_other_staff high (z=7.1) |
| 3305880 | Raymond School District | NH | 1,248 | 105.5 | 1,036.0 | 11.8 | 1.2 | 18,541 | students_per_other_staff low (z=-7.1) |
| 1803180 | Randolph Eastern School Corp | IN | 908 | 59.2 | 6.0 | 15.3 | 151.3 | 9,406 | students_per_other_staff high (z=7.0) |
| 1808850 | Peru Community Schools | IN | 2,082 | 133.4 | 14.0 | 15.6 | 148.7 | 9,159 | students_per_other_staff high (z=6.9) |
| 1803870 | Gary Community School Corp | IN | 5,010 | 186.0 | 35.0 | 26.9 | 143.1 | 11,822 | students_per_other_staff high (z=6.8) |
| 0691001 | Amador County Office of Education | CA | 193 | 25.2 | 75.2 | 7.6 | 2.6 | 68,803 | students_per_other_staff low (z=-4.9); exp_per_student high (z=6.7) |
| 4901080 | Uintah District | UT | 7,257 | 300.9 | 52.6 | 24.1 | 138.0 | 8,365 | students_per_other_staff high (z=6.7) |
| 3200060 | CLARK COUNTY SCHOOL DISTRICT | NV | 330,225 | 14,882.0 | 2,468.0 | 22.2 | 133.8 | 8,925 | students_per_other_staff high (z=6.6) |
| 1706390 | Bismarck Henning CUSD | IL | 593 | 35.0 | 4.5 | 16.9 | 131.8 | 18,966 | students_per_other_staff high (z=6.6) |
| 3200030 | CHURCHILL COUNTY SCHOOL DISTRICT | NV | 3,396 | 212.0 | 26.0 | 16.0 | 130.6 | 11,678 | students_per_other_staff high (z=6.5) |
| 3200210 | HUMBOLDT COUNTY SCHOOL DISTRICT | NV | 3,514 | 261.0 | 27.0 | 13.5 | 130.1 | 13,115 | students_per_other_staff high (z=6.5) |
| 1810170 | Shoals Community School Corp | IN | 642 | 52.7 | 5.0 | 12.2 | 128.4 | 9,534 | students_per_other_staff high (z=6.5) |
| 4900450 | Juab District | UT | 2,616 | 114.2 | 20.6 | 22.9 | 127.2 | 7,843 | students_per_other_staff high (z=6.5) |
| 0409460 | Winslow Unified District (4387) | AZ | 2,025 | 105.5 | 16.0 | 19.2 | 126.6 | 8,843 | students_per_other_staff high (z=6.4) |
| 1806270 | Manchester Community Schools | IN | 1,629 | 83.2 | 13.0 | 19.6 | 125.3 | 9,338 | students_per_other_staff high (z=6.4) |
| 1801710 | Central Noble Com School Corp | IN | 1,247 | 68.5 | 10.0 | 18.2 | 124.7 | 9,289 | students_per_other_staff high (z=6.4) |
| 4900030 | Alpine District | UT | 81,715 | 3,205.1 | 658.4 | 25.5 | 124.1 | 7,055 | students_per_other_staff high (z=6.4) |
| 4900930 | Sevier District | UT | 4,779 | 220.1 | 38.7 | 21.7 | 123.5 | 8,576 | students_per_other_staff high (z=6.4) |
| 1742510 | Willow Grove SD 46 | IL | 185 | 15.7 | 1.5 | 11.8 | 123.3 | 9,811 | students_per_other_staff high (z=6.4) |
| 4900090 | Box Elder District | UT | 12,011 | 526.0 | 98.3 | 22.8 | 122.2 | 8,168 | students_per_other_staff high (z=6.3) |
| 1711520 | Cypress SD 64 | IL | 121 | 10.3 | 1.0 | 11.8 | 121.0 | 12,182 | students_per_other_staff high (z=6.3) |
| 1811700 | Union Township School Corp | IN | 1,452 | 84.2 | 12.0 | 17.2 | 121.0 | 10,201 | students_per_other_staff high (z=6.3) |
| 1802800 | Duneland School Corporation | IN | 5,874 | 302.9 | 49.0 | 19.4 | 119.9 | 9,611 | students_per_other_staff high (z=6.3) |
| 1810450 | South Montgomery Com Sch Corp | IN | 1,716 | 125.6 | 14.4 | 13.7 | 119.2 | 10,124 | students_per_other_staff high (z=6.3) |
| 4900660 | North Sanpete District | UT | 2,627 | 119.0 | 22.3 | 22.1 | 117.9 | 8,624 | students_per_other_staff high (z=6.2) |
| 4900390 | Iron District | UT | 9,777 | 429.0 | 83.1 | 22.8 | 117.6 | 7,509 | students_per_other_staff high (z=6.2) |
| 0805250 | Las Animas School District No. Re-1 | CO | 2,309 | 38.6 | 145.1 | 59.8 | 15.9 | 8,049 | students_per_teacher high (z=6.2) |
| 3200300 | LYON COUNTY SCHOOL DISTRICT | NV | 9,066 | 529.0 | 78.0 | 17.1 | 116.2 | 10,341 | students_per_other_staff high (z=6.2) |
| 3200390 | CARSON CITY SCHOOL DISTRICT | NV | 8,131 | 496.0 | 71.0 | 16.4 | 114.5 | 11,174 | students_per_other_staff high (z=6.2) |
| 4901200 | Weber District | UT | 32,567 | 1,452.1 | 290.5 | 22.4 | 112.1 | 7,690 | students_per_other_staff high (z=6.1) |
| 4900120 | Cache District | UT | 18,778 | 773.1 | 172.2 | 24.3 | 109.0 | 7,863 | students_per_other_staff high (z=6.0) |
| 3411040 | MOUNTAINSIDE SCHOOL DISTRICT | NJ | 258 | 71.3 | 45.9 | 3.6 | 5.6 | 50,345 | students_per_teacher low (z=-6.0); exp_per_student high (z=5.5) |
| 4900240 | Duchesne District | UT | 5,285 | 256.8 | 49.4 | 20.6 | 107.0 | 9,018 | students_per_other_staff high (z=6.0) |
| 4900210 | Davis District | UT | 74,289 | 3,032.9 | 694.2 | 24.5 | 107.0 | 7,622 | students_per_other_staff high (z=6.0) |
| 1740320 | Villa Grove CUSD 302 | IL | 651 | 47.4 | 6.1 | 13.7 | 106.4 | 11,810 | students_per_other_staff high (z=5.9) |
| 1741250 | Waukegan CUSD 60 | IL | 15,772 | 834.0 | 152.0 | 18.9 | 103.8 | 17,065 | students_per_other_staff high (z=5.9) |
| 3200480 | WASHOE COUNTY SCHOOL DISTRICT | NV | 67,113 | 3,648.0 | 652.0 | 18.4 | 102.9 | 9,563 | students_per_other_staff high (z=5.8) |
| 1727990 | New Berlin CUSD 16 | IL | 939 | 65.0 | 9.2 | 14.4 | 102.1 | 12,021 | students_per_other_staff high (z=5.8) |
| 4900420 | Jordan District | UT | 56,176 | 2,367.3 | 550.9 | 23.7 | 102.0 | 7,219 | students_per_other_staff high (z=5.8) |
| 4900960 | South Sanpete District | UT | 3,448 | 176.5 | 34.0 | 19.5 | 101.3 | 9,213 | students_per_other_staff high (z=5.8) |
| 4213320 | Laurel Highlands SD | PA | 2,928 | 195.0 | 29.0 | 15.0 | 101.0 | 14,707 | students_per_other_staff high (z=5.8) |
| 1727780 | Nauvoo-Colusa CUSD 325 | IL | 242 | 20.5 | 2.4 | 11.8 | 100.8 | 15,517 | students_per_other_staff high (z=5.8) |
| 4900540 | Millard District | UT | 3,077 | 150.8 | 31.2 | 20.4 | 98.7 | 10,579 | students_per_other_staff high (z=5.7) |
| 1804140 | Monroe-Gregg School District | IN | 1,522 | 110.1 | 16.0 | 13.8 | 95.1 | 9,525 | students_per_other_staff high (z=5.6) |
| 3904428 | Madeira City | OH | 1,516 | 83.1 | 749.1 | 18.2 | 2.0 | 13,426 | students_per_other_staff low (z=-5.6) |
| 4900270 | Emery District | UT | 2,313 | 123.9 | 24.6 | 18.7 | 94.0 | 11,348 | students_per_other_staff high (z=5.6) |
| 2905850 | BRECKENRIDGE R-I | MO | 59 | 14.9 | 3.1 | 4.0 | 19.0 | 20,034 | students_per_teacher low (z=-5.6) |
| 1804590 | School City of Hobart | IN | 4,103 | 182.5 | 44.0 | 22.5 | 93.2 | 8,973 | students_per_other_staff high (z=5.6) |
| 1801170 | Cannelton City Schools | IN | 279 | 17.8 | 3.0 | 15.7 | 93.0 | 9,502 | students_per_other_staff high (z=5.5) |
| 4900300 | Garfield District | UT | 975 | 57.6 | 10.6 | 16.9 | 92.3 | 11,108 | students_per_other_staff high (z=5.5) |
| 1811250 | Taylor Community School Corp | IN | 1,292 | 91.0 | 14.0 | 14.2 | 92.3 | 9,358 | students_per_other_staff high (z=5.5) |
| 2721210 | MILROY PUBLIC SCHOOL DISTRICT | MN | 37 | 9.2 | 6.7 | 4.0 | 5.5 | 25,973 | students_per_teacher low (z=-5.5) |
| 1723160 | Lisbon CCSD 90 | IL | 108 | 10.6 | 1.2 | 10.2 | 90.0 | 13,648 | students_per_other_staff high (z=5.4) |
| 4900630 | Nebo District | UT | 33,834 | 1,452.1 | 376.4 | 23.3 | 89.9 | 7,298 | students_per_other_staff high (z=5.4) |
| 0691006 | El Dorado County Office of Education | CA | 987 | 64.0 | 282.8 | 15.4 | 3.5 | 49,014 | students_per_other_staff low (z=-4.0); exp_per_student high (z=5.4) |
| 4900150 | Carbon District | UT | 3,607 | 180.2 | 40.6 | 20.0 | 88.9 | 9,346 | students_per_other_staff high (z=5.4) |
| 4900690 | North Summit District | UT | 1,076 | 55.2 | 12.1 | 19.5 | 88.9 | 10,901 | students_per_other_staff high (z=5.4) |
| 3200090 | DOUGLAS COUNTY SCHOOL DISTRICT | NV | 5,834 | 427.0 | 66.0 | 13.7 | 88.4 | 10,563 | students_per_other_staff high (z=5.4) |
| 1742690 | Windsor CUSD 1 | IL | 368 | 29.8 | 4.2 | 12.3 | 88.2 | 12,408 | students_per_other_staff high (z=5.4) |
| 1726970 | Meridian CUSD 101 | IL | 440 | 26.9 | 5.0 | 16.4 | 88.0 | 17,268 | students_per_other_staff high (z=5.4) |
| 1733930 | Riverdale CUSD 100 | IL | 1,157 | 74.0 | 530.0 | 15.6 | 2.2 | 11,690 | students_per_other_staff low (z=-5.4) |
| 4900480 | Kane District | UT | 1,358 | 70.2 | 15.5 | 19.4 | 87.3 | 11,663 | students_per_other_staff high (z=5.4) |
| 1810530 | South Ripley Com Sch Corp | IN | 1,130 | 83.7 | 13.0 | 13.5 | 86.9 | 10,924 | students_per_other_staff high (z=5.3) |
| 3406150 | GREENWICH TOWNSHIP SCHOOL DISTRICT | NJ | 61 | 14.6 | 9.9 | 4.2 | 6.2 | 28,443 | students_per_teacher low (z=-5.3) |
| 4900180 | Daggett District | UT | 206 | 16.6 | 2.4 | 12.4 | 86.6 | 18,684 | students_per_other_staff high (z=5.3) |
| 4900990 | South Summit District | UT | 1,713 | 88.0 | 19.8 | 19.5 | 86.4 | 9,880 | students_per_other_staff high (z=5.3) |
| 4900510 | Logan City District | UT | 5,894 | 252.7 | 68.5 | 23.3 | 86.1 | 8,326 | students_per_other_staff high (z=5.3) |
| 2000013 | Triplains | KS | 71 | 16.9 | 13.7 | 4.2 | 5.2 | 19,606 | students_per_teacher low (z=-5.3) |
| 0636000 | Sausalito Marin City | CA | 119 | 10.9 | 22.4 | 10.9 | 5.3 | 47,176 | exp_per_student high (z=5.3) |
| 2511730 | Truro | MA | 106 | 16.0 | 17.3 | 6.6 | 6.1 | 47,038 | exp_per_student high (z=5.3) |
| 4900330 | Grand District | UT | 1,586 | 95.6 | 18.8 | 16.6 | 84.1 | 11,491 | students_per_other_staff high (z=5.3) |
| 3200240 | LANDER COUNTY SCHOOL DISTRICT | NV | 1,002 | 59.0 | 12.0 | 17.0 | 83.5 | 12,616 | students_per_other_staff high (z=5.2) |
| 2931530 | WEBSTER GROVES | MO | 4,683 | 315.5 | 56.3 | 14.8 | 83.2 | 11,661 | students_per_other_staff high (z=5.2) |
| 3200330 | MINERAL COUNTY SCHOOL DISTRICT | NV | 582 | 57.0 | 7.0 | 10.2 | 83.1 | 14,960 | students_per_other_staff high (z=5.2) |
| 3806910 | FINLEY-SHARON 19 | ND | 78 | 18.1 | 9.4 | 4.3 | 8.3 | 27,269 | students_per_teacher low (z=-5.2) |
| 4224990 | Washington SD | PA | 1,465 | 118.7 | 17.8 | 12.3 | 82.3 | 14,934 | students_per_other_staff high (z=5.2) |
| 4900360 | Granite District | UT | 66,767 | 2,867.5 | 811.9 | 23.3 | 82.2 | 8,514 | students_per_other_staff high (z=5.2) |
| 1719230 | Hillside SD 93 | IL | 410 | 44.0 | 5.0 | 9.3 | 82.0 | 21,768 | students_per_other_staff high (z=5.2) |
| 2912690 | GRUNDY CO. R-V | MO | 122 | 17.1 | 52.2 | 7.1 | 2.3 | 18,484 | students_per_other_staff low (z=-5.2) |
| 4900060 | Beaver District | UT | 1,567 | 75.8 | 19.2 | 20.7 | 81.8 | 10,263 | students_per_other_staff high (z=5.2) |
| 2006870 | Hamilton | KS | 62 | 14.2 | 10.4 | 4.4 | 6.0 | 22,226 | students_per_teacher low (z=-5.1) |
| 5516830 | Winneconne Community School District | WI | 1,682 | 89.1 | 20.8 | 18.9 | 80.9 | 10,545 | students_per_other_staff high (z=5.1) |
| 5305040 | Mill A School District | WA | 46 | 10.5 | 2.4 | 4.4 | 19.6 | 37,717 | students_per_teacher low (z=-5.1); exp_per_student high (z=4.4) |
| 4900142 | Canyons District | UT | 35,330 | 1,502.8 | 443.0 | 23.5 | 79.8 | 8,161 | students_per_other_staff high (z=5.1) |
| 4900600 | Murray District | UT | 6,388 | 277.1 | 80.3 | 23.1 | 79.6 | 8,124 | students_per_other_staff high (z=5.1) |
| 3803590 | BURKE CENTRAL 36 | ND | 85 | 19.1 | 9.4 | 4.5 | 9.1 | 26,353 | students_per_teacher low (z=-5.0) |
| 4901110 | Wasatch District | UT | 7,333 | 343.8 | 93.9 | 21.3 | 78.1 | 9,723 | students_per_other_staff high (z=5.0) |
| 2915630 | NORTH DAVIESS R-III | MO | 67 | 14.9 | 6.7 | 4.5 | 10.1 | 21,955 | students_per_teacher low (z=-5.0) |
| 2917910 | LAREDO R-VII | MO | 36 | 8.0 | 7.5 | 4.5 | 4.8 | 23,417 | students_per_teacher low (z=-5.0) |
| 0602070 | Alpine County Unified | CA | 79 | 11.0 | 28.6 | 7.2 | 2.8 | 43,481 | students_per_other_staff low (z=-4.7); exp_per_student high (z=5.0) |
| 2311820 | RSU 07/MSAD 07 | ME | 60 | 13.2 | 10.1 | 4.5 | 5.9 | 33,883 | students_per_teacher low (z=-5.0); exp_per_student high (z=4.0) |
| 1714410 | Eswood CCSD 269 | IL | 76 | 8.0 | 1.0 | 9.5 | 76.0 | 18,816 | students_per_other_staff high (z=5.0) |
| 3401290 | Beach Haven School District | NJ | 55 | 12.0 | 3.1 | 4.6 | 17.7 | 38,836 | students_per_teacher low (z=-4.9); exp_per_student high (z=4.5) |
| 1734620 | Rondout SD 72 | IL | 141 | 16.5 | 14.7 | 8.6 | 9.6 | 42,780 | exp_per_student high (z=4.9) |
| 2917000 | LACLEDE CO. C-5 | MO | 443 | 34.5 | 6.0 | 12.8 | 73.8 | 8,977 | students_per_other_staff high (z=4.9) |
| 0904020 | SHARON SCHOOL DISTRICT | CT | 115 | 21.0 | 22.4 | 5.5 | 5.1 | 42,209 | students_per_teacher low (z=-4.2); exp_per_student high (z=4.9) |
| 3200420 | PERSHING COUNTY SCHOOL DISTRICT | NV | 658 | 75.0 | 9.0 | 8.8 | 73.1 | 18,427 | students_per_other_staff high (z=4.8) |
| 1720910 | Kell Cons SD 2 | IL | 95 | 11.0 | 1.3 | 8.6 | 73.1 | 15,116 | students_per_other_staff high (z=4.8) |
| 1740410 | Virginia CUSD 64 | IL | 306 | 27.0 | 4.2 | 11.3 | 72.9 | 13,990 | students_per_other_staff high (z=4.8) |
| 3817520 | ST THOMAS 43 | ND | 54 | 11.5 | 9.0 | 4.7 | 6.0 | 26,389 | students_per_teacher low (z=-4.8) |
| 0900630 | CANAAN SCHOOL DISTRICT | CT | 63 | 11.5 | 8.4 | 5.5 | 7.5 | 41,746 | students_per_teacher low (z=-4.2); exp_per_student high (z=4.8) |
| 1704950 | Bannockburn SD 106 | IL | 148 | 18.8 | 14.2 | 7.9 | 10.4 | 41,649 | exp_per_student high (z=4.8) |
| 3173120 | LOUP COUNTY PUBLIC SCHOOLS | NE | 70 | 14.8 | 15.0 | 4.7 | 4.7 | 34,157 | students_per_teacher low (z=-4.8); exp_per_student high (z=4.0) |
| 3409480 | Mannington Township School District | NJ | 156 | 17.6 | 11.4 | 8.9 | 13.7 | 40,756 | exp_per_student high (z=4.7) |
| 2920670 | MEHLVILLE R-IX | MO | 10,308 | 693.4 | 147.1 | 14.9 | 70.1 | 10,069 | students_per_other_staff high (z=4.7) |
| 4503600 | Spartanburg 05 | SC | 8,802 | 588.3 | 126.1 | 15.0 | 69.8 | 10,406 | students_per_other_staff high (z=4.7) |
| 4901170 | Wayne District | UT | 487 | 30.4 | 7.0 | 16.0 | 69.5 | 13,304 | students_per_other_staff high (z=4.7) |
| 1742960 | Wolf Branch SD 113 | IL | 763 | 49.0 | 11.0 | 15.6 | 69.4 | 13,502 | students_per_other_staff high (z=4.7) |
| 4400690 | New Shoreham | RI | 133 | 21.6 | 21.0 | 6.2 | 6.3 | 40,083 | exp_per_student high (z=4.7) |
| 1717310 | Grant CCSD 110 | IL | 612 | 42.0 | 9.0 | 14.6 | 68.0 | 14,959 | students_per_other_staff high (z=4.6) |
| 4400390 | Foster | RI | 272 | 21.8 | 4.0 | 12.5 | 68.0 | 17,081 | students_per_other_staff high (z=4.6) |
| 5500840 | Barneveld School District | WI | 438 | 34.1 | 23.1 | 12.8 | 19.0 | 39,785 | exp_per_student high (z=4.6) |
| 4900870 | Salt Lake District | UT | 23,165 | 1,120.6 | 342.3 | 20.7 | 67.7 | 9,689 | students_per_other_staff high (z=4.6) |
| 1743800 | Zeigler-Royalton CUSD 188 | IL | 590 | 43.1 | 8.8 | 13.7 | 67.4 | 9,856 | students_per_other_staff high (z=4.6) |
| 1740200 | Venice CUSD 3 | IL | 80 | 12.0 | 5.6 | 6.7 | 14.3 | 39,188 | exp_per_student high (z=4.6) |
| 1739120 | Tolono CUSD 7 | IL | 1,618 | 115.1 | 24.3 | 14.1 | 66.5 | 12,482 | students_per_other_staff high (z=4.6) |
| 4900720 | Ogden City District | UT | 11,782 | 563.0 | 177.8 | 20.9 | 66.3 | 9,221 | students_per_other_staff high (z=4.6) |
| 3200270 | LINCOLN COUNTY SCHOOL DISTRICT | NV | 993 | 89.0 | 15.0 | 11.2 | 66.2 | 15,348 | students_per_other_staff high (z=4.6) |
| 3402610 | Califon Borough School District | NJ | 77 | 15.4 | 8.5 | 5.0 | 9.1 | 37,052 | students_per_teacher low (z=-4.6); exp_per_student high (z=4.4) |
| 4900900 | San Juan District | UT | 3,051 | 171.9 | 46.5 | 17.7 | 65.7 | 13,337 | students_per_other_staff high (z=4.5) |
| 0601980 | Allensworth Elementary | CA | 88 | 4.7 | 1.3 | 18.9 | 65.7 | 12,341 | students_per_other_staff high (z=4.5) |
| 5304150 | LaCrosse School District | WA | 66 | 11.6 | 4.1 | 5.7 | 16.1 | 38,758 | students_per_teacher low (z=-4.0); exp_per_student high (z=4.5) |
| 3904750 | Ridgemont Local | OH | 513 | 44.2 | 175.5 | 11.6 | 2.9 | 13,058 | students_per_other_staff low (z=-4.5) |
| 3173560 | MC PHERSON COUNTY SCHOOLS | NE | 65 | 12.9 | 7.9 | 5.0 | 8.2 | 30,308 | students_per_teacher low (z=-4.5) |
| 3415840 | STOW CREEK TOWNSHIP SCHOOL DISTRICT | NJ | 116 | 22.9 | 11.2 | 5.1 | 10.4 | 21,595 | students_per_teacher low (z=-4.5) |
| 0102550 | Oneonta City | AL | 1,503 | 88.0 | 23.2 | 17.1 | 64.8 | 8,985 | students_per_other_staff high (z=4.5) |
| 3027730 | Westby K-12 Schools | MT | 58 | 11.4 | 9.7 | 5.1 | 6.0 | 28,328 | students_per_teacher low (z=-4.5) |
| 2922470 | NEWTOWN-HARRIS R-III | MO | 80 | 15.8 | 6.5 | 5.1 | 12.3 | 20,975 | students_per_teacher low (z=-4.5) |
| 3905009 | Bloomfield-Mespo Local | OH | 228 | 25.3 | 76.9 | 9.0 | 3.0 | 16,197 | students_per_other_staff low (z=-4.5) |
| 1709330 | Cerro Gordo CUSD 100 | IL | 484 | 35.0 | 7.5 | 13.8 | 64.5 | 13,655 | students_per_other_staff high (z=4.5) |
| 3305700 | Pittsburg School District | NH | 83 | 16.3 | 16.1 | 5.1 | 5.2 | 32,386 | students_per_teacher low (z=-4.5) |
| 3400870 | Alpine Elementary School District | NJ | 138 | 22.4 | 16.9 | 6.2 | 8.2 | 38,174 | exp_per_student high (z=4.5) |
| 3200180 | EUREKA COUNTY SCHOOL DISTRICT | NV | 321 | 61.0 | 5.0 | 5.3 | 64.2 | 25,287 | students_per_teacher low (z=-4.3); students_per_other_staff high (z=4.5) |
| 1712960 | East Alton SD 13 | IL | 767 | 53.3 | 12.0 | 14.4 | 63.9 | 15,163 | students_per_other_staff high (z=4.5) |
| 4012180 | FREEDOM | OK | 67 | 13.0 | 12.0 | 5.1 | 5.6 | 30,507 | students_per_teacher low (z=-4.4) |
| 3200360 | NYE COUNTY SCHOOL DISTRICT | NV | 5,367 | 341.0 | 85.0 | 15.7 | 63.1 | 12,768 | students_per_other_staff high (z=4.4) |
| 2728350 | PILLAGER PUBLIC SCHOOL DISTRICT | MN | 1,164 | 66.3 | 18.5 | 17.6 | 63.1 | 10,603 | students_per_other_staff high (z=4.4) |
| 4503570 | Spartanburg 04 | SC | 2,894 | 167.7 | 46.4 | 17.3 | 62.4 | 9,796 | students_per_other_staff high (z=4.4) |
| 1712930 | Earlville CUSD 9 | IL | 411 | 33.6 | 6.6 | 12.2 | 62.3 | 12,112 | students_per_other_staff high (z=4.4) |
| 1712510 | Donovan CUSD 3 | IL | 284 | 25.4 | 4.6 | 11.2 | 62.1 | 12,130 | students_per_other_staff high (z=4.4) |
| 2504710 | Erving | MA | 128 | 16.2 | 26.6 | 7.9 | 4.8 | 37,211 | exp_per_student high (z=4.4) |
| 5605680 | Sheridan County School District #3 | WY | 93 | 15.2 | 20.6 | 6.1 | 4.5 | 37,108 | exp_per_student high (z=4.4) |
| 4606960 | Big Stone City School District 25-1 | SD | 67 | 12.8 | 10.6 | 5.2 | 6.3 | 19,075 | students_per_teacher low (z=-4.3) |
| 3018240 | Melstone Elem | MT | 40 | 7.6 | 3.7 | 5.3 | 10.8 | 21,925 | students_per_teacher low (z=-4.3) |
| 1739660 | Union SD 81 | IL | 103 | 13.4 | 5.5 | 7.7 | 18.7 | 36,650 | exp_per_student high (z=4.3) |
| 2919920 | MALTA BEND R-V | MO | 90 | 17.0 | 14.2 | 5.3 | 6.4 | 19,578 | students_per_teacher low (z=-4.3) |
| 5309570 | Washtucna School District | WA | 57 | 10.0 | 3.5 | 5.7 | 16.4 | 36,596 | students_per_teacher low (z=-4.0); exp_per_student high (z=4.3) |
| 1739480 | Tri Point CUSD 6-J | IL | 358 | 36.7 | 5.9 | 9.8 | 60.7 | 20,142 | students_per_other_staff high (z=4.3) |
| 3904541 | Hicksville Exempted Village | OH | 907 | 64.9 | 287.4 | 14.0 | 3.2 | 12,389 | students_per_other_staff low (z=-4.3) |
| 1707740 | Buncombe Cons SD 43 | IL | 60 | 6.0 | 1.0 | 10.0 | 60.0 | 12,850 | students_per_other_staff high (z=4.3) |
| 2906150 | COOPER CO. R-IV | MO | 94 | 17.6 | 9.3 | 5.3 | 10.1 | 20,532 | students_per_teacher low (z=-4.3) |
| 1701416 | Milford Area PSD 124 | IL | 538 | 50.5 | 9.0 | 10.7 | 59.8 | 16,619 | students_per_other_staff high (z=4.3) |
| 3176800 | SIOUX COUNTY PUBLIC SCHOOLS | NE | 100 | 18.7 | 9.5 | 5.4 | 10.5 | 29,520 | students_per_teacher low (z=-4.3) |
| 0900930 | CORNWALL SCHOOL DISTRICT | CT | 91 | 14.5 | 11.2 | 6.3 | 8.1 | 36,077 | exp_per_student high (z=4.3) |
| 2906450 | CAINSVILLE R-I | MO | 78 | 14.5 | 17.2 | 5.4 | 4.5 | 19,038 | students_per_teacher low (z=-4.2) |
| 2909090 | CLARKSBURG C-2 | MO | 54 | 10.0 | 15.0 | 5.4 | 3.6 | 16,574 | students_per_teacher low (z=-4.2) |
| 4822020 | GUTHRIE CSD | TX | 106 | 19.6 | 12.4 | 5.4 | 8.5 | 29,189 | students_per_teacher low (z=-4.2) |
| 0500076 | OZARK MOUNTAIN SCHOOL DISTRICT | AR | 613 | 113.2 | 96.4 | 5.4 | 6.4 | 13,181 | students_per_teacher low (z=-4.2) |
| 3812720 | MENOKEN 33 | ND | 44 | 4.0 | 0.8 | 11.0 | 58.7 | 11,955 | students_per_other_staff high (z=4.2) |
| 5303300 | Green Mountain School District | WA | 163 | 8.8 | 2.8 | 18.5 | 58.6 | 11,675 | students_per_other_staff high (z=4.2) |
| 2913620 | HANCOCK PLACE | MO | 1,490 | 99.5 | 25.6 | 15.0 | 58.2 | 12,001 | students_per_other_staff high (z=4.2) |
| 2012900 | Weskan | KS | 100 | 18.3 | 8.1 | 5.5 | 12.3 | 17,490 | students_per_teacher low (z=-4.2) |
| 0903530 | REGIONAL SCHOOL DISTRICT 12 | CT | 683 | 77.9 | 136.4 | 8.8 | 5.0 | 35,082 | exp_per_student high (z=4.1) |
| 3816470 | SAWYER 16 | ND | 44 | 8.0 | 11.0 | 5.5 | 4.0 | 34,682 | students_per_teacher low (z=-4.1); exp_per_student high (z=4.1) |
| 0904650 | UNION SCHOOL DISTRICT | CT | 52 | 7.8 | 8.2 | 6.6 | 6.3 | 34,865 | exp_per_student high (z=4.1) |
| 2733720 | NETT LAKE PUBLIC SCHOOL DISTRICT | MN | 57 | 8.3 | 14.4 | 6.9 | 3.9 | 34,789 | exp_per_student high (z=4.1) |
| 3411670 | North Wildwood School District | NJ | 227 | 33.3 | 30.6 | 6.8 | 7.4 | 34,780 | exp_per_student high (z=4.1) |
| 1802160 | Clinton Prairie School Corporation | IN | 1,301 | 68.6 | 23.0 | 19.0 | 56.6 | 8,164 | students_per_other_staff high (z=4.1) |
| 1720970 | Kenilworth SD 38 | IL | 479 | 56.7 | 33.0 | 8.4 | 14.5 | 34,672 | exp_per_student high (z=4.1) |
| 2006510 | Southern Cloud | KS | 171 | 30.7 | 17.1 | 5.6 | 10.0 | 18,088 | students_per_teacher low (z=-4.1) |
| 1729420 | Oblong CUSD 4 | IL | 615 | 45.0 | 10.9 | 13.7 | 56.3 | 11,403 | students_per_other_staff high (z=4.1) |
| 0101410 | Eufaula City | AL | 5,427 | 148.5 | 138.4 | 36.5 | 39.2 | 5,298 | students_per_teacher high (z=4.1) |
| 3409690 | Margate City School District | NJ | 351 | 48.8 | 45.5 | 7.2 | 7.7 | 34,493 | exp_per_student high (z=4.1) |
| 4845990 | WILSON ISD | TX | 103 | 18.4 | 18.6 | 5.6 | 5.5 | 21,398 | students_per_teacher low (z=-4.1) |
| 2500551 | Greenfield Commonwealth Virtual District | MA | 590 | 37.5 | 10.5 | 15.7 | 56.0 | 9,229 | students_per_other_staff high (z=4.1) |
| 1811730 | Union School Corporation | IN | 3,371 | 143.5 | 96.7 | 23.5 | 34.9 | 4,188 | exp_per_student low (z=-4.1) |
| 0403240 | Gadsden Elementary District (4505) | AZ | 5,110 | 140.5 | 490.1 | 36.4 | 10.4 | 7,894 | students_per_teacher high (z=4.1) |
| 4029430 | TALOGA | OK | 96 | 17.1 | 17.2 | 5.6 | 5.6 | 27,510 | students_per_teacher low (z=-4.1) |
| 0408640 | Topock Elementary District (4376) | AZ | 109 | 3.0 | 18.8 | 36.3 | 5.8 | 14,789 | students_per_teacher high (z=4.1) |
| 3178670 | WHEELER CENTRAL SCHOOLS | NE | 99 | 17.6 | 13.8 | 5.6 | 7.1 | 31,455 | students_per_teacher low (z=-4.0) |
| 3016290 | Lavina K-12 Schools | MT | 69 | 12.3 | 9.0 | 5.6 | 7.7 | 20,652 | students_per_teacher low (z=-4.0) |
| 4811040 | BOYS RANCH ISD | TX | 309 | 54.8 | 29.2 | 5.6 | 10.6 | 22,424 | students_per_teacher low (z=-4.0) |
| 1740890 | Warsaw CUSD 316 | IL | 402 | 32.0 | 7.3 | 12.6 | 55.1 | 11,816 | students_per_other_staff high (z=4.0) |
| 1729520 | Odell CCSD 435 | IL | 143 | 16.4 | 2.6 | 8.7 | 55.0 | 14,755 | students_per_other_staff high (z=4.0) |

## Flags by direction and threshold

| threshold | teacher high | teacher low | other-staff high | other-staff low | exp high | exp low | union | remaining |
|---|---|---|---|---|---|---|---|---|
| 3.5 | 13 | 86 | 144 | 54 | 79 | 1 | 340 | 10628 |
| 4.0 | 7 | 46 | 115 | 17 | 39 | 1 | 202 | 10766 |
| 5.0 | 4 | 13 | 77 | 9 | 11 | 0 | 107 | 10861 |

## Flagged at 4.0 but not at 5.0 (95 districts), grouped by state

Median ratios in the sample: 14.3 students per teacher, 13.8 students per other staff, $12,003 per student.

| leaid | district_name | state | students | teachers FTE | other FTE | stud/teacher | stud/other | $/student | reason |
|---|---|---|---|---|---|---|---|---|---|
| 0102550 | Oneonta City | AL | 1,503 | 88.0 | 23.2 | 17.1 | 64.8 | 8,985 | students_per_other_staff high (z=4.5) |
| 0101410 | Eufaula City | AL | 5,427 | 148.5 | 138.4 | 36.5 | 39.2 | 5,298 | students_per_teacher high (z=4.1) |
| 0500076 | OZARK MOUNTAIN SCHOOL DISTRICT | AR | 613 | 113.2 | 96.4 | 5.4 | 6.4 | 13,181 | students_per_teacher low (z=-4.2) |
| 0403240 | Gadsden Elementary District (4505) | AZ | 5,110 | 140.5 | 490.1 | 36.4 | 10.4 | 7,894 | students_per_teacher high (z=4.1) |
| 0408640 | Topock Elementary District (4376) | AZ | 109 | 3.0 | 18.8 | 36.3 | 5.8 | 14,789 | students_per_teacher high (z=4.1) |
| 0602070 | Alpine County Unified | CA | 79 | 11.0 | 28.6 | 7.2 | 2.8 | 43,481 | students_per_other_staff low (z=-4.7); exp_per_student high (z=5.0) |
| 0601980 | Allensworth Elementary | CA | 88 | 4.7 | 1.3 | 18.9 | 65.7 | 12,341 | students_per_other_staff high (z=4.5) |
| 0904020 | SHARON SCHOOL DISTRICT | CT | 115 | 21.0 | 22.4 | 5.5 | 5.1 | 42,209 | students_per_teacher low (z=-4.2); exp_per_student high (z=4.9) |
| 0900630 | CANAAN SCHOOL DISTRICT | CT | 63 | 11.5 | 8.4 | 5.5 | 7.5 | 41,746 | students_per_teacher low (z=-4.2); exp_per_student high (z=4.8) |
| 0900930 | CORNWALL SCHOOL DISTRICT | CT | 91 | 14.5 | 11.2 | 6.3 | 8.1 | 36,077 | exp_per_student high (z=4.3) |
| 0903530 | REGIONAL SCHOOL DISTRICT 12 | CT | 683 | 77.9 | 136.4 | 8.8 | 5.0 | 35,082 | exp_per_student high (z=4.1) |
| 0904650 | UNION SCHOOL DISTRICT | CT | 52 | 7.8 | 8.2 | 6.6 | 6.3 | 34,865 | exp_per_student high (z=4.1) |
| 1714410 | Eswood CCSD 269 | IL | 76 | 8.0 | 1.0 | 9.5 | 76.0 | 18,816 | students_per_other_staff high (z=5.0) |
| 1734620 | Rondout SD 72 | IL | 141 | 16.5 | 14.7 | 8.6 | 9.6 | 42,780 | exp_per_student high (z=4.9) |
| 1720910 | Kell Cons SD 2 | IL | 95 | 11.0 | 1.3 | 8.6 | 73.1 | 15,116 | students_per_other_staff high (z=4.8) |
| 1740410 | Virginia CUSD 64 | IL | 306 | 27.0 | 4.2 | 11.3 | 72.9 | 13,990 | students_per_other_staff high (z=4.8) |
| 1704950 | Bannockburn SD 106 | IL | 148 | 18.8 | 14.2 | 7.9 | 10.4 | 41,649 | exp_per_student high (z=4.8) |
| 1742960 | Wolf Branch SD 113 | IL | 763 | 49.0 | 11.0 | 15.6 | 69.4 | 13,502 | students_per_other_staff high (z=4.7) |
| 1717310 | Grant CCSD 110 | IL | 612 | 42.0 | 9.0 | 14.6 | 68.0 | 14,959 | students_per_other_staff high (z=4.6) |
| 1743800 | Zeigler-Royalton CUSD 188 | IL | 590 | 43.1 | 8.8 | 13.7 | 67.4 | 9,856 | students_per_other_staff high (z=4.6) |
| 1740200 | Venice CUSD 3 | IL | 80 | 12.0 | 5.6 | 6.7 | 14.3 | 39,188 | exp_per_student high (z=4.6) |
| 1739120 | Tolono CUSD 7 | IL | 1,618 | 115.1 | 24.3 | 14.1 | 66.5 | 12,482 | students_per_other_staff high (z=4.6) |
| 1709330 | Cerro Gordo CUSD 100 | IL | 484 | 35.0 | 7.5 | 13.8 | 64.5 | 13,655 | students_per_other_staff high (z=4.5) |
| 1712960 | East Alton SD 13 | IL | 767 | 53.3 | 12.0 | 14.4 | 63.9 | 15,163 | students_per_other_staff high (z=4.5) |
| 1712930 | Earlville CUSD 9 | IL | 411 | 33.6 | 6.6 | 12.2 | 62.3 | 12,112 | students_per_other_staff high (z=4.4) |
| 1712510 | Donovan CUSD 3 | IL | 284 | 25.4 | 4.6 | 11.2 | 62.1 | 12,130 | students_per_other_staff high (z=4.4) |
| 1739660 | Union SD 81 | IL | 103 | 13.4 | 5.5 | 7.7 | 18.7 | 36,650 | exp_per_student high (z=4.3) |
| 1739480 | Tri Point CUSD 6-J | IL | 358 | 36.7 | 5.9 | 9.8 | 60.7 | 20,142 | students_per_other_staff high (z=4.3) |
| 1707740 | Buncombe Cons SD 43 | IL | 60 | 6.0 | 1.0 | 10.0 | 60.0 | 12,850 | students_per_other_staff high (z=4.3) |
| 1701416 | Milford Area PSD 124 | IL | 538 | 50.5 | 9.0 | 10.7 | 59.8 | 16,619 | students_per_other_staff high (z=4.3) |
| 1720970 | Kenilworth SD 38 | IL | 479 | 56.7 | 33.0 | 8.4 | 14.5 | 34,672 | exp_per_student high (z=4.1) |
| 1729420 | Oblong CUSD 4 | IL | 615 | 45.0 | 10.9 | 13.7 | 56.3 | 11,403 | students_per_other_staff high (z=4.1) |
| 1740890 | Warsaw CUSD 316 | IL | 402 | 32.0 | 7.3 | 12.6 | 55.1 | 11,816 | students_per_other_staff high (z=4.0) |
| 1729520 | Odell CCSD 435 | IL | 143 | 16.4 | 2.6 | 8.7 | 55.0 | 14,755 | students_per_other_staff high (z=4.0) |
| 1802160 | Clinton Prairie School Corporation | IN | 1,301 | 68.6 | 23.0 | 19.0 | 56.6 | 8,164 | students_per_other_staff high (z=4.1) |
| 1811730 | Union School Corporation | IN | 3,371 | 143.5 | 96.7 | 23.5 | 34.9 | 4,188 | exp_per_student low (z=-4.1) |
| 2012900 | Weskan | KS | 100 | 18.3 | 8.1 | 5.5 | 12.3 | 17,490 | students_per_teacher low (z=-4.2) |
| 2006510 | Southern Cloud | KS | 171 | 30.7 | 17.1 | 5.6 | 10.0 | 18,088 | students_per_teacher low (z=-4.1) |
| 2504710 | Erving | MA | 128 | 16.2 | 26.6 | 7.9 | 4.8 | 37,211 | exp_per_student high (z=4.4) |
| 2500551 | Greenfield Commonwealth Virtual District | MA | 590 | 37.5 | 10.5 | 15.7 | 56.0 | 9,229 | students_per_other_staff high (z=4.1) |
| 2311820 | RSU 07/MSAD 07 | ME | 60 | 13.2 | 10.1 | 4.5 | 5.9 | 33,883 | students_per_teacher low (z=-5.0); exp_per_student high (z=4.0) |
| 2728350 | PILLAGER PUBLIC SCHOOL DISTRICT | MN | 1,164 | 66.3 | 18.5 | 17.6 | 63.1 | 10,603 | students_per_other_staff high (z=4.4) |
| 2733720 | NETT LAKE PUBLIC SCHOOL DISTRICT | MN | 57 | 8.3 | 14.4 | 6.9 | 3.9 | 34,789 | exp_per_student high (z=4.1) |
| 2917000 | LACLEDE CO. C-5 | MO | 443 | 34.5 | 6.0 | 12.8 | 73.8 | 8,977 | students_per_other_staff high (z=4.9) |
| 2920670 | MEHLVILLE R-IX | MO | 10,308 | 693.4 | 147.1 | 14.9 | 70.1 | 10,069 | students_per_other_staff high (z=4.7) |
| 2922470 | NEWTOWN-HARRIS R-III | MO | 80 | 15.8 | 6.5 | 5.1 | 12.3 | 20,975 | students_per_teacher low (z=-4.5) |
| 2919920 | MALTA BEND R-V | MO | 90 | 17.0 | 14.2 | 5.3 | 6.4 | 19,578 | students_per_teacher low (z=-4.3) |
| 2906150 | COOPER CO. R-IV | MO | 94 | 17.6 | 9.3 | 5.3 | 10.1 | 20,532 | students_per_teacher low (z=-4.3) |
| 2906450 | CAINSVILLE R-I | MO | 78 | 14.5 | 17.2 | 5.4 | 4.5 | 19,038 | students_per_teacher low (z=-4.2) |
| 2909090 | CLARKSBURG C-2 | MO | 54 | 10.0 | 15.0 | 5.4 | 3.6 | 16,574 | students_per_teacher low (z=-4.2) |
| 2913620 | HANCOCK PLACE | MO | 1,490 | 99.5 | 25.6 | 15.0 | 58.2 | 12,001 | students_per_other_staff high (z=4.2) |
| 3027730 | Westby K-12 Schools | MT | 58 | 11.4 | 9.7 | 5.1 | 6.0 | 28,328 | students_per_teacher low (z=-4.5) |
| 3018240 | Melstone Elem | MT | 40 | 7.6 | 3.7 | 5.3 | 10.8 | 21,925 | students_per_teacher low (z=-4.3) |
| 3016290 | Lavina K-12 Schools | MT | 69 | 12.3 | 9.0 | 5.6 | 7.7 | 20,652 | students_per_teacher low (z=-4.0) |
| 3817520 | ST THOMAS 43 | ND | 54 | 11.5 | 9.0 | 4.7 | 6.0 | 26,389 | students_per_teacher low (z=-4.8) |
| 3812720 | MENOKEN 33 | ND | 44 | 4.0 | 0.8 | 11.0 | 58.7 | 11,955 | students_per_other_staff high (z=4.2) |
| 3816470 | SAWYER 16 | ND | 44 | 8.0 | 11.0 | 5.5 | 4.0 | 34,682 | students_per_teacher low (z=-4.1); exp_per_student high (z=4.1) |
| 3173120 | LOUP COUNTY PUBLIC SCHOOLS | NE | 70 | 14.8 | 15.0 | 4.7 | 4.7 | 34,157 | students_per_teacher low (z=-4.8); exp_per_student high (z=4.0) |
| 3173560 | MC PHERSON COUNTY SCHOOLS | NE | 65 | 12.9 | 7.9 | 5.0 | 8.2 | 30,308 | students_per_teacher low (z=-4.5) |
| 3176800 | SIOUX COUNTY PUBLIC SCHOOLS | NE | 100 | 18.7 | 9.5 | 5.4 | 10.5 | 29,520 | students_per_teacher low (z=-4.3) |
| 3178670 | WHEELER CENTRAL SCHOOLS | NE | 99 | 17.6 | 13.8 | 5.6 | 7.1 | 31,455 | students_per_teacher low (z=-4.0) |
| 3305700 | Pittsburg School District | NH | 83 | 16.3 | 16.1 | 5.1 | 5.2 | 32,386 | students_per_teacher low (z=-4.5) |
| 3401290 | Beach Haven School District | NJ | 55 | 12.0 | 3.1 | 4.6 | 17.7 | 38,836 | students_per_teacher low (z=-4.9); exp_per_student high (z=4.5) |
| 3409480 | Mannington Township School District | NJ | 156 | 17.6 | 11.4 | 8.9 | 13.7 | 40,756 | exp_per_student high (z=4.7) |
| 3402610 | Califon Borough School District | NJ | 77 | 15.4 | 8.5 | 5.0 | 9.1 | 37,052 | students_per_teacher low (z=-4.6); exp_per_student high (z=4.4) |
| 3415840 | STOW CREEK TOWNSHIP SCHOOL DISTRICT | NJ | 116 | 22.9 | 11.2 | 5.1 | 10.4 | 21,595 | students_per_teacher low (z=-4.5) |
| 3400870 | Alpine Elementary School District | NJ | 138 | 22.4 | 16.9 | 6.2 | 8.2 | 38,174 | exp_per_student high (z=4.5) |
| 3411670 | North Wildwood School District | NJ | 227 | 33.3 | 30.6 | 6.8 | 7.4 | 34,780 | exp_per_student high (z=4.1) |
| 3409690 | Margate City School District | NJ | 351 | 48.8 | 45.5 | 7.2 | 7.7 | 34,493 | exp_per_student high (z=4.1) |
| 3200420 | PERSHING COUNTY SCHOOL DISTRICT | NV | 658 | 75.0 | 9.0 | 8.8 | 73.1 | 18,427 | students_per_other_staff high (z=4.8) |
| 3200270 | LINCOLN COUNTY SCHOOL DISTRICT | NV | 993 | 89.0 | 15.0 | 11.2 | 66.2 | 15,348 | students_per_other_staff high (z=4.6) |
| 3200180 | EUREKA COUNTY SCHOOL DISTRICT | NV | 321 | 61.0 | 5.0 | 5.3 | 64.2 | 25,287 | students_per_teacher low (z=-4.3); students_per_other_staff high (z=4.5) |
| 3200360 | NYE COUNTY SCHOOL DISTRICT | NV | 5,367 | 341.0 | 85.0 | 15.7 | 63.1 | 12,768 | students_per_other_staff high (z=4.4) |
| 3904750 | Ridgemont Local | OH | 513 | 44.2 | 175.5 | 11.6 | 2.9 | 13,058 | students_per_other_staff low (z=-4.5) |
| 3905009 | Bloomfield-Mespo Local | OH | 228 | 25.3 | 76.9 | 9.0 | 3.0 | 16,197 | students_per_other_staff low (z=-4.5) |
| 3904541 | Hicksville Exempted Village | OH | 907 | 64.9 | 287.4 | 14.0 | 3.2 | 12,389 | students_per_other_staff low (z=-4.3) |
| 4012180 | FREEDOM | OK | 67 | 13.0 | 12.0 | 5.1 | 5.6 | 30,507 | students_per_teacher low (z=-4.4) |
| 4029430 | TALOGA | OK | 96 | 17.1 | 17.2 | 5.6 | 5.6 | 27,510 | students_per_teacher low (z=-4.1) |
| 4400690 | New Shoreham | RI | 133 | 21.6 | 21.0 | 6.2 | 6.3 | 40,083 | exp_per_student high (z=4.7) |
| 4400390 | Foster | RI | 272 | 21.8 | 4.0 | 12.5 | 68.0 | 17,081 | students_per_other_staff high (z=4.6) |
| 4503600 | Spartanburg 05 | SC | 8,802 | 588.3 | 126.1 | 15.0 | 69.8 | 10,406 | students_per_other_staff high (z=4.7) |
| 4503570 | Spartanburg 04 | SC | 2,894 | 167.7 | 46.4 | 17.3 | 62.4 | 9,796 | students_per_other_staff high (z=4.4) |
| 4606960 | Big Stone City School District 25-1 | SD | 67 | 12.8 | 10.6 | 5.2 | 6.3 | 19,075 | students_per_teacher low (z=-4.3) |
| 4822020 | GUTHRIE CSD | TX | 106 | 19.6 | 12.4 | 5.4 | 8.5 | 29,189 | students_per_teacher low (z=-4.2) |
| 4845990 | WILSON ISD | TX | 103 | 18.4 | 18.6 | 5.6 | 5.5 | 21,398 | students_per_teacher low (z=-4.1) |
| 4811040 | BOYS RANCH ISD | TX | 309 | 54.8 | 29.2 | 5.6 | 10.6 | 22,424 | students_per_teacher low (z=-4.0) |
| 4901170 | Wayne District | UT | 487 | 30.4 | 7.0 | 16.0 | 69.5 | 13,304 | students_per_other_staff high (z=4.7) |
| 4900870 | Salt Lake District | UT | 23,165 | 1,120.6 | 342.3 | 20.7 | 67.7 | 9,689 | students_per_other_staff high (z=4.6) |
| 4900720 | Ogden City District | UT | 11,782 | 563.0 | 177.8 | 20.9 | 66.3 | 9,221 | students_per_other_staff high (z=4.6) |
| 4900900 | San Juan District | UT | 3,051 | 171.9 | 46.5 | 17.7 | 65.7 | 13,337 | students_per_other_staff high (z=4.5) |
| 5304150 | LaCrosse School District | WA | 66 | 11.6 | 4.1 | 5.7 | 16.1 | 38,758 | students_per_teacher low (z=-4.0); exp_per_student high (z=4.5) |
| 5309570 | Washtucna School District | WA | 57 | 10.0 | 3.5 | 5.7 | 16.4 | 36,596 | students_per_teacher low (z=-4.0); exp_per_student high (z=4.3) |
| 5303300 | Green Mountain School District | WA | 163 | 8.8 | 2.8 | 18.5 | 58.6 | 11,675 | students_per_other_staff high (z=4.2) |
| 5500840 | Barneveld School District | WI | 438 | 34.1 | 23.1 | 12.8 | 19.0 | 39,785 | exp_per_student high (z=4.6) |
| 5605680 | Sheridan County School District #3 | WY | 93 | 15.2 | 20.6 | 6.1 | 4.5 | 37,108 | exp_per_student high (z=4.4) |

### Between-group summary

- by state: IL 22, MO 8, NJ 7, CT 5, NE 4, NV 4, UT 4, MT 3, ND 3, OH 3, TX 3, WA 3, AL 2, AZ 2, CA 2, IN 2, KS 2, MA 2, MN 2, OK 2, RI 2, SC 2, AR 1, ME 1, NH 1, SD 1, WI 1, WY 1
- students: median 148, min 40, max 23,165; 55 have fewer than 300 students
- by rule: students_per_teacher 36, students_per_other_staff 42, exp_per_student 28

## Students per other-staff FTE by state

National median 13.8, IQR 10.9 to 17.3. Sorted by state median.

| state | n | p25 | median | p75 | flagged by other-staff rule at 5 |
|---|---|---|---|---|---|
| UT | 35 | 82.0 | 89.9 | 110.6 | 30 |
| NV | 17 | 66.2 | 88.4 | 130.1 | 11 |
| WA | 255 | 23.0 | 26.4 | 29.3 | 0 |
| AL | 137 | 18.7 | 21.3 | 24.6 | 0 |
| SC | 68 | 16.7 | 21.3 | 24.4 | 0 |
| ID | 108 | 16.7 | 19.9 | 24.7 | 1 |
| CA | 780 | 14.9 | 18.3 | 21.7 | 4 |
| LA | 70 | 15.1 | 17.4 | 19.3 | 0 |
| MI | 512 | 13.9 | 16.5 | 19.4 | 0 |
| HI | 1 | 16.4 | 16.4 | 16.4 | 0 |
| WI | 408 | 13.9 | 16.0 | 18.3 | 1 |
| MO | 507 | 12.7 | 16.0 | 23.0 | 2 |
| RI | 36 | 12.9 | 15.2 | 17.4 | 0 |
| NC | 115 | 13.1 | 15.1 | 16.8 | 0 |
| PA | 493 | 12.8 | 15.0 | 18.0 | 2 |
| DE | 16 | 13.8 | 15.0 | 17.2 | 0 |
| MA | 268 | 12.6 | 14.9 | 17.1 | 0 |
| OR | 134 | 12.8 | 14.8 | 17.3 | 0 |
| MD | 24 | 14.1 | 14.7 | 15.7 | 0 |
| OK | 499 | 11.7 | 14.4 | 17.3 | 0 |
| FL | 67 | 12.2 | 14.3 | 16.2 | 0 |
| KS | 278 | 11.7 | 14.1 | 16.7 | 0 |
| IL | 751 | 11.2 | 14.0 | 20.2 | 16 |
| MN | 321 | 12.0 | 14.0 | 15.8 | 0 |
| GA | 177 | 12.0 | 13.7 | 15.4 | 0 |
| CO | 125 | 11.4 | 13.7 | 15.9 | 0 |
| AZ | 176 | 10.4 | 13.7 | 16.5 | 3 |
| TX | 993 | 11.5 | 13.4 | 15.5 | 0 |
| MS | 135 | 11.1 | 13.0 | 15.0 | 0 |
| IA | 320 | 11.3 | 13.0 | 14.8 | 0 |
| TN | 141 | 11.4 | 12.9 | 14.9 | 0 |
| MT | 196 | 10.0 | 12.7 | 16.2 | 0 |
| IN | 288 | 9.7 | 12.3 | 15.3 | 14 |
| SD | 145 | 9.9 | 12.3 | 15.4 | 0 |
| AR | 232 | 10.5 | 12.1 | 13.9 | 0 |
| KY | 171 | 11.0 | 12.0 | 13.2 | 0 |
| ND | 143 | 9.2 | 11.8 | 14.1 | 0 |
| NJ | 481 | 9.8 | 11.8 | 13.8 | 0 |
| NE | 239 | 8.8 | 11.0 | 13.1 | 0 |
| NH | 132 | 8.4 | 10.1 | 12.1 | 1 |
| WY | 48 | 7.6 | 9.2 | 10.9 | 0 |
| CT | 156 | 7.9 | 9.2 | 10.5 | 0 |
| ME | 165 | 7.0 | 8.3 | 9.5 | 0 |
| OH | 605 | 5.7 | 7.2 | 9.0 | 1 |
