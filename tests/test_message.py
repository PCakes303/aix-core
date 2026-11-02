import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schemas/aix-message.schema.json").read_text(encoding="utf-8"))
VALID = json.loads((ROOT / "examples/task-request.json").read_text(encoding="utf-8"))

class AIXMessageTests(unittest.TestCase):
    def test_positive_fixture_is_valid(self):
        self.assertEqual(list(Draft202012Validator(SCHEMA, format_checker=Draft202012Validator.FORMAT_CHECKER).iter_errors(VALID)), [])

    def test_missing_security_is_rejected(self):
        bad = dict(VALID)
        bad.pop("security")
        self.assertTrue(list(Draft202012Validator(SCHEMA).iter_errors(bad)))

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

if __name__ == "__main__":
    unittest.main()
