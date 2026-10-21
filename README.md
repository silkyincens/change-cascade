# ChangeCascade

**AI-assisted experimental local prototype.** Public synthetic inputs only; no deployment, publication or live business workflow is claimed.

Inspect fictional dependency cycles and prerequisite order before a human-reviewed change. No real infrastructure change is executed. This is one complete Project, not an additional IC entry.

## Domain and literal fixture outcome

A dependency says **dependent requires prerequisite**. The derived display arrow is prerequisite-to-dependent. Bounded two-pass DFS computes strongly connected components; members and group IDs use sorted ASCII. A group's ID is its first member. A self-loop is a cyclic singleton. Condensation edges remove within-cycle edges, deduplicate between-group dependencies, and expose a DAG. Each stage includes all currently available prerequisite-free groups in ASCII order. Selected nodes lock at record creation; impact contains their entire cycles and every downstream dependent, never upstream prerequisites.

The original8-node fixture has atomic cycles [api,cache] and [archive,ingest]. Stages are [archive,secrets,theme], [auth], [api], [dashboard]. Selecting auth impacts [api,auth,cache,dashboard]; selecting dashboard impacts only dashboard. UI checkboxes can explore different **local** selections without changing a loaded chain record's locked selection. The frontend independently derives SCC membership using bounded transitive closure rather than copying the contract's DFS algorithm.

Source shape is `{schema,nodes,dependencies}`, with schema ChangeCascade-graph-v1,1..12 unique ASCII node IDs and1..64 Unicode-codepoint labels with Python str.strip boundary rules,0..40 distinct known-endpoint edges. Unknown fields, duplicate JSON keys/IDs/edges and malformed selections reject. Selected sets contain1..12 distinct known nodes.

## Contract API and workflow

| Method | Meaning |
| --- | --- |
| `lock_source(record_id,url,sha,seeds_json)` | Owner locks complete graph and canonical selected IDs; LOCKED/revision0. |
| `derive(record_id,expected_revision)` | Owner re-fetches and fully derives SCC/stages/impact; DERIVED/revision1. |
| `confirm(record_id,expected_revision)` | Owner re-fetches/recomputes again and binds chain/contract/owner/record/source/selection/revision/operation; CONFIRMED/revision2. |
| `revoke(record_id,expected_revision,reason)` | Owner terminal revocation from any unrevoked stage; preserve history. |
| `get_record(record_id)` | Actual SDK decoded dictionary of frozen graph, selection, result and certificate. |
| `preview_impact(record_id,seeds_json)` | Read-only impact set over immutable graph with an alternative validated selection. |
| `get_configuration()` | Protocol and resource limits. |

All owner transitions use compare-and-set revisions. IDs can never be reused. A confirmed record proves a deterministic derivation of declared synthetic source bytes, not real-world dependency truth or an executed change.

## Local reproduction

Use Python3.12 and install pinned `requirements.txt` in a local virtual environment, then run `python tools/verify.py` **inside this package directory**. gltest owns its cwd `artifacts` directory. This executes actual pinned GenVM v0.2.12 SDK/storage/validator code, full official semantic/lint/schema, and records source SHA. The runner is `py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`. Both constructors take **zero arguments**. `tests/conftest.py` only handles upstream Windows fd0 cleanup and warp metadata refresh; it never substitutes contract algorithms. External web responses are controlled test fixtures. Direct tests do not prove live network multi-validator consensus or gas.

```powershell
python tools/verify.py
Set-Location frontend
pnpm install --frozen-lockfile
pnpm test
pnpm build
pnpm dev
```

`python tools/verify_frontend.py` records actual frontend test, TypeScript and Vite exit codes and all frontend input hashes. The frontend uses actual `genlayer-js@2.0.0-rc.2`, `viem@2.57.7`, TypeScript5.9.3, Vite7.1.12 and Vitest3.2.4. Domain code and UI are original; generic MIT wallet/JSON/context plumbing is shared with the separately reviewed profile05 work.

## Exact public source setup

