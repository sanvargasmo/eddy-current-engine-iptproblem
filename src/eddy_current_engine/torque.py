"""Torque decomposition and reduced terminal-speed model."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class TorqueCoefficients:
    c11: complex
    c22: complex
    c12: complex
    c21: complex

    def combination(self, phase: np.ndarray | float, field_1: float = 1.0, field_2: float = 1.0):
        return (
            self.c11 * field_1**2
            + self.c22 * field_2**2
            + (self.c12 + self.c21) * field_1 * field_2 * np.cos(phase)
        )


# Computed by the numerical sector integrals in the original notebook.
REFERENCE_COEFFICIENTS = TorqueCoefficients(
    c11=-2.039681546062127e-08 + 8.716743117406581e-23j,
    c22=-1.5005748980207866e-08 + 3.4563715227091387e-22j,
    c12=-2.4629007844518002e-06 + 8.650124211904223e-08j,
    c21=-1.3692936273609294e-06 - 5.538586326887562e-08j,
)


def instantaneous_torque(
    time: np.ndarray | float,
    phase: float,
    drive_angular_frequency: float,
    rotor_speed: float,
    conductivity: float,
    field_1: float,
    field_2: float,
    coefficients: TorqueCoefficients = REFERENCE_COEFFICIENTS,
) -> np.ndarray:
    """Evaluate the real torque over the electrical drive cycle."""

    carrier_1 = np.cos(drive_angular_frequency * np.asarray(time))
    carrier_2 = np.cos(drive_angular_frequency * np.asarray(time) + phase)
    value = conductivity * rotor_speed * (
        coefficients.c11 * field_1**2 * carrier_1**2
        + coefficients.c22 * field_2**2 * carrier_2**2
        + (coefficients.c12 + coefficients.c21) * field_1 * field_2 * carrier_1 * carrier_2
    )
    return np.real(value)


def cycle_average_torque(
    phase: np.ndarray | float,
    rotor_speed: float,
    conductivity: float,
    field_1: float,
    field_2: float,
    coefficients: TorqueCoefficients = REFERENCE_COEFFICIENTS,
) -> np.ndarray:
    """Analytic time average of :func:`instantaneous_torque`."""

    return 0.5 * conductivity * rotor_speed * np.real(
        coefficients.combination(phase, field_1, field_2)
    )


def reduced_terminal_speed(
    phase: np.ndarray | float,
    drive_factor: float,
    overlap_area_1: float,
    overlap_area_2: float,
    drive_angular_frequency: float,
    coefficients: TorqueCoefficients = REFERENCE_COEFFICIENTS,
) -> np.ndarray:
    """Reproduce the notebook's reduced terminal-speed expression.

    Common field, conductivity, and thickness factors cancel in this reduced
    model. The real part is returned because the physical angular speed is real.
    """

    phase_array = np.asarray(phase)
    denominator = coefficients.combination(phase_array)
    numerator = -drive_factor * overlap_area_1 * overlap_area_2 * drive_angular_frequency * np.sin(phase_array)
    with np.errstate(divide="ignore", invalid="ignore"):
        speed = np.real(numerator / denominator)
    return speed
