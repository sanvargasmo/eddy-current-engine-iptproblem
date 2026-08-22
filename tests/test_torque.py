import numpy as np
import pytest

from eddy_current_engine import (
    analyze_geometry,
    cycle_average_torque,
    drive_geometry_factor,
    instantaneous_torque,
    reduced_terminal_speed,
)


def test_cycle_average_matches_numerical_average():
    omega_drive = 2.0 * np.pi * 60.0
    period = 2.0 * np.pi / omega_drive
    time = np.linspace(0.0, period, 20001, endpoint=False)
    kwargs = dict(
        phase=0.37,
        rotor_speed=1.2,
        conductivity=31.95973e6,
        field_1=0.006,
        field_2=0.004,
    )
    instantaneous = instantaneous_torque(time, drive_angular_frequency=omega_drive, **kwargs)
    analytic = cycle_average_torque(**kwargs)
    assert np.mean(instantaneous) == pytest.approx(float(analytic), rel=2e-12)


def test_reference_reduced_terminal_speed():
    measured = analyze_geometry(resolution=256).measurements
    factor = drive_geometry_factor(
        measured["disk_1_disk_2_only"].centroid,
        measured["triple"].centroid,
        0.04,
    ).real
    speed = reduced_terminal_speed(
        0.07,
        factor,
        measured["disk_1_disk_2_only"].area,
        measured["triple"].area,
        2.0 * np.pi * 60.0,
    )
    assert float(speed) == pytest.approx(0.3730732929943495, rel=5e-6)
