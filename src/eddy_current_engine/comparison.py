"""Load and summarize the calibrated IPT position comparison."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import numpy as np


REQUIRED_COLUMNS = (
    "position_mm",
    "position_uncertainty_mm",
    "theoretical_rad_per_s",
    "theoretical_uncertainty_rad_per_s",
    "experimental_rad_per_s",
    "experimental_uncertainty_rad_per_s",
)


@dataclass(frozen=True)
class PositionComparison:
    """Calibrated theory and experiment evaluated at the same disk positions."""

    position_mm: np.ndarray
    position_uncertainty_mm: np.ndarray
    theoretical_rad_per_s: np.ndarray
    theoretical_uncertainty_rad_per_s: np.ndarray
    experimental_rad_per_s: np.ndarray
    experimental_uncertainty_rad_per_s: np.ndarray


def load_position_comparison(path: str | Path) -> PositionComparison:
    """Read the public position-comparison table and validate its numeric columns."""

    source = Path(path)
    with source.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        missing = set(REQUIRED_COLUMNS).difference(reader.fieldnames or ())
        if missing:
            names = ", ".join(sorted(missing))
            raise ValueError(f"Comparison data is missing columns: {names}")
        rows = list(reader)

    if not rows:
        raise ValueError("Comparison data must contain at least one row")

    values = {
        name: np.asarray([float(row[name]) for row in rows], dtype=float)
        for name in REQUIRED_COLUMNS
    }
    if not all(np.all(np.isfinite(array)) for array in values.values()):
        raise ValueError("Comparison data contains non-finite values")
    if np.any(np.diff(values["position_mm"]) <= 0.0):
        raise ValueError("Comparison positions must be strictly increasing")
    if any(np.any(values[name] < 0.0) for name in REQUIRED_COLUMNS[1:]):
        raise ValueError("Speeds and uncertainties must be non-negative")

    return PositionComparison(**values)


def comparison_statistics(data: PositionComparison) -> dict[str, float | int]:
    """Return compact agreement metrics for the calibrated comparison."""

    residual = data.theoretical_rad_per_s - data.experimental_rad_per_s
    peak_index = int(np.argmax(data.experimental_rad_per_s))
    return {
        "point_count": int(data.position_mm.size),
        "rmse_rad_per_s": float(np.sqrt(np.mean(residual**2))),
        "maximum_absolute_residual_rad_per_s": float(np.max(np.abs(residual))),
        "experimental_peak_position_mm": float(data.position_mm[peak_index]),
        "experimental_peak_speed_rad_per_s": float(data.experimental_rad_per_s[peak_index]),
    }
