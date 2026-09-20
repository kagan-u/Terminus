# ARCHITECTURE

how terminus works under the hood.

---

## the recursive structure

terminus is built on the same principle as the classic 42.zip: zip-in-zip recursion.

```
                    Terminus.zip (497 KB)
                    |
        +-----------+-----------+
        |           |           |
   bomb_0000   bomb_0001   ... bomb_0015
   (30 KiB)    (30 KiB)        (30 KiB)
        |           |           |
    +---+---+   +---+---+   +---+---+
    |   |   |   |   |   |   |   |   |
   ... ... ... ... ... ... ... ... ...
        |
        v (50 levels deep)
        |
   data.bin (43 bytes of zeros)
```

each zip contains 16 copies of the previous level's zip. at the bottom (level 0), there's a single 43-byte file of null data.

---

## extraction tree

when you unzip Terminus.zip, here's what happens:

```
EXTRACT Terminus.zip
|
+-> 16 files: bomb_0000.zip ... bomb_0015.zip
    |
    +-> EXTRACT bomb_0000.zip
    |   +-> 16 files: bomb_0000.zip ... bomb_0015.zip
    |       |
    |       +-> EXTRACT (level 2)
    |       |   +-> 16 files each
    |       |       |
    |       |       +-> ... (continue for 50 levels)
    |       |           |
    |       |           +-> EXTRACT (level 49)
    |       |               +-> 16 files: data.bin (43 bytes each)
    |
    +-> EXTRACT bomb_0001.zip
    |   +-> same as above...
    |
    +-> ... (16 times)
```

total files at level 0: 16 x 16 x 16 x ... x 16 (50 times) = 16^50

---

## why this works

the ZIP format uses DEFLATE compression (LZ77 + Huffman coding).

important: each ZIP entry is compressed independently. DEFLATE does NOT share dictionaries or references between different entries. so "16 copies stored once" is not technically accurate.

what actually happens:

```
ENTRY 1: bomb_0000.zip (~30 KB compressed)
  - DEFLATE compresses this entry on its own
  - the inner zip contains highly compressible data (zeros)
  - result: small compressed size

ENTRY 2: bomb_0001.zip (~30 KB compressed)
  - DEFLATE compresses this entry independently
  - same input = same compressed output
  - result: same small compressed size

... (16 entries total, all identical)
```

each entry is compressed separately, but because the input data is identical (all zeros), each entry compresses to roughly the same small size. the zip doesn't deduplicate across entries -- it just benefits from the fact that each entry is highly compressible on its own.

this is why the zip grows by ~8KB per level instead of 16x per level. each new entry adds a fixed overhead, not 16x the previous size.

---

## the math

```
zip_size(level) = 120 + level x 8192

where:
  120    = level 0 zip size (headers + 43-byte payload)
  8192   = average bytes added per level (empirically measured)
```

measured values vs model:

```
Level  Measured   Model     Error
-----  ---------  --------  -----
  0    120 B      120 B     0%
 10    58.35 KB   80.12 KB  -27%
 20    136.51 KB  160.12 KB -15%
 30    231.44 KB  240.12 KB -4%
 40    336.19 KB  320.12 KB +5%
 50    508.95 KB  400.12 KB +27%
```

the model is approximate. the real zip has additional overhead from:
- central directory entries growing with level
- filename strings in each entry
- zip64 extended fields

but for order-of-magnitude estimates, the linear model works fine.

---

## ZIP format internals

```
+-----------------------------------+
| Local file header #1              | <- 30 bytes + filename
| Compressed data (DEFLATE)         | <- the actual content
+-----------------------------------+
| Local file header #2              |
| Compressed data                   |
+-----------------------------------+
| ...                               |
+-----------------------------------+
| Central directory header #1       | <- 46 bytes + filename
| Central directory header #2       |
| ...                               |
+-----------------------------------+
| End of central directory record   | <- 22 bytes
+-----------------------------------+
```

for Terminus.zip:
- 16 local file headers + compressed data
- 16 central directory entries
- 1 end-of-central-directory record
- zip64 extensions for large file support

---

## scaling limits

| Parameter         | Practical Limit | Why                                    |
|-------------------|-----------------|----------------------------------------|
| Level             | ~200            | build time grows, zip gets larger      |
| Branching         | ~1000           | more copies = more zip overhead        |
| Payload           | ~10000 bytes    | larger payload = larger level 0 zip    |
| Total output      | unlimited       | it's just a number                     |

level 200 would produce 16^200 files (a number with 241 digits). the zip would be ~1.6 MB. build time would be a few minutes.

there's no real hard limit. you could go to level 1000 if you wanted. the output would be incomprehensibly large.
