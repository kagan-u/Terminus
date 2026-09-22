#!/usr/bin/env python3
"""
TERMINUS BUILD
live build simulation with real-time progress.
simulates the recursive build without writing huge files.
"""

import sys
import time
import io
import zipfile
import math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def live_build(branching=16, level=50, payload=43, real=False):
    print("\n  TERMINUS LIVE BUILD")
    print(f"  branching: {branching} | level: {level} | payload: {payload}B")
    print(f"  mode: {'REAL' if real else 'SIMULATED'}")
    print("  " + "=" * 60)

    total_files = branching ** level
    print(f"  target: {total_files:.4e} files")
    print()

    start = time.time()
    zip_size = 120

    for depth in range(level + 1):
        t0 = time.perf_counter()

        if real:
            # actually build this level from scratch (slow for high levels)
            def build(d):
                if d == 0:
                    buf = io.BytesIO()
                    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
                        zf.writestr("x", b'\x00' * payload)
                    return buf.getvalue()
                inner = build(d - 1)
                buf = io.BytesIO()
                with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
                    for i in range(branching):
                        zf.writestr(f"{i:02x}", inner)
                return buf.getvalue()

            try:
                data = build(depth)
                zip_size = len(data)
            except MemoryError:
                print(f"\n  [!] memory limit hit at depth {depth}")
                break
        else:
            # quadratic estimate
            a, b, c = 68.5, 5850.0, 120.0
            zip_size = a * depth**2 + b * depth + c
            zip_size *= (1 + (payload - 43) * 0.001)
            zip_size *= (1 + (branching - 16) * 0.02)
            # simulate build time
            time.sleep(0.01 if depth < 20 else 0.005)

        files_here = branching ** depth
        elapsed = time.time() - start

        # progress bar
        pct = depth / level
        bar_len = 40
        filled = int(pct * bar_len)
        bar = "#" * filled + "-" * (bar_len - filled)

        # output size
        out_bytes = files_here * payload
        if out_bytes < 1024:
            out_str = f"{out_bytes}B"
        elif out_bytes < 1024**2:
            out_str = f"{out_bytes/1024:.1f}KB"
        elif out_bytes < 1024**3:
            out_str = f"{out_bytes/1024**2:.1f}MB"
        else:
            out_str = f"{out_bytes:.2e}B"

        sys.stdout.write(
            f"\r  [{bar}] {pct*100:5.1f}% "
            f"L{depth:>3} | "
            f"zip {zip_size/1024:>7.1f}KB | "
            f"out {out_str:>12} | "
            f"{elapsed:5.1f}s"
        )
        sys.stdout.flush()

    elapsed = time.time() - start

    print(f"\n\n  " + "=" * 60)
    print(f"  BUILD COMPLETE")
    print(f"  time:        {elapsed:.2f}s")
    print(f"  zip size:    {zip_size:,.0f} bytes ({zip_size/1024:.1f} KB)")
    print(f"  total files: {total_files:.4e}")
    print(f"  total bytes: {total_files * payload:.4e}")
    print(f"  ratio:       1:{(total_files * payload) / zip_size:.4e}")
    print(f"  " + "=" * 60)

    if not real:
        print(f"\n  (simulated. use --real for actual build)")

    print()


if __name__ == "__main__":
    real = '--real' in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith('--')]

    br = int(args[0]) if len(args) > 0 else 16
    lv = int(args[1]) if len(args) > 1 else 50
    pl = int(args[2]) if len(args) > 2 else 43

    br = min(br, 1000)
    lv = min(lv, 200)
    pl = min(pl, 10000)

    live_build(br, lv, pl, real)
