# AIX Core

**Repository:** `PCakes303/aix-core`  
**Portfolio position:** 11 / 31 public repositories  
**Maturity:** experimental specification scaffold  
**License:** [Scoped mixed-license policy](LICENSE.md).

## Purpose

AIX (Agent Interoperability eXchange) defines a semantic interoperability layer for exchanging agent intents, tasks, responses, capability requirements, context references, status, errors, and provenance across heterogeneous agent systems.

AIX is an **extension layer**, not a replacement for MCP, A2A, HTTP, OpenAPI, JSON-RPC, or existing transports. AIX defines shared semantics and mapping profiles; other standards and transports remain responsible for their established roles.

## Current scope

- Experimental AIX message envelope schema (Draft 2020-12).
- Task lifecycle vocabulary and message-type registry.
- Context and evidence references.
- Security-context and provenance references.
- Synthetic positive and negative conformance fixtures.
- Mapping principles and explicit non-goals.

## License status

This repository documents the ecosystem's intended scoped mixed-license policy: Apache-2.0 for eligible original code and machine-readable contracts, and CC BY 4.0 for eligible original human-readable documentation. Its manifest remains `pending-review` until contributor authority, file-level provenance and third-party notices are checked. Do not assume every file is cleared for redistribution. Third-party material retains upstream terms; data, evidence, fixtures, sample payloads and media receive no blanket license. See [LICENSE.md](LICENSE.md).

## Validation

Requires Python 3.10+ and `jsonschema==4.25.1`.

```bash
python -m pip install -r requirements-dev.txt
python tools/validate_message.py examples/task-request.json
python -m unittest discover -s tests -v
python tools/starter_build.py
```

The CLI parser caps each envelope at 1 MiB and JSON nesting at 32 levels. The schema bounds message arrays, references, identifiers, extension maps, and nested metadata. These are structural checks only; they do not authenticate or authorize messages.

## Security boundary

Schema validity does not authenticate senders, authorize requests, validate referenced resources, prevent replay, or guarantee message delivery. Receivers must independently authenticate the sender, verify trust domain and message integrity, enforce replay/idempotency controls, evaluate authorization, and check access to references.

AIX excludes private model reasoning and chain-of-thought. No production transport, SDK, runtime, cryptographic signing, or standards certification is provided by this scaffold.
