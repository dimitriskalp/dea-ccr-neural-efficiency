# Sample diagnostics: where the exclusions fall

Base: 10,916 districts after the state rule (UT, NV removed); 236 excluded by the four later rules, 10,680 retained. Report only.

## Districts removed per state

Share = removed / districts after the state rule. States losing more than 5 % are flagged: KS (18 of 278, 6.5 %), IN (15 of 288, 5.2 %).

| state | districts | removed | share removed | data-quality screen | temporal consistency | enrollment consistency | virtual-school share | flag |
|---|---|---|---|---|---|---|---|---|
| KS | 278 | 18 | 6.5% | 2 | 0 | 11 | 5 | > 5 % |
| IN | 288 | 15 | 5.2% | 14 | 0 | 0 | 1 | > 5 % |
| NJ | 481 | 24 | 5.0% | 3 | 2 | 19 | 0 |  |
| CO | 125 | 6 | 4.8% | 1 | 0 | 4 | 1 |  |
| IL | 751 | 33 | 4.4% | 18 | 11 | 4 | 0 |  |
| AZ | 176 | 7 | 4.0% | 4 | 2 | 1 | 0 |  |
| NH | 132 | 5 | 3.8% | 2 | 1 | 2 | 0 |  |
| MO | 507 | 15 | 3.0% | 5 | 1 | 9 | 0 |  |
| AL | 137 | 4 | 2.9% | 0 | 0 | 0 | 4 |  |
| ID | 108 | 3 | 2.8% | 1 | 0 | 0 | 2 |  |
| WA | 255 | 7 | 2.7% | 1 | 3 | 3 | 0 |  |
| ME | 165 | 4 | 2.4% | 0 | 0 | 4 | 0 |  |
| OK | 499 | 12 | 2.4% | 0 | 2 | 10 | 0 |  |
| CA | 780 | 18 | 2.3% | 8 | 4 | 6 | 0 |  |
| WI | 408 | 9 | 2.2% | 1 | 2 | 3 | 3 |  |
| IA | 320 | 7 | 2.2% | 0 | 0 | 5 | 2 |  |
| TN | 141 | 3 | 2.1% | 0 | 0 | 2 | 1 |  |
| ND | 143 | 3 | 2.1% | 2 | 0 | 1 | 0 |  |
| WY | 48 | 1 | 2.1% | 0 | 0 | 1 | 0 |  |
| MN | 321 | 6 | 1.9% | 1 | 0 | 2 | 3 |  |
| MI | 512 | 9 | 1.8% | 0 | 0 | 5 | 4 |  |
| MA | 268 | 4 | 1.5% | 1 | 0 | 2 | 1 |  |
| NE | 239 | 3 | 1.3% | 0 | 0 | 3 | 0 |  |
| MT | 196 | 2 | 1.0% | 0 | 2 | 0 | 0 |  |
| TX | 993 | 9 | 0.9% | 0 | 3 | 4 | 2 |  |
| PA | 493 | 4 | 0.8% | 2 | 0 | 2 | 0 |  |
| OR | 134 | 1 | 0.7% | 0 | 0 | 0 | 1 |  |
| SD | 145 | 1 | 0.7% | 0 | 0 | 1 | 0 |  |
| CT | 156 | 1 | 0.6% | 0 | 0 | 1 | 0 |  |
| GA | 177 | 1 | 0.6% | 0 | 0 | 1 | 0 |  |
| OH | 605 | 1 | 0.2% | 1 | 0 | 0 | 0 |  |
| FL | 67 | 0 | 0.0% | 0 | 0 | 0 | 0 |  |
| DE | 16 | 0 | 0.0% | 0 | 0 | 0 | 0 |  |
| AR | 232 | 0 | 0.0% | 0 | 0 | 0 | 0 |  |
| HI | 1 | 0 | 0.0% | 0 | 0 | 0 | 0 |  |
| NC | 115 | 0 | 0.0% | 0 | 0 | 0 | 0 |  |
| MD | 24 | 0 | 0.0% | 0 | 0 | 0 | 0 |  |
| LA | 70 | 0 | 0.0% | 0 | 0 | 0 | 0 |  |
| KY | 171 | 0 | 0.0% | 0 | 0 | 0 | 0 |  |
| MS | 135 | 0 | 0.0% | 0 | 0 | 0 | 0 |  |
| RI | 36 | 0 | 0.0% | 0 | 0 | 0 | 0 |  |
| SC | 68 | 0 | 0.0% | 0 | 0 | 0 | 0 |  |

