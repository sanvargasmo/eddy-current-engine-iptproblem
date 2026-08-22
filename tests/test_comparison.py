from pathlib import Path

import numpy as np

from eddy_current_engine import comparison_statistics, load_position_comparison


def test_public_position_comparison_regression():
    project = Path(__file__).resolve().parents[1]
    data = load_position_comparison(project / "data" / "ipt_position_comparison.csv")

    np.testing.assert_array_equal(data.position_mm, [0, 6, 12, 18, 24, 30, 36, 42])
    assert data.experimental_rad_per_s[4] == 14.72
    assert data.theoretical_rad_per_s[3] == 16.15

    statistics = comparison_statistics(data)
    assert statistics["point_count"] == 8
    assert statistics["experimental_peak_position_mm"] == 18.0
    assert 0.8 < statistics["rmse_rad_per_s"] < 0.9


def test_comparison_positions_must_increase(tmp_path: Path):
    bad = tmp_path / "comparison.csv"
    bad.write_text(
        "position_mm,position_uncertainty_mm,theoretical_rad_per_s,"
        "theoretical_uncertainty_rad_per_s,experimental_rad_per_s,"
        "experimental_uncertainty_rad_per_s\n"
        "1,0,1,0,1,0\n"
        "1,0,1,0,1,0\n",
        encoding="utf-8",
    )

    try:
        load_position_comparison(bad)
    except ValueError as error:
        assert "strictly increasing" in str(error)
    else:
        raise AssertionError("Expected non-increasing comparison data to fail")
