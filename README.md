# EvoOM Guard — external-repository demonstration

> This repository exists only to **demonstrate [EvoOM Guard](https://github.com/EvoRiseKsa/EvoOM-Guard-m)
> against real patch scenarios** — on a separate target project, running the
> **published** release exactly as any user would. Nothing here is a custom test
> engine; it uses the shipped `evo-guard`.
>
> **Honest scope:** this repo is separate from the tool's codebase but lives under
> the **same account** — it is a reproducible external-repository demonstration,
> **not** third-party validation. Every claim below is re-proven on every push by
> the [Demo proof suite](../../actions/workflows/proof.yml) (green = every
> verdict below still holds against the published release).

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
pip install pytest   # the demo project's own test runner (Guard runs YOUR suite)
curl -sSL -o evo-guard.pyz https://github.com/EvoRiseKsa/EvoOM-Guard-m/releases/download/v3.4.0/evo-guard.pyz
curl -sSL -o SHA256SUMS    https://github.com/EvoRiseKsa/EvoOM-Guard-m/releases/download/v3.4.0/SHA256SUMS
sha256sum -c SHA256SUMS    # verify the artifact before running it

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

*(Output above is re-verified in CI against `evo-guard 3.4.0`.)*

## The v3.4 identity and execution-fidelity proofs

The proof workflow adds four assertions that are specific to v3.4. They are
machine-checked against the published `.pyz`, not inferred from documentation:

| Proof | What CI requires |
|---|---|
| **Pinned V2 pack identity** | `pack-native/` must hash to the value in `pack-native.v2.sha256`; the PASS attestation must repeat the same SHA and `EVOGUARD_PACK_V2` format. |
| **Fail-before-test tamper detection** | Appending one byte to a copied pack under the original pin must return `ERROR verifier_pack_identity_mismatch` with `test_command_ran: false`. |
| **Mandatory independent pack phase** | The forged CLI leaves the repo's two tests green, but the pack fails 0/1; the composed result must be FAIL 2/3. |
| **Exact container identity** | A digest-pinned Python base builds the judge image; Guard's delivered `image_digest` must equal Docker's inspected image ID, with setup and suite both reporting Docker and the pack passing 1/1. |

`pack-native.v2.sha256` deliberately lives **outside** `pack-native/`, otherwise
the pin file would recursively become part of the identity it records. Any
change to a pack byte, path, or directory requires a deliberate pin update via
`python evo-guard.pyz pack-doctor ./pack-native --json`.

## In CI

`.github/workflows/evoom-guard.yml` gates every PR to this demo with the published
v3.4.0 action pinned to its immutable release commit
(`58561f898613d860f9270ffdd06d42c4023306da`). Open a PR that edits
`repo/tests/` and it gets a REJECTED verdict as a PR comment.

## The realistic fixture: a Node workspaces monorepo

`node-workspace/` is a **npm-workspaces monorepo** (two packages, colocated
`*.test.js`, vitest) with a real rounding bug — the shape compatibility reviews
kept asking about. Four scenarios, [re-proven on every push](../../actions/workflows/proof.yml)
through the **structured vitest oracle** (`verdict_source: junit+exit`):

| Scenario | Patch | Verdict |
|---|---|---|
| Honest fix | `patches-node/1-honest-fix.txt` | ✅ PASS (3/3) |
| Weaken a colocated `.test.js` | `patches-node/2-edit-colocated-test.txt` | ⛔ REJECTED (pre-gate) |
| Plant `vitest.config.js` to narrow discovery | `patches-node/3-vitest-config-edit.txt` | ⛔ REJECTED (pre-gate) |
| Rewrite `package.json` `scripts.test` to a fake echo | `patches-node/4-pkgjson-test-tamper.txt` | ❌ **FAIL 2/3** — the tamper is *neutralized*: the harness fields are restored, the real vitest still runs, the bug still fails |

The workspace carries its own protected policy contract
([`node-workspace/.evoguard.json`](node-workspace/.evoguard.json)) — the judge
command, setup, and policy identity live in the repo, untouchable by any patch.

## Clickable evidence

* **[Demo proof suite runs](../../actions/workflows/proof.yml)** — every push
  re-runs all four scenarios against the published `.pyz` and asserts each
  verdict from the JSON (three of the four intentionally exit non-zero).
* **[Guard-gated PR checks](../../actions/workflows/evoom-guard.yml)** — the
  published Marketplace action gating this repo's own PRs.
* **[A real REJECTED sticky comment](https://github.com/EvoRiseKsa/evoom-guard-demo/pull/1#issuecomment-4945847383)**
  — the historical PR that edits `repo/tests/` and gets the reward-hack verdict
  posted (and updated in place) by the action, exactly as an adopter would see it.
* Release provenance: the pinned artifact is
  [`v3.4.0/evo-guard.pyz`](https://github.com/EvoRiseKsa/EvoOM-Guard-m/releases/tag/v3.4.0)
  with its `SHA256SUMS` alongside.

## Layout

```
repo/            the project under test (a temperature converter + its own tests)
pack/            the judge-owned black-box protocol pack (lives OUTSIDE repo/)
pack-native/     the judge-owned repo-native V2 pack; its pin is stored beside it
patches/         the four scenario patches above
node-workspace/  the npm-workspaces monorepo fixture (no committed node_modules —
                 the policy's setup_command installs from the lockfile at judge time)
patches-node/    the four Node-workspace scenario patches
```
