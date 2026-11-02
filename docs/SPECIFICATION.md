# AIX Core Semantics (Experimental 0.1.0)

## 1. Status and role

This document defines an experimental semantic layer for interoperable agent task exchange. AIX is an extension/interoperability layer over established standards and transports. It does not replace MCP, A2A, HTTP, OpenAPI, JSON-RPC, or a transport protocol.

## 2. Message envelope

Every message carries a version, unique message identifier, creation timestamp, sender principal reference, message type, task object, security context, and provenance trace. A recipient reference is optional where routing is handled by an outer protocol.

## 3. Message categories

- `task.request`: propose a task to a recipient.
- `task.accepted`: recipient accepts responsibility for the task.
- `task.rejected`: recipient declines the task with an error or reason in a future profile.
- `task.acknowledged`: receipt acknowledged; not equivalent to acceptance or completion.
- `task.status`: progress or state update.
- `task.result`: task output or output references.
- `task.error`: failure information.
- `capability.query` / `capability.response`: capability negotiation.
- `context.reference`: reference to external context without embedding unrestricted content.

## 4. Task lifecycle

States: proposed, accepted, rejected, queued, running, blocked, succeeded, failed, cancelled, expired. Acknowledgement is a message event, not a task state. Implementations must not infer exactly-once execution. Retries require stable idempotency keys and receiver-side deduplication policy.

## 5. Context and evidence

Large context and evidence should be referenced, not embedded by default. References may include media type and SHA-256 digest. A digest supports integrity comparison only; it does not prove authenticity or truth. Receivers must independently authorize access to referenced resources.

## 6. Security context

The envelope may carry authentication-context, requested-scope, policy, and authorization-decision references. These are claims/references, not proofs. The receiving system authenticates the sender, validates trust-domain membership, evaluates policy, checks resource access, and enforces replay protections outside the schema.

## 7. Provenance and tracing

Trace, parent-message, causation, source-protocol, and mapping-profile references support correlation and mapping diagnostics. They do not establish trusted time or non-repudiation.

## 8. Privacy

Private model reasoning, hidden chain-of-thought, credentials, and secrets are excluded. Use minimal, task-relevant context and controlled references.
