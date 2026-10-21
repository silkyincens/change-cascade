# ChangeCascade Implementation Plan

**Goal:** Deliver the original complete local Project in DESIGN.md.
**Architecture:** zero-constructor pinned SDK contract, strict immutable public synthetic source, exact deterministic domain logic, actual wallet UI with receipt proof and unknown recovery.
**Spec:** DESIGN.md

Global: only profile08/projects edits, never browser/IC/registry; byte-bound32768; no credentials; actual v0.2.12 runner; preserve null external status.
Review focus: duplicate/unknown schema and resource edges; exact canonical order; full forged validator packet; caller authorization/CAS/nonce; chunking/impact semantics; SDK raw/normalized conflicts; UI stale async IDs; ZIP exactbytes.

- [x] Write literal SDK tests before domain code and observe RED against absent APIs.
- [x] Implement strict source/caller/state/algorithm contracts; observe actual SDK GREEN and complete semantic/lint/schema.
- [x] Write frontend domain/UI/wallet tests first; implement distinct controls and visuals, observe RED/GREEN and tsc/Vite.
- [x] Document exact fixtures/source/limits; compute source/frontend identities and allowlist CRC/hash packages.
- [x] Request independent read-only peer, fix Important findings via RED/GREEN and re-freeze.
