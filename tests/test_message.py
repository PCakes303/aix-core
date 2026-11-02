import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
from tools.validate_message import load_message, validate

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schemas/aix-message.schema.json").read_text(encoding="utf-8"))
VALID = json.loads((ROOT / "examples/task-request.json").read_text(encoding="utf-8"))

class AIXMessageTests(unittest.TestCase):
    def test_positive_fixture_is_valid(self):
        self.assertEqual(list(Draft202012Validator(SCHEMA, format_checker=FormatChecker()).iter_errors(VALID)), [])

    def test_missing_security_is_rejected(self):
        bad = dict(VALID)
        bad.pop("security")
        self.assertTrue(list(Draft202012Validator(SCHEMA, format_checker=FormatChecker()).iter_errors(bad)))

    def test_unknown_top_level_field_is_rejected(self):
        bad = dict(VALID)
        bad["unexpected"] = True
        self.assertTrue(list(Draft202012Validator(SCHEMA).iter_errors(bad)))

    def test_unknown_message_type_is_rejected(self):
        bad = dict(VALID)
        bad["message_type"] = "execute-anything"
        self.assertTrue(list(Draft202012Validator(SCHEMA).iter_errors(bad)))

    def test_invalid_task_state_is_rejected(self):
        bad = json.loads(json.dumps(VALID))
        bad["task"]["state"] = "done-ish"
        self.assertTrue(list(Draft202012Validator(SCHEMA).iter_errors(bad)))

    def test_missing_idempotency_key_is_permitted_for_non_retry_profile(self):
        msg = json.loads(json.dumps(VALID))
        msg["task"].pop("idempotency_key")
        self.assertEqual(list(Draft202012Validator(SCHEMA).iter_errors(msg)), [])

    def test_cli_accepts_valid_fixture(self):
        result = subprocess.run([sys.executable, "tools/validate_message.py"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_cli_rejects_invalid_fixture(self):
        result = subprocess.run([sys.executable, "tools/validate_message.py", "examples/invalid-missing-security.json"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)

    def test_array_and_string_bounds(self):
        for mutate in (
            lambda m: m.update(capability_requirements=["c"] * 129),
            lambda m: m.update(context_refs=[{"uri":"https://example.org/x","media_type":"text/plain"}] * 129),
            lambda m: m.update(evidence_refs=[{"evidence_type":"test","uri":"https://example.org/x","observed_at":"2026-01-01T00:00:00Z"}] * 129),
            lambda m: m["security"].update(requested_scopes=["s"] * 129),
            lambda m: m["task"].update(objective="o" * 4001),
            lambda m: m.update(message_id="m" * 129),
        ):
            bad = json.loads(json.dumps(VALID)); mutate(bad)
            self.assertTrue(list(Draft202012Validator(SCHEMA, format_checker=FormatChecker()).iter_errors(bad)))

    def test_unknown_nested_properties_rejected(self):
        for target in ("sender", "security", "provenance", "task"):
            bad = json.loads(json.dumps(VALID)); bad[target]["unexpected"] = True
            self.assertTrue(list(Draft202012Validator(SCHEMA, format_checker=FormatChecker()).iter_errors(bad)))

    def test_extension_namespace_and_count_bounds(self):
        bad = json.loads(json.dumps(VALID)); bad["extensions"] = {"Bad Namespace": {}}
        self.assertTrue(list(Draft202012Validator(SCHEMA).iter_errors(bad)))
        bad = json.loads(json.dumps(VALID)); bad["extensions"] = {f"ext{i}": {} for i in range(65)}
        self.assertTrue(list(Draft202012Validator(SCHEMA).iter_errors(bad)))

    def test_strict_parser_rejects_duplicate_nonfinite_depth_and_size(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "message.json"
            for raw in ('{"a":1,"a":2}', '{"x":NaN}', '{"x":' + ("[" * 33) + "0" + ("]" * 33) + '}'):
                path.write_text(raw, encoding="utf-8")
                with self.assertRaises(ValueError):
                    load_message(path)
            path.write_bytes(b" " * (1_048_577))
            with self.assertRaisesRegex(ValueError, "byte limit"):
                load_message(path)

if __name__ == "__main__":
    unittest.main()
