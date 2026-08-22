"""Phase-dependent drive term translated from the Mathematica expression."""

from __future__ import annotations

import numpy as np


def polar_coordinates(point: tuple[float, float]) -> tuple[float, float]:
    radius = float(np.hypot(*point))
    angle = float(np.mod(np.arctan2(point[1], point[0]), 2.0 * np.pi))
    return radius, angle


def drive_geometry_factor(
    point_1: tuple[float, float],
    point_2: tuple[float, float],
    disk_radius: float,
) -> complex:
    """Return the complex geometric prefactor multiplying ``sin(phase)``."""

    if disk_radius <= 0.0:
        raise ValueError("disk_radius must be positive")

    rho_1, theta_1 = polar_coordinates(point_1)
    rho_2, theta_2 = polar_coordinates(point_2)
    imaginary = 1j

    numerator = (
        imaginary
        * np.exp(imaginary * (theta_1 + theta_2))
        * (-np.exp(2.0 * imaginary * theta_1) + np.exp(2.0 * imaginary * theta_2))
        * rho_1
        * (-disk_radius**2 + rho_1**2)
        * rho_2
        * (disk_radius**2 - rho_2**2)
    )
    denominator = (
        4.0
        * np.pi
        * (-np.exp(imaginary * theta_2) * disk_radius**2 + np.exp(imaginary * theta_1) * rho_1 * rho_2)
        * (np.exp(imaginary * theta_1) * disk_radius**2 - np.exp(imaginary * theta_2) * rho_1 * rho_2)
        * (
            np.exp(2.0 * imaginary * theta_1) * rho_1 * rho_2
            + np.exp(2.0 * imaginary * theta_2) * rho_1 * rho_2
            - np.exp(imaginary * (theta_1 + theta_2)) * (rho_1**2 + rho_2**2)
        )
    )
    if abs(denominator) <= np.finfo(float).tiny:
        raise ValueError("The selected points produce a singular drive factor.")
    return complex(numerator / denominator)


def phase_drive(factor: complex, phase: np.ndarray | float) -> np.ndarray:
    """Evaluate the real phase-dependent drive response."""

    return np.real(factor * np.sin(phase))
