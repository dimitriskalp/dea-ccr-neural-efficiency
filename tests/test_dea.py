"""
Tests for src/dea.py.

Small hand-computed cases, a duality check against the multiplier form,
unit invariance, and sanity properties on a seeded subset of the real data.
Run from the project root: python -m pytest
"""

from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from scipy.optimize import linprog

import dea
from build_dataset import DEA_INPUTS, DEA_OUTPUTS

TOL = dea.EFF_TOL
DATA = Path(__file__).resolve().parents[1] / "data/processed/dea_districts_2019.csv"
needs_data = pytest.mark.skipif(not DATA.exists(), reason="dataset not built")


# ---------------------------------------------------------------------------
# Hand-computed cases
# ---------------------------------------------------------------------------

def test_one_input_one_output_matches_ratio_formula():
    """With one input and one output, theta_i = (y_i/x_i) / max_j (y_j/x_j)."""
    rng = np.random.default_rng(0)
    x = rng.uniform(1, 100, size=40)
    y = rng.uniform(1, 100, size=40)
    res = dea.run_dea(x[:, None], y[:, None], model="ccr", verbose=False)
    ratio = y / x
    expected = ratio / ratio.max()
    np.testing.assert_allclose(res["theta_ccr"], expected, atol=1e-8)
    assert res["efficient_ccr"].sum() == 1
    assert res["strongly_efficient"].sum() == 1


def test_two_inputs_one_output_hand_example():
    """Two inputs, one output equal to 1 for every unit.

    Units (x1, x2):  A(1,4)  B(2,2)  C(4,1)  D(4,4)  E(3,3)  F(1,6)

    The efficient frontier is A-B-C.  Radial contraction towards the origin:
      D = (4,4): theta*(4,4) hits B at theta = 0.5       -> peer B, lambda 1
      E = (3,3): theta*(3,3) hits B at theta = 2/3       -> peer B, lambda 1
      F = (1,6): x1 cannot fall below 1 (no unit has x1 < 1 and every unit
                 needs sum(lambda) >= 1 to produce y = 1), so theta = 1, but
                 A = (1,4) uses 2 fewer units of x2: input slack (0, 2).
                 F is weakly efficient: theta = 1 and NOT strongly efficient.
    Because every output equals 1, CRS and VRS coincide here, so
    theta_BCC = theta_CCR and scale efficiency = 1 for every unit.
    """
    X = np.array([[1, 4], [2, 2], [4, 1], [4, 4], [3, 3], [1, 6]], float)
    Y = np.ones((6, 1))
    res = dea.run_dea(X, Y, model="all", verbose=False)

    np.testing.assert_allclose(res["theta_ccr"], [1, 1, 1, 0.5, 2 / 3, 1],
                               atol=1e-8)
    np.testing.assert_allclose(res["theta_bcc"], res["theta_ccr"], atol=1e-8)
    np.testing.assert_allclose(res["scale_eff"], 1.0, atol=1e-8)

    assert list(res["strongly_efficient"]) == [True, True, True, False, False,
                                               False]
    assert res["efficient_ccr"][5] and not res["strongly_efficient"][5]
    np.testing.assert_allclose(res["slack_in"][5], [0.0, 2.0], atol=1e-7)
    np.testing.assert_allclose(res["slack_in"][:3], 0.0, atol=1e-7)

    # Peers of D and E: only B (index 1), with lambda = 1.
    for o in (3, 4):
        assert list(res["peers"][o]) == [1]
        assert abs(res["lambda"][o, 1] - 1.0) < 1e-7
    assert list(res["peers"][5]) == [0]            # F is projected onto A
    assert res["peer_count"][1] == 2               # B serves D and E
    assert res["peer_count"][0] == 1               # A serves F
    assert res["peer_count"][3] == 0

    # Super-efficiency: defined for the theta = 1 units, NaN otherwise.
    assert np.isnan(res["super_eff"][3]) and np.isnan(res["super_eff"][4])
    assert np.all(res["super_eff"][[0, 1, 2]] >= 1 - TOL)
    # B without itself: (2,2) vs the A-C hull; 0.5*A + 0.5*C = (2.5, 2.5)
    # gives theta = 1.25.
    assert abs(res["super_eff"][1] - 1.25) < 1e-7
    # F without itself is still dominated by A at theta = 1.
    assert abs(res["super_eff"][5] - 1.0) < 1e-7


# ---------------------------------------------------------------------------
# Real data
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def sample():
    df = dea.load_data(DATA, sample=300, seed=1)
    return df, df[DEA_INPUTS].to_numpy(float), df[DEA_OUTPUTS].to_numpy(float)


@pytest.fixture(scope="module")
def sample_result(sample):
    _, X, Y = sample
    return dea.run_dea(X, Y, model="all", verbose=False)


def ccr_multiplier(X: np.ndarray, Y: np.ndarray, o: int) -> float:
    """CCR multiplier (dual) form for unit o.

        max  u . y_o
        s.t. v . x_o = 1
             u . y_j - v . x_j <= 0   for all j
             u, v >= 0
    """
    n, m = X.shape
    s = Y.shape[1]
    c = np.concatenate([np.zeros(m), -Y[o]])            # maximise u.y_o
    A_ub = np.hstack([-X, Y])                           # (n, m + s)
    b_ub = np.zeros(n)
    A_eq = np.concatenate([X[o], np.zeros(s)])[None, :]
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=[1.0],
                  bounds=(0, None), method="highs")
    assert res.status == 0, res.message
    return -res.fun


