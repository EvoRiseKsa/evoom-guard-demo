# EvoOM Guard — independent demo

> This repository exists only to **demonstrate [EvoOM Guard](https://github.com/EvoRiseKsa/EvoOM-Guard-m)
> against real patch scenarios** — on a tiny project the tool does **not** own,
> running the **published** release exactly as any user would. Nothing here is a
> custom test engine; it uses the shipped `evo-guard`.

## The four scenarios

| Scenario | Patch | Expected |
|---|---|---|
| **Honest fix** | adds a new function, harness untouched | PASS |
| **Edit tests** | rewrites the tests to `assert True` | REJECTED |
| **Fake stdout** | breaks the code **and** prints a fake `9999 tests passed` | FAIL |
| **Blackbox attack** | wrong CLI answer **and** forges the JUnit report (`atexit`+`os._exit`) | FAIL |

Each proves a distinct claim: an honest fix passes; you cannot pass by editing the
harness; you cannot pass by lying to **stdout** (the verdict is read from a
judge-owned JUnit report + exit code); and you cannot pass by **forging the report**
from inside the run (the black-box judge grades from its own process).

## Run it yourself (5 minutes)

```bash
curl -sSL -o evo-guard.pyz https://github.com/EvoRiseKsa/EvoOM-Guard-m/releases/download/v3.2.1/evo-guard.pyz

# 1 - Honest fix (Basic Guard)
python evo-guard.pyz guard ./repo --patch patches/1-honest-fix.txt
#   -> PASS: "all repo tests pass and the patch leaves the test harness untouched"

# 2 - Edit the tests (Basic Guard)
python evo-guard.pyz guard ./repo --patch patches/2-edit-tests.txt
#   -> REJECTED: "the patch edits or deletes the judging tests ... (tests/test_ops.py)"

# 3 - Fake success on stdout (Basic Guard)
python evo-guard.pyz guard ./repo --patch patches/3-fake-stdout.txt
#   -> FAIL: "the repo's tests fail on this patch (1/2 passed)"  (the fake "9999 passed" is ignored)

# 4 - Forge the report under the black-box judge
python evo-guard.pyz guard ./repo --patch patches/4-blackbox-forgery.txt --verifier-pack ./pack --blackbox
#   -> FAIL: "the black-box pack failed (0/1)"  (forgery earns no false PASS)
```

*(Output above is real, captured from `evo-guard 3.2.1`.)*

## In CI

`.github/workflows/evoom-guard.yml` gates every PR to this demo with the published
action (`EvoRiseKsa/EvoOM-Guard-m@v3.2.1`). Open a PR that edits `repo/tests/` and
it gets a REJECTED verdict as a PR comment.

## Layout

```
repo/       the project under test (a temperature converter + its own tests)
pack/       the judge-owned black-box protocol pack (lives OUTSIDE repo/)
patches/    the four scenario patches above
```
