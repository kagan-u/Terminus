#!/usr/bin/env python3
"""
TERMINUS HASH
integrity verification for Terminus artifacts.
"""

import hashlib
import sys
import os
import json

KNOWN = {
    'Terminus.zip': {
        'sha256': '5269c1b60f9497eb8a6bf9734e819f2a2e2aa2d2b8166fe49f116d852b5522de',
        'size': 508950,
    },
}


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()


def verify(path):
    name = os.path.basename(path)
    actual = sha256_of(path)
    size = os.path.getsize(path)

    print(f"\n  FILE: {path}")
    print(f"  SIZE: {size:,} bytes")
    print(f"  SHA256: {actual}")

    if name in KNOWN:
        expected = KNOWN[name]
        size_ok = size == expected['size']
        hash_ok = actual == expected['sha256']

        print(f"  EXPECTED SIZE: {expected['size']:,} bytes  [{'OK' if size_ok else 'FAIL'}]")
        print(f"  EXPECTED SHA256: {expected['sha256']}")
        print(f"  HASH: [{'OK' if hash_ok else 'FAIL'}]")

        if size_ok and hash_ok:
            print("\n  [+] INTEGRITY OK\n")
            return True
        else:
            print("\n  [!] INTEGRITY CHECK FAILED\n")
            return False
    else:
        print("  (no known reference for this file)")
        print()
        return True


def generate_manifest():
    manifest = {}
    for name, info in KNOWN.items():
        if os.path.exists(name):
            manifest[name] = {
                'sha256': sha256_of(name),
                'size': os.path.getsize(name),
            }
    with open('MANIFEST.json', 'w') as f:
        json.dump(manifest, f, indent=2)
    print("  MANIFEST.json generated")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        target = 'Terminus.zip'
    elif sys.argv[1] == '--manifest':
        generate_manifest()
        sys.exit(0)
    else:
        target = sys.argv[1]

    if not os.path.exists(target):
        print(f"  file not found: {target}")
        sys.exit(1)

    ok = verify(target)
    sys.exit(0 if ok else 1)
