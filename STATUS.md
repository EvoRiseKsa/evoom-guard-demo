# Demonstration status and claim boundary

## Current snapshot

This repository is intentionally a frozen proof snapshot for the published
EvoOM Guard v3.5.2 `evo-guard.pyz` asset, SHA-256
`a370fac23233ea6f317d5d7e5347389197fc936bd9b5903c685b1d3755e0046f`.
Its workflows, scenarios, packs, pins, and retained evidence establish only
the v3.5.2 claims documented in [`README.md`](README.md).

The snapshot must not be silently retargeted to a later release. Changing its
asset, scenarios, or evidence in place would erase the reproducible boundary
of the historical proof.

## What it does not establish

- It does not validate EvoOM Guard v3.7.0, the Trusted Finalizer workflow, raw
  Git source/context derivation, or artifact admission.
- It is a same-owner external-repository demonstration, not independent
  third-party validation.
- A green workflow proves only the declared scenarios against the pinned bytes;
  it is not a field-accuracy, security, or adoption guarantee.

## v3.7 evidence and a future demo

The current v3.7 Trusted Finalizer pilot and its recorded evidence live in the
separate [evoom-guard-finalizer-pilot](https://github.com/EvoRiseKsa/evoom-guard-finalizer-pilot)
repository. That pilot is also same-owner technical evidence and must not be
presented as independent validation.

A v3.7 demonstration should be published as a new, versioned project or
versioned proof set. Before it can make a claim, it must pin the immutable
v3.7.0 release asset and policy/pack identities, define new scenarios, and
record its own evidence. Until then, no v3.7 outcome may be inferred from this
v3.5.2 snapshot.
