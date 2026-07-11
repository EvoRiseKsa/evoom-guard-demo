# EvoOM Guard — independent demo

A tiny, neutral project (a temperature converter) used to demonstrate
[**EvoOM Guard**](https://github.com/EvoRiseKsa/EvoOM-Guard-m) on a repository the
project does **not** own — running the **published** release, exactly as any user
would. Nothing here is a custom test engine; it uses the shipped `evo-guard`.

## Run it yourself (2 minutes)

```bash
# get the published gate (pin the tag)
curl -sSL -o evo-guard.pyz https://github.com/EvoRiseKsa/EvoOM-Guard-m/releases/download/v3.2.1/evo-guard.pyz

# four candidate patches, four honest verdicts:
python evo-guard.pyz guard ./repo --patch patches/1-honest.txt --verifier-pack ./pack --blackbox   # ✅ PASS
python evo-guard.pyz guard ./repo --patch patches/2-cheat.txt  --verifier-pack ./pack --blackbox   # ⛔ REJECTED
python evo-guard.pyz guard ./repo --patch patches/3-break.txt  --verifier-pack ./pack --blackbox   # ❌ FAIL
python evo-guard.pyz guard ./repo --patch patches/4-forge.txt  --verifier-pack ./pack --blackbox   # ❌ FAIL (no false PASS)
```

## What each scenario proves (real output)

| Patch | What it does | Verdict |
|---|---|---|
| `1-honest.txt` | adds `c_to_k()`, harness untouched | ✅ **PASS** (pack 1/1 **and** repo suite) |
| `2-cheat.txt` | rewrites the tests to `assert True` | ⛔ **REJECTED** (harness edit, caught pre-run) |
| `3-break.txt` | breaks `f_to_c()` | ❌ **FAIL** (the composite catches the regression the pack never sees) |
| `4-forge.txt` | returns a wrong CLI answer **and** forges the JUnit report via `atexit`+`os._exit(0)` | ❌ **FAIL** — the black-box judge grades from its own process, so the forgery earns **no false PASS** |

## In CI

`.github/workflows/evoom-guard.yml` gates every PR to this demo with the published
action (`EvoRiseKsa/EvoOM-Guard-m@v3.2.1`). Open a PR that edits `repo/tests/` and
watch it get `REJECTED`.

## Layout

```
repo/       the project under test (tempconv + its own tests)
pack/       the judge-owned black-box protocol pack (lives OUTSIDE repo/)
patches/    the four candidate patches above
```
