# TERMINUS - DONT EXTRACT!

```
████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗██╗   ██╗███████╗
╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██║   ██║██╔════╝
   ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║██║   ██║███████╗
   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██║   ██║╚════██║
   ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║╚██████╔╝███████║
   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝
```

**RECURSIVE ZIP BOMB**

497 KB compressed -> 6.91 x 10^61 bytes output

---

## what is this

a recursive zip bomb. ~497 KB compressed, produces a theoretical output of 6.91 x 10^61 bytes.

built on the 42.zip algorithm. level 50, branching factor 16, 43-byte payload.

---

## DO NOT EXTRACT

```
+-----------------------------------------------------------------------+
|                                                                       |
|   Terminus.zip creates 1.6 x 10^61 files                             |
|   Requires 6.91 x 10^61 bytes of disk space                          |
|   Attempting extraction can exhaust available storage and resources   |
|   and may make the system unusable.                                   |
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
| SIZE             | 497 KB (508,950 bytes)                             |
| SHA256           | 5269c1b60f9497eb8a6bf9734e819f2a2e2aa2d2b8166fe49 |
|                  | f116d852b5522de                                     |
| FILES INSIDE     | 16 (bomb_0000.zip - bomb_0015.zip)                |
| EACH INNER       | ~30.75 KiB (all identical)                         |
| TOTAL FILES      | 1,606,938,044,258,990,275,541,962,092,341,      |
|                  | 162,602,522,202,993,782,792,835,301,376           |
| DIGITS           | 61                                                 |
| OUTPUT SIZE      | 6.91 x 10^61 bytes                                |
| RATIO            | 1 : 1.36 x 10^56                                  |
| BUILD TIME       | 0.36 seconds                                       |
+------------------+----------------------------------------------------+
```

verify integrity:

```bash
python3 terminus_hash.py
# or
shasum -a 256 Terminus.zip
```

---

## versions

| name | branch | level | payload | files | output |
|------|--------|-------|---------|-------|--------|
| mini | 4 | 10 | 43B | 10^6 | 10^7 |
| basic | 8 | 20 | 43B | 10^18 | 10^19 |
| **standard** | 16 | 50 | 43B | 10^60 | 10^61 |
| deep | 16 | 100 | 43B | 10^120 | 10^122 |
| wide | 256 | 50 | 1B | 10^120 | 10^120 |
| **ultra** | 256 | 100 | 1B | 10^240 | 10^240 |
| mega | 256 | 150 | 1B | 10^361 | 10^361 |
| god | 65536 | 100 | 1B | 10^481 | 10^481 |

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

## visuals

### charts

![Zip Size Growth](terminus_charts/01_zip_size_growth.png)

![File Count Explosion](terminus_charts/02_file_count_explosion.png)

![Compression Ratio](terminus_charts/03_compression_ratio.png)

![Zip vs Output](terminus_charts/04_zip_vs_output.png)

![Bombs Comparison](terminus_charts/05_bombs_comparison.png)

![Scale Comparison](terminus_charts/06_scale_comparison.png)

![Growth Breakdown](terminus_charts/07_growth_breakdown.png)

### video

![Terminus Explosion](terminus-explosion.gif)

---

## quick start

### make commands

```bash
make help        # list all commands
make sim         # interactive simulator
make build       # live build simulation
make tui         # interactive terminal UI
make anim        # terminal animation
make benchmark   # performance benchmarks
make config      # compare all versions
make ultra       # list ultra versions
make hash        # verify integrity
make chart       # generate charts
make video       # generate video
make test        # run python tests
make testjs      # run javascript tests
```

### simulation

```bash
# interactive mode
python3 terminus_sim.py

# cli mode
python3 terminus_sim.py 16 50 43

# with payload type
python3 terminus_sim.py 16 50 43 text

# animation
python3 terminus_anim.py

# create config file
python3 terminus_sim.py --config

# compare with known bombs
python3 terminus_sim.py --compare
```

### versions & optimizer

