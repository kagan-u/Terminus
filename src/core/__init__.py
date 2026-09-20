"""terminus core simulation engine."""

import math

def quadratic_model(level):
    a, b, c = 68.5, 5850.0, 120.0
    return a * level**2 + b * level + c

def simulate(branching=16, level=50, payload=43, payload_type='zeros'):
    compressibility = {
        'zeros': 0.95,
        'text': 0.60,
        'random': 0.10,
        'binary': 0.30,
    }
    comp = compressibility.get(payload_type, 0.95)
    
    total_files = branching ** level
    total_bytes = total_files * payload
    
    levels = []
    for d in range(level + 1):
        zip_size = quadratic_model(d)
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
    
    return {
        'branching': branching,
        'level': level,
        'payload': payload,
        'payload_type': payload_type,
        'levels': levels,
        'total_files': total_files,
        'total_bytes': total_bytes,
        'zip_size': levels[-1]['zip_size'],
        'ratio': total_bytes / levels[-1]['zip_size'],
    }

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
