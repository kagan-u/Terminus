#!/usr/bin/env python3
"""
TERMINUS OPTIMIZER
finds the optimal configuration for maximum output within zip size limits.
"""

import math


def zip_overhead():
    """minimum bytes per zip entry."""
    return 116  # headers + footers


def estimate_zip_size(branching, level, payload):
    """estimate zip size - uses quadratic model from actual measurements."""
    # quadratic model calibrated to actual terminus builds
    # zip_size(level) = a*level^2 + b*level + c
    # for branching=16, payload=43: 508950 bytes at level 50
    # adjust for different branching/payload
    a = 68.5
    b = 5850.0
    c = 120.0

    base = a * level**2 + b * level + c

    # scale by payload ratio (larger payload = slightly larger zip)
    base *= (1 + (payload - 43) * 0.001)

    # scale by branching (more entries per level = more overhead)
    branching_factor = 1 + (branching - 16) * 0.02
    base *= branching_factor

    return int(base)


def find_optimal(max_zip_kb=500, max_level=200):
    """find config with maximum output within size limit."""
    max_bytes = max_zip_kb * 1024
    best = None
    best_output = 0

    for branching in [4, 8, 16, 32, 64, 128, 256]:
        for payload in [1, 2, 4, 8, 16, 32, 43, 64, 128, 256]:
            for level in range(10, max_level + 1, 5):
                zs = estimate_zip_size(branching, level, payload)
                if zs > max_bytes:
                    continue
                tf = branching ** level
                tb = tf * payload
                if tb > best_output:
                    best_output = tb
                    best = {
                        'branching': branching,
                        'level': level,
                        'payload': payload,
                        'zip_size': zs,
                        'total_files': tf,
                        'total_bytes': tb,
                        'ratio': tb / zs,
                    }
    return best


def compare():
    """print comparison table."""
    print("\n  TERMINUS CONFIG COMPARISON")
    print("  " + "=" * 75)
    print(f"  {'Config':<25} {'Zip':>10} {'Files':>12} {'Output':>15} {'Ratio':>15}")
    print("  " + "-" * 75)

    configs = [
        ("Terminus (16^50, 43B)", 16, 50, 43),
        ("Deep (16^100, 43B)", 16, 100, 43),
        ("Wide (256^50, 1B)", 256, 50, 1),
        ("Extreme (256^100, 1B)", 256, 100, 1),
        ("Mega (256^150, 1B)", 256, 150, 1),
        ("Ultra (65536^100, 1B)", 65536, 100, 1),
    ]

    for name, br, lv, pl in configs:
        zs = estimate_zip_size(br, lv, pl)
        tf = br ** lv
        tb = tf * pl
        zip_kb = zs // 1024
        # ratio as string to avoid overflow
        digits_tf = len(str(tf))
        digits_tb = len(str(tb))
        print(f"  {name:<25} {zip_kb:>10}KB 10^{digits_tf-1:<3} files 10^{digits_tb-1:<3} bytes")

    print("  " + "=" * 75)

    print("\n  OPTIMAL (within 500KB zip)")
    print("  " + "-" * 75)
    best = find_optimal(500, 200)
    if best:
        print(f"  branching:   {best['branching']}")
        print(f"  level:       {best['level']}")
        print(f"  payload:     {best['payload']}B")
        print(f"  zip size:    {best['zip_size']/1024:.1f}KB")
        print(f"  total files: {best['total_files']:.4e}")
        print(f"  output:      {best['total_bytes']:.4e} bytes")
        print(f"  ratio:       1:{best['ratio']:.4e}")
    print("  " + "=" * 75)


if __name__ == "__main__":
    compare()
