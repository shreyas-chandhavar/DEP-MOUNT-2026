# Verified local SolidWorks Pack-and-Go archive

**Archive received:** `DEP_ConceptB_J3_Fastener_Integration_Rev00.zip`  
**Date received:** 13 November 2026  
**Size:** 1,416,391 bytes (~1.42 MB decimal)  
**SHA-256:** `00089ba6995064ad658995934e6c79af6a5711a2299485a35efe38b5335130a5`  
**ZIP test:** Each entry passed CRC validation; no corrupted entries detected.  
**Repository status:** The actual ZIP binary remains outside GitHub until a user-side upload. This manifest is **not** the native CAD file.

## Inventory: 8 files

| File name | Type / intended role |
|---|---|
| `DEP_ConceptB_J3_Fastener_Integration_Rev00.SLDASM` | Top-level J3 trial assembly |
| `DEP_ConceptB_Cradle_J3_Dowel_Trial.SLDPRT` | Custom tapered cradle |
| `DEP_Motor_Adapter_J3_Dowel_Trial.SLDPRT` | Custom motor adapter |
| `DEP_Airframe_Mating_Interface_J3_Trial.SLDPRT` | Custom airframe mating interface |
| `hex screw gradeab_iso.sldprt` | SOLIDWORKS Toolbox-derived hex screws |
| `plain washer normal grade a_iso.sldprt` | SOLIDWORKS Toolbox-derived flat washers |
| `torque nut 03_iso.sldprt` | SOLIDWORKS Toolbox-derived locking nuts |
| `parallel pin hardened_iso.sldprt` | SOLIDWORKS Toolbox-derived parallel pins |

**Reproducibility caveat:** The list confirms file presence and valid ZIP compression/CRC only. Resolving configuration-specific references, preserving toolbox configuration data and mating functionality requires a real SolidWorks reopen test. The saved hardware implementation remains a **provisional CAD integration**, not hardware qualification.

**Redistribution caveat:** Four part files appear to be supplied/derived from SOLIDWORKS Toolbox. Before distributing the complete ZIP publicly, the author should confirm their license permits redistribution of the Toolbox models. A public STEP export of the author-created assembly together with images may be a better external review artifact if Toolbox redistribution is restricted. The four custom CAD files can remain preserved locally.

## Identical-archive verification

On Windows PowerShell run:

```powershell
Get-FileHash .\DEP_ConceptB_J3_Fastener_Integration_Rev00.zip -Algorithm SHA256
```

Compare the output with the hash above.

## CAD evidence

The last user-supplied four screenshots on 13 November 2026 show the **actual tapered two-flange J3 configuration**. After publishing original screenshots, their repository paths should match:

- `assets/cad/j3_side_actual_2026-11-13.png`
- `assets/cad/j3_end_actual_2026-11-13.png`
- `assets/cad/j3_isometric_front_actual_2026-11-13.png`
- `assets/cad/j3_isometric_rear_actual_2026-11-13.png`

Do not substitute unrelated or generative CAD illustrations as evidence.
