"""
Tests for the run-to-run comparison in src/dea.py (synthetic frames, no data).
"""

import json

import pandas as pd

import dea


def _frame(rows):
    cols = ["leaid", "district_name", "state", "theta_ccr", "theta_bcc",
            "scale_eff", "peers"]
    df = pd.DataFrame(rows, columns=cols)
    df["super_eff"] = float("nan")
    df["peer_count"] = 0
    df["n_peers"] = df.peers.map(lambda j: len(json.loads(j)))
    return df


def test_efficiency_change_section_tracks_departed_peer():
    old = _frame([
        ("0000001", "Alpha", "AA", 1.0, 1.0, 1.0, json.dumps({"0000001": 1.0})),
        ("0000002", "Beta", "BB", 0.5, 0.6, 0.5 / 0.6, json.dumps({"0000001": 0.5})),
        ("0000003", "Gamma", "CC", 0.8, 0.9, 0.8 / 0.9, json.dumps({"0000004": 0.8})),
        ("0000004", "Delta", "DD", 1.0, 1.0, 1.0, json.dumps({"0000004": 1.0})),
    ])
    # Alpha was excluded; Beta, who used Alpha, rises; Gamma is unchanged;
    # Delta stays efficient.
    new = _frame([
        ("0000002", "Beta", "BB", 0.7, 0.75, 0.7 / 0.75, json.dumps({"0000004": 0.7})),
        ("0000003", "Gamma", "CC", 0.8, 0.9, 0.8 / 0.9, json.dumps({"0000004": 0.8})),
        ("0000004", "Delta", "DD", 1.0, 1.0, 1.0, json.dumps({"0000004": 1.0})),
    ])
    text = "\n".join(dea.efficiency_change_section(new, old, "old.csv"))
    assert "no longer in the sample (1): Alpha (AA, 0000001)" in text
    assert "no longer efficient (0): none" in text
    assert "newly efficient (0): none" in text
    # Beta is the one unit that used Alpha: median change +0.2
    assert "| Alpha (AA) | 1 | 0.5000 | 0.7000 | +0.2000 |" in text
    assert "| no departed peer | 2 |" in text
    assert "common units" in text and "Spearman theta_CCR" in text
    assert "units with a lower theta: 0" in text
