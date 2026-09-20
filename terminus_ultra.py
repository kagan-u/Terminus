#!/usr/bin/env python3
"""
TERMINUS ULTRA
the most powerful version.

branching: 256, level: 100, payload: 1 byte
theoretical: 256^100 = 10^240 files

educational / research artifact.
"""

import zipfile
import io
import sys
import time


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


def build(name='ultra', branching=256, level=100, payload=1):
    total_files = branching ** level
    total_bytes = total_files * payload

    print(f"\n  TERMINUS {name.upper()}")
    print(f"  branching: {branching} | level: {level} | payload: {payload}B")
    print(f"  files:  {total_files:.4e}")
    print(f"  output: {total_bytes:.4e} bytes")
    print(f"  atoms:  10^80")
    print(f"  ratio:  {total_bytes/1e80:.4e}x universe")
    print()

    start = time.time()

    for depth in range(level + 1):
        data = create_level(depth, branching, payload)
        size = len(data)

        elapsed = time.time() - start
        eta = (elapsed / depth) * (level - depth) if depth > 0 else 0

        sys.stdout.write(
            f"\r  depth {depth:>3}/{level} | "
            f"zip: {size:>10,}B | "
            f"eta: {eta:>6.0f}s"
        )
        sys.stdout.flush()

    elapsed = time.time() - start
    print(f"\n\n  build: {elapsed:.1f}s | zip: {size:,} bytes ({size/1024:.1f} KB)")

    output = f"Terminus_{name}.zip"
    with open(output, "wb") as f:
        f.write(data)
    print(f"  saved: {output}\n")


def list_versions():
    print("\n  TERMINUS VERSIONS")
    print("  " + "=" * 60)
    print(f"  {'Name':<12} {'Branch':>8} {'Level':>6} {'Payload':>8} {'Files':>12} {'Output':>12}")
    print("  " + "-" * 60)

    for name, cfg in VERSIONS.items():
        br = cfg['branching']
        lv = cfg['level']
        pl = cfg['payload']
        tf = br ** lv
        tb = tf * pl
        digits_tf = len(str(tf))
        digits_tb = len(str(tb))
        print(f"  {name:<12} {br:>8} {lv:>6} {pl:>8}B  10^{digits_tf-1:<3}    10^{digits_tb-1:<3}")

    print("  " + "=" * 60)


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == '--list':
        list_versions()
    elif len(sys.argv) >= 2 and sys.argv[1] in VERSIONS:
        cfg = VERSIONS[sys.argv[1]]
        build(sys.argv[1], cfg['branching'], cfg['level'], cfg['payload'])
    elif len(sys.argv) >= 4:
        br = min(int(sys.argv[1]), 65536)
        lv = min(int(sys.argv[2]), 200)
        pl = min(int(sys.argv[3]), 1000)
        build('custom', br, lv, pl)
    else:
        list_versions()
        print("\n  usage: python3 terminus_ultra.py [version]")
        print("  example: python3 terminus_ultra.py ultra\n")
