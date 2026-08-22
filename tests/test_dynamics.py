import numpy as np
import pytest

from eddy_current_engine import FirstOrderRotor, normalized_rotor


def test_first_order_rotor_limits():
    rotor = normalized_rotor(terminal_speed=3.0, time_constant=0.2, initial_speed=0.5)
    assert float(rotor.angular_speed(0.0)) == pytest.approx(0.5)
    assert float(rotor.angular_speed(20.0)) == pytest.approx(3.0)
    assert rotor.time_constant == pytest.approx(0.2)


def test_analytic_solution_satisfies_ode():
    rotor = FirstOrderRotor(inertia=0.4, damping=2.0, drive_torque=6.0)
    time = np.linspace(0.0, 1.0, 2001)
    speed = rotor.angular_speed(time)
    derivative = np.gradient(speed, time)
    residual = rotor.inertia * derivative + rotor.damping * speed - rotor.drive_torque
    assert np.max(np.abs(residual[2:-2])) < 2e-5
