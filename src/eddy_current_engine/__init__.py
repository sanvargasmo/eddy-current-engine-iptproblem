"""Tools for the reduced eddy-current engine model."""

from .comparison import PositionComparison, comparison_statistics, load_position_comparison
from .drive import drive_geometry_factor, phase_drive, polar_coordinates
from .dynamics import FirstOrderRotor, normalized_rotor
from .geometry import GeometryAnalysis, RegionMeasurement, analyze_geometry
from .parameters import Disk, ElectromagneticParameters, GeometryParameters
from .torque import (
    REFERENCE_COEFFICIENTS,
    TorqueCoefficients,
    cycle_average_torque,
    instantaneous_torque,
    reduced_terminal_speed,
)

__all__ = [
    "Disk",
    "ElectromagneticParameters",
    "FirstOrderRotor",
    "GeometryAnalysis",
    "GeometryParameters",
    "PositionComparison",
    "REFERENCE_COEFFICIENTS",
    "RegionMeasurement",
    "TorqueCoefficients",
    "analyze_geometry",
    "cycle_average_torque",
    "comparison_statistics",
    "drive_geometry_factor",
    "instantaneous_torque",
    "load_position_comparison",
    "normalized_rotor",
    "phase_drive",
    "polar_coordinates",
    "reduced_terminal_speed",
]
