# Security Policy

AIX Core is an experimental specification scaffold. Do not use it as a security boundary or production protocol without independent implementation review.

Schema validation does not authenticate a sender, establish trust-domain membership, authorize actions, verify evidence references, prevent replay, or ensure confidentiality. Receivers must independently authenticate, authorize, validate resource access, and enforce replay/idempotency protections.

Do not put credentials, secrets, private model reasoning, or unnecessary personal data into messages. Report vulnerabilities through GitHub private vulnerability reporting if enabled.
