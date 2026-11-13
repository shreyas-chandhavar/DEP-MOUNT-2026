# 04 — SolidWorks CAD, fastener and dowel review

## Actual geometry

See the [four-view original SolidWorks CAD gallery](../assets/cad/README.md) and [source image provenance / SHA-256 record](../assets/cad/IMAGE_PROVENANCE.md). The four actual screenshots have been re-uploaded in chat and prepared for repository transfer; the GitHub PNG files themselves remain pending until their image bytes are published. No generic CAD renders are substituted.


The original SolidWorks model `DEP_ConceptB_J3_Fastener_Integration_Rev00.SLDASM` is a **tapered central cradle** between **two unequal circular end flanges**, not a generic four-arm spider mount. The new November 13 screenshots show actual **side**, **end**, and **two isometric** views. Original images should be uploaded to `assets/cad/`; the STEP/Pack-and-Go ZIP is retained by the author offline.

**Do not treat any decorative CAD illustration as project evidence.**

### Installed trial hardware vs. BOM

| Hardware | Provisional BOM quantity | Verification state |
|---|---:|---|
| M6 ISO 4017 class 8.8 bolt | 8 | Trial ×30 mm length; final grip, engagement and accessible nut side not proven |
| M6 ISO 7089 plain washer 200 HV | 16 | Preview/assembly model; seat and interference check open |
| M6 ISO 7042 locking nut class 8 | 8 | Modelled; physical access and full thread engagement open |
| Ø4 ×14 mm ISO 8734 steel dowel | 4 | Nominal arrangement; axial depth, fits and retention not qualified |

The observed SolidWorks feature tree can include **trial instances beyond intended BOM quantity**; the BOM lists proposed installed hardware, not an independently counted as-built list. Do not infer the total from a screenshot alone.

## Documented SolidWorks interference check

Visible interference results included:
- **206.95 mm³** grouped screw/motor-adapter overlap; investigate physical intersection rather than dismiss as thread display.
- **48.68 mm³** groups in other fastener/component combinations.
- **≈20 mm³** intermediate groups.
- **0.0017 mm³** screw/washer tiny overlaps; possibly simplified Toolbox geometry, but not individually adjudicated.

These values are **reported overlap volumes**, not measured stress or strength demand. A properly constrained concentric mate **does not prove** a collision-free part.

## Dowel engagement limits

A nominal Ø4 ×14 mm pin was intended to bridge two mating components. The earlier 6.5/7.5 mm engagement proposal sums to the entire pin length and leaves no nominal pin-end clearance if both holes are blind; actual engagement and minimum bottom clearance must be checked against model and hardware tolerances. Earlier 8.05 mm distance measurements between selected entities do **not** in themselves establish actual hole depth or axis alignment.

## Design decision

Native SolidWorks assembly saved; Pack-and-Go archive locally saved. **For portfolio only**, the CAD work is frozen with open interference, thread, preload, pin-fit and assembly constraints. **No manufacturing, procurement or flight release.**
