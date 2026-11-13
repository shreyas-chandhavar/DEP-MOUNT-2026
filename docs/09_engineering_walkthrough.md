# DEP-MOUNT 2026 — Engineering study walkthrough

**Status:** Independent preliminary investigation, Concept B J3, Rev A In Work. **Hardware release: HOLD**.

## The problem addressed

A distributed-electric-propulsion motor mount must transmit external aerodynamic/propeller thrust and moments through a light structure into motor and airframe attachments. The design challenge is not simply low static stress: the connection must also be buildable, clampable, fit for actual fasteners/dowels and tolerant of the required operating loads.

## What we actually did

| Stage | Engineering work | Preserved supporting evidence | Decision or limitation |
|---|---|---|---|
| 1. Architecture | Compared Concept A four-rod support with Concept B tapered cradle, including recorded mass estimates (about 916 g versus 820 g for initial stage-specific concepts) | [Requirements](01_problem_and_requirements.md) and recorded [README comparison](../README.md) | Concept B selected for further engineering; numbers are not reconciled certified whole-assembly masses |
| 2. CAD + FEA | Built unequal-flange tapered-cradle assembly in SolidWorks; preliminary structural FEA ≈1.7–1.98 MPa local equivalent stress and ≈0.004 mm displacement | [CAD review](04_cad_review.md) and [native archive manifest](../cad/PACK_AND_GO_MANIFEST.md) | Preliminary comparative screening only; no qualified contact, stability or fatigue checks |
| 3. Loading | Separate source-informed 2019 correlated cases from 2024 isolated signed cases; idealised bolt-group and dowel reactions under explicitly assumed installation positions | [10-case CSV](../data/nasa_2019_correlated_case_proxy_demands.csv), [load audit](02_load_cases_and_joint_demands.md), [bolt chart](../assets/figures/correlated_bolt_demands.svg) | Max reported positive bolt reactions 569.17 N (airframe) and 548.17 N (motor), **not** verified clamp force |
| 4. Joint design audit | Reviewed M6 bolts/nuts/washers, nominal Ø4 dowel arrangement, seating and installation interference volumes | [CAD/hardware audit](04_cad_review.md) | Nonzero interference; preload, thread depth, pin fit, actual bolt length and local contact remain open |
| 5. DOE | Evaluated 800 modelled geometric/fastener configurations and recorded conditional proxy feasibility | [original source CSV](../data/DEP_MOUNT_7L2_Adapter_Joint_DOE.csv) and [DOE charts](../assets/figures/doe_mass_vs_rigidity_recovered.svg) | 179 conditional joint-screen passes reported by original study; **not** all equivalent to the dataset's basic geometry-gate count |
| 6. Surrogate ML | Used held-out surrogate modelling and guard-band screening for mass, stiffness, thread, clamp-related proxies | [7M-5 original notebook](../notebooks/DEP_MOUNT_7M5_J3_Failure_Aware_Optimization.ipynb), [7L notebook](../notebooks/DEP_MOUNT_7L_ML_Visualization.ipynb), [Python source](../scripts/DEP_MOUNT_7M5_J3_Failure_Aware_Optimization.py) | Reported 25,000 virtual proposals are model predictions only; observed threshold false passes prevent automatic design authorization |
| 7. Configuration/PLM | Recorded preliminary TurboPLM seven-line EBOM, draft requirements and ECR-10002 | [PLM study](05_plm.md), [manual BOM snapshot](../data/plm/DEP_2026_eBOM_manual_backup_2026-11-12.csv) | Concept gate passed; formal design validation and hardware release **HOLD** |

## Why the low-mass optimization was rejected

The screen identified a modelled 412.75 g adapter option, but the mass comparisons were not reconciled to the complete retained CAD assembly, and surrogate classification errors occurred near an important thread-coverage gate. More importantly, physical joint mechanics and fastening geometry were not demonstrated. The design decision was therefore **retain the reference J3 CAD**, not release the nominal lightest analytical point.

## How to inspect or reproduce the preserved evidence

- **Original input:** [7L-2 analytical DOE, 800 rows × 12 columns](../data/DEP_MOUNT_7L2_Adapter_Joint_DOE.csv)
- **Original executable source, no saved executed output:** [7M-5 notebook](../notebooks/DEP_MOUNT_7M5_J3_Failure_Aware_Optimization.ipynb) and [Python script](../scripts/DEP_MOUNT_7M5_J3_Failure_Aware_Optimization.py)
- **7L visualization source:** [7L notebook](../notebooks/DEP_MOUNT_7L_ML_Visualization.ipynb). **Needs 7L-1 original CSV for its full workflow**.
- **Fresh charts shown here:** [mass–rigidity](../assets/figures/doe_mass_vs_rigidity_recovered.svg) and [OD–mass](../assets/figures/doe_outer_diameter_mass_recovered.svg), drawn directly from the committed 7L-2 CSV, not extracted original notebook plots.
- **Check input integrity:** `python scripts/verify_repository.py` (runs on GitHub Actions). It does **not** reproduce the author's complete FEA or certify joint performance.

## Native CAD and original output custody

The original SolidWorks side, end and two isometric screenshots are now **published in the [actual CAD gallery](../assets/cad/README.md)**, each linked to its original full-resolution PNG. The separate native SolidWorks Pack-and-Go ZIP is not published and may contain commercial Toolbox-derived components requiring a redistribution review. No generic CAD model has been substituted for the author's geometry.

## What remains unverified for hardware use

Final aircraft-level load envelope and coordinate basis; fastener seating and interface interferences; clamp/preload/contact/slip/separation; bolt grip and thread engagement; dowel interference fit, end clearance and retention; local strength/buckling; dynamic response and fatigue; materials/process qualification; physical test and assembly release.

**Portfolio conclusion:** The study demonstrates a disciplined **design trade-off and negative release decision**. The evidence supports conceptual work and investigation, **not** a built, safe or flight-approved part.
