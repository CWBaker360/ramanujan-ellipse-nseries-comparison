#!/usr/bin/env python3
"""Verify the Ramanujan-versus-N-Series ellipse comparison."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import mpmath as mp


B_VALUES = ("0.90", "0.75", "0.50", "0.25")
N_VALUES = (32, 64, 128, 256)


def exact_perimeter(a: mp.mpf, b: mp.mpf) -> mp.mpf:
    eccentricity = mp.sqrt(1 - (b / a) ** 2)
    return 4 * a * mp.ellipe(eccentricity**2)


def ramanujan_second(a: mp.mpf, b: mp.mpf) -> mp.mpf:
    h = ((a - b) / (a + b)) ** 2
    return mp.pi * (a + b) * (
        1 + 3 * h / (10 + mp.sqrt(4 - 3 * h))
    )


def polygon_perimeter(a: mp.mpf, b: mp.mpf, n: int) -> mp.mpf:
    half_step = mp.pi / n
    chord_factor = 2 * mp.sin(half_step)
    return mp.fsum(
        chord_factor
        * mp.sqrt(
            a * a * mp.sin((2 * j + 1) * half_step) ** 2
            + b * b * mp.cos((2 * j + 1) * half_step) ** 2
        )
        for j in range(n)
    )


def two_scale(a: mp.mpf, b: mp.mpf, n: int) -> mp.mpf:
    p_n = polygon_perimeter(a, b, n)
    p_2n = polygon_perimeter(a, b, 2 * n)
    return (4 * p_2n - p_n) / 3


def three_scale(a: mp.mpf, b: mp.mpf, n: int) -> mp.mpf:
    p_n = polygon_perimeter(a, b, n)
    p_2n = polygon_perimeter(a, b, 2 * n)
    p_4n = polygon_perimeter(a, b, 4 * n)
    return p_n / 45 - 4 * p_2n / 9 + 64 * p_4n / 45


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--precision", type=int, default=80)
    parser.add_argument("--output-dir", type=Path, default=Path("output"))
    args = parser.parse_args()

    if args.precision < 50:
        raise ValueError("Use at least 50 decimal digits.")

    mp.mp.dps = args.precision
    a = mp.mpf("1")
    rows = []

    for b_text in B_VALUES:
        b = mp.mpf(b_text)
        exact = exact_perimeter(a, b)
        ramanujan = ramanujan_second(a, b)
        ram_error = abs(ramanujan - exact)

        for n in N_VALUES:
            raw = polygon_perimeter(a, b, n)
            two = two_scale(a, b, n)
            three = three_scale(a, b, n)
            rows.append(
                {
                    "a": "1.0",
                    "b": b_text,
                    "N": n,
                    "exact_perimeter": mp.nstr(exact, 35),
                    "ramanujan_perimeter": mp.nstr(ramanujan, 35),
                    "ramanujan_abs_error": mp.nstr(ram_error, 25),
                    "raw_polygon_abs_error": mp.nstr(abs(raw - exact), 25),
                    "two_scale_abs_error": mp.nstr(abs(two - exact), 25),
                    "three_scale_abs_error": mp.nstr(abs(three - exact), 25),
                }
            )

    args.output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = args.output_dir / "ellipse_ramanujan_nseries_results.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    expected = {
        ("0.90", 256): mp.mpf("6.3248746258994009612e-17"),
        ("0.75", 64): mp.mpf("2.3965732540718419386e-13"),
        ("0.75", 256): mp.mpf("5.8512498655566939602e-17"),
        ("0.50", 32): mp.mpf("7.3447413137632796868e-12"),
        ("0.50", 64): mp.mpf("2.1009401675875643626e-13"),
        ("0.50", 128): mp.mpf("3.2828297893624561488e-15"),
        ("0.50", 256): mp.mpf("5.1294637911290928764e-17"),
        ("0.25", 32): mp.mpf("1.8148136300180527772e-7"),
        ("0.25", 256): mp.mpf("4.5417700419121316437e-17"),
    }

    lookup = {
        (row["b"], int(row["N"])): mp.mpf(row["three_scale_abs_error"])
        for row in rows
    }

    manuscript_values_passed = all(
        abs(lookup[key] - value) <= mp.mpf("1e-18") * max(1, abs(value))
        for key, value in expected.items()
    )

    e64 = lookup[("0.50", 64)]
    e128 = lookup[("0.50", 128)]
    e256 = lookup[("0.50", 256)]
    ratio_64_128 = e64 / e128
    ratio_128_256 = e128 / e256
    sixth_order_ratio_passed = (
        abs(ratio_64_128 - 64) < mp.mpf("0.1")
        and abs(ratio_128_256 - 64) < mp.mpf("0.1")
    )

    by_key = {(row["b"], int(row["N"])): row for row in rows}
    comparison_regimes_passed = (
        mp.mpf(by_key[("0.90", 256)]["three_scale_abs_error"])
        > mp.mpf(by_key[("0.90", 256)]["ramanujan_abs_error"])
        and mp.mpf(by_key[("0.75", 256)]["three_scale_abs_error"])
        < mp.mpf(by_key[("0.75", 256)]["ramanujan_abs_error"])
        and mp.mpf(by_key[("0.50", 256)]["three_scale_abs_error"])
        < mp.mpf(by_key[("0.50", 256)]["ramanujan_abs_error"])
        and mp.mpf(by_key[("0.25", 256)]["three_scale_abs_error"])
        < mp.mpf(by_key[("0.25", 256)]["ramanujan_abs_error"])
    )

    overall = bool(
        manuscript_values_passed
        and sixth_order_ratio_passed
        and comparison_regimes_passed
    )

    summary = {
        "precision_dps": args.precision,
        "ellipse_cases": len(B_VALUES),
        "base_N_values": list(N_VALUES),
        "manuscript_values_passed": bool(manuscript_values_passed),
        "sixth_order_ratio_64_to_128": mp.nstr(ratio_64_128, 20),
        "sixth_order_ratio_128_to_256": mp.nstr(ratio_128_256, 20),
        "sixth_order_ratio_passed": bool(sixth_order_ratio_passed),
        "comparison_regimes_passed": bool(comparison_regimes_passed),
        "verification_passed": overall,
    }

    (args.output_dir / "ellipse_ramanujan_nseries_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )
    (args.output_dir / "ellipse_ramanujan_nseries_summary.txt").write_text(
        "\n".join(f"{key}: {value}" for key, value in summary.items()) + "\n",
        encoding="utf-8",
    )

    print("\n".join(f"{key}: {value}" for key, value in summary.items()))
    if not overall:
        raise SystemExit("Verification failed.")


if __name__ == "__main__":
    main()
