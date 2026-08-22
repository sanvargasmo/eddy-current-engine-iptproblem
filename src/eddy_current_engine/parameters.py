"""Reference parameters for the eddy-current engine model."""

from __future__ import annotations

from dataclasses import dataclass
from math import pi


@dataclass(frozen=True)
class Disk:
    """Circular region in the plane, expressed in SI units."""

    center: tuple[float, float]
    radius: float

    def __post_init__(self) -> None:
        if self.radius <= 0.0:
            raise ValueError("Disk radius must be positive.")


@dataclass(frozen=True)
class GeometryParameters:
    """Three-disk geometry used by the Python torque notebook."""

    disk_1: Disk = Disk((0.0, 0.0), 0.040)
    disk_2: Disk = Disk((0.0, -0.009), (0.02807 + 0.0398) / 2.0)
    disk_3: Disk = Disk((0.021, -0.009), 0.040)
    origin_disk: int = 1

    def __post_init__(self) -> None:
        if self.origin_disk not in (1, 2, 3):
            raise ValueError("origin_disk must be 1, 2, or 3.")

    def disks(self) -> tuple[Disk, Disk, Disk]:
        return self.disk_1, self.disk_2, self.disk_3


@dataclass(frozen=True)
class ElectromagneticParameters:
    """Reference electromagnetic parameters from the validated notebook path."""

    magnetic_field_1: float = 0.006
    magnetic_field_2: float = 0.006
    conductivity: float = 31.95973e6
    drive_frequency_hz: float = 60.0
    rotor_speed: float = 1.0
    disk_radius: float = 0.040
    thickness: float = 0.00172
    overlap_area_1: float = 0.0008429971011798
    overlap_area_2: float = 0.002656629827314824

    def __post_init__(self) -> None:
        positive = {
            "conductivity": self.conductivity,
            "drive_frequency_hz": self.drive_frequency_hz,
            "disk_radius": self.disk_radius,
            "thickness": self.thickness,
            "overlap_area_1": self.overlap_area_1,
            "overlap_area_2": self.overlap_area_2,
        }
        for name, value in positive.items():
            if value <= 0.0:
                raise ValueError(f"{name} must be positive.")

    @property
    def drive_angular_frequency(self) -> float:
        return 2.0 * pi * self.drive_frequency_hz
