"""Publication-style plotting helpers for the eddy-current model."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from .comparison import PositionComparison
from .geometry import GeometryAnalysis


COLORS = {
    "disk_1": "#2563eb",
    "disk_2": "#f59e0b",
    "disk_3": "#dc2626",
    "triple": "#7c3aed",
    "disk_2_disk_3_only": "#10b981",
    "disk_1_disk_2_only": "#06b6d4",
}


def _save(fig: plt.Figure, output: str | Path | None) -> plt.Figure:
    if output is not None:
        path = Path(output)
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, dpi=180, bbox_inches="tight")
    return fig


def plot_geometry(analysis: GeometryAnalysis, output: str | Path | None = None) -> plt.Figure:
    """Plot the three disks and highlight the torque integration regions."""

    fig, ax = plt.subplots(figsize=(7.2, 6.2))
    for index, disk in enumerate(analysis.disks, start=1):
        x, y = disk.exterior.xy
        ax.plot(x, y, color=COLORS[f"disk_{index}"], lw=1.8, label=f"Disk {index}")

    for name, region in analysis.regions.items():
        if region.is_empty:
            continue
        geometries = getattr(region, "geoms", [region])
        for geometry in geometries:
            x, y = geometry.exterior.xy
            ax.fill(x, y, color=COLORS[name], alpha=0.45)
        centroid = analysis.measurements[name].centroid
        ax.scatter(*centroid, s=34, color=COLORS[name], edgecolor="white", zorder=5)

    ax.set(
        xlabel="x (m)",
        ylabel="y (m)",
        title="Three-disk overlap geometry",
        aspect="equal",
    )
    ax.grid(alpha=0.18)
    ax.legend(frameon=False, ncol=3, loc="upper center")
    return _save(fig, output)


def plot_torque_cycle(
    phase_time: np.ndarray,
    torque: np.ndarray,
    average: float,
    output: str | Path | None = None,
) -> plt.Figure:
    """Plot instantaneous torque against electrical-cycle phase."""

    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    ax.plot(phase_time, torque, color="#2563eb", lw=2.0, label="Instantaneous torque")
    ax.axhline(average, color="#dc2626", ls="--", lw=1.7, label="Cycle average")
    ax.set(
        xlabel=r"Electrical phase $\Omega t$ (rad)",
        ylabel="Torque (N m)",
        title="Eddy-current torque over one drive cycle",
    )
    ax.grid(alpha=0.22)
    ax.legend(frameon=False)
    return _save(fig, output)


def plot_phase_response(
    phases: np.ndarray,
    drive: np.ndarray,
    selected_phase: float,
    output: str | Path | None = None,
) -> plt.Figure:
    """Plot the corrected phase-dependent drive response."""

    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    ax.plot(phases, drive, color="#7c3aed", lw=2.2)
    ax.axvline(selected_phase, color="#111827", ls="--", lw=1.4, label="Selected phase")
    ax.set(
        xlabel=r"Relative phase $\phi$ (rad)",
        ylabel="Geometric drive factor",
        title="Phase-dependent drive",
    )
    ax.grid(alpha=0.22)
    ax.legend(frameon=False)
    return _save(fig, output)


def plot_transient(
    time: np.ndarray,
    angular_speed: np.ndarray,
    terminal_speed: float,
    output: str | Path | None = None,
) -> plt.Figure:
    """Plot the normalized first-order rotor transient."""

    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    ax.plot(time, angular_speed, color="#059669", lw=2.2, label=r"$\omega(t)$")
    ax.axhline(terminal_speed, color="#dc2626", ls="--", lw=1.5, label="Terminal speed")
    ax.set(
        xlabel="Time (s)",
        ylabel="Angular speed (rad/s)",
        title="First-order rotor response",
    )
    ax.grid(alpha=0.22)
    ax.legend(frameon=False)
    return _save(fig, output)


def plot_theory_experiment_comparison(
    data: PositionComparison,
    output: str | Path | None = None,
) -> plt.Figure:
    """Plot the calibrated terminal-speed prediction against the measurements."""

    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    ax.errorbar(
        data.position_mm,
        data.theoretical_rad_per_s,
        yerr=data.theoretical_uncertainty_rad_per_s,
        fmt="o",
        ms=5.5,
        color="#111827",
        ecolor="#111827",
        capsize=3.0,
        elinewidth=1.2,
        label=r"Theoretical $\omega_{\max}$ with $\alpha_{\mathrm{fric}}(y)$",
    )
    ax.errorbar(
        data.position_mm,
        data.experimental_rad_per_s,
        yerr=data.experimental_uncertainty_rad_per_s,
        fmt="s",
        ms=5.2,
        color="#dc2626",
        ecolor="#dc2626",
        capsize=3.0,
        elinewidth=1.2,
        label=r"Experimental $\omega_{\max}$",
    )
    ax.set(
        xlabel=r"Disk position $y$ (mm)",
        ylabel=r"Terminal angular speed $\omega_{\max}$ (rad/s)",
        title="Calibrated theory versus experiment",
        xlim=(-2.0, 44.0),
        ylim=(-0.8, 17.0),
    )
    ax.grid(alpha=0.20)
    ax.legend(frameon=False, loc="lower center")
    return _save(fig, output)
