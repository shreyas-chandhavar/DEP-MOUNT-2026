# 06 — Open risks and engineering release decision

**Preliminary portfolio engineering investigation: concluded. Physical hardware release: HOLD.**

| Priority | Unverified item | Why it matters |
|---|---|---|
| Critical | Final equipment load envelope, axes, motor/propeller CG and real moment application | Published reference cases are not an installation-approved aircraft load set |
| Critical | M6 bolt preload, clamp load, torque scatter and contact pressure | Idealized bolt reactions cannot show separation, slip or prying margins |
| Critical | Fastener interference and tool access | Significant nonzero CAD volumes remain; connection can be impossible to assemble even with correct mates |
| Critical | Pin fits, dowel retention, hole depths and tolerance stack | Ø4 nominal drawing dimensions are not a defined pin/hole manufacturing fit |
| Critical | Thread engagement, net sections and local bearing | Proof comparison alone does not establish component or nut/thread capacity |
| High | Dynamic/modal and fatigue | No measured excitation spectrum, hardware fatigue test or qualified modal match |
| High | Shell stability / local buckling under actual imperfections | Idealized strength/rigidity proxies do not prove the real cradle geometry |
| High | Material properties, allowables, coatings, temperature | Material/process basis not established for aircraft hardware release |
| High | Physical test/independent review | No prototype, instrumented verification or conformity/test evidence |
| Administrative | Source DOE CSV and full native CAD package not in public repo | Published evidence remains partial and must be described as such |

### What is supported

A genuine preliminary conceptual design decision, documented analytical load screening, conditional fastener strength proxies, an ML approximation study with reported false-pass errors, a native CAD model saved locally, and a registered configuration change-management baseline.

### What is not supported

A claim of **no CAD interference**, safety factor verified for the whole joint, production-ready/flightworthy design, actual qualified mass reduction, experimentally validated fatigue life or NASA endorsement.

### Frozen-study disposition

The preliminary investigation is complete for an independently reviewable engineering portfolio; any later physical product development **must reopen and close** the indicated engineering verification gates before hardware release.
