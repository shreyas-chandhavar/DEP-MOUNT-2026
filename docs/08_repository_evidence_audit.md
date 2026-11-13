# 08 — Repository evidence audit and source-availability register

**Audit baseline:** 13 November 2026 · **Repository:** [DEP-MOUNT-2026](https://github.com/shreyas-chandhavar/DEP-MOUNT-2026) · **Concept B J3 / Rev A In Work**

## Published, directly accessible in GitHub

| Evidence | Location | Scope and qualification |
|---|---|---|
| Project description and outcome | [README](../README.md) | Independent, preliminary portfolio study; hardware-release **HOLD** |
| Ten correlated source-scenario proxy results | [2019 analytical case table](../data/nasa_2019_correlated_case_proxy_demands.csv) | Project-specific idealized load reactions, not measured/certified joint demands |
| Graphs of the tabulated reactions | [bolt](../assets/figures/correlated_bolt_demands.svg) · [dowel](../assets/figures/correlated_dowel_demands.svg) | **Redrawn from published numerical summary**, not original Colab exports |
| Preliminary eBOM | [seven-item eBOM](../data/ebom_revA_preliminary.csv) | Transcribed preliminary configuration, not a native TurboPLM export |
| Problem, DOE/ML and hardware limitations | [technical documentation](01_problem_and_requirements.md), [DOE/ML](03_doe_ml.md), [CAD audit](04_cad_review.md), [release risks](06_open_risks.md) | Technical summaries, not independently re-executable source-code notebooks |
| Original 7M-5 notebook and Python script | [notebook](../notebooks/DEP_MOUNT_7M5_J3_Failure_Aware_Optimization.ipynb), [script](../scripts/DEP_MOUNT_7M5_J3_Failure_Aware_Optimization.py) | Source code preserved; notebook has no saved cell outputs |
| Original 7L visualization notebook | [7L notebook](../notebooks/DEP_MOUNT_7L_ML_Visualization.ipynb) | Source code preserved; full rerun needs unavailable 7L-1 dataset |
| Original 7L-2 modelled DOE | [800-row CSV](../data/DEP_MOUNT_7L2_Adapter_Joint_DOE.csv) | Recovered data; structural audit 800 rows × 12 fields |
| Recovered DOE figures | [mass vs rigidity](../assets/figures/doe_mass_vs_rigidity_recovered.svg) · [OD vs mass](../assets/figures/doe_outer_diameter_mass_recovered.svg) | Newly derived directly from original DOE table, not preserved Colab outputs |
| Transcribed PLM backup | [seven-line screenshot-transcribed BOM](../data/plm/DEP_2026_eBOM_manual_backup_2026-11-12.csv) | Manual source, not TurboPLM-native export |
| Native CAD archive custody | [Pack-and-Go manifest](../cad/PACK_AND_GO_MANIFEST.md) | Local ZIP reported CRC-checked; ZIP not included in this repository |

## Original work identified from earlier uploads but NOT yet published

The following **still unavailable** files were identified by filename in the user's earlier ChatGPT attachments. Being discoverable as a prior attachment **does not mean GitHub received the binary/source file**. In this session, access to the original archived files' raw bytes was unavailable; do not claim they were transferred.

| Prior artifact | Target GitHub path (only after exact source bytes can be recovered) | Status |
|---|---|---|
| `DEP_MOUNT_Phase6D_Colab_Architecture_Comparison (1).ipynb` | `notebooks/DEP_MOUNT_Phase6D_Colab_Architecture_Comparison.ipynb` | Pending |
| `Untitled8.ipynb`, `Untitled9.ipynb` | `notebooks/` with meaningful phase labels after inspection | Pending |
| Original Phase 7L-1 DOE and additional output figures | `data/` and `assets/figures/` | Pending full inventory/transfer |
| `Screenshot (1349).png` — actual J3 side | `assets/cad/j3_side_actual_2026-11-13.png` | Pending |
| `Screenshot (1350).png` — actual J3 end | `assets/cad/j3_end_actual_2026-11-13.png` | Pending |
| `Screenshot (1351).png` — actual J3 isometric | `assets/cad/j3_isometric_front_actual_2026-11-13.png` | Pending |
| `Screenshot (1352).png` — second isometric | `assets/cad/j3_isometric_rear_actual_2026-11-13.png` | Pending |
| `DEP_ConceptB_J3_Fastener_Integration_Rev00.zip` | Release-controlled native CAD archive, separate from publication if licensing requires | Pending license review + binary transfer |
| `DEP_MOUNT_2026_Original_Evidence_To_Upload.zip` | Source evidence package; inspect structure before placement | Indexed as an upload; binary transfer pending |

The script [verify_repository.py](../scripts/verify_repository.py) checks current **published** CSV tables, identifiers, maxima, BOM quantities and release notices. The [automated workflow](../.github/workflows/evidence-integrity.yml) runs the same check for future changes. This is **data consistency testing only**; it does not rederive NASA source loads or prove joint strength.

## Explicit engineering disposition

- **Concept design and initial modeling:** documented as a portfolio case study.
- **Verified physical hardware / certification:** not demonstrated.
- **Major outstanding release gates:** full load envelope, preload/contact, fit and dowel retention, fastener interference, true thread engagement, fatigue, modal/buckling, manufacturing and testing.
- **Revision A lifecycle:** In Work; ECR-10002 open; no manufacturing or flight release.

**Do not add generic CAD images as if they depict the author's SOLIDWORKS model. Do not label newly generated proxy figures as the original Colab plots.**

The 7L-2 dataset, two original source notebooks, a Python script and the transcribed eBOM **have now been published**. The CAD screenshots, additional historical notebooks, original output plots and native CAD binaries **have not**. This is a transparent file-level status register.
