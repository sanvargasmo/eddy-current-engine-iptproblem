#!/usr/bin/env python3
"""Run a configurable eddy-current engine experiment."""

from __future__ import annotations

import argparse
import json
from dataclasses import replace
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from eddy_current_engine import (
    Disk,
    ElectromagneticParameters,
    GeometryParameters,
    analyze_geometry,
    cycle_average_torque,
    drive_geometry_factor,
    instantaneous_torque,
    normalized_rotor,
    phase_drive,
    reduced_terminal_speed,
)
from eddy_current_engine.visualization import (
    plot_geometry,
    plot_phase_response,
    plot_torque_cycle,
    plot_transient,
)


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--phase", type=float, default=0.07, help="Relative field phase in radians.")
    result.add_argument("--frequency-hz", type=float, default=60.0, help="Electrical drive frequency.")
    result.add_argument("--conductivity", type=float, default=31.95973e6, help="Conductivity in S/m.")
    result.add_argument("--rotor-speed", type=float, default=1.0, help="Speed used in the torque model (rad/s).")
    result.add_argument("--field-1", type=float, default=0.006, help="First magnetic-field amplitude (T).")
    result.add_argument("--field-2", type=float, default=0.006, help="Second magnetic-field amplitude (T).")
    result.add_argument("--time-constant", type=float, default=0.20, help="Normalized rotor time constant (s).")
    result.add_argument("--t-final", type=float, default=1.0, help="End time of the transient (s).")
    result.add_argument("--points", type=int, default=500, help="Samples per plotted curve.")
    result.add_argument("--geometry-resolution", type=int, default=256, help="Segments per disk quadrant.")
    result.add_argument("--disk-1-x", type=float, default=0.0)
    result.add_argument("--disk-1-y", type=float, default=0.0)
    result.add_argument("--disk-1-radius", type=float, default=0.040)
    result.add_argument("--disk-2-x", type=float, default=0.0)
    result.add_argument("--disk-2-y", type=float, default=-0.009)
    result.add_argument("--disk-2-radius", type=float, default=(0.02807 + 0.0398) / 2.0)
    result.add_argument("--disk-3-x", type=float, default=0.021)
    result.add_argument("--disk-3-y", type=float, default=-0.009)
    result.add_argument("--disk-3-radius", type=float, default=0.040)
    result.add_argument("--output-dir", type=Path, default=Path("results/eddy_current"))
    return result


def run(args: argparse.Namespace) -> dict[str, object]:
    if args.points < 50:
        raise ValueError("--points must be at least 50")
    if args.t_final <= 0.0:
        raise ValueError("--t-final must be positive")

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    reference = ElectromagneticParameters()
    electromagnetic = replace(
        reference,
        drive_frequency_hz=args.frequency_hz,
        conductivity=args.conductivity,
        rotor_speed=args.rotor_speed,
        magnetic_field_1=args.field_1,
        magnetic_field_2=args.field_2,
    )
    geometry_parameters = GeometryParameters(
        disk_1=Disk((args.disk_1_x, args.disk_1_y), args.disk_1_radius),
        disk_2=Disk((args.disk_2_x, args.disk_2_y), args.disk_2_radius),
        disk_3=Disk((args.disk_3_x, args.disk_3_y), args.disk_3_radius),
    )
    geometry = analyze_geometry(geometry_parameters, resolution=args.geometry_resolution)
    measurements = geometry.measurements

    point_1 = measurements["disk_1_disk_2_only"].centroid
    point_2 = measurements["triple"].centroid
    complex_factor = drive_geometry_factor(point_1, point_2, args.disk_1_radius)
    factor = float(np.real(complex_factor))

    terminal_speed = float(
        reduced_terminal_speed(
            args.phase,
            factor,
            measurements["disk_1_disk_2_only"].area,
            measurements["triple"].area,
            electromagnetic.drive_angular_frequency,
        )
    )

    time_cycle = np.linspace(0.0, 2.0 * np.pi / electromagnetic.drive_angular_frequency, args.points)
    torque = instantaneous_torque(
        time_cycle,
        args.phase,
        electromagnetic.drive_angular_frequency,
        electromagnetic.rotor_speed,
        electromagnetic.conductivity,
        electromagnetic.magnetic_field_1,
        electromagnetic.magnetic_field_2,
    )
    average_torque = float(
        cycle_average_torque(
            args.phase,
            electromagnetic.rotor_speed,
            electromagnetic.conductivity,
            electromagnetic.magnetic_field_1,
            electromagnetic.magnetic_field_2,
        )
    )

    phases = np.linspace(-np.pi, np.pi, args.points)
    drive = phase_drive(complex_factor, phases)
    time = np.linspace(0.0, args.t_final, args.points)
    rotor = normalized_rotor(terminal_speed, args.time_constant)
    speed = rotor.angular_speed(time)

    figures = {
        "geometry": output_dir / "geometry.png",
        "phase_response": output_dir / "phase_response.png",
        "torque_cycle": output_dir / "torque_cycle.png",
        "rotor_transient": output_dir / "rotor_transient.png",
    }
    plot_geometry(geometry, figures["geometry"])
    plot_phase_response(phases, drive, args.phase, figures["phase_response"])
    plot_torque_cycle(
        electromagnetic.drive_angular_frequency * time_cycle,
        torque,
        average_torque,
        figures["torque_cycle"],
    )
    plot_transient(time, speed, terminal_speed, figures["rotor_transient"])
    plt.close("all")

    reference_geometry = GeometryParameters()
    coefficients_match_geometry = geometry_parameters == reference_geometry
    metrics: dict[str, float | int | str | bool | dict[str, float]] = {
        "phase_rad": args.phase,
        "frequency_hz": args.frequency_hz,
        "conductivity_s_per_m": args.conductivity,
        "drive_geometry_factor_real": factor,
        "drive_geometry_factor_imag": float(np.imag(complex_factor)),
        "cycle_average_torque_n_m": average_torque,
        "reduced_terminal_speed_rad_per_s": terminal_speed,
        "time_constant_s": args.time_constant,
        "geometry_resolution": args.geometry_resolution,
        "reference_torque_coefficients_match_geometry": coefficients_match_geometry,
        "disk_geometry": {
            "disk_1": {"center": [args.disk_1_x, args.disk_1_y], "radius": args.disk_1_radius},
            "disk_2": {"center": [args.disk_2_x, args.disk_2_y], "radius": args.disk_2_radius},
            "disk_3": {"center": [args.disk_3_x, args.disk_3_y], "radius": args.disk_3_radius},
        },
        "areas_m2": {name: item.area for name, item in measurements.items()},
    }
    (output_dir / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    return metrics


def main() -> None:
    args = parser().parse_args()
    metrics = run(args)
    print(f"Results: {args.output_dir}")
    print(f"Reduced terminal speed: {metrics['reduced_terminal_speed_rad_per_s']:.8g} rad/s")
    print(f"Cycle-average torque: {metrics['cycle_average_torque_n_m']:.8g} N m")
    if not metrics["reference_torque_coefficients_match_geometry"]:
        print("Warning: disk geometry changed; recompute the torque coefficients for quantitative use.")


if __name__ == "__main__":
    main()
