# AIX Core

**Repository:** `PCakes303/aix-core`  
**Portfolio position:** 11 / 31 public repositories  
**Maturity:** experimental specification scaffold  
**License:** pending review

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

The repository's code, documentation, schemas, examples, and other materials do not yet have an approved license decision. No root `LICENSE` file or GitHub license declaration is present. Reuse and redistribution rights must not be assumed; licensing remains pending repository-specific review.

## Validation

Requires Python 3.10+ and `jsonschema==4.25.1`.

```bash
python -m pip install -r requirements-dev.txt
python tools/validate_message.py examples/task-request.json
python -m unittest discover -s tests -v
python tools/starter_build.py
```

## Security boundary

Schema validity does not authenticate senders, authorize requests, validate referenced resources, prevent replay, or guarantee message delivery. Receivers must independently authenticate the sender, verify trust domain and message integrity, enforce replay/idempotency controls, evaluate authorization, and check access to references.

AIX excludes private model reasoning and chain-of-thought. No production transport, SDK, runtime, cryptographic signing, or standards certification is provided by this scaffold.
