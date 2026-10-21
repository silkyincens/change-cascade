# profile08 frozen local review request

Author: /root/genlayer_projects05. Read-only independent review is pending; the author has not marked either Project complete. Root assigns the reviewer. Do not edit sources or repeat all SDK/bootstrap checks. Report any Important finding to root and the author before a revised candidate is frozen.

## Frozen identities

| Project | Contract SHA256 | Frontend input tree SHA256 | ZIP SHA256 | Files | SDK / frontend tests |
| --- | --- | --- | --- | --- | --- |
| ChangeCascade | ab862b7423adc1211efcba6fef6ea5c937b424e5eb9ff3baa642a6e8c691c0ef | c0130b35eedc2e62dac065f196896d47404cac081b69d47ada154dc2e50d46c8 | 0ef667c993e002b3d0311ab20d728d3f04e665a3d39d68356f81ba8257ca2262 | 61 | 32 / 60 |
| DeficitDesk | 1a92cbe7f2d98fe5890a4f0bd009933cc5e534e6d86dd5e20e27a4cddd7407ea | c0f13ae4b9f2effe4f778bc5d1be012478d54c9b11039256e1fde79b5a1b9e23 | e05dae273d5f76c399c517f691e76c1b5bf74472acdbaa8e423663e9d3180b93 | 58 | 35 / 57 |

Root PUBLISH_MANIFEST.json binds each contract, frontend tree, source snapshot, per-package manifest, ZIP size/hash and exact entry hashes. The candidate ZIPs are source-only; every ZIP CRC and entry SHA was checked against disk. Source fixture SHA uses read_bytes(), with no newline normalization. Public source URL, deployment, publication, hosting and live business-flow fields are null.

## Scope and review priorities

Read each DESIGN.md, README.md, contract.py, frontend/src and tests. Evidence is in each evidence/ directory. verification.json binds actual SDK tests and full official lint/semantic/schema success to current contract bytes. frontend-verification.json binds frontend tests, TypeScript and Vite success to all current frontend input bytes. sdk-red.log, frontend-red.log and frontend-ui-red.log preserve failures before implementation; DeficitDesk also records receipt-binding-red.log before its complete scheduling receipt was added. These are local results, not browser or live network evidence.

ChangeCascade: verify strict bounded schema/duplicate keys and dependencies; maximal SCC groups, self-loop interpretation, deterministic condensation/stages; prerequisite-to-dependent impact direction; complete source/result binding and fresh independent validator recomputation at lock/derive/confirm; owner/CAS/terminal revoke; original literal tests and independent frontend algorithm. UI must distinguish local edited selections from the frozen chain record and discard any callback if visible address or record ID changes.

DeficitDesk: verify immutable public operator policy, exact operator addresses and monotonic nonce; revision CAS, global job ID uniqueness, FIFO queue/lifetime limits; persistent deficit/cursor DRR, no FIFO bypass, empty reset/early-stop/no-op and chunk invariance; bounded history; complete receipt binding and canonical receipt digest; source packet validation at lock/activate and terminal revoke. Scheduling declares fictional jobs and never executes workers or moves assets. UI must use loaded chain revision/nonce/flow operator for real writes, while keeping the independent local simulation separate.

Both: actual installed genlayer-js helper/viem formatter characterization, dict ABI, independent raw FINALIZED/NORMAL/leader_only=false/MAJORITY_AGREE/unique leader SUCCESS; exact original hash/sender/recipient/value=0, and every available SDK numeric/named conflict. UNKNOWN_NO_HASH must be saved before wallet submission; unknown outcomes survive reload, retain original context, and never replay automatically. Manual wallet-original-hash attachment only observes that submission. Busy controls and asynchronous visible address/ID protection are exercised through actual main handlers.

Shared generic MIT wallet/context/test plumbing was adapted from the author's reviewed profile05 Projects; domain contracts, fixtures, domain tests and visuals are original and are not renamed ICs.

## Explicit limits

No browser visual review, public deployment, wallet business-flow transaction, real multi-validator consensus, public hosting, real users, financing or awards have been verified. The reference raw Studio receipt is historical constructor evidence used only to characterize the SDK. Vite reports an SDK bundle larger than 500 kB. Browser-local pending guards do not survive cleared storage or coordinate unrelated browser sessions. Never read or write private keys, seed phrases or API credentials.

## Peer P2 correction: Unicode label interoperability

The original ChangeCascade candidate is preserved in historical/pre-unicode-fix-change-cascade-publish.zip (SHA4d5f170849c96033adfb5b90a795f5f68c24d33eec761b3d06d1596016c8e26d). Peer /root/genlayer_contract_pair02 independently reproduced valid33-nonBMP and BOM-prefixed labels in the actual SDK but rejected frontend loads. Author regressions recorded2 failed8 passed for codepoint count, then3 failed10 passed for Python-strip boundary parity. Current source uses Unicode codepoint length and the exact Python boundary whitespace set;33/64 nonBMP and BOM are accepted,65 codepoints and boundaryU0085/U001C rejected. Full60 frontend tests/TypeScript/Vite exit0 now bind the new tree. Contract and every fixture are byte-identical to the reviewed original archive; see evidence/unicode-peer-fix.json. DeficitDesk remains the identical57-entry candidate. This correction awaits the same independent peer's narrow recheck, not author self-closure.

Final source review is closed after the Unicode fix by /root/genlayer_contract_pair02. FINAL-METADATA-RESEAL.json records the single necessary final docs-only archive change (AI-assisted prototype, peer result, nonblocking reason limit); every contract/frontend/fixture byte remains identical to the reviewed corrected candidates. Current table contains final metadata archive identities; source review report is outputs/genlayer-builders-2026-10-21/peer-audits/profile08-unicode-label/PEER08-REVIEW.json. Only final archive narrow verification remains pending.