## Enrollment (fall membership) of excluded vs retained districts

| group | n | median | q25 | q75 | min | max |
|---|---|---|---|---|---|---|
| retained | 10,680 | 1,207 | 481 | 3,121 | 30 | 495,255 |
| excluded (all rules) | 236 | 500 | 184 | 1,528 | 34 | 34,528 |
| data-quality screen | 67 | 440 | 142 | 1,338 | 36 | 15,772 |
| temporal consistency | 33 | 167 | 73 | 438 | 34 | 6,835 |
| enrollment consistency | 106 | 465 | 212 | 1,503 | 55 | 34,528 |
| virtual-school share | 30 | 2,406 | 1,053 | 4,413 | 265 | 10,612 |

## Locale of excluded vs retained districts

Locale comes from the SEDA covariates (share of pupils in urban, suburban, town and rural schools); the CCD LEA directory for 2018-19 has no locale field. 'Dominant' is the locale with the largest share. 0 districts of the base have no locale covariates.

| group | n with locale | urban (dominant) | suburb (dominant) | town (dominant) | rural (dominant) | mean urban share | mean suburb share | mean town share | mean rural share |
|---|---|---|---|---|---|---|---|---|---|
| retained | 10,680 | 5.8% | 23.4% | 18.7% | 52.1% | 5.6% | 22.6% | 18.2% | 53.6% |
| excluded (all rules) | 236 | 3.0% | 19.9% | 16.5% | 60.6% | 2.9% | 19.7% | 16.1% | 61.4% |
| data-quality screen | 67 | 7.5% | 20.9% | 16.4% | 55.2% | 6.2% | 20.5% | 16.7% | 56.6% |
| temporal consistency | 33 | 0.0% | 12.1% | 12.1% | 75.8% | 0.0% | 12.1% | 14.1% | 73.7% |
| enrollment consistency | 106 | 1.9% | 22.6% | 12.3% | 63.2% | 2.4% | 22.3% | 11.1% | 64.2% |
| virtual-school share | 30 | 0.0% | 16.7% | 36.7% | 46.7% | 0.2% | 16.9% | 34.5% | 48.5% |

## Data-quality exclusions in IN

14 of the 288 IN districts after the state rule are removed by the data-quality screen, all by `students_per_other_staff` and all on the high side (robust z 5.4 to 7.0); their other two ratios are unremarkable.

| ratio | national median | IN median | z of state median | rank of state median | IN IQR (log) | national IQR (log) | flagged high / low |
|---|---|---|---|---|---|---|---|
| students_per_teacher | 14.26 | 16.42 | +0.61 | 11 of 42 | 0.185 | 0.310 | 0 / 0 |
| students_per_other_staff | 13.81 | 12.34 | -0.33 | 31 of 42 | 0.452 | 0.460 | 14 / 0 |
| exp_per_student | 12,009.61 | 9,803.60 | -0.78 | 37 of 42 | 0.138 | 0.364 | 0 / 0 |

The state median of `students_per_other_staff` is close to the national median (z -0.33) and the within-state spread matches the national one, so unlike Utah and Nevada, IN does not report the input on a different basis. What it has is a one-sided tail: within IN the robust z of this ratio exceeds 3 for 17 districts, 4 for 15 and 5 for 14, with none below -3 (state median z -0.33, maximum +7.02). The flagged districts report 3 to 49 other-staff FTE against 18 to 303 teacher FTE, and 93% of them report a whole number of other-staff FTE against 26% of the other IN districts, which points to partial reporting of the non-teaching categories by those districts rather than to a state convention. The screen is doing what it should: removing individual districts with an implausible input, not a state.
