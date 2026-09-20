#!/usr/bin/env python3
"""
terminus animation
visual representation of the recursive explosion.
"""

import sys
import time
import math

def sci(n):
    return f"{n:.2e}"

def animate_level(level, branching=16, delay=0.1):
    """animate the extraction process level by level."""
    
    print()
    print("  \033[96m╔═══════════════════════════════════════════════════════╗\033[0m")
    print("  \033[96m║\033[0m \033[93mTERMINUS EXTRACTION SIMULATION\033[0m                     \033[96m║\033[0m")
    print("  \033[96m╚═══════════════════════════════════════════════════════╝\033[0m")
    print()
    
    # phase 1: extraction
    print("  \033[97mPhase 1: Extracting Terminus.zip\033[0m")
    print()
    
    for d in range(min(level + 1, 15)):
        files = branching ** d
        
        # file count visualization
        if files <= 16:
            blocks = files
            viz = "\033[93m" + "█" * blocks + "\033[0m"
        elif files <= 256:
            blocks = int(math.log2(files))
            viz = "\033[93m" + "█" * blocks + "\033[0m" + f" ({files} files)"
        else:
            viz = f"\033[91m{sci(files)} files\033[0m"
        
        print(f"    Level {d:>2}: {viz}")
        time.sleep(delay)
    
    print()
    print("    \033[90m... (continues for 50 levels) ...\033[0m")
    print()
    
    # phase 2: the numbers
    print("  \033[97mPhase 2: The Numbers\033[0m")
    print()
    
    numbers = [
        (0, "120 B", "43 B", "0.36x"),
        (5, "22.40 KB", "43 MB", "1.97e3x"),
        (10, "58.35 KB", "43 TB", "7.93e8x"),
        (15, "96.68 KB", "43 EB", "5.01e14x"),
        (20, "136.51 KB", "43 YB", "3.70e20x"),
        (30, "231.44 KB", "4.62e13 YB", "2.41e32x"),
        (40, "336.19 KB", "5.08e19 YB", "1.77e44x"),
        (50, "508.95 KB", "5.72e37 YB", "1.36e56x"),
    ]
    
    print("    \033[90mZip Size      Output          Ratio\033[0m")
    print("    \033[90m----------    --------------  ----------------\033[0m")
    
    for d, zip_sz, output, ratio in numbers:
        time.sleep(delay * 2)
        
        if d == 50:
            print(f"    \033[93m{zip_sz:<13}\033[0m \033[91m{output:<15}\033[0m \033[91m{ratio}\033[0m  \033[91m<-- TERMINUS\033[0m")
        else:
            print(f"    {zip_sz:<13} {output:<15} {ratio}")
    
    print()
    
    # phase 3: comparison
    print("  \033[97mPhase 3: Scale Comparison\033[0m")
    print()
    
    comparisons = [
        ("Wikipedia", "20 GB", "3.22e51x bigger"),
        ("Internet", "120 ZB", "4.88e38x bigger"),
        ("Stars", "10^24", "6.22e36x bigger"),
        ("Sand", "7.5e18", "2.14e42x bigger"),
        ("Cells", "3.7e13", "4.34e47x bigger"),
        ("Atoms", "10^80", "6.22e20x smaller"),
    ]
    
    for name, size, comparison in comparisons:
        time.sleep(delay * 2)
        print(f"    vs {name:<12} ({size:<8}): \033[93m{comparison}\033[0m")
    
    print()
    
    # phase 4: explosion visualization
    print("  \033[97mPhase 4: Explosion\033[0m")
    print()
    
    explosion_frames = [
        "         \033[93m*\033[0m",
        "        \033[93m***\033[0m",
        "       \033[93m*****\033[0m",
        "      \033[93m*******\033[0m",
        "     \033[93m*********\033[0m",
        "    \033[91m***********\033[0m",
        "   \033[91m*************\033[0m",
        "  \033[91m***************\033[0m",
        " \033[91m*****************\033[0m",
        "\033[91m*******************\033[0m",
    ]
    
    for frame in explosion_frames:
        sys.stdout.write(f"\r    {frame}")
        sys.stdout.flush()
        time.sleep(0.1)
    
    print()
    print()
    
    # final
    print("  \033[91m╔═══════════════════════════════════════════════════════╗\033[0m")
    print("  \033[91m║\033[0m \033[1m1.61 x 10^61 files. 6.91 x 10^61 bytes.\033[0m            \033[91m║\033[0m")
    print("  \033[91m║\033[0m \033[1mThat's what's inside 497 KB.\033[0m                      \033[91m║\033[0m")
    print("  \033[91m╚═══════════════════════════════════════════════════════╝\033[0m")
    print()

def main():
    level = 50
    if len(sys.argv) > 1:
        level = int(sys.argv[1])
    animate_level(level)

if __name__ == "__main__":
    main()
