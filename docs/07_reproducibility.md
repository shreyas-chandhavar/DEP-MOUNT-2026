# 07 — Evidence provenance, reproduction and missing source files

**Engineering disposition: Preliminary portfolio study only; physical hardware release: HOLD.**

## Hierarchy of evidence

1. Original author-run Python notebooks and recorded outputs (not all independently re-executed)
2. User-supplied SolidWorks and TurboPLM screenshots
3. Locally archived native CAD and scenario files (not yet included in public repository)
4. Clearly labelled summary transcriptions and diagrams

**Important:** The source NASA cases were used to inform idealized preliminary models. Numeric reactions and DOE outcomes depend on independently selected mount geometry, local axes and stiffness distribution; they are **not** direct NASA hardware verification outputs.

## Published original analysis source and input data

- [7M-5 original Colab source notebook](../notebooks/DEP_MOUNT_7M5_J3_Failure_Aware_Optimization.ipynb), [Python copy](../scripts/DEP_MOUNT_7M5_J3_Failure_Aware_Optimization.py)
- [7L original visualisation notebook](../notebooks/DEP_MOUNT_7L_ML_Visualization.ipynb)
- [Original 7L-2 DOE analytical dataset](../data/DEP_MOUNT_7L2_Adapter_Joint_DOE.csv), 800 rows and 12 columns
- [Manually screenshot-transcribed TurboPLM BOM](../data/plm/DEP_2026_eBOM_manual_backup_2026-11-12.csv)
- Two **newly reconstructed** [DOE scatter charts](../assets/figures/doe_mass_vs_rigidity_recovered.svg), not source notebook outputs

None of the two published source notebooks has saved execution outputs; these are preserved executable methods rather than claims of a reproduced run. Source-data consistency is checked by [GitHub Actions](../.github/workflows/evidence-integrity.yml), not by flight certification.

## Existing off-repo assets to add

- Three original Colab notebooks: `DEP_MOUNT_Phase6D_Colab_Architecture_Comparison (1).ipynb`, `Untitled8.ipynb`, `Untitled9.ipynb`
- Their **34** extracted output plots and 12 curated figures
- Four actual final SolidWorks screenshots supplied on 13 November 2026
- Latest SolidWorks Pack-and-Go archive, saved by author, including referenced components
- Original Phase 7L-1 DOE CSV and remaining original notebook phase inputs, if retained
- Original closeout study archive, comparison logs and recorded PLM snapshot

These files are **not implied to have been uploaded** simply because their names appear here.

## Recommended original screenshot filenames

| Uploaded file | Target repository path |
|---|---|
| Screenshot (1349).png — side view | `assets/cad/j3_side_actual_2026-11-13.png` |
| Screenshot (1350).png — end view | `assets/cad/j3_end_actual_2026-11-13.png` |
| Screenshot (1351).png — isometric | `assets/cad/j3_isometric_front_actual_2026-11-13.png` |
| Screenshot (1352).png — second isometric | `assets/cad/j3_isometric_rear_actual_2026-11-13.png` |

These are **original screenshots**; cropping to remove SOLIDWORKS menus is acceptable if geometry is not modified.

## Public sources

- NASA, *Development of a Maxwell X-57 High Lift Motor Reference Design* (2019), NTRS https://ntrs.nasa.gov/citations/20190029267
- NASA-STD-5020B, *Requirements for Threaded Fastening Systems in Spaceflight Hardware*, informative https://standards.nasa.gov/node/254
- ISO 4017/7089/7042/8734 — standard component designations, **not** proof of fit or compliance

## Publishing and licensing

No repository-wide license has been selected. Do not upload commercial ISO standards PDFs, third-party proprietary CAD/Toolbox libraries or unreviewed confidential source materials. If the owner later selects an open-source software license, document the scope separately from third-party materials and CAD drawings.
