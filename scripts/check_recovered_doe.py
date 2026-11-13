"""Source-data integrity audit: original DEP-MOUNT 7L-2 analytical DOE.

Checks CSV structure and the original geometry/stiffness gate count; does not
recreate any original model or establish mechanical/flight acceptability.
"""
import csv
import math
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "data" / "DEP_MOUNT_7L2_Adapter_Joint_DOE.csv"
expected = [
    "index", "thickness_mm", "outer_diameter_mm", "inner_diameter_mm", "preload_N",
    "Adapter mass (g)", "Relative flexural rigidity", "Thread ratio (5th percentile)",
    "Thread-screen coverage", "Friction no-slip coverage", "Clamp + depth coverage",
    "Geometry/stiffness gate"
]
with p.open(encoding="utf-8", newline="") as stream:
    rd = csv.DictReader(stream)
    assert rd.fieldnames == expected, "Unexpected 7L-2 source schema"
    rows = list(rd)
assert len(rows) == 800, "Expected 800 original DOE records"
for i, row in enumerate(rows):
    assert len(row) == 12 and None not in row, f"Broken CSV record {i}"
    assert int(row["index"]) == i, f"Unexpected record index {i}"
    for field in expected[1:]:
        assert math.isfinite(float(row[field])), f"Nonfinite {field} at index {i}"
    assert row["Geometry/stiffness gate"] in ("0.0", "1.0", "0", "1"), (
        f"Unexpected geometry/stiffness gate at record {i}"
    )
passed = sum(float(row["Geometry/stiffness gate"]) >= .5 for row in rows)
assert passed == 379, f"Expected 379 SINGLE gate pass records, found {passed}"
assert all(float(row["Adapter mass (g)"]) > 0 for row in rows)
print(f"PASS: 800 DOE rows, 12 columns, numeric validity, {passed} geometry/stiffness gate passes")
print("NOTE: single-field geometry pass is not the recorded 179 combined conditional joint passes.")
print("LIMITATION: no model recalculation, FEA/contact validation, or hardware-release verification.")