@needs_data
def test_duality_envelopment_equals_multiplier(sample, sample_result):
    """Strong LP duality: both forms must give the same optimal value."""
    _, X, Y = sample
    Xs, _ = dea.rescale(X)
    Ys, _ = dea.rescale(Y)
    rng = np.random.default_rng(7)
    for o in rng.choice(len(X), size=25, replace=False):
        dual = ccr_multiplier(Xs, Ys, o)
        assert abs(dual - sample_result["theta_ccr"][o]) < 1e-7, o


@needs_data
@pytest.mark.parametrize("which,col", [("X", 0), ("X", 1), ("X", 2),
                                       ("Y", 0), ("Y", 1)])
def test_unit_invariance_times_1000(sample, sample_result, which, col):
    """Multiplying any single column by 1000 leaves every theta unchanged."""
    _, X, Y = sample
    X2, Y2 = X.copy(), Y.copy()
    (X2 if which == "X" else Y2)[:, col] *= 1000.0
    res = dea.run_dea(X2, Y2, model="all", verbose=False)
    np.testing.assert_allclose(res["theta_ccr"], sample_result["theta_ccr"],
                               atol=1e-7)
    np.testing.assert_allclose(res["theta_bcc"], sample_result["theta_bcc"],
                               atol=1e-7)


@needs_data
def test_rescaling_does_not_change_scores(sample, sample_result):
    """Solving on raw units (dollars ~1e8) gives the same theta as rescaled."""
    _, X, Y = sample
    raw = dea.run_dea(X, Y, model="all", do_rescale=False, verbose=False)
    np.testing.assert_allclose(raw["theta_ccr"], sample_result["theta_ccr"],
                               atol=1e-7)
    np.testing.assert_allclose(raw["theta_bcc"], sample_result["theta_bcc"],
                               atol=1e-7)
    # The phase-2 objective "maximise the sum of slacks" weighs dollars and
    # FTE differently depending on units, so the slack VALUES may come from a
    # different optimal projection. What theory guarantees invariant is the
    # efficiency classification: theta and whether all slacks are zero.
    np.testing.assert_array_equal(raw["strongly_efficient"],
                                  sample_result["strongly_efficient"])
    np.testing.assert_array_equal(raw["efficient_ccr"],
                                  sample_result["efficient_ccr"])


@needs_data
def test_properties(sample_result):
    r = sample_result
    th_c, th_b = r["theta_ccr"], r["theta_bcc"]
    assert np.all(np.isfinite(th_c)) and np.all(np.isfinite(th_b))
    assert np.all(th_c > 0) and np.all(th_c <= 1 + TOL)
    assert np.all(th_b > 0) and np.all(th_b <= 1 + TOL)
    assert r["efficient_ccr"].sum() >= 1
    assert np.all(th_c <= th_b + TOL)                 # CRS frontier dominates
    assert np.all(r["scale_eff"] <= 1 + TOL)
    eff = r["efficient_ccr"]
    assert np.all(r["super_eff"][eff] >= 1 - TOL)
    assert np.all(np.isnan(r["super_eff"][~eff]))
    assert np.all(r["slack_in"] >= -1e-6) and np.all(r["slack_out"] >= -1e-6)
    assert all(s == "optimal" for s in r["status_ccr_p1"])
    assert all(s == "optimal" for s in r["status_ccr_p2"])
    assert all(s == "optimal" for s in r["status_bcc"])
    # Every inefficient unit has at least one peer; peer_count sums match.
    assert np.all(r["n_peers"] >= 1)
    assert r["peer_count"].sum() == sum(
        len(p[p != o]) for o, p in enumerate(r["peers"]))


@needs_data
def test_parallel_equals_serial(sample, sample_result):
    _, X, Y = sample
    par = dea.run_dea(X, Y, model="all", n_jobs=2, verbose=False)
    for key in ("theta_ccr", "theta_bcc", "super_eff", "slack_in"):
        np.testing.assert_array_equal(par[key], sample_result[key])
    assert par["status_ccr_p1"] == sample_result["status_ccr_p1"]


@needs_data
def test_results_frame_columns_and_peers_json(sample, sample_result):
    import json
    df, _, _ = sample
    tbl = dea.results_frame(df, sample_result)
    assert len(tbl) == len(df) and tbl["leaid"].str.len().eq(7).all()
    for v in DEA_INPUTS + DEA_OUTPUTS:
        assert f"slack_{v}" in tbl
    peers = json.loads(tbl["peers"].iloc[0])
    assert len(peers) == tbl["n_peers"].iloc[0]
    assert all(len(k) == 7 for k in peers)
    assert tbl["strongly_efficient"].dtype == bool


def test_failed_lp_is_recorded_not_dropped(monkeypatch):
    """If the solver reports a failure, the unit stays with NaN and a status."""
    import types

    real = dea._solve
    calls = {"n": 0}

    def flaky(**kw):
        calls["n"] += 1
        if calls["n"] == 2:                   # second LP "fails"
            return types.SimpleNamespace(status=4, x=None, fun=None,
                                         message="numerical")
        return real(**kw)

    monkeypatch.setattr(dea, "_solve", flaky)
    X = np.array([[1.0], [2.0], [3.0]])
    Y = np.array([[1.0], [1.0], [1.0]])
    res = dea.run_dea(X, Y, model="ccr", verbose=False)
    assert res["n"] == 3 and len(res["theta_ccr"]) == 3
    assert np.isnan(res["theta_ccr"][1])
    assert res["status_ccr_p1"][1] == "numerical_difficulties"
    assert res["status_ccr_p2"][1] == dea.SKIPPED
    assert res["status_ccr_p1"][0] == "optimal"
