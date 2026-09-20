#!/usr/bin/env python3
"""
terminus simulator
run this to see what terminus.zip would do if extracted.
no files are created, it's all math.
"""

import math
import sys


def fmt_iec(b):
    """1024-based units (KiB, MiB, etc)"""
    if b == 0:
        return "0 B"
    units = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']
    i = 0
    while b >= 1024 and i < len(units) - 1:
        b /= 1024
        i += 1
    return f"{b:.2f} {units[i]}"


def fmt_si(b):
    """1000-based units (kB, MB, etc)"""
    if b == 0:
        return "0 B"
    units = ['B', 'kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    i = 0
    while b >= 1000 and i < len(units) - 1:
        b /= 1000
        i += 1
    return f"{b:.2f} {units[i]}"


def simulate(branching, level, payload):
    """
    core simulation. models the recursive zip structure.

    the zip size model is based on empirical measurements of actual
    terminus builds. level 0 starts at ~120 bytes (zip headers + 43 byte
    payload), and each additional level adds roughly 8KB because we're
    storing 16 identical copies of the previous level.

    DEFLATE is really good at deduplication, so the 16 copies don't
    multiply the size by 16 -- they just add a flat overhead.
    """
    L0_SIZE = 120      # level 0 zip size in bytes
    LEVEL_GROWTH = 8192  # bytes added per level (~8KB)

    total_files = branching ** level
    total_bytes = total_files * payload

    levels = []
    for d in range(level + 1):
        if d == 0:
            zip_size = L0_SIZE
        else:
            zip_size = L0_SIZE + d * LEVEL_GROWTH

        files_here = branching ** d
        uncompressed = files_here * payload
        ratio = uncompressed / zip_size if zip_size > 0 else 0

        levels.append({
            'depth': d,
            'zip_size': zip_size,
            'files': files_here,
            'uncompressed': uncompressed,
            'ratio': ratio,
        })

    return {
        'branching': branching,
        'level': level,
        'payload': payload,
        'levels': levels,
        'total_files': total_files,
        'total_bytes': total_bytes,
        'zip_size': levels[-1]['zip_size'],
        'ratio': total_bytes / levels[-1]['zip_size'],
    }


def print_results(r):
    br, lv, pl = r['branching'], r['level'], r['payload']

    print()
    print("=" * 72)
    print("  TERMINUS - SAFE SIMULATION")
    print("  no files created, no risk. just math.")
    print("=" * 72)
    print()

    # config
    print(f"  config: branching={br}  level={lv}  payload={pl}B")
    print()

    # main results
    digits_count = int(math.log10(r['total_files'])) + 1

    print("  results:")
    print(f"    total files:      {r['total_files']:,}")
    print(f"    digits:           {digits_count}")
    print(f"    scientific:       {r['total_files']:.4e}")
    print()
    print(f"    zip size:         {fmt_iec(r['zip_size'])} / {fmt_si(r['zip_size'])}")
    print(f"    output size:      {fmt_iec(r['total_bytes'])} / {fmt_si(r['total_bytes'])}")
    print(f"    output scientific:{r['total_bytes']:.4e}")
    print()
    print(f"    ratio:            1:{r['ratio']:.4e}")
    print()

    # level table
    print("  level-by-level breakdown:")
    print("  " + "-" * 68)
    print(f"  {'lv':>4}  {'zip size':>12}  {'files':>25}  {'digits':>7}  {'ratio':>14}")
    print("  " + "-" * 68)

    for lv in r['levels']:
        d = lv['depth']
        # show first 6, then every 10th, then the last one
        if d <= 5 or d % 10 == 0 or d == r['level']:
            z = fmt_iec(lv['zip_size'])
            f = f"{lv['files']:,}"
            dg = int(math.log10(lv['files'])) + 1
            rt = f"{lv['ratio']:.2e}"
            print(f"  {d:>4}  {z:>12}  {f:>25}  {dg:>7}  1:{rt:>12}")

    print("  " + "-" * 68)
    print()

    # comparisons
    wiki = r['total_bytes'] / (20 * 1024**3)
    inet = r['total_bytes'] / (120 * 1024**7)
    atoms = 10**80 / r['total_files']

    print("  comparisons:")
    print(f"    vs wikipedia (20GB):       {wiki:.2e}x bigger")
    print(f"    vs entire internet (120ZB): {inet:.2e}x bigger")
    print(f"    vs atoms in universe:       {atoms:.2e}x smaller (atoms win)")
    print()

    # zip structure note
    print("  zip structure:")
    print("    terminus.zip contains 16 files (bomb_0000.zip to bomb_0015.zip)")
    print("    each is ~30.75 KiB, all identical")
    print("    DEFLATE stores 16 identical copies once, so overhead is minimal")
    print("    each level adds ~8KB to the zip but multiplies output by 16")
    print()

    print("=" * 72)
    print("  done. nothing was created.")
    print("=" * 72)
    print()


def main():
    # defaults match the actual terminus.zip
    DEFAULT_BR = 16
    DEFAULT_LV = 50
    DEFAULT_PL = 43

    if len(sys.argv) >= 4:
        # cli mode: terminus_sim.py branching level payload
        try:
            br = int(sys.argv[1])
            lv = int(sys.argv[2])
            pl = int(sys.argv[3])
        except ValueError:
            print("usage: python3 terminus_sim.py [branching] [level] [payload]")
            sys.exit(1)
    else:
        # interactive mode
        print()
        print("  TERMINUS simulator")
        print("  enter values or press enter for defaults")
        print()
        try:
            raw = input(f"  branching  [{DEFAULT_BR}]: ").strip()
            br = int(raw) if raw else DEFAULT_BR

            raw = input(f"  level      [{DEFAULT_LV}]: ").strip()
            lv = int(raw) if raw else DEFAULT_LV

            raw = input(f"  payload    [{DEFAULT_PL}]: ").strip()
            pl = int(raw) if raw else DEFAULT_PL
        except (ValueError, EOFError):
            br, lv, pl = DEFAULT_BR, DEFAULT_LV, DEFAULT_PL

    # safety caps
    lv = min(lv, 200)
    br = min(br, 1000)
    pl = min(pl, 10000)

    r = simulate(br, lv, pl)
    print_results(r)


if __name__ == "__main__":
    main()
