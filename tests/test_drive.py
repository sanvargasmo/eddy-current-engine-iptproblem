import numpy as np
import pytest

from eddy_current_engine import analyze_geometry, drive_geometry_factor, phase_drive


def test_reference_drive_factor():
    measured = analyze_geometry(resolution=256).measurements
    factor = drive_geometry_factor(
        measured["disk_1_disk_2_only"].centroid,
        measured["triple"].centroid,
        0.04,
    )
    assert factor.real == pytest.approx(0.02437680566851484, rel=1e-5)
    assert abs(factor.imag) < 1e-14


def test_phase_is_actually_varied():
    phase = np.array([0.0, np.pi / 2.0, np.pi])
    response = phase_drive(2.0, phase)
    assert response == pytest.approx([0.0, 2.0, 0.0], abs=1e-14)
