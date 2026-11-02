# Standards Mapping Guide

## Principle

AIX adds shared semantics where systems need a common task and context model. It should preserve and reference native protocol concepts rather than reimplement their transport or tool-execution mechanisms.

## Mapping workflow

1. Identify the source protocol and version.
2. Map source concepts to AIX fields and record unmapped concepts.
3. Identify information loss, default values, and semantic mismatches.
4. Preserve native identifiers and references in provenance.
5. Never silently widen requested scopes or weaken authorization.
6. Validate mapped messages and test round trips where feasible.

## Candidate relationships

- MCP: tool/resource interaction remains MCP-native; AIX may describe a higher-level task intent and reference MCP resources or results.
- A2A: agent discovery, task lifecycle, and message transport remain A2A-native; AIX may provide a common semantic profile where useful.
- HTTP/OpenAPI: remain transport/API contracts; AIX can be carried as an application-level payload where appropriate.
- JSON-RPC: remains an RPC envelope; AIX semantics must not be confused with JSON-RPC request identifiers or error semantics.

These are mapping hypotheses, not claims of certified compatibility. Each concrete mapping requires a versioned profile and conformance tests.
