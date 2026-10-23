# Sample flow, school districts 2018-19

Settings: data-quality threshold 5, state rule on, virtual threshold 10 %. Each row removes districts given the rules above it; 'standalone' counts are flags evaluated on the sample after the data-quality screen, so the difference is the overlap with earlier rules.

| step | removed | remaining | note |
|---|---|---|---|
| merged (directory, staff, finance, scores) | 0 | 11,252 |  |
| complete DEA variables | 273 | 10,979 |  |
| strictly positive DEA variables | 11 | 10,968 |  |
| state comparability rule (UT, NV) | 52 | 10,916 | other staff reported on a different basis |
| data-quality screen (|robust z| <= 5) | 67 | 10,849 | implausible input ratios |
| temporal consistency screen | 33 | 10,816 | FY2019 one-year spike or dip in F-33 |
| enrollment consistency screen (variant B, high side) | 106 | 10,710 | V33 high vs SEDA grade 3-8 enrollment; standalone on the post-DQ sample 107, of which 0 already removed |
| virtual-school share (FULLVIRTUAL >= 10 %) | 30 | 10,680 | standalone on the post-DQ sample 39, of which 9 already removed |
