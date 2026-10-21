#!/usr/bin/env python3
"""
Hot Wheels 2026 Mainline Cases Generator
========================================
Exports individual manifests and poster sheets for all 15 Hot Wheels mainline mixes (A through Q).
"""

import os
import json

def export_all_cases(manifest_file: str = "cases_2026_full.json", output_dir: str = "."):
    if not os.path.exists(manifest_file):
        print(f"Error: {manifest_file} not found.")
        return

    with open(manifest_file, "r", encoding="utf-8") as f:
        all_cases = json.load(f)

    print(f"Loaded {len(all_cases)} cases. Exporting individual manifests...")

    for code, data in all_cases.items():
        fname = os.path.join(output_dir, f"2026_case_{code.lower()}_manifest.json")
        with open(fname, "w", encoding="utf-8") as out:
            json.dump(data, out, indent=2)
        print(f"  • Case {code}: {data['total_count']} models (STH: {data['sth_name']}, TH: {data['th_name']}) -> {fname}")

    print("\n✅ All 15 cases (A through Q) exported successfully!")

if __name__ == "__main__":
    export_all_cases()
