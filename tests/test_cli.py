import json
import os
import subprocess
import sys
from pathlib import Path


def test_cli_smoke(tmp_path: Path):
    project = Path(__file__).resolve().parents[1]
    output = tmp_path / "result"
    environment = os.environ.copy()
    environment["MPLBACKEND"] = "Agg"
    completed = subprocess.run(
        [
            sys.executable,
            str(project / "scripts" / "run_experiment.py"),
            "--points",
            "60",
            "--geometry-resolution",
            "32",
            "--output-dir",
            str(output),
        ],
        cwd=project,
        env=environment,
        check=True,
        capture_output=True,
        text=True,
    )
    metrics = json.loads((output / "metrics.json").read_text(encoding="utf-8"))
    assert "Results:" in completed.stdout
    assert metrics["reduced_terminal_speed_rad_per_s"] > 0.0
    assert len(list(output.glob("*.png"))) == 5
    assert (output / "theory_vs_experiment.png").stat().st_size > 0
    comparison = metrics["theory_experiment_comparison"]
    assert comparison["point_count"] == 8
    assert comparison["experimental_peak_position_mm"] == 18.0
