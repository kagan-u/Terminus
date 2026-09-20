# SECURITY

safe usage guidelines for Terminus.

---

## do not extract

Terminus.zip is a research artifact. extracting it will create 1.6 x 10^61 files and require 6.91 x 10^61 bytes of disk space. this will exhaust storage and memory, likely making the system unusable.

---

## safe operations

these are safe to perform on Terminus.zip:

```bash
# check file size
ls -lh Terminus.zip

# verify integrity
shasum -a 256 Terminus.zip
# expected: 5269c1b60f9497eb8a6bf9734e819f2a2e2aa2d2b8166fe49f116d852b5522de

# list contents without extracting
zipinfo Terminus.zip
unzip -l Terminus.zip
```

## unsafe operations

do NOT perform these:

```bash
# THIS WILL DESTROY YOUR SYSTEM
unzip Terminus.zip
tar xf Terminus.zip
7z x Terminus.zip
```

---

## use the simulator

instead of extracting, use the simulation tool to explore theoretical behavior:

```bash
python3 terminus_sim.py              # interactive
python3 terminus_sim.py 16 50 43     # cli
```

the simulator never creates files. it only calculates theoretical output.

---

## system limits

most operating systems have limits on:

- maximum number of files per directory
- maximum number of files per filesystem
- maximum total files on the system

extracting Terminus would exceed all of these. depending on the OS and configuration:

- the extraction process may hang or crash
- the filesystem may become unmountable
- data loss is possible if the filesystem fills completely

---

## vulnerability reporting

if you find a security issue with this project (not the zip bomb itself, but the code/docs), open a github issue.

---

## is this malware

no. Terminus is a research artifact demonstrating recursive compression techniques. it is not designed to be deployed against any system. it has no payload, no propagation mechanism, no command-and-control. it's a zip file that expands to a large size if extracted.
