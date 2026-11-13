# 05 — TurboPLM engineering BOM and change control

## System configuration

- Project: **DEP-2026 — DEP-MOUNT 2026**
- Top assembly: **DEP-ASM-1000**, Concept B J3 Motor Mount Assembly
- Revision: **A — In Work**
- Study baseline: **Concept B J3 Preliminary Engineering Baseline — R00**, snapshot created 12 Nov 2026
- Concept Gate: **Passed**, 13 Nov 2026
- Design Gate: **In Progress** (no design qualification pass)
- Validation / Pilot / Production: **Not Started**
- Change request: **ECR-10002 — J3 Fastener Architecture Verification and Design Closure — OPEN**

## eBOM snapshot

| Find | Part number | Description | Qty | State |
|---:|---|---|---:|---|
| 10 | DEP-PRT-1100 | Concept B J3 Tapered Cradle | 1 | Rev A, In Work |
| 20 | DEP-PRT-1200 | J3 Motor Adapter | 1 | Rev A, In Work |
| 30 | DEP-PRT-1300 | J3 Airframe Mating Interface | 1 | Rev A, In Work |
| 40 | DEP-HDW-2100 | M6 ISO 4017 bolt, class 8.8, final length TBD | 8 | Rev A, In Work |
| 50 | DEP-HDW-2200 | M6 ISO 7089 washer, 200 HV | 16 | Rev A, In Work |
| 60 | DEP-HDW-2300 | M6 ISO 7042 locking nut, class 8 | 8 | Rev A, In Work |
| 70 | DEP-HDW-2400 | ISO 8734 Ø4 ×14 dowel | 4 | Rev A, In Work |

The TurboPLM CSV export redirected to its dashboard; this is a manually recorded/transcribed snapshot, **not a native authenticated system export**.

## Requirement links

- **REQ-10007 — Motor and Airframe Interface Load Transfer:** four linked structural part/assembly objects; Draft.
- **REQ-10008 — Bolted Joint Integrity:** seven linked parts/assembly/hardware objects; Draft.

Approving requirements is **not warranted** until the acceptance criteria have evidence.

## Reason ECR-10002 stays open

Preload retention, contact stiffness and separation, thread engagement, all-metal nut retention, fit-dependent dowel load sharing, local hole strength, installation clearance and fatigue/thermal conditions are not proven.

## Configuration release logic

The **Concept Gate** is about architecture selection; it can pass based on documented preliminary trade-off evidence. The **Design Gate** cannot be passed merely because the feature tree and BOM are populated. The assembly and seven children remain **In Work**; the baseline preserves their preliminary configuration without authorizing fabrication or use.
