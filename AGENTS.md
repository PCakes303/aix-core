# Agent instructions

- Treat AIX as a semantic extension layer over established standards and transports.
- Do not claim AIX replaces MCP, A2A, HTTP, OpenAPI, or JSON-RPC.
- Preserve explicit versioning, deterministic schemas, and documented mapping profiles.
- Never represent schema validation as authentication, authorization, replay protection, or transport security.
- Do not include private model reasoning or chain-of-thought in AIX messages.
- Use synthetic examples and data-minimized context/evidence references.
- Document breaking changes through an ADR and compatibility review.
- Run `python tools/starter_build.py` before proposing changes.
