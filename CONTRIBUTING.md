# CONTRIBUTING

how to contribute to Terminus.

---

## ground rules

- this is a research artifact. keep it that way.
- no payloads, no malware, no exploitation code.
- tests must pass before any PR is merged.
- all docs and comments in english, casual tone.
- no corporate language.

---

## getting started

```bash
git clone https://github.com/kagan-u/Terminus.git
cd Terminus
pip install -r requirements.txt
```

run the tests:

```bash
make test
make testjs
```

---

## project layout

| path | what it is |
|------|-----------|
| `terminus_*.py` | top-level tools |
| `src/core/` | simulation engine |
| `src/cli/` | terminal interfaces |
| `tests/` | test suite |
| `docs/` | documentation |
| `js/` | javascript port |

---

## what to work on

check [ROADMAP.md](ROADMAP.md) for planned features.

good first issues:
- improve the quadratic model with more measurements
- add more payload types to the simulator
- write more tests
- fix docs inaccuracies
- add benchmarks for your machine

---

## pulling it together

1. fork the repo
2. create a branch: `git checkout -b my-feature`
3. make your changes
4. run tests: `make test`
5. commit: `git commit -m "add my feature"`
6. push: `git push origin my-feature`
7. open a PR

---

## code style

- python: follow existing style, no type hints needed
- comments: only what is not obvious
- no emojis in code
- keep functions small and focused
