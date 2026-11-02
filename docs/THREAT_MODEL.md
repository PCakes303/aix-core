# Threat Model

## Assets
Task intent, actor and recipient references, context/evidence pointers, task state, and provenance metadata.

## Threats
Spoofed principal claims, replayed messages, duplicate execution, malicious references, scope confusion, schema abuse, oversized payloads, information disclosure, and misleading provenance.

## Prototype mitigations
Strict message shape, enumerated message types and task states, bounded identifiers/text fields, idempotency-key field, namespaced extension location, and explicit security/provenance references.

## Not mitigated by schema alone
Sender authentication, trust-domain verification, authorization, replay prevention, deduplication, transport integrity/confidentiality, reference dereferencing controls, rate limiting, and trusted timestamps.

## Required receiver controls
Authenticate independently; authorize every operation; enforce idempotency and replay windows; validate and constrain reference dereferencing; apply size/rate limits; protect sensitive context; record security-relevant events; and reject unsupported protocol mappings safely.
