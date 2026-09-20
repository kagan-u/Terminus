#!/usr/bin/env python3
"""
terminus video generator
creates an mp4 video showing the recursive explosion.
requires: pip install matplotlib numpy imageio[ffmpeg]
"""

import math
import sys
import os
import shutil

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import numpy as np
except ImportError:
    print("  pip install matplotlib numpy")
    sys.exit(1)

try:
    import imageio.v2 as imageio
except ImportError:
    print("  pip install imageio[ffmpeg]")
    sys.exit(1)

OUTPUT_DIR = "terminus_frames"
VIDEO_FILE = "terminus_explosion.mp4"
FPS = 30
DURATION = 10  # seconds
TOTAL_FRAMES = FPS * DURATION

def quadratic_model(level):
    a, b, c = 68.5, 5850.0, 120.0
    return a * level**2 + b * level + c

def sci(n):
    return f"{n:.2e}"

def create_frame(frame_num):
    """create a single frame of the video."""
    t = frame_num / TOTAL_FRAMES  # 0.0 to 1.0

    fig, ax = plt.subplots(figsize=(16, 9), facecolor='#0d1117')
    ax.set_facecolor('#0d1117')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)
    ax.axis('off')

    # phase 1: title (0-15%)
    if t < 0.15:
        alpha = max(0.0, min(1.0, t / 0.05)) if t < 0.05 else max(0.0, min(1.0, 1.0 - (t - 0.10) / 0.05))
        ax.text(50, 45, 'TERMINUS', fontsize=48, color='white', ha='center', va='center',
                fontweight='bold', alpha=alpha)
        ax.text(50, 35, '497 KB -> 6.91e61 bytes', fontsize=20, color='#58a6ff', ha='center',
                va='center', alpha=alpha)

    # phase 2: zip file visual (15-35%)
    elif t < 0.35:
        progress = (t - 0.15) / 0.20
        num_zips = int(progress * 16)
        for i in range(min(num_zips, 16)):
            row = i // 4
            col = i % 4
            x = 20 + col * 15
            y = 15 + row * 12
            rect = mpatches.FancyBboxPatch((x, y), 10, 8, boxstyle="round,pad=0.3",
                                           facecolor='#161b22', edgecolor='#58a6ff', linewidth=1.5)
            ax.add_patch(rect)
            ax.text(x + 5, y + 4, f'bomb_{i:04d}.zip', fontsize=7, color='#8b949e',
                    ha='center', va='center')
        ax.text(50, 55, f'Extracting Terminus.zip... {num_zips}/16', fontsize=16,
                color='#58a6ff', ha='center', va='center')

    # phase 3: level progression (35-70%)
    elif t < 0.70:
        progress = (t - 0.35) / 0.35
        level = int(progress * 50)
        level = min(level, 50)

        ax.text(50, 55, f'Level {level}', fontsize=24, color='#f0883e', ha='center',
                va='center', fontweight='bold')

        zip_size = quadratic_model(level)
        files = 16 ** level
        output_bytes = files * 43

        # zip size bar
        bar_width = (zip_size / quadratic_model(50)) * 60
        rect = mpatches.FancyBboxPatch((20, 38), bar_width, 6, boxstyle="round,pad=0.3",
                                       facecolor='#58a6ff', edgecolor='#8b949e', linewidth=1)
        ax.add_patch(rect)
        ax.text(20 + bar_width / 2, 41, f'{zip_size/1024:.1f} KB', fontsize=10, color='white',
                ha='center', va='center')

        # file count
        if level <= 10:
            file_str = f'{files:,}'
        else:
            file_str = sci(files)
        ax.text(50, 28, f'{file_str} files', fontsize=18, color='#f85149', ha='center',
                va='center')

        # output size
        ax.text(50, 18, f'{sci(output_bytes)} bytes', fontsize=14, color='#8b949e',
                ha='center', va='center')

        # ratio
        ratio = output_bytes / zip_size if zip_size > 0 else 0
        ax.text(50, 8, f'Ratio: 1:{sci(ratio)}', fontsize=12, color='#3fb950', ha='center',
                va='center')

    # phase 4: final explosion (70-90%)
    elif t < 0.90:
        progress = (t - 0.70) / 0.20

        # expanding circles
        for i in range(20):
            radius = progress * (i + 1) * 3
            alpha = max(0, 1.0 - progress * 1.5) * (1 - i / 20)
            circle = plt.Circle((50, 30), radius, fill=False, color='#f85149',
                                linewidth=0.5, alpha=alpha)
            ax.add_patch(circle)

        # text
        ax.text(50, 45, '1.61e60 files', fontsize=36, color='#f85149', ha='center',
                va='center', fontweight='bold', alpha=progress)
        ax.text(50, 30, '6.91e61 bytes', fontsize=24, color='#f0883e', ha='center',
                va='center', alpha=progress)
        ax.text(50, 15, 'from 497 KB', fontsize=18, color='#58a6ff', ha='center',
                va='center', alpha=progress)

    # phase 5: outro (90-100%)
    else:
        progress = (t - 0.90) / 0.10
        ax.text(50, 40, 'TERMINUS', fontsize=48, color='white', ha='center', va='center',
                fontweight='bold')
        ax.text(50, 28, '497 KB compressed', fontsize=16, color='#58a6ff', ha='center',
                va='center')
        ax.text(50, 22, '6.91 x 10^61 bytes output', fontsize=16, color='#f85149', ha='center',
                va='center')
        ax.text(50, 12, 'github.com/kagan-u/Terminus', fontsize=12, color='#8b949e',
                ha='center', va='center')

    frame_path = f'{OUTPUT_DIR}/frame_{frame_num:04d}.png'
    fig.savefig(frame_path, dpi=120, facecolor='#0d1117', bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    return frame_path

def generate_video():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"  generating {TOTAL_FRAMES} frames...")
    frames = []
    for i in range(TOTAL_FRAMES):
        path = create_frame(i)
        frames.append(imageio.imread(path))
        if (i + 1) % 30 == 0 or i == TOTAL_FRAMES - 1:
            print(f"    frame {i+1}/{TOTAL_FRAMES}")

    print(f"  encoding video...")
    imageio.mimsave(VIDEO_FILE, frames, fps=FPS, codec='libx264', quality=8)

    # cleanup frames
    shutil.rmtree(OUTPUT_DIR)

    print(f"\n  \033[92mvideo saved: {VIDEO_FILE}\033[0m")
    print(f"  duration: {DURATION}s | fps: {FPS} | resolution: 1920x1080")

if __name__ == "__main__":
    print("\n  \033[96mTERMINUS VIDEO GENERATOR\033[0m\n")
    generate_video()
