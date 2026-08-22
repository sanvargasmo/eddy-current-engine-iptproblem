# Result provenance

The README result figures were extracted losslessly from the embedded images in `eddy_current_engine_report.pdf`, supplied by Santiago Vargas Mora. They correspond to the following presentation slides:

| Repository figure | Slide | Reported content |
| --- | ---: | --- |
| `ipt_angular_velocity_time.jpg` | 20 | Measured angular velocity at $y=24\,\mathrm{mm}$ and $V_{\mathrm{in}}=90.0\,\mathrm{V}$, exponential fit, $R^2=0.9909$, and asymptote $L\approx14.72\,\mathrm{rad\,s^{-1}}$ |
| `ipt_theory_experiment.jpg` | 36 | Theoretical and experimental terminal angular velocity versus displacement $y$ |
| `ipt_phase_optimization.jpg` | 37 | Theoretical $\omega_{\max}(\varphi)$ for seven disk positions |
| `ipt_efficiency_optimization.jpg` | 39 | Model efficiency versus field amplitude and optimum $B_0=0.0222\,\mathrm{T}$ |
| `ipt_current_density.jpg` | 40 | Spatial analytic current-density field over one magnetic-field period |

## Interpretation boundary

The report combines three evidence levels:

1. **Measured:** the transient angular-velocity points and the experimental points in the position comparison.
2. **Calibrated theory:** the position and phase sweeps, which use the geometric model together with experimentally determined friction.
3. **Analytic field calculation:** the current-density field and sector-integrated torque coefficients.

The reusable package and notebooks reproduce the analytic geometry, drive, current-density, torque, and reduced dynamics calculations. The images above remain the canonical record of the final IPT calibration shown by the reporter. The command-line example is an exploratory reduced model and should not be confused with the presentation's calibrated $14.72\,\mathrm{rad\,s^{-1}}$ result.

## Audited experimental source

The associated experimental workbooks in the private project Drive include position-dependent friction fits. They were reviewed to confirm that the report's position comparison includes measured friction rather than the uncalibrated first-order demonstration originally shown in this repository. The private raw measurements are intentionally not duplicated in this public repository.
