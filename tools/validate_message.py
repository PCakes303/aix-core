#!/usr/bin/env python3
"""Validate an AIX experimental envelope; this does not perform security checks."""
import json
import sys
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]

def main(argv=None):
    args = argv if argv is not None else sys.argv[1:]
    message_path = Path(args[0]) if args else ROOT / "examples/task-request.json"
    schema = json.loads((ROOT / "schemas/aix-message.schema.json").read_text(encoding="utf-8"))
    message = json.loads(message_path.read_text(encoding="utf-8"))
    errors = sorted(
        Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER).iter_errors(message),
        key=lambda error: list(error.absolute_path)
    )
    if errors:
        for error in errors:
            print(f"{'/'.join(map(str, error.absolute_path))}: {error.message}", file=sys.stderr)
        return 1
    print("AIX envelope is schema-valid; authentication and authorization are not performed.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
