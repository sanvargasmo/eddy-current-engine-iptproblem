"""First-order rotor dynamics under constant drive and linear eddy damping."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class FirstOrderRotor:
    inertia: float
    damping: float
    drive_torque: float
    initial_speed: float = 0.0
    initial_angle: float = 0.0

    def __post_init__(self) -> None:
        if self.inertia <= 0.0:
            raise ValueError("inertia must be positive")
        if self.damping <= 0.0:
            raise ValueError("damping must be positive")

    @property
    def terminal_speed(self) -> float:
        return self.drive_torque / self.damping

    @property
    def time_constant(self) -> float:
        return self.inertia / self.damping

    def angular_speed(self, time: np.ndarray | float) -> np.ndarray:
        time_array = np.asarray(time, dtype=float)
        if np.any(time_array < 0.0):
            raise ValueError("time must be non-negative")
        return self.terminal_speed + (self.initial_speed - self.terminal_speed) * np.exp(
            -time_array / self.time_constant
        )

    def angle(self, time: np.ndarray | float) -> np.ndarray:
        time_array = np.asarray(time, dtype=float)
        if np.any(time_array < 0.0):
            raise ValueError("time must be non-negative")
        return (
            self.initial_angle
            + self.terminal_speed * time_array
            + (self.initial_speed - self.terminal_speed)
            * self.time_constant
            * (1.0 - np.exp(-time_array / self.time_constant))
        )


def normalized_rotor(terminal_speed: float, time_constant: float, initial_speed: float = 0.0) -> FirstOrderRotor:
    """Construct a rotor with unit inertia for normalized transient studies."""

    if time_constant <= 0.0:
        raise ValueError("time_constant must be positive")
    damping = 1.0 / time_constant
    return FirstOrderRotor(1.0, damping, damping * terminal_speed, initial_speed)
