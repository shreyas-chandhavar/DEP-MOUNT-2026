#!/usr/bin/env python3
"""Structural consistency checks for published DEP-MOUNT 2026 portfolio evidence.

Scope: transcribed data and repository completeness only, NOT structural or flight validation.
Python standard library; run from any working directory.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_csv(path: str) -> list[dict[str, str]]:
    with (ROOT / path).open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        rows = list(reader)
        require(reader.fieldnames is not None, f"CSV header missing: {path}")
        require(bool(rows), f"No records: {path}")
        require(all(None not in r and all(v is not None for v in r.values()) for r in rows),
                f"CSV column mismatch: {path}")
        return rows


def audit_correlated_load_cases() -> None:
    data = load_csv("data/nasa_2019_correlated_case_proxy_demands.csv")
    cols = (
        "Airframe_peak_positive_bolt_N",
        "Motor_peak_positive_bolt_N",
        "Airframe_peak_nominal_dowel_N",
        "Motor_peak_nominal_dowel_N",
    )
    require(len(data) == 10, "Expected 10 correlated NASA 2019 *project-model* scenarios")
    require([int(r["Case"]) for r in data] == list(range(1, 11)), "Case numbering invalid")
    for r in data:
        require(all(math.isfinite(float(r[col])) and float(r[col]) >= 0 for col in cols),
                "Invalid/non-finite demand proxy")

    expected_peaks = {
        "Airframe_peak_positive_bolt_N": 569.17,
        "Motor_peak_positive_bolt_N": 548.17,
        "Airframe_peak_nominal_dowel_N": 271.22,
        "Motor_peak_nominal_dowel_N": 311.21,
    }
    for col, expected in expected_peaks.items():
        observed = max(float(r[col]) for r in data)
        require(math.isclose(observed, expected, rel_tol=0, abs_tol=0.005),
                f"Peak mismatch for {col}: {observed} vs {expected}")
    require(max(int(r["Case"]) for r in data
                if float(r["Airframe_peak_positive_bolt_N"]) == 569.17) == 8,
            "Expected tied airframe bolt maxima in recorded cases 4/8")
    print("PASS: 10 correlated scenario records and published proxy maxima")


def audit_ebom() -> None:
    rows = load_csv("data/ebom_revA_preliminary.csv")
    require(len(rows) == 7, "Expected seven unique eBOM line items")
    require(len({row["PartNumber"] for row in rows}) == 7, "Duplicate eBOM part number")
    require([int(row["Find"]) for row in rows] == [10, 20, 30, 40, 50, 60, 70],
            "eBOM find-number sequence changed")
    require([int(row["Quantity"]) for row in rows] == [1, 1, 1, 8, 16, 8, 4],
            "Preliminary eBOM quantities changed")
    require(all(row["Revision"] == "A" and row["Status"] == "In Work" for row in rows),
            "Unapproved revision/lifecycle change")
    require("TBD" in next(row["Description"] for row in rows
                          if row["PartNumber"] == "DEP-HDW-2100"),
            "M6 bolt length must remain unverified/TBD")
    print("PASS: seven preliminary Rev A eBOM items, quantities, and HOLD-sensitive bolt length")


def audit_visual_and_disposition_files() -> None:
    for file in (
        "assets/figures/correlated_bolt_demands.svg",
        "assets/figures/correlated_dowel_demands.svg",
    ):
        content = (ROOT / file).read_text(encoding="utf-8")
        require(content.lstrip().startswith("<svg"), f"Invalid SVG: {file}")
        require(len(content) > 1000, f"Potentially truncated chart: {file}")

    for file in ("README.md", "docs/06_open_risks.md", "docs/07_reproducibility.md"):
        content = (ROOT / file).read_text(encoding="utf-8").upper()
        require("HOLD" in content, f"Release limitation missing from {file}")
    print("PASS: published charts are present and key release warnings retained")


if __name__ == "__main__":
    try:
        audit_correlated_load_cases()
        audit_ebom()
        audit_visual_and_disposition_files()
    except (AssertionError, ValueError, KeyError, OSError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
    print("Repository evidence consistency: PASS (NOT an engineering verification/release)")
