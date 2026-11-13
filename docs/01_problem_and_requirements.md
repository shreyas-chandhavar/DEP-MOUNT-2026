# 01 — Engineering problem, scope and requirements

## Design problem

A distributed electric propulsion motor support must carry thrust, transverse propeller loads, torque, inertial forces and installation/ground loads from propulsion hardware into the aircraft structure. The purpose is to investigate a **lightweight, mechanically defensible load path**, not demonstrate a certified aircraft part.

The study compares two distinct support concepts: **Concept A**, a four-rod mount, and **Concept B**, a tapered-shell/cradle configuration. The second was selected for the detailed J3 interface investigation.

## Intended study deliverables
- Maintain traceable load sources, coordinate assumptions and reaction equilibrium.
- Screen mass, rigidity, structural response and fastener load-path sensitivities.
- Compare physically meaningful architecture and fastener design decisions.
- Use machine-learning surrogates only as approximations to an analytical model, with independently checked acceptance decisions.
- Archive native CAD and engineering BOM/configuration information.
- Separate analysis completion from **physical qualification and production release**.

## Controlled requirements — TurboPLM

| Requirement | Statement summary | Present verification |
|---|---|---|
| REQ-10007 · Motor and Airframe Interface Load Transfer | The assembly must transfer the defined forces and moments through motor-side and airframe-side connections without loss of structural integrity. | Source-based reactions screened, **final actual equipment load definition and integrated structural proof OPEN** |
| REQ-10008 · Bolted Joint Integrity | The interfaces must maintain clamping/load transfer without unacceptably yielding, slipping, separating, or failing in bearing/thread engagement. | Nominal reactions and proof-load scenarios calculated; **preload, contact, prying, thread, fatigue and strength qualification OPEN** |

Both requirements were recorded in **Draft** state; linking them to CAD parts is traceability, **not evidence of test pass**.

## Geometric configuration

The working configuration is a tapered central cradle joining dissimilar circular end flanges. The proposed engineering BOM identifies **four M6 bolt positions and two Ø4 dowels at each interface**. Physical geometry, local material and pin fit are *not* completely qualified.

## Engineering scope boundary

No real aircraft installation was measured, no physical prototype or instrumented joint was tested, and the final assembly does not have fatigue, modal, buckling imperfection, contact, prying or installation preload release evidence. See [open risks](06_open_risks.md).
