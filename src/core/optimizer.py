#!/usr/bin/env python3
"""
TERMINUS OPTIMIZER
finds the optimal configuration for maximum damage.
"""

import math
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def zip_overhead_per_entry():
    """minimum bytes per zip entry (header + footer)."""
    # local file header: 30 bytes + filename
    # data descriptor: 16 bytes
    # central directory: 46 bytes + filename
    # end of central directory: 22 bytes
    return 30 + 1 + 16 + 46 + 1 + 22  # ~116 bytes minimum per entry


def estimate_zip_size(branching, level, payload):
    """estimate zip size for given config."""
    overhead = zip_overhead_per_entry()
    entry_size = overhead + payload
    # each level multiplies entries by branching
    total_entries = sum(branching ** d for d in range(level + 1))
    return total_entries * entry_size


def find_optimal(max_zip_kb=500, max_level=200):
    """find optimal config within zip size limit."""
    max_bytes = max_zip_kb * 1024

    print("\n  TERMINUS OPTIMIZER")
    print("  " + "=" * 50)
    print(f"  max zip size: {max_zip_kb} KB")
    print(f"  max level: {max_level}")
    print()

    best = None
    best_output = 0

    for branching in [4, 8, 16, 32, 64, 128, 256]:
        for payload in [1, 2, 4, 8, 16, 32, 43, 64, 128, 256]:
            for level in range(10, max_level + 1, 5):
                zip_size = estimate_zip_size(branching, level, payload)
                if zip_size > max_bytes:
                    continue

                total_files = branching ** level
                total_bytes = total_files * payload
                ratio = total_bytes / zip_size

                if total_bytes > best_output:
                    best_output = total_bytes
                    best = {
                        'branching': branching,
                        'level': level,
                        'payload': payload,
                        'zip_size': zip_size,
                        'total_files': total_files,
                        'total_bytes': total_bytes,
                        'ratio': ratio,
                    }

    if best:
        print("  OPTIMAL CONFIGURATION")
        print("  " + "-" * 50)
        print(f"  branching:   {best['branching']}")
        print(f"  level:       {best['level']}")
        print(f"  payload:     {best['payload']} bytes")
        print(f"  zip size:    {best['zip_size']/1024:.1f} KB")
        print(f"  total files: {best['total_files']:.4e}")
        print(f"  output:      {best['total_bytes']:.4e} bytes")
        print(f"  ratio:       1:{best['ratio']:.4e}")
        print("  " + "=" * 50)

    return best


def compare_configs():
    """compare different configurations."""
    print("\n  CONFIGURATION COMPARISON")
    print("  " + "=" * 70)
    print(f"  {'Config':<25} {'Zip':>10} {'Files':>12} {'Output':>15} {'Ratio':>15}")
    print("  " + "-" * 70)

    configs = [
        ("current (16^50, 43B)", 16, 50, 43),
        ("deep (16^100, 43B)", 16, 100, 43),
        ("wide (256^50, 1B)", 256, 50, 1),
        ("extreme (256^100, 1B)", 256, 100, 1),
        ("mega (256^150, 1B)", 256, 150, 1),
        ("ultra (65536^100, 1B)", 65536, 100, 1),
    ]

    for name, br, lv, pl in configs:
        zs = estimate_zip_size(br, lv, pl)
        tf = br ** lv
        tb = tf * pl
        rt = tb / zs
        print(f"  {name:<25} {zs/1024:>8.1f}KB {tf:>12.2e} {tb:>15.2e} 1:{rt:.2e}")

    print("  " + "=" * 70)


if __name__ == "__main__":
    compare_configs()
    print()
    find_optimal(500, 200)
