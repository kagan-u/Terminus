# EXTRACTION

step-by-step guide to understanding recursive extraction.

## how it works

Terminus is a recursive zip bomb. when you extract it, you don't get files directly - you get more zip files. extracting those gives you more zip files. this continues for 50 levels.

```
Terminus.zip
├── bomb_0000.zip (level 49)
│   ├── bomb_0000.zip (level 48)
│   │   ├── bomb_0000.zip (level 47)
│   │   │   └── ... (continues 46 more levels)
│   │   ├── bomb_0001.zip
│   │   └── ... (16 total at this level)
├── bomb_0001.zip
├── bomb_0002.zip
└── ... (16 total at level 50)
```

## safe extraction steps

### step 1: check the zip

```bash
# see what's inside without extracting
unzip -l Terminus.zip
zipinfo Terminus.zip
```

you'll see 16 zip files, each named `bomb_XXXX.zip`.

### step 2: extract level 0

```bash
# create a test directory
mkdir -p test_extract
cd test_extract

# extract level 0
unzip ../Terminus.zip
```

you'll get 16 zip files. each is about 30 KB.

### step 3: extract level 1

```bash
# extract one of the level 1 zips
unzip bomb_0000.zip
```

you'll get 16 more zip files. each is still about 30 KB.

### step 4: continue (don't actually do this)

if you kept extracting:
- level 2: 256 zips
- level 3: 4,096 zips
- level 10: 1,099,511,627,776 zips (1 trillion)
- level 20: 1.2 x 10^24 zips
- level 50: 1.61 x 10^61 zips

## automated extraction

some tools extract nested archives automatically:

### 7-zip

```bash
# 7-zip extracts nested archives when you use "extract here"
7z x Terminus.zip

# WARNING: this will recursively extract ALL nested zips
# your system will run out of disk space very quickly
```

### the unzip command

```bash
# standard unzip does NOT extract nested archives
unzip Terminus.zip
# you'll just get 16 zip files
```

## recursive extraction script

here's what a recursive extraction would look like:

```python
import zipfile
import os

def recursive_extract(zip_path, max_level=50):
    """WARNING: this will consume all available disk space."""
    level = 0
    
    while level < max_level:
        if not zipfile.is_zipfile(zip_path):
            break
        
        with zipfile.ZipFile(zip_path, 'r') as zf:
            # extract to current directory
            zf.extractall('.')
            
            # find next zip to extract
            zips = [f for f in zf.namelist() if f.endswith('.zip')]
            if not zips:
                break
            
            zip_path = zips[0]  # extract first zip
            level += 1
            
            files = 16 ** level
            print(f"level {level}: {files:,} files")

# DO NOT RUN THIS
# recursive_extract('Terminus.zip')
```

## why this is dangerous

1. **disk exhaustion**: 1.61 x 10^61 files at 43 bytes each = 6.91 x 10^61 bytes
2. **memory exhaustion**: the OS tries to track all files
3. **inode exhaustion**: most filesystems have limited inodes
4. **time**: extracting this would take longer than the age of the universe

## safe alternatives

use the simulator instead:

```bash
python3 terminus_sim.py
python3 terminus_anim.py
```

these never create files. they only calculate and display theoretical results.
