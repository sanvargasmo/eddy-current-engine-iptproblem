import csv
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]


def test_readme_uses_ipt_report_figures():
    readme = (PROJECT / "README.md").read_text(encoding="utf-8")
    figures = [
        "ipt_angular_velocity_time.jpg",
        "ipt_theory_experiment.jpg",
        "ipt_phase_optimization.jpg",
        "ipt_efficiency_optimization.jpg",
        "ipt_current_density.jpg",
    ]
    for filename in figures:
        assert f"figures/{filename}" in readme
        assert (PROJECT / "figures" / filename).stat().st_size > 20_000


def test_readme_uses_github_supported_math_macros():
    readme = (PROJECT / "README.md").read_text(encoding="utf-8")

    assert r"\operatorname" not in readme


def test_readme_preserves_theory_from_ipt_presentation():
    readme = (PROJECT / "README.md").read_text(encoding="utf-8")
    equations = [
        r"\mathbf{J}_{\mathrm{tot}}=\sigma\mathbf{E}_{\mathrm{tot}}",
        r"\tau_{\mathrm{drive}}",
        r"\tau_{\mathrm{damp}}",
        r"\omega_{\max}",
        r"\eta(B_0)",
        r"B_{0,\eta_{\max}}",
    ]

    for equation in equations:
        assert equation in readme


def test_reported_headline_values_are_preserved():
    with (PROJECT / "data" / "ipt_report_summary.csv").open(encoding="utf-8", newline="") as stream:
        values = {row["quantity"]: float(row["value"]) for row in csv.DictReader(stream)}

    assert values["transient_asymptote"] == 14.72
    assert values["transient_fit_r_squared"] == 0.9909
    assert values["optimal_field_for_efficiency"] == 0.0222
