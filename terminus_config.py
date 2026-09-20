#!/usr/bin/env python3
"""
TERMINUS CONFIG
finds optimal configuration and compares versions.
"""

VERSIONS = {
    'mini':     {'branching': 4,    'level': 10,  'payload': 43},
    'basic':    {'branching': 8,    'level': 20,  'payload': 43},
    'standard': {'branching': 16,   'level': 50,  'payload': 43},
    'deep':     {'branching': 16,   'level': 100, 'payload': 43},
    'wide':     {'branching': 256,  'level': 50,  'payload': 1},
    'mega':     {'branching': 256,  'level': 150, 'payload': 1},
    'ultra':    {'branching': 256,  'level': 100, 'payload': 1},
    'god':      {'branching': 65536,'level': 100, 'payload': 1},
}


def estimate_zip_size(branching, level, payload):
    """quadratic model calibrated to actual builds."""
    a, b, c = 68.5, 5850.0, 120.0
    base = a * level**2 + b * level + c
    base *= (1 + (payload - 43) * 0.001)
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
                    }
    return best


def compare():
    """print comparison table."""
    print("\n  TERMINUS COMPARISON")
    print("  " + "=" * 75)
    print(f"  {'Version':<12} {'Branch':>8} {'Level':>6} {'Zip':>10} {'Files':>12} {'Output':>12}")
    print("  " + "-" * 75)

    for name, cfg in VERSIONS.items():
        br = cfg['branching']
        lv = cfg['level']
        pl = cfg['payload']
        zs = estimate_zip_size(br, lv, pl)
        tf = br ** lv
        tb = tf * pl
        digits_tf = len(str(tf))
        digits_tb = len(str(tb))
        print(f"  {name:<12} {br:>8} {lv:>6} {zs//1024:>8}KB  10^{digits_tf-1:<3}    10^{digits_tb-1:<3}")

    print("  " + "=" * 75)

    print("\n  OPTIMAL (within 500KB zip)")
    print("  " + "-" * 75)
    best = find_optimal(500, 200)
    if best:
        print(f"  branching:   {best['branching']}")
        print(f"  level:       {best['level']}")
        print(f"  payload:     {best['payload']}B")
        print(f"  zip size:    {best['zip_size']//1024}KB")
        print(f"  total files: {best['total_files']:.4e}")
        print(f"  output:      {best['total_bytes']:.4e} bytes")
    print("  " + "=" * 75)


if __name__ == "__main__":
    compare()
