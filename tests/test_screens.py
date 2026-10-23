"""
Tests for the report-only screens in src/screens.py that need no raw data.
Run from the project root: python -m pytest
"""

import re

import numpy as np
import pandas as pd

import screens


def test_virtual_share_screen_small_case():
    """Three districts: one with a 40 % fully virtual school, one with a
    'virtual with face-to-face options' school at 10 %, one with none."""
    df = pd.DataFrame({"leaid": ["0000001", "0000002", "0000003"],
                       "students": [1000, 1000, 500]})
    schools_m = pd.DataFrame({
        "LEAID":  ["0000001", "0000001", "0000002", "0000002", "0000003"],
        "NCESSCH": list("abcde"),
        "STUDENT_COUNT": [600.0, 400.0, 900.0, 100.0, 500.0],
        "VIRTUAL": ["NOTVIRTUAL", "FULLVIRTUAL", "SUPPVIRTUAL", "FACEVIRTUAL",
                    "MISSING"],
    })
    out = screens.virtual_share_screen(df, schools_m)

    assert list(out.members) == [1000, 1000, 500]
    np.testing.assert_allclose(out.share_full, [0.4, 0.0, 0.0])
    np.testing.assert_allclose(out.share_full_prim, [0.4, 0.1, 0.0])
    assert list(out.members_unknown) == [0, 0, 500]
    # share >= threshold excludes; 10 % counts at the 10 % cut-off
    assert list(out.vs_flag_full_5) == [True, False, False]
    assert list(out.vs_flag_full_prim_10) == [True, True, False]
    assert list(out.vs_flag_full_prim_20) == [True, False, False]
    assert list(out.n_full) == [1, 0, 0] and list(out.n_full_prim) == [1, 1, 0]


def test_virtual_share_screen_district_without_schools_is_not_flagged():
    df = pd.DataFrame({"leaid": ["0000009"], "students": [100]})
    schools_m = pd.DataFrame({"LEAID": ["0000001"], "NCESSCH": ["a"],
                              "STUDENT_COUNT": [100.0], "VIRTUAL": ["FULLVIRTUAL"]})
    out = screens.virtual_share_screen(df, schools_m)
    assert not out.checkable.iloc[0]
    assert not out.vs_flag_full_5.iloc[0]
    assert np.isnan(out.share_full.iloc[0])


def test_virtual_name_proxy_ignores_preschool():
    pat = re.compile(screens.VIRTUAL_NAME_PATTERN, re.I)
    assert pat.search("Andover eCademy")
    assert pat.search("Insight School of Washington Virtual")
    assert pat.search("Denver Online High School")
    assert not pat.search("Northwood Pre-School")
    assert not pat.search("Hilliard City School District Preschool")
