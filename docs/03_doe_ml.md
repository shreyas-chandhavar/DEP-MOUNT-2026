# 03 — Physics-based DOE and surrogate modelling

## Study objective

Investigate whether alternative adapter/joint geometry could reduce analytical mass without losing stiffness or failing basic geometry and fastening feasibility gates.

### Recorded analytical screening

- **800** candidate configurations screened using a project-defined analytical model.
- **179** conditionally passed the combined proxy gates.
- Failure gates included geometry/legacy constraints, rigidity, flange/bolt edge, clamp depth, thread coverage and related hardware accessibility proxies.
- **25,000** additional machine-learning candidate predictions were screened; a subset of **3,796** passed heuristic guard-band criteria, but these were **not physical or CAD/contact verified passes**.
- A highlighted conditional DOE-212 candidate had motor-adapter **OD ≈146.918 mm, ID ≈92.964 mm, mass ≈412.752 g and rigidity proxy ≈0.845**.

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

The original notebook evidence is available in the author's separate local package but has **not yet been committed to this repository**. Some notebook phases depend on an original DOE source CSV that also remains outside the published repo. Independent complete rerun is therefore not claimed.

**Final design decision:** retain baseline J3 for this preliminary study; only reconsider optimised candidates after verifying geometry, complete mass accounting, bolt/clamp/contact mechanics, pin fit and representative engineering loads.
