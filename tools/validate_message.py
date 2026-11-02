#!/usr/bin/env python3
"""Validate a bounded AIX experimental envelope; this performs no authentication or authorization."""
import json
import sys
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "aix-message.schema.json"
MAX_MESSAGE_BYTES = 1_048_576
MAX_JSON_DEPTH = 32


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result: raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _depth(raw):
    level = 0
    in_string = escaped = False
    for char in raw:
        if in_string:
            if escaped: escaped = False
            elif char == "\\": escaped = True
            elif char == '"': in_string = False
        elif char == '"': in_string = True
        elif char in "[{":
            level += 1
            if level > MAX_JSON_DEPTH: raise ValueError("JSON nesting exceeds depth limit")
        elif char in "]}":
            level -= 1
            if level < 0: raise ValueError("invalid JSON structure")


def load_message(path):
    raw_bytes = Path(path).read_bytes()
    if len(raw_bytes) > MAX_MESSAGE_BYTES: raise ValueError("AIX message exceeds byte limit")
    raw = raw_bytes.decode("utf-8")
    _depth(raw)
    return json.loads(raw, object_pairs_hook=_pairs,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError(f"invalid JSON number: {value}")))


def validate(message):
    try:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        errors = sorted(validator.iter_errors(message),
                        key=lambda error: (tuple(str(part) for part in error.absolute_path), error.message))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return [f"normative AIX schema unavailable or invalid: {type(exc).__name__}"]
    return [f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}" for error in errors]


def main(argv=None):
    args = argv if argv is not None else sys.argv[1:]
    path = Path(args[0]) if args else ROOT / "examples" / "task-request.json"
    try:
        message = load_message(path)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError, RecursionError) as exc:
        print(f"AIX message input error: {exc}", file=sys.stderr)
        return 2
    errors = validate(message)
    if errors:
        for error in errors: print(error, file=sys.stderr)
        return 1
    print("AIX envelope is schema-valid; authentication and authorization are not performed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
