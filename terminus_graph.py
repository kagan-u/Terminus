#!/usr/bin/env python3
"""
terminus graphics
matplotlib charts for visual analysis.
"""

import math
import sys
import os

try:
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    import numpy as np
except ImportError:
    print("  pip install matplotlib numpy")
    sys.exit(1)

OUTPUT_DIR = "terminus_charts"

def quadratic_model(level):
    a, b, c = 68.5, 5850.0, 120.0
    return a * level**2 + b * level + c

def generate_all():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    levels = np.arange(0, 51, 1)
    zip_sizes = [quadratic_model(d) for d in levels]
    file_counts = [16**d for d in levels]
    output_bytes = [16**d * 43 for d in levels]
    ratios = [o / z if z > 0 else 0 for o, z in zip(output_bytes, zip_sizes)]

    plt.style.use('dark_background')
    fig_color = '#0d1117'
    accent = '#58a6ff'

    # ---- chart 1: zip size growth ----
    fig, ax = plt.subplots(figsize=(12, 6), facecolor=fig_color)
    ax.set_facecolor(fig_color)
    ax.fill_between(levels, zip_sizes, alpha=0.3, color=accent)
    ax.plot(levels, zip_sizes, color=accent, linewidth=2)
    ax.set_xlabel('Depth Level', fontsize=12, color='white')
    ax.set_ylabel('Zip Size (bytes)', fontsize=12, color='white')
    ax.set_title('TERMINUS — Zip Size Growth (Quadratic Model)', fontsize=14, color='white', fontweight='bold')
    ax.tick_params(colors='white')
    ax.grid(True, alpha=0.2)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x/1024:.0f} KB' if x >= 1024 else f'{x:.0f} B'))
    for spine in ax.spines.values():
        spine.set_color('#30363d')
    fig.tight_layout()
    fig.savefig(f'{OUTPUT_DIR}/01_zip_size_growth.png', dpi=150, facecolor=fig_color)
    plt.close()
    print(f"  [1/7] {OUTPUT_DIR}/01_zip_size_growth.png")

    # ---- chart 2: file count explosion (log scale) ----
    fig, ax = plt.subplots(figsize=(12, 6), facecolor=fig_color)
    ax.set_facecolor(fig_color)
    ax.plot(levels, file_counts, color='#f85149', linewidth=2)
    ax.set_yscale('log')
    ax.set_xlabel('Depth Level', fontsize=12, color='white')
    ax.set_ylabel('Total Files (log)', fontsize=12, color='white')
    ax.set_title('TERMINUS — File Count Explosion', fontsize=14, color='white', fontweight='bold')
    ax.tick_params(colors='white')
    ax.grid(True, alpha=0.2, which='both')
    for spine in ax.spines.values():
        spine.set_color('#30363d')
    fig.tight_layout()
    fig.savefig(f'{OUTPUT_DIR}/02_file_count_explosion.png', dpi=150, facecolor=fig_color)
    plt.close()
    print(f"  [2/7] {OUTPUT_DIR}/02_file_count_explosion.png")

    # ---- chart 3: compression ratio (log scale) ----
    fig, ax = plt.subplots(figsize=(12, 6), facecolor=fig_color)
    ax.set_facecolor(fig_color)
    ax.plot(levels[3:], ratios[3:], color='#f0883e', linewidth=2)
    ax.set_yscale('log')
    ax.set_xlabel('Depth Level', fontsize=12, color='white')
    ax.set_ylabel('Compression Ratio (log)', fontsize=12, color='white')
    ax.set_title('TERMINUS — Compression Ratio vs Depth', fontsize=14, color='white', fontweight='bold')
    ax.tick_params(colors='white')
    ax.grid(True, alpha=0.2, which='both')
    for spine in ax.spines.values():
        spine.set_color('#30363d')
    fig.tight_layout()
    fig.savefig(f'{OUTPUT_DIR}/03_compression_ratio.png', dpi=150, facecolor=fig_color)
    plt.close()
    print(f"  [3/7] {OUTPUT_DIR}/03_compression_ratio.png")

    # ---- chart 4: zip size vs output (dual axis) ----
    fig, ax1 = plt.subplots(figsize=(12, 6), facecolor=fig_color)
    ax1.set_facecolor(fig_color)
    ax1.fill_between(levels, zip_sizes, alpha=0.3, color=accent)
    ax1.plot(levels, zip_sizes, color=accent, linewidth=2, label='Zip Size')
    ax1.set_xlabel('Depth Level', fontsize=12, color='white')
    ax1.set_ylabel('Zip Size (bytes)', fontsize=12, color=accent)
    ax1.tick_params(axis='y', colors=accent)
    ax1.tick_params(axis='x', colors='white')
    ax2 = ax1.twinx()
    ax2.plot(levels, output_bytes, color='#f85149', linewidth=2, label='Output Size')
    ax2.set_yscale('log')
    ax2.set_ylabel('Output Size (bytes, log)', fontsize=12, color='#f85149')
    ax2.tick_params(axis='y', colors='#f85149')
    ax1.set_title('TERMINUS — Zip Size vs Output Size', fontsize=14, color='white', fontweight='bold')
    ax1.grid(True, alpha=0.2)
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', facecolor='#161b22', edgecolor='#30363d', labelcolor='white')
    for spine in ax1.spines.values():
        spine.set_color('#30363d')
    for spine in ax2.spines.values():
        spine.set_color('#30363d')
    fig.tight_layout()
    fig.savefig(f'{OUTPUT_DIR}/04_zip_vs_output.png', dpi=150, facecolor=fig_color)
    plt.close()
    print(f"  [4/7] {OUTPUT_DIR}/04_zip_vs_output.png")

    # ---- chart 5: known bombs comparison (bar) ----
    bombs = ['42.zip', 'zipbomb.py', 'Terminus']
    bomb_sizes_kb = [42, 10240, 508.95]
    bomb_outputs_pb = [4.5, 0.01, 6.91e46]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), facecolor=fig_color)
    for ax in [ax1, ax2]:
        ax.set_facecolor(fig_color)
        ax.tick_params(colors='white')
        for spine in ax.spines.values():
            spine.set_color('#30363d')

    colors = ['#238636', '#58a6ff', '#f85149']
    bars1 = ax1.bar(bombs, bomb_sizes_kb, color=colors, edgecolor='white', linewidth=0.5)
    ax1.set_ylabel('Zip Size (KB)', fontsize=12, color='white')
    ax1.set_title('Zip Size Comparison', fontsize=13, color='white', fontweight='bold')
    ax1.set_yscale('log')
    ax1.grid(True, alpha=0.2, axis='y')

    bars2 = ax2.bar(bombs, bomb_outputs_pb, color=colors, edgecolor='white', linewidth=0.5)
    ax2.set_ylabel('Output Size (PB, log)', fontsize=12, color='white')
    ax2.set_title('Output Size Comparison', fontsize=13, color='white', fontweight='bold')
    ax2.set_yscale('log')
    ax2.grid(True, alpha=0.2, axis='y')

    fig.suptitle('TERMINUS vs Known Zip Bombs', fontsize=14, color='white', fontweight='bold', y=1.02)
    fig.tight_layout()
    fig.savefig(f'{OUTPUT_DIR}/05_bombs_comparison.png', dpi=150, facecolor=fig_color, bbox_inches='tight')
    plt.close()
    print(f"  [5/7] {OUTPUT_DIR}/05_bombs_comparison.png")

    # ---- chart 6: scale comparison (bubble) ----
    refs = ['Wikipedia', 'Internet', 'Stars', 'Sand', 'Cells', 'Atoms', 'Terminus']
    ref_sizes = [20e9, 120e27, 1e24, 7.5e18, 3.7e13, 1e80, 6.91e61]
    ref_colors = ['#8b949e', '#8b949e', '#8b949e', '#8b949e', '#8b949e', '#8b949e', '#f85149']

    fig, ax = plt.subplots(figsize=(12, 6), facecolor=fig_color)
    ax.set_facecolor(fig_color)
    scatter = ax.scatter(range(len(refs)), [1]*len(refs), s=[math.log10(s)*50 for s in ref_sizes], c=ref_colors, alpha=0.7, edgecolors='white', linewidths=0.5)
    for i, (name, size) in enumerate(zip(refs, ref_sizes)):
        ax.annotate(f'{name}\n{size:.1e}', (i, 1), textcoords="offset points", xytext=(0, -40 if i != 6 else 30), ha='center', fontsize=9, color='white', fontweight='bold' if i == 6 else 'normal')
    ax.set_xlim(-0.5, len(refs) - 0.5)
    ax.set_ylim(0.5, 1.5)
    ax.axis('off')
    ax.set_title('TERMINUS — Scale Comparison (bubble size = log₁₀(bytes))', fontsize=14, color='white', fontweight='bold')
    fig.tight_layout()
    fig.savefig(f'{OUTPUT_DIR}/06_scale_comparison.png', dpi=150, facecolor=fig_color)
    plt.close()
    print(f"  [6/7] {OUTPUT_DIR}/06_scale_comparison.png")

    # ---- chart 7: growth breakdown (stacked area) ----
    fig, ax = plt.subplots(figsize=(12, 6), facecolor=fig_color)
    ax.set_facecolor(fig_color)
    zip_overhead = [z - 120 for z in zip_sizes]
    payload_total = [16**d * 43 for d in levels]
    ax.stackplot(levels, zip_overhead, payload_total, labels=['Zip Overhead', 'Payload Total'], colors=['#58a6ff', '#f85149'], alpha=0.7)
    ax.set_yscale('log')
    ax.set_xlabel('Depth Level', fontsize=12, color='white')
    ax.set_ylabel('Size (bytes, log)', fontsize=12, color='white')
    ax.set_title('TERMINUS — Growth Breakdown (Overhead vs Payload)', fontsize=14, color='white', fontweight='bold')
    ax.tick_params(colors='white')
    ax.grid(True, alpha=0.2, which='both')
    ax.legend(loc='upper left', facecolor='#161b22', edgecolor='#30363d', labelcolor='white')
    for spine in ax.spines.values():
        spine.set_color('#30363d')
    fig.tight_layout()
    fig.savefig(f'{OUTPUT_DIR}/07_growth_breakdown.png', dpi=150, facecolor=fig_color)
    plt.close()
    print(f"  [7/7] {OUTPUT_DIR}/07_growth_breakdown.png")

    print(f"\n  all charts saved to {OUTPUT_DIR}/")

if __name__ == "__main__":
    print("\n  \033[96mTERMINUS CHART GENERATOR\033[0m\n")
    generate_all()
