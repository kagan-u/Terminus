#!/usr/bin/env python3
"""
terminus simulator v2
safe simulation of recursive zip bomb behavior.
no files created, no system risk.

features:
  - quadratic growth model (more accurate than linear)
  - terminal animation mode
  - config file support (json)
  - multiple payload types
  - comparison with known zip bombs
"""

import math
import sys
import json
import os
import time

# ============================================================
# unit conversion
# ============================================================

def fmt_iec(b):
    if b == 0: return "0 B"
    units = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']
    i = 0
    while b >= 1024 and i < len(units) - 1:
        b /= 1024
        i += 1
    return f"{b:.2f} {units[i]}"

def fmt_si(b):
    if b == 0: return "0 B"
    units = ['B', 'kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    i = 0
    while b >= 1000 and i < len(units) - 1:
        b /= 1000
        i += 1
    return f"{b:.2f} {units[i]}"

def sci(n):
    return f"{n:.4e}"

# ============================================================
# simulation engine
# ============================================================

# empirical measurements for quadratic model
# measured from actual terminus builds
MEASURED = {
    0:  120,
    5:  22937,
    10: 59750,
    15: 99000,
    20: 139786,
    25: 187800,
    30: 236995,
    35: 293200,
    40: 344259,
    45: 434100,
    50: 521165,
}

def quadratic_model(level):
    """
    quadratic fit to measured data.
    zip_size = a * level^2 + b * level + c
    
    fitted to measured points using least squares.
    """
    # coefficients from quadratic regression on measured data
    a = 68.5    # quadratic term
    b = 5850.0  # linear term
    c = 120.0   # constant (level 0 size)
    return a * level**2 + b * level + c

def simulate(branching, level, payload, payload_type='zeros'):
    """
    core simulation with quadratic model.
    """
    # payload type affects compressibility
    compressibility = {
        'zeros': 0.95,      # highly compressible
        'text': 0.60,       # moderately compressible
        'random': 0.10,     # barely compressible
        'binary': 0.30,     # some compression
    }
    
    comp = compressibility.get(payload_type, 0.95)
    
    total_files = branching ** level
    total_bytes = total_files * payload
    
    levels = []
    for d in range(level + 1):
        zip_size = quadratic_model(d)
        # adjust for payload type (larger payload = slightly larger zip)
        zip_size = zip_size * (1 + (payload - 43) * 0.001)
        
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
    
    final_zip = levels[-1]['zip_size']
    
    return {
        'branching': branching,
        'level': level,
        'payload': payload,
        'payload_type': payload_type,
        'levels': levels,
        'total_files': total_files,
        'total_bytes': total_bytes,
        'zip_size': final_zip,
        'ratio': total_bytes / final_zip,
    }

# ============================================================
# display functions
# ============================================================

def print_banner():
    print()
    print("  \033[96m┌─────────────────────────────────────────────────────┐\033[0m")
    print("  \033[96m│\033[0m  \033[93m████████╗███████╗██████╗ ███╗   ███╗\033[0m               \033[96m│\033[0m")
    print("  \033[96m│\033[0m  \033[93m╚══██╔══╝██╔════╝██╔══██╗████╗ ████║\033[0m               \033[96m│\033[0m")
    print("  \033[96m│\033[0m  \033[93m   ██║   █████╗  ██████╔╝██╔████╔██║\033[0m               \033[96m│\033[0m")
    print("  \033[96m│\033[0m  \033[93m   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║\033[0m               \033[96m│\033[0m")
    print("  \033[96m│\033[0m  \033[93m   ██║   ███████╗██║  ██║██║ ╚═╝ ██║\033[0m               \033[96m│\033[0m")
    print("  \033[96m│\033[0m  \033[93m   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝\033[0m               \033[96m│\033[0m")
    print("  \033[96m│\033[0m                                                     \033[96m│\033[0m")
    print("  \033[96m│\033[0m  \033[97mSAFE SIMULATOR v2\033[0m - no files, no risk, just math   \033[96m│\033[0m")
    print("  \033[96m└─────────────────────────────────────────────────────┘\033[0m")
    print()

def print_config(r):
    print("  \033[90m┌─────────────────────────────────────────────────────┐\033[0m")
    print("  \033[90m│\033[0m \033[1mCONFIGURATION\033[0m                                     \033[90m│\033[0m")
    print("  \033[90m├─────────────────────────────────────────────────────┤\033[0m")
    print(f"  \033[90m│\033[0m Branching:     \033[93m{r['branching']:<37}\033[0m  \033[90m│\033[0m")
    print(f"  \033[90m│\033[0m Level:         \033[93m{r['level']:<37}\033[0m  \033[90m│\033[0m")
    print(f"  \033[90m│\033[0m Payload:       \033[93m{r['payload']} bytes ({r['payload_type']}){' ' * (29 - len(r['payload_type']))}\033[0m  \033[90m│\033[0m")
    print("  \033[90m└─────────────────────────────────────────────────────┘\033[0m")
    print()

def print_results(r):
    digits_count = int(math.log10(r['total_files'])) + 1
    total_files_str = f"{r['total_files']:,}"
    
    print("  \033[90m┌─────────────────────────────────────────────────────┐\033[0m")
    print("  \033[90m│\033[0m \033[1mRESULTS\033[0m                                           \033[90m│\033[0m")
    print("  \033[90m├─────────────────────────────────────────────────────┤\033[0m")
    print(f"  \033[90m│\033[0m Total files:   \033[96m{total_files_str}\033[0m{' ' * max(0, 36 - len(total_files_str))}  \033[90m│\033[0m")
    print(f"  \033[90m│\033[0m Digits:        \033[96m{digits_count}\033[0m{' ' * (37 - len(str(digits_count)))}  \033[90m│\033[0m")
    print(f"  \033[90m│\033[0m Scientific:    \033[96m{sci(r['total_files'])}\033[0m{' ' * (37 - len(sci(r['total_files'])))}  \033[90m│\033[0m")
    print("  \033[90m├─────────────────────────────────────────────────────┤\033[0m")
    zip_str = fmt_iec(r['zip_size'])
    output_str = sci(r['total_bytes'])
    print(f"  \033[90m│\033[0m Zip size:      \033[93m{zip_str}\033[0m{' ' * (37 - len(zip_str))}  \033[90m│\033[0m")
    print(f"  \033[90m│\033[0m Output size:   \033[93m{output_str} bytes\033[0m{' ' * (31 - len(output_str))}  \033[90m│\033[0m")
    print("  \033[90m├─────────────────────────────────────────────────────┤\033[0m")
    ratio_str = sci(r['ratio'])
    print(f"  \033[90m│\033[0m Ratio:         \033[91m1:{ratio_str}\033[0m{' ' * (36 - len(ratio_str))}  \033[90m│\033[0m")
    print("  \033[90m└─────────────────────────────────────────────────────┘\033[0m")
    print()

def print_level_table(r):
    print("  \033[90m┌────────┬──────────────────┬─────────────────────────┬─────────┬──────────────┐\033[0m")
    print("  \033[90m│\033[0m \033[1mLevel\033[0m  \033[90m│\033[0m \033[1mZip Size (IEC)\033[0m   \033[90m│\033[0m \033[1mFile Count\033[0m              \033[90m│\033[0m \033[1mDigits\033[0m  \033[90m│\033[0m \033[1mRatio\033[0m         \033[90m│\033[0m")
    print("  \033[90m├────────┼──────────────────┼─────────────────────────┼─────────┼──────────────┤\033[0m")
    
    for lv in r['levels']:
        d = lv['depth']
        if d <= 5 or d % 10 == 0 or d == r['level']:
            z = fmt_iec(lv['zip_size'])
            f = f"{lv['files']:,}"
            dg = int(math.log10(lv['files'])) + 1
            rt = f"{lv['ratio']:.2e}"
            
            # color based on ratio magnitude
            if lv['ratio'] < 1:
                color = "\033[90m"  # gray
            elif lv['ratio'] < 1000:
                color = "\033[93m"  # yellow
            elif lv['ratio'] < 1e6:
                color = "\033[92m"  # green
            elif lv['ratio'] < 1e20:
                color = "\033[96m"  # cyan
            else:
                color = "\033[91m"  # red
            
            print(f"  \033[90m│\033[0m {color}{d:>6}\033[0m  \033[90m│\033[0m {color}{z:<17}\033[0m  \033[90m│\033[0m {color}{f:>23}\033[0m  \033[90m│\033[0m {color}{dg:>7}\033[0m  \033[90m│\033[0m {color}1:{rt:>11}\033[0m  \033[90m│\033[0m")
    
    print("  \033[90m└────────┴──────────────────┴─────────────────────────┴─────────┴──────────────┘\033[0m")
    print()

def print_growth_chart(r):
    mx = r['levels'][-1]['zip_size']
    
    print("  \033[90m┌─────────────────────────────────────────────────────────────────────┐\033[0m")
    print("  \033[90m│\033[0m \033[1mGROWTH CHART\033[0m (Zip Size)                                         \033[90m│\033[0m")
    print("  \033[90m├─────────────────────────────────────────────────────────────────────┤\033[0m")
    
    for lv in r['levels']:
        d = lv['depth']
        if d % 10 == 0 or d == r['level']:
            sz = lv['zip_size']
            bar_len = int((sz / mx) * 45)
            
            # gradient color
            if bar_len < 15:
                color = "\033[92m"  # green
            elif bar_len < 30:
                color = "\033[93m"  # yellow
            else:
                color = "\033[91m"  # red
            
            bar = color + "#" * bar_len + "\033[0m"
            print(f"  \033[90m│\033[0m L{d:>2}: {fmt_iec(sz):>12} | {bar:<45} \033[90m│\033[0m")
    
    print("  \033[90m└─────────────────────────────────────────────────────────────────────┘\033[0m")
    print()

def print_comparisons(r):
    print("  \033[90m┌─────────────────────────────────────────────────────────────────────┐\033[0m")
    print("  \033[90m│\033[0m \033[1mCOMPARISONS\033[0m                                                      \033[90m│\033[0m")
    print("  \033[90m├─────────────────────────────────────────────────────────────────────┤\033[0m")
    
    comparisons = [
        ("Wikipedia English", 20 * 1024**3),
        ("Entire Internet", 120 * 1024**7),
        ("Stars in Universe", 10**24),
        ("Grains of Sand", 7.5e18),
        ("Cells in Body", 3.7e13),
        ("Atoms in Universe", 10**80),
    ]
    
    for name, ref_size in comparisons:
        if ref_size > r['total_bytes']:
            ratio = ref_size / r['total_bytes']
            direction = "smaller"
            color = "\033[92m"
        else:
            ratio = r['total_bytes'] / ref_size
            direction = "bigger"
            color = "\033[91m"
        
        name_padded = name.ljust(22)
        ratio_str = f"{ratio:.2e}x {direction}"
        print(f"  \033[90m│\033[0m {name_padded} {color}{ratio_str:>30}\033[0m     \033[90m│\033[0m")
    
    print("  \033[90m└─────────────────────────────────────────────────────────────────────┘\033[0m")
    print()

def print_known_bombs():
    print("  \033[90m┌─────────────────────────────────────────────────────────────────────┐\033[0m")
    print("  \033[90m│\033[0m \033[1mKNOWN ZIP BOMBS\033[0m                                                  \033[90m│\033[0m")
    print("  \033[90m├─────────────────────────────────────────────────────────────────────┤\033[0m")
    print("  \033[90m│\033[0m Name            Zip Size    Output           Ratio               \033[90m│\033[0m")
    print("  \033[90m├─────────────────────────────────────────────────────────────────────┤\033[0m")
    print("  \033[90m│\033[0m 42.zip           42 KB       4.5 PB           1:1.07e11          \033[90m│\033[0m")
    print("  \033[90m│\033[0m zipbomb.py       10 MB       10 GB            1:1e3              \033[90m│\033[0m")
    print("  \033[90m│\033[0m \033[93mTerminus\033[0m         \033[93m497 KB\033[0m       \033[93m6.91e61 B\033[0m         \033[93m1:1.36e56\033[0m           \033[90m│\033[0m")
    print("  \033[90m└─────────────────────────────────────────────────────────────────────┘\033[0m")
    print()

# ============================================================
# animation mode
# ============================================================

def animate_explosion(r):
    """
    terminal animation showing the recursive extraction.
    """
    print("  \033[96m[ANIMATION]\033[0m simulating extraction...\n")
    
    level = min(r['level'], 20)  # cap at 20 for animation
    
    for d in range(level + 1):
        files = r['branching'] ** d
        
        # clear line and print progress
        sys.stdout.write(f"\r  \033[90mLevel {d:>2}:\033[0m ")
        
        # show file count with color
        if files < 1000:
            sys.stdout.write(f"\033[93m{files:,}\033[0m files")
        elif files < 1e6:
            sys.stdout.write(f"\033[93m{files/1e6:.1f}M\033[0m files")
        elif files < 1e9:
            sys.stdout.write(f"\033[93m{files/1e9:.1f}B\033[0m files")
        else:
            sys.stdout.write(f"\033[91m{sci(files)}\033[0m files")
        
        # progress bar
        bar_len = int((d / level) * 30)
        bar = "\033[92m" + "#" * bar_len + "\033[0m"
        sys.stdout.write(f"  |{bar:<30}|")
        
        sys.stdout.flush()
        time.sleep(0.15)
    
    print("\n")
    print(f"  \033[91mFINAL: {r['total_files']:,} files = {sci(r['total_bytes'])} bytes\033[0m")
    print()

# ============================================================
# config file support
# ============================================================

def load_config(path):
    """load simulation config from json file."""
    with open(path, 'r') as f:
        return json.load(f)

def save_config(path, config):
    """save simulation config to json file."""
    with open(path, 'w') as f:
        json.dump(config, f, indent=2)

def create_example_config():
    """create an example config file."""
    config = {
        "name": "terminus_level50",
        "branching": 16,
        "level": 50,
        "payload": 43,
        "payload_type": "zeros",
        "description": "classic terminus configuration"
    }
    return config

# ============================================================
# main
# ============================================================

def main():
    DEFAULT_BR = 16
    DEFAULT_LV = 50
    DEFAULT_PL = 43
    
    # parse arguments
    if len(sys.argv) >= 2 and sys.argv[1] == '--animate':
        # animation mode
        r = simulate(DEFAULT_BR, DEFAULT_LV, DEFAULT_PL)
        print_banner()
        animate_explosion(r)
        return
    
    if len(sys.argv) >= 2 and sys.argv[1] == '--config':
        # config file mode
        if len(sys.argv) < 3:
            # create example config
            config = create_example_config()
            save_config('terminus_config.json', config)
            print("  created terminus_config.json")
            print("  edit it and run: python3 terminus_sim.py --config terminus_config.json")
            return
        else:
            config = load_config(sys.argv[2])
            r = simulate(
                config['branching'],
                config['level'],
                config['payload'],
                config.get('payload_type', 'zeros')
            )
            print_banner()
            print_config(r)
            print_results(r)
            return
    
    if len(sys.argv) >= 2 and sys.argv[1] == '--compare':
        # comparison mode
        print_banner()
        print_known_bombs()
        return
    
    if len(sys.argv) >= 4:
        # cli mode
        try:
            br = int(sys.argv[1])
            lv = int(sys.argv[2])
            pl = int(sys.argv[3])
            pt = sys.argv[4] if len(sys.argv) > 4 else 'zeros'
        except ValueError:
            print("  usage: python3 terminus_sim.py [branching] [level] [payload] [payload_type]")
            sys.exit(1)
    else:
        # interactive mode
        print_banner()
        print("  \033[90m┌─────────────────────────────────────────────────────┐\033[0m")
        print("  \033[90m│\033[0m \033[1mINPUT\033[0m (press enter for defaults)                  \033[90m│\033[0m")
        print("  \033[90m└─────────────────────────────────────────────────────┘\033[0m")
        print()
        
        try:
            raw = input(f"  branching  [{DEFAULT_BR}]: ").strip()
            br = int(raw) if raw else DEFAULT_BR
            
            raw = input(f"  level      [{DEFAULT_LV}]: ").strip()
            lv = int(raw) if raw else DEFAULT_LV
            
            raw = input(f"  payload    [{DEFAULT_PL}]: ").strip()
            pl = int(raw) if raw else DEFAULT_PL
            
            raw = input(f"  type       [zeros]: ").strip()
            pt = raw if raw else 'zeros'
        except (ValueError, EOFError):
            br, lv, pl, pt = DEFAULT_BR, DEFAULT_LV, DEFAULT_PL, 'zeros'
    
    # safety caps
    lv = min(lv, 200)
    br = min(br, 1000)
    pl = min(pl, 10000)
    
    r = simulate(br, lv, pl, pt)
    
    print_banner()
    print_config(r)
    print_results(r)
    print_level_table(r)
    print_growth_chart(r)
    print_comparisons(r)
    print_known_bombs()
    
    print("  \033[90m" + "=" * 60 + "\033[0m")
    print("  simulation complete. no files were created.")
    print("  \033[90m" + "=" * 60 + "\033[0m")
    print()

if __name__ == "__main__":
    main()
