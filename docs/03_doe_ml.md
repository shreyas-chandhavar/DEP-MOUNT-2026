# 03 — Physics-based DOE and surrogate modelling

## Study objective

Investigate whether alternative adapter/joint geometry could reduce analytical mass without losing stiffness or failing basic geometry and fastening feasibility gates.

### Recorded analytical screening

- **800** candidate configurations screened using a project-defined analytical model.
- **179** conditionally passed the combined proxy gates.
- Failure gates included geometry/legacy constraints, rigidity, flange/bolt edge, clamp depth, thread coverage and related hardware accessibility proxies.
- **25,000** additional machine-learning candidate predictions were screened; a subset of **3,796** passed heuristic guard-band criteria, but these were **not physical or CAD/contact verified passes**.
- A highlighted conditional DOE-212 candidate had motor-adapter **OD ≈146.918 mm, ID ≈92.964 mm, mass ≈412.752 g and rigidity proxy ≈0.845**.

### What the recovered dataset itself establishes

The committed CSV contains exactly **800** distinct indexed analytical rows (0–799), with **379 rows** marked as passing the dataset's *single geometry/stiffness gate*. This is **not** interchangeable with the independently reported **179 full conditional multi-constraint passes**. No single-field count is presented as the final joint screening outcome.

### Why no automatic low-mass release?

A near-perfect mass/rigidity regression metric was recorded, but the **thread-coverage model had held-out R² approximately 0.9901 and two false-pass errors at an acceptance threshold**. The screening model is a predictor of an underlying analytical proxy, not a substitute for actual fastener/contact mechanics.

The conditional **412.75 g** candidate therefore was **not** implemented in the native J3 assembly. The current **Ø152 / Ø88 mm** adapter reference was retained.

## Engineering distinctions

| Measure | Appropriate reading | Inappropriate reading |
|---|---|---|
| DOE mass | Modelled geometry/material mass under specific assumptions | Measured assembled aircraft mass |
| Conditional pass | Meets chosen proxy gates within screened settings | Flight-qualified design |
| ML validation | Agreement against analytical source-model outputs | Experimental structural validation |
| Lower mass | Hypothesis for further verified engineering | Guaranteed system mass saving |
| Rigid-group demand | Preliminary force-distribution result | Contact/fatigue/joint safety approval |

## Reproducibility constraints

Two **original source-code notebooks** and the **original 800-row 7L-2 DOE table** are now in the repository: [7M-5](../notebooks/DEP_MOUNT_7M5_J3_Failure_Aware_Optimization.ipynb), [7L visualisation](../notebooks/DEP_MOUNT_7L_ML_Visualization.ipynb), [DOE data](../data/DEP_MOUNT_7L2_Adapter_Joint_DOE.csv), and [7M-5 Python source](../scripts/DEP_MOUNT_7M5_J3_Failure_Aware_Optimization.py). Both notebooks are **source-only with zero saved outputs**. The 7L visualisation also requires an unavailable Phase 7L-1 file; independent full re-execution is not claimed. [Mass–rigidity](../assets/figures/doe_mass_vs_rigidity_recovered.svg) and [OD–mass](../assets/figures/doe_outer_diameter_mass_recovered.svg) views are newly generated directly from the recovered 7L-2 CSV, **not original notebook plots**.

**Final design decision:** retain baseline J3 for this preliminary study; only reconsider optimised candidates after verifying geometry, complete mass accounting, bolt/clamp/contact mechanics, pin fit and representative engineering loads.
