# Eddy Current Engine - IPT Problem 8

Reproducible Python implementation and experimental summary for the International Physicists' Tournament problem **Eddy Current Engine**. The project separates the measured response, three-disk geometry, phase-dependent electromagnetic drive, induced torque, and rotor dynamics so that each assumption can be inspected independently.

The figures below are the original embedded results from the 60-slide reporter presentation supplied with this project.

## IPT report results

### Measured angular-velocity transient

For a displacement of $y=24\,\mathrm{mm}$ and an input voltage of $V_{\mathrm{in}}=90.0\,\mathrm{V}$, the measured angular speed approaches

$$
\omega_\infty \approx 14.72\,\mathrm{rad\,s^{-1}}.
$$

The exponential fit reported in the presentation has $R^2=0.9909$.

![Measured angular velocity and exponential fit](figures/ipt_angular_velocity_time.jpg)

### Theory versus experiment

The position sweep compares the terminal angular velocity predicted by the model, including the measured position-dependent friction coefficient $\alpha_{\mathrm{fric}}(y)$, against the experimental values. Both exhibit the same non-monotonic dependence on position and locate the high-speed region near $y=18$-$24\,\mathrm{mm}$.

![Theoretical and experimental terminal angular velocity versus position](figures/ipt_theory_experiment.jpg)

### Angular-velocity optimization

The phase sweep shows that the relative phase $\varphi$ and disk position must be optimized together. In the reported parameter sweep, the largest theoretical angular velocity occurs near $y=18\,\mathrm{mm}$ and $\varphi\approx\pi/2$.

![Maximum angular velocity as a function of phase and position](figures/ipt_phase_optimization.jpg)

### Efficiency optimization

The reported efficiency is non-monotonic in magnetic-field amplitude. The model predicts an optimum at

$$
B_{0,\eta_{\max}}=0.0222\,\mathrm{T},
$$

with a peak efficiency of approximately $5.7\%$ for the parameters used in the presentation.

![Efficiency as a function of magnetic-field amplitude](figures/ipt_efficiency_optimization.jpg)

### Spatial current-density result

The analytic current solution produces the asymmetric current pattern responsible for the net torque in the shaded-field geometry.

![Analytic eddy-current density field](figures/ipt_current_density.jpg)

Detailed provenance and the distinction between reported, digitized, and computed quantities are documented in [docs/results_provenance.md](docs/results_provenance.md).

## Geometry used by the numerical model

![Three-disk overlap geometry](figures/geometry.png)

## Model scope

The repository implements four connected components:

1. Polygonally converged overlap areas, centroids, and radial widths for three disks.
2. The complex geometric drive prefactor translated from the original Mathematica expression.
3. Numerical torque coefficients and their instantaneous and cycle-averaged response.
4. A transparent first-order rotor model, $I\dot{\omega}=\tau_{\mathrm{drive}}-\gamma\omega$.

The electromagnetic drive varies with relative phase as

$$
D(\phi)=\operatorname{Re}\!\left(C_D\sin\phi\right),
$$

and the cycle-averaged torque is

$$
\langle\tau\rangle=\frac{\sigma\omega}{2}\operatorname{Re}\!\left[
c_{11}B_1^2+c_{22}B_2^2+(c_{12}+c_{21})B_1B_2\cos\phi
\right].
$$

The reference numerical coefficients are regression-tested against the original sector integrations. They belong to the reference disk geometry. If the disk centers or radii are changed, the geometry and drive factor are updated immediately, but the torque coefficients must be recomputed in `notebooks/Coefficient_Integration.ipynb` before interpreting the torque quantitatively.

## Audit corrections

The source notebooks were reviewed before building this project. Three issues were separated from the validated calculation path:

- A stored “Mathematica comparison” used a different set of disk centers and radii, so it was not a valid cross-check of the Python geometry.
- The original phase sweep loop evaluated a fixed numerical sine in every iteration, producing ten identical curves. The new implementation evaluates the actual phase argument.
- One dynamics notebook mixed dimensional and dimensionless parameter sets and contained a plot label inconsistent with the expression being evaluated. The cleaned project therefore keeps the validated torque calculation and places the rotor transient in an explicit first-order model.

## Installation

```bash
git clone https://github.com/sanvargasmo/eddy-current-engine-iptproblem.git
cd eddy-current-engine-iptproblem
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[test,notebooks]"
```

The installation remains in `.venv` after Ubuntu or the computer is closed. On later sessions, only reactivate it:

```bash
cd ~/eddy-current-engine-iptproblem
source .venv/bin/activate
```

## Run a parameter experiment

```bash
python scripts/run_experiment.py \
  --phase 0.07 \
  --frequency-hz 60 \
  --conductivity 3.195973e7 \
  --field-1 0.006 \
  --field-2 0.006 \
  --rotor-speed 1.0 \
  --time-constant 0.20 \
  --t-final 1.0 \
  --output-dir results/example
```

This creates four figures and a machine-readable `metrics.json`. To inspect all options:

```bash
python scripts/run_experiment.py --help
```

Disk positions and radii are also exposed. For example:

```bash
python scripts/run_experiment.py \
  --disk-2-y -0.011 \
  --disk-3-x 0.024 \
  --output-dir results/changed_geometry
```

The command prints a warning when custom geometry is combined with the stored reference torque coefficients.

## Interactive notebooks

- `notebooks/Parameter_Explorer.ipynb`: the main entry point. All frequently changed physical and numerical parameters are in one cell.
- `notebooks/Coefficient_Integration.ipynb`: full numerical sector integration used to obtain $c_{11},c_{22},c_{12},c_{21}$.
- `notebooks/Analytic_Current_Visualization.ipynb`: Mathematica-to-SymPy translation and spatial current-density snapshots/animation.

Open Jupyter with:

```bash
jupyter lab
```

## Tests

```bash
pytest
```

The tests cover geometry regression, phase variation, analytic versus numerical torque averaging, the reduced-model regression value, rotor dynamics, and a complete command-line smoke test. The reduced value tested internally is a numerical checkpoint for the sector-integral implementation; it is not the calibrated IPT terminal speed reported above.

## Repository structure

```text
eddy-current-engine-iptproblem/
├── src/eddy_current_engine/     # reusable physics modules
├── scripts/run_experiment.py    # command-line parameter runner
├── notebooks/                   # parameter exploration and derivations
├── docs/                        # presentation and result provenance
├── data/                        # reported and audited summary values
├── tests/                       # regression and consistency tests
├── figures/                     # reference outputs used here
└── .github/workflows/tests.yml  # continuous integration
```

No software license has been selected for this repository.