The original MIT fixture `fixtures/graph.json` has byte SHA-256 `be2bb3dbb6356f98919c3c0aee53a445064cc317c75882a9d59605163e592ac1`. Every contract fetch independently checks HTTP200, UTF-8 exact bytes, duplicate JSON keys, strict complete schema and bounds. Responses must contain1..32768 bytes; this check occurs **after download** and does not claim bandwidth or redirect control. The immutable raw GitHub source URL must contain a lowercase exact40hex commit and end in `/profile08/projects/change-cascade/fixtures/graph.json`. Paths containing dot segments, queries, foreign namespaces or mutable branches reject. Validators independently re-fetch, validate and recompute the complete bound source packet. Forged result/binding and changed-byte proposals reject. No LLM is used.

`fixtures/source.json` keeps an explicit test locator in `test_url`, while **public_url and publication are null**. No contract address is configured. Root or an independent deployer must publish exact source bytes, verify digest, deploy the zero-argument contract on Stable Studio61999, and supply the actual address and immutable public URL. Local JSON editing/export does not publish or change the chain. Export shows the exact UTF-8 LF byte digest; normalization or reordered fields can change that digest even when semantics agree. Publish the exported bytes separately if using an edited policy/graph.

## Actual wallet proof and unknown recovery

Writes verify the injected wallet account/network and submit value0 exactly once. Completion uses an independent unformatted public `eth_getTransactionByHash` proof with exact original hash/sender/target/value0 and FINALIZED / NORMAL / leader_only=false / MAJORITY_AGREE, plus exactly one current leader with execution_result SUCCESS. Available normalized SDK hash/sender/target/value/status/execution/leader fields must agree, including each numeric execution result and any named/numeric contradiction. Missing Studio fields stay missing; no success fields are invented. Actual unmocked SDK-helper and viem-formatter tests reproduce missing train fields and numeric-zero loss on a captured public constructor example; this is **not live business-flow verification**. Nonfatal validator IDLE does not replace leader evidence.

Before the submitter is called, a pending record with original address/account/record/method and unknown hash is saved in same-tab session storage. Network errors, invalid/missing hashes, ambiguous/failed proof and post-proof read failures retain it and block another write. Only explicit wallet rejection4001 clears a hashless attempt. If the original hash was lost, attach the exact hash from wallet activity and observe it; no recovery method resends a write. Original caller/target/value remain bound. Keep the hash if leaving the page: a browser-local guard cannot survive cleared storage or an unrelated browser session. No keys or secrets are read or stored.

Busy operations disable all configuration inputs. Loaded records and action handlers compare the visible address/record ID; invalidated epochs discard late reads and transaction callbacks after context changes. Actual `main.ts` event-handler tests exercise A-to-B read/action races. Public raw receipt examples, controlled DOM/transport tests and SDK direct actors do not constitute real users or live wallet workflows.

## Evidence and release status

Local recorded checks: 32 actual SDK tests; 60 frontend tests; official semantic/lint/schema, TypeScript and Vite exit0. Inspect `evidence/verification.json` and `evidence/frontend-verification.json` for exact current hashes/results. The actual SDK bundle produces Vite's disclosed >500kB size notice; it is not a build failure. Browser visual review, fixture publication, contract deployment, hosting, live business flow, real users, financing and awards remain **null / unverified**. Independent peer review is tracked separately. Source-only allowlisted ZIPs exclude .sdk/.venv/node_modules/dist/cache/artifacts/environment files, and every archive entry is CRC/length/SHA verified.

Unicode label revision: frontend counts Unicode codepoints, matching Python contract len(label), including33/64 non-BMP labels;65 codepoints are rejected. The peer-reproduced failure and test-first correction are retained in evidence/unicode-regression-red.log. Contract and source fixtures are unchanged.
Frontend label boundary whitespace also matches Python str.strip: BOM remains valid text, while U+0085/U+001C at either boundary are rejected. Three additional RED failures are retained in evidence/unicode-trim-regression-red.log.

Independent source review by /root/genlayer_contract_pair02 closed after correction of the ChangeCascade Unicode-label interoperability P2. Reviewer identity/results are recorded by the author in evidence/independent-review.json, with exact reviewed candidate identities; this final archive adds documentation/metadata only. Final archive narrow verification is recorded separately at the project root. No source/frontend test rerun was needed for this metadata-only reseal.

Nonblocking UI limitation: revoke reasons use UTF16 length/maxlength200, whereas the contract permits200 Unicode codepoints. Some101..200 non-BMP reasons require shorter UI text; ordinary shorter reasons remain available. The reviewer did not request this scope expansion. SDK bundle size and browser-local pending guard limitations remain disclosed.