```bash
# compare all versions
python3 terminus_config.py

# build ultra version (256^100)
python3 terminus_ultra.py ultra

# list all versions
python3 terminus_ultra.py --list
```

### live build

```bash
# simulated build (fast)
python3 terminus_build.py 16 50 43

# real build (actually creates levels)
python3 terminus_build.py 16 20 43 --real
```

### interactive tools

```bash
# curses terminal UI
python3 terminus_tui.py

# rich terminal UI
python3 src/cli/rich_ui.py
```

### benchmarks

```bash
# build/read/compression benchmarks
python3 terminus_benchmark.py
```

### integrity

```bash
# verify Terminus.zip
python3 terminus_hash.py

# generate MANIFEST.json
python3 terminus_hash.py --manifest
```

### graphics

```bash
# generate charts (requires: pip install matplotlib numpy)
python3 terminus_graph.py

# generate video (requires: pip install matplotlib numpy imageio[ffmpeg])
python3 terminus_video.py

# interactive plotly charts
python3 src/web/plotly_charts.py
```

### JavaScript

```bash
# run demo
node examples/demo.js

# run tests
node tests/test.js
```

### Docker

```bash
docker build -t terminus .
docker run --rm terminus python terminus_sim.py 16 10 43
```

### verify manually

```bash
ls -lh Terminus.zip
shasum -a 256 Terminus.zip
zipinfo Terminus.zip
```

no files created by simulation. just math.

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

## project structure

```
Terminus/
├── Terminus.zip                 the bomb
├── Makefile                     command entry point
├── presets.json                 version presets
│
├── terminus_sim.py              safe simulator
├── terminus_anim.py             terminal animation
├── terminus_build.py            live build simulation
├── terminus_tui.py              curses interactive TUI
├── terminus_benchmark.py        performance benchmarks
├── terminus_hash.py             integrity verification
├── terminus_banner.py           ASCII banner generator
├── terminus_graph.py            matplotlib charts
├── terminus_video.py            video generator
├── terminus_ultra.py            version builder
├── terminus_config.py           version config & optimizer
│
├── src/
│   ├── core/
│   │   ├── __init__.py          simulation engine
│   │   └── optimizer.py         config optimizer
│   ├── cli/
│   │   ├── main.py              cli entry point
│   │   └── rich_ui.py           rich terminal ui
│   └── web/
│       └── plotly_charts.py     plotly charts
├── js/
│   └── terminus.js              javascript port
├── examples/
│   └── demo.js                  javascript demo
├── tests/
│   ├── test_simulation.py       python tests
│   └── test.js                  javascript tests
├── docs/
│   ├── ARCHITECTURE.md          how the recursion works
│   ├── TECHNICAL.md             algorithm deep dive
│   ├── EXTRACTION.md            extraction guide
│   ├── COMPARISON.md            vs other zip bombs
│   ├── BENCHMARKS.md            performance data
│   └── CHANGELOG.md             version history
├── .github/workflows/ci.yml     github actions
├── README.md
├── CONTRIBUTING.md
├── ROADMAP.md
├── SECURITY.md
├── LICENSE                      CC0 1.0
├── Dockerfile
├── requirements.txt
├── pyproject.toml
└── package.json
```

---

## docs

| document | description |
|----------|-------------|
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | how the recursion works |
| [TECHNICAL.md](docs/TECHNICAL.md) | algorithm deep dive |
| [EXTRACTION.md](docs/EXTRACTION.md) | step-by-step extraction guide |
| [COMPARISON.md](docs/COMPARISON.md) | vs other zip bombs |
| [BENCHMARKS.md](docs/BENCHMARKS.md) | performance data |
| [CHANGELOG.md](docs/CHANGELOG.md) | version history |
| [SECURITY.md](SECURITY.md) | safe usage guidelines |
| [CONTRIBUTING.md](CONTRIBUTING.md) | how to contribute |
| [ROADMAP.md](ROADMAP.md) | planned features |

---

## install

```bash
pip install -e .
npm install
```

---

## license

CC0 1.0 Universal
