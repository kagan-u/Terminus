# COMPARISON

how Terminus stacks up against other known zip bombs.

## known zip bombs

### 42.zip

the classic. discovered in the wild, distributed via forums and email.

| property | value |
|----------|-------|
| zip size | 42 KB |
| nesting depth | 16 levels |
| branching factor | varies (5-10) |
| uncompressed output | 4.5 PB |
| ratio | 1:1.07 x 10^11 |

42.zip was the first widely known zip bomb. it exploited the same recursive technique but at a smaller scale.

### zipbomb.py

a python-based generator for research.

| property | value |
|----------|-------|
| zip size | 10 MB |
| nesting depth | varies |
| uncompressed output | 10 GB |
| ratio | 1:1,000 |

zipbomb.py focuses on generating customizable zip bombs for testing. it prioritizes flexibility over maximum compression.

### zip bomb (rossspencer)

another variant for security testing.

| property | value |
|----------|-------|
| zip size | 1.2 KB |
| nesting depth | 1 level |
| uncompressed output | 18.5 MB |
| ratio | 1:15,400 |

a simpler approach. single-level but still effective for testing.

## terminus

| property | value |
|----------|-------|
| zip size | 497 KB |
| nesting depth | 50 levels |
| branching factor | 16 |
| total files | 1.61 x 10^61 |
| uncompressed output | 6.91 x 10^61 bytes |
| ratio | 1:1.36 x 10^56 |

## comparison table

| name | zip size | output | ratio | levels | year |
|------|----------|--------|-------|--------|------|
| 42.zip | 42 KB | 4.5 PB | 1:1.07e11 | 16 | 2010 |
| zipbomb.py | 10 MB | 10 GB | 1:1e3 | variable | 2019 |
| rosspencer | 1.2 KB | 18.5 MB | 1:1.54e4 | 1 | 2019 |
| **Terminus** | **497 KB** | **6.91e61 B** | **1:1.36e56** | **50** | **2026** |

## what makes terminus different

### depth over width

42.zip goes 16 levels deep with variable branching. terminus goes 50 levels deep with fixed branching of 16. the extra depth creates exponentially more files.

### small zip, massive output

terminus is only 497 KB - smaller than most photos. but it contains more bytes than there are atoms in the observable universe (10^80 atoms, but most of those atoms are in stars - the "useful" matter is much less).

### pure recursion

no tricks, no special payloads. just zip-in-zip-in-zip... 50 times. each level multiplies by 16.

## scale visualization

```
42.zip output:     4.5 PB
                    |
                    v
Terminus output:   6.91 x 10^61 bytes
                    |
                    | <-- this gap is 10^46 times larger
                    v
```

if 42.zip's output was a grain of sand:
- terminus's output would be larger than all the sand on earth
- times the number of earths that could fit in the observable universe

## other approaches

### zip slip (CVE-2018-1000035)

a vulnerability in zip extraction that allows writing files outside the target directory. not a zip bomb, but related to zip security.

### decompression bombs

general term for any compressed file designed to exhaust resources when decompressed. includes:
- gzip bombs
- bzip2 bombs
- xz bombs
- 7z bombs

zip bombs are a specific type of decompression bomb.

### zip of zip (non-recursive)

sometimes a zip contains multiple zips that are not nested. this is just a collection, not a bomb.

## conclusion

terminus is the largest known recursive zip bomb. it demonstrates how simple recursion can create incomprehensible scale from a tiny package.
