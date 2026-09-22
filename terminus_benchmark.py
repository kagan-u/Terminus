#!/usr/bin/env python3
"""
TERMINUS BENCHMARK
measures compression performance and memory usage.
"""

import time
import zipfile
import io
import sys
import os
import gc
import tracemalloc
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def bench_build(branching, level, payload):
    """benchmark a build cycle."""
    tracemalloc.start()

    def create(depth):
        if depth == 0:
            buf = io.BytesIO()
            with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
                zf.writestr("x", b'\x00' * payload)
            return buf.getvalue()
        inner = create(depth - 1)
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
            for i in range(branching):
                zf.writestr(f"{i:02x}", inner)
        return buf.getvalue()

    gc.collect()
    start = time.perf_counter()
    data = create(level)
    elapsed = time.perf_counter() - start

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        'branching': branching,
        'level': level,
        'payload': payload,
        'zip_size': len(data),
        'build_time': elapsed,
        'peak_memory': peak,
    }


def bench_extract(level, branching, payload):
    """benchmark reading (not extracting) nested structure."""
    def create(depth):
        if depth == 0:
            buf = io.BytesIO()
            with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
                zf.writestr("x", b'\x00' * payload)
            return buf.getvalue()
        inner = create(depth - 1)
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
            for i in range(branching):
                zf.writestr(f"{i:02x}", inner)
        return buf.getvalue()

    data = create(min(level, 5))

    gc.collect()
    start = time.perf_counter()
    depth_read = 0
    current = data
    while depth_read < min(level, 20):
        if not zipfile.is_zipfile(io.BytesIO(current)):
            break
        with zipfile.ZipFile(io.BytesIO(current), 'r') as zf:
            names = zf.namelist()
            if not names:
                break
            current = zf.read(names[0])
            depth_read += 1
    elapsed = time.perf_counter() - start

    return {
        'depth_read': depth_read,
        'read_time': elapsed,
    }


def compression_ratio_test(payload_size):
    """test DEFLATE compression ratio for different payload sizes."""
    data = b'\x00' * payload_size
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        zf.writestr("x", data)
    return len(buf.getvalue()), payload_size


def run_benchmarks():
    print("\n  TERMINUS BENCHMARK")
    print("  " + "=" * 70)

    # build benchmarks
    print("\n  [1] BUILD PERFORMANCE\n")
    print(f"  {'Config':<25} {'Zip':>10} {'Time':>10} {'Peak Mem':>12}")
    print("  " + "-" * 60)

    configs = [
        (16, 10, 43),
        (16, 20, 43),
        (16, 30, 43),
        (16, 40, 43),
        (16, 50, 43),
        (256, 20, 1),
    ]

    results = []
    for br, lv, pl in configs:
        r = bench_build(br, lv, pl)
        results.append(r)
        print(
            f"  {f'{br}^{lv}x{pl}B':<25} "
            f"{r['zip_size']//1024:>8}KB "
            f"{r['build_time']:>8.3f}s "
            f"{r['peak_memory']//1024:>10}KB"
        )

    # extraction read benchmarks
    print("\n  [2] READ PERFORMANCE (nested traversal)\n")
    for br, lv, pl in [(16, 20, 43), (16, 30, 43)]:
        r = bench_extract(lv, br, pl)
        print(f"  {f'{br}^{lv}':<20} read {r['depth_read']:>2} levels in {r['read_time']:.4f}s")

    # compression ratio
    print("\n  [3] DEFLATE RATIO (zeros payload)\n")
    print(f"  {'Payload':>12} {'Zip':>10} {'Ratio':>15}")
    print("  " + "-" * 40)
    for size in [1, 10, 100, 1000, 10000, 100000]:
        zs, orig = compression_ratio_test(size)
        ratio = orig / zs if zs > 0 else 0
        print(f"  {orig:>10}B {zs:>8}B {ratio:>14.1f}x")

    # summary
    print("\n  [4] SUMMARY\n")
    best_ratio = max(results, key=lambda r: r['zip_size'])
    fastest = min(results, key=lambda r: r['build_time'])
    smallest_mem = min(results, key=lambda r: r['peak_memory'])
    print(f"  largest zip:  {best_ratio['branching']}^{best_ratio['level']} = {best_ratio['zip_size']//1024}KB")
    print(f"  fastest:      {fastest['branching']}^{fastest['level']} = {fastest['build_time']:.3f}s")
    print(f"  lightest:     {smallest_mem['branching']}^{smallest_mem['level']} = {smallest_mem['peak_memory']//1024}KB peak")
    print("  " + "=" * 70)


if __name__ == "__main__":
    run_benchmarks()
