# BENCHMARKS

performance data for Terminus.

---

## build performance

```
+-------+-----------+---------------------+--------+
| Level | Zip Size  | Total Files (16^N)  | Time   |
+-------+-----------+---------------------+--------+
|     0 | 120 B     | 1                   | <1 ms  |
|     5 | 22.40 KB  | 1,048,576           | <1 ms  |
|    10 | 58.35 KB  | 1.10e+12            | 10 ms  |
|    15 | 96.68 KB  | 1.15e+18            | 20 ms  |
|    20 | 136.51 KB | 1.21e+24            | 40 ms  |
|    30 | 231.44 KB | 1.33e+36            | 80 ms  |
|    40 | 336.19 KB | 1.46e+48            | 210 ms |
|    50 | 493.60 KB | 1.61e+60            | 360 ms |
+-------+-----------+---------------------+--------+
```

build time grows linearly. each level is slightly slower because the input zip is larger.

---

## zip size per level

```
Level    Zip Size    Growth    Bar
-----    --------    ------    ---
  0      120 B       -         |
  5      22.40 KB    +4.4 KB   |#####
 10      58.35 KB    +7.2 KB   |##############
 15      96.68 KB    +7.7 KB   |#######################
 20     136.51 KB    +8.0 KB   |################################
 30     231.44 KB    +9.5 KB   |####################################################
 40     336.19 KB    +10.5 KB  |#####################################################################
 50     493.60 KB    +15.7 KB  |######################################################################################################
```

growth per level is roughly 8-10 KB. it accelerates slightly at higher levels because zip overhead grows.

---

## compression ratio per level

```
Level    Ratio            Scientific      Log10
-----    -----            ----------      -----
  0      0.36x            3.58e-01       -0.45
  5      1,966x           1.97e+03        3.29
 10      792,766,357x     7.93e+08        8.90
 15      5.01e+14x        5.01e+14       14.70
 20      3.70e+20x        3.70e+20       20.57
 30      2.41e+32x        2.41e+32       32.38
 40      1.77e+44x        1.77e+44       44.25
 50      1.37e+56x        1.37e+56       56.14
```

each level adds ~11 to the log10 of the ratio. that's 10^11 more compression per level.

---

## output size comparison

```
Level    Output Size       Comparable To
-----    -----------       -------------
  0      43 B              a text message
  5      43 MB             a short movie
 10      43 TB             a large server's HDD
 15      43 EB             all data ever created by humans
 20      43 YB             367x the entire internet
 30      4.62e13 YB        4.62e19x the entire internet
 40      5.08e19 YB        incomprehensible
 50      5.72e37 YB        4.88e38x the entire internet
```

---

## memory usage during build

the build process holds one level's zip in memory at a time. the previous level is garbage collected.

```
Level    Peak Memory
-----    -----------
  0      ~1 KB
 10      ~60 KB
 20      ~140 KB
 30      ~235 KB
 40      ~340 KB
 50      ~500 KB
```

even level 50 uses less than 1 MB of RAM. the algorithm is very memory-efficient.

---

## timing breakdown

for level 50 (0.36 seconds total):

```
Phase               Time        Percent
-----------------   ----------  -------
Level 0-10          0.010 s     2.8%
Level 11-20         0.030 s     8.3%
Level 21-30         0.061 s     16.9%
Level 31-40         0.098 s     27.2%
Level 41-50         0.147 s     40.8%
-----------------   ----------  -------
Total               0.360 s     100%
```

the later levels take longer because:
1. the input zip is larger
2. DEFLATE has more data to process
3. more zip entries to write

---

## vs flat zip bomb

a flat zip bomb (single entry of zeros) achieves about 1:1000 compression.

```
Method         Zip Size    Output      Ratio
------         --------    ------      -----
Flat           50 MB       50 GB       1:1,000
Recursive L50  493 KB      6.91e61 B   1:1.37e56
```

recursive is 10^53 times more effective per byte of zip.

that's why 42.zip (and terminus) use recursion instead of flat compression.
