# ADR 0001: AIX as an extension layer

- **Status:** accepted
- **Decision:** AIX defines shared semantics and mapping profiles over existing agent standards and transports. It does not replace MCP, A2A, HTTP, OpenAPI, or JSON-RPC.
- **Rationale:** preserve established transport, tool, and discovery ecosystems while addressing cross-system semantic interoperability.
- **Consequences:** AIX must prove incremental value through mapping and conformance experiments; no independent transport is introduced by this repository.
